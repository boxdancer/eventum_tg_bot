import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from constants.admin import (
    ADMIN_CALLBACK_PREFIX,
    ALL_CATEGORIES,
    AUDIENCE_PAGE_SIZE,
    BROADCAST_DELAY_SECONDS,
    BROADCAST_DRAFT_KEY,
    CALLBACK_SEPARATOR,
    CATEGORY_LABELS,
    DISPLAY_NAME_LIMIT,
    DISPLAY_USERNAME_LIMIT,
    PERIOD_LABELS,
    AdminAction,
    AdminText,
    AudiencePeriod,
)
from constants.audience import AudienceCategory
from logger_config import get_logger
from telegram import Bot, Message, Update
from telegram.constants import ChatType
from telegram.error import RetryAfter, TelegramError
from telegram.ext import ContextTypes

from bot.audience import Audience
from bot.utils.button import Button

logger = get_logger(__name__)


def admin_button(label: str, action: AdminAction, *parts: str | int) -> Button:
    callback = CALLBACK_SEPARATOR.join(str(part) for part in (action, *parts))
    return Button(label, callback_data=f"{ADMIN_CALLBACK_PREFIX}{callback}")


@dataclass
class BroadcastDraft:
    token: str
    category: AudienceCategory | None
    since: datetime | None
    preview_message_id: int | None = None


