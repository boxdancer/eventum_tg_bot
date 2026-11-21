import asyncio

from constants.audience import AudienceCategory
from constants.constants import ExamType
from telegram import Message, Update
from telegram.ext import ContextTypes

from bot.audience import Audience
from bot.handlers.handlers import EgeBaseHandler, EgeProfileHandler, OgeHandler
from bot.utils.subscription_checker import is_subscribed, send_subscription_required


class ExamFlowHandler:
    def __init__(self, scheduler, owner_id: int, audience: Audience):
        self.scheduler = scheduler
        self.owner_id = owner_id
        self.audience = audience
        self.tasks: set[asyncio.Task[None]] = set()
        self.handlers = {
            ExamType.EGE_PROFILE.value: (
                EgeProfileHandler(scheduler, self),
                AudienceCategory.EGE,
            ),
            ExamType.EGE_BASE.value: (EgeBaseHandler(scheduler, self), AudienceCategory.EGE),
            ExamType.OGE.value: (OgeHandler(scheduler, self), AudienceCategory.OGE),
        }

    def track_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def stop(self):
        tasks = list(self.tasks)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def handle_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query:
            return
        await query.answer()
        message = query.message
        user_choice = query.data
        if not isinstance(message, Message) or user_choice is None:
            return
        flow = self.handlers.get(user_choice)
        if flow is None:
            return
        user_id = query.from_user.id

        if not await is_subscribed(context.bot, user_id):
            await send_subscription_required(message)
            return

        handler, category = flow
        await self.audience.set_category(user_id, category)

        await context.bot.send_message(
            chat_id=self.owner_id,
            text=f"{query.from_user.name} chose: {user_choice}",
        )

        await handler.handle(message, query.from_user.name)