class AdminHandler:
    def __init__(self, audience: Audience, owner_id: int):
        self.audience = audience
        self.owner_id = owner_id
        self.broadcast_task: asyncio.Task | None = None

    def allowed(self, update: Update) -> bool:
        chat = update.effective_chat
        user = update.effective_user
        return bool(chat and chat.type == ChatType.PRIVATE and user and user.id == self.owner_id)

    @staticmethod
    def menu():
        return Button.create_markup(
            [
                [
                    admin_button(AdminText.USERS, AdminAction.USERS),
                    admin_button(AdminText.BROADCAST, AdminAction.BROADCAST),
                ]
            ]
        )

    async def open(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        user_data = context.user_data
        if not self.allowed(update) or message is None or user_data is None:
            return
        user_data.pop(BROADCAST_DRAFT_KEY, None)
        await message.reply_text(AdminText.TITLE, reply_markup=self.menu())

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if query is None:
            return
        if not self.allowed(update):
            await query.answer(AdminText.DENIED, show_alert=True)
            return

        await query.answer()
        user_data = context.user_data
        if user_data is None or query.data is None or not isinstance(query.message, Message):
            return
        action, *parts = query.data.removeprefix(ADMIN_CALLBACK_PREFIX).split(CALLBACK_SEPARATOR)
        try:
            action = AdminAction(action)
        except ValueError:
            return

        if action == AdminAction.MENU and not parts:
            user_data.pop(BROADCAST_DRAFT_KEY, None)
            await query.edit_message_text(AdminText.TITLE, reply_markup=self.menu())
        elif action in (AdminAction.USERS, AdminAction.BROADCAST):
            await self.choose_segment(query, context, action, parts)
        elif action in (AdminAction.SEND, AdminAction.CANCEL) and len(parts) == 1:
            draft = user_data.get(BROADCAST_DRAFT_KEY)
            if draft is None or draft.token != parts[0]:
                return
            if action == AdminAction.SEND and draft.preview_message_id == query.message.message_id:
                await self.confirm(query, context, draft)
            elif action == AdminAction.CANCEL:
                user_data.pop(BROADCAST_DRAFT_KEY)
                await self.finish_draft(query, AdminText.CANCELLED)

    async def choose_segment(self, query, context, action: AdminAction, parts: list[str]):
        back = [admin_button(AdminText.MENU, AdminAction.MENU)]
        if not parts:
            buttons = [admin_button(label, action, key) for key, label in CATEGORY_LABELS.items()]
            context.user_data.pop(BROADCAST_DRAFT_KEY, None)
            await query.edit_message_text(
                AdminText.CHOOSE_CATEGORY,
                reply_markup=Button.create_markup([buttons, back]),
            )
            return

        category_key = parts[0]
        if category_key not in CATEGORY_LABELS:
            return
        if len(parts) == 1:
            buttons = [
                admin_button(label, action, category_key, key)
                for key, label in PERIOD_LABELS.items()
            ]
            context.user_data.pop(BROADCAST_DRAFT_KEY, None)
            await query.edit_message_text(
                AdminText.CHOOSE_PERIOD,
                reply_markup=Button.create_markup([buttons, back]),
            )
            return

        period = parts[1]
        if period not in PERIOD_LABELS:
            return
        category = None if category_key == ALL_CATEGORIES else AudienceCategory(category_key)
        since = (
            None
            if period == AudiencePeriod.ALL
            else datetime.now(UTC) - timedelta(days=int(period))
        )

        if action == AdminAction.BROADCAST and len(parts) == 2:
            count = await self.audience.count(category, since)
            if not count:
                context.user_data.pop(BROADCAST_DRAFT_KEY, None)
                await query.edit_message_text(AdminText.NO_RECIPIENTS, reply_markup=self.menu())
                return
            draft = BroadcastDraft(uuid4().hex, category, since)
            context.user_data[BROADCAST_DRAFT_KEY] = draft
            await query.edit_message_text(
                AdminText.ENTER_MESSAGE.format(count=count),
                reply_markup=Button.create_markup(
                    [[admin_button(AdminText.CANCEL, AdminAction.CANCEL, draft.token)]]
                ),
            )
        elif action == AdminAction.USERS:
            if len(parts) == 2:
                page = 0
            elif (
                len(parts) == 3 and parts[2].isascii() and parts[2].isdigit() and len(parts[2]) <= 9
            ):
                page = int(parts[2])
            else:
                return
            await self.show_users(query, category_key, category, period, since, page)

    async def show_users(self, query, category_key, category, period, since, page):
        count = await self.audience.count(category, since)
        last_page = max(0, (count - 1) // AUDIENCE_PAGE_SIZE)
        page = min(page, last_page)
        rows = await self.audience.page(
            category, since, offset=page * AUDIENCE_PAGE_SIZE, limit=AUDIENCE_PAGE_SIZE
        )
        lines = [
            f"{CATEGORY_LABELS[category_key]} · {PERIOD_LABELS[period]}",
            AdminText.PAGE.format(count=count, page=page + 1, pages=last_page + 1),
            "",
        ]
        for row in rows:
            name = " ".join(part for part in (row.first_name, row.last_name) if part)
            name = " ".join(name.split())[:DISPLAY_NAME_LIMIT] or AdminText.NO_NAME
            username = f" @{row.username[:DISPLAY_USERNAME_LIMIT]}" if row.username else ""
            lines.append(f"{name}{username} · {row.telegram_id}")

        navigation = []
        if page > 0:
            navigation.append(
                admin_button(AdminText.BACK, AdminAction.USERS, category_key, period, page - 1)
            )
        if page < last_page:
            navigation.append(
                admin_button(AdminText.NEXT, AdminAction.USERS, category_key, period, page + 1)
            )
        buttons = [navigation] if navigation else []
        buttons.append([admin_button(AdminText.MENU, AdminAction.MENU)])
        await query.edit_message_text("\n".join(lines), reply_markup=Button.create_markup(buttons))

    async def receive_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        user_data = context.user_data
        if not self.allowed(update) or message is None or user_data is None:
            return
        draft = user_data.get(BROADCAST_DRAFT_KEY)
        if draft is None or draft.preview_message_id is not None:
            return
        if message.media_group_id:
            await message.reply_text(AdminText.SEND_ONE_MESSAGE)
            return

        keyboard = Button.create_markup(
            [
                [
                    admin_button(AdminText.CONFIRM, AdminAction.SEND, draft.token),
                    admin_button(AdminText.CANCEL, AdminAction.CANCEL, draft.token),
                ]
            ]
        )
        try:
            preview = await context.bot.copy_message(
                chat_id=message.chat_id,
                from_chat_id=message.chat_id,
                message_id=message.message_id,
                reply_markup=keyboard,
            )
        except TelegramError as error:
            logger.warning("Broadcast preview failed: %s", type(error).__name__)
            await message.reply_text(AdminText.PREVIEW_FAILED)
            return
        draft.preview_message_id = preview.message_id

    async def finish_draft(self, query, text: str):
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(text, reply_markup=self.menu())

    async def confirm(self, query, context, draft: BroadcastDraft):
        preview_message_id = draft.preview_message_id
        if preview_message_id is None:
            return
        if self.broadcast_task and not self.broadcast_task.done():
            await query.message.reply_text(AdminText.BUSY)
            return

        recipients = await self.audience.recipient_ids(draft.category, draft.since)
        context.user_data.pop(BROADCAST_DRAFT_KEY)
        if not recipients:
            await self.finish_draft(query, AdminText.NO_RECIPIENTS)
            return

        self.broadcast_task = asyncio.create_task(
            self.broadcast(context.bot, recipients, query.message.chat_id, preview_message_id)
        )
        await self.finish_draft(query, AdminText.STARTED.format(count=len(recipients)))

    async def broadcast(
        self, bot: Bot, recipients: list[int], source_chat_id: int, message_id: int
    ):
        sent = 0
        logger.info("Broadcast started: recipients=%s", len(recipients))
        for index, telegram_id in enumerate(recipients):
            if index:
                await asyncio.sleep(BROADCAST_DELAY_SECONDS)
            while True:
                try:
                    await bot.copy_message(
                        chat_id=telegram_id,
                        from_chat_id=source_chat_id,
                        message_id=message_id,
                    )
                    sent += 1
                    break
                except RetryAfter as error:
                    delay = error.retry_after
                    await asyncio.sleep(
                        delay.total_seconds() if isinstance(delay, timedelta) else delay
                    )
                except TelegramError as error:
                    logger.warning(
                        "Broadcast delivery failed for %s: %s",
                        telegram_id,
                        type(error).__name__,
                    )
                    break
        failed = len(recipients) - sent
        logger.info("Broadcast finished: sent=%s failed=%s", sent, failed)
        try:
            await bot.send_message(
                chat_id=self.owner_id,
                text=AdminText.REPORT.format(total=len(recipients), sent=sent, failed=failed),
            )
        except TelegramError as error:
            logger.warning("Broadcast report delivery failed: %s", type(error).__name__)

    async def stop(self):
        if self.broadcast_task is not None:
            if not self.broadcast_task.done():
                logger.info("Cancelling active broadcast on shutdown")
                self.broadcast_task.cancel()
            await asyncio.gather(self.broadcast_task, return_exceptions=True)
