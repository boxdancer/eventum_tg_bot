import asyncio
from telegram import Update, Message
from telegram.ext import ContextTypes

from bot.utils.button import Button
from bot.utils.message_scheduler import MessageScheduler
from constants.constants import (
    ExamType,
    EGE_MESSAGE_1,
    TEXT_EGE_BTN_1,
    URL_EGE_BTN_1,
    DELAY_MSG_0,
    DELAY_MSG_20,
    EGE_MESSAGE_2,
    EGE_MESSAGE_3,
    TEXT_EGE_BTN_3,
    DELAY_MSG_50,
    URL_EGE_BTN_3,
    EGE_MESSAGE_4,
    DELAY_MSG_80,
    URL_EGE_BTN_4,
    TEXT_EGE_BTN_4,
    OGE_MESSAGE_1,
    TEXT_OGE_BTN_1,
    URL_OGE_BTN_1,
    OGE_MESSAGE_2,
    OGE_MESSAGE_3,
    TEXT_OGE_BTN_3,
    URL_OGE_BTN_3,
    URL_OGE_BTN_4,
    TEXT_OGE_BTN_4,
    OGE_MESSAGE_4,
)


class ExamFlowHandler:
    def __init__(self, scheduler: MessageScheduler):
        self.scheduler = scheduler

    async def handle_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query:
            return
        await query.answer()
        user_choice = query.data
        username = query.from_user.name
        message = query.message

        if user_choice == ExamType.EGE:
            await self._handle_ege(message, username)
        elif user_choice == ExamType.OGE:
            await self._handle_oge(message, username)

    async def _handle_ege(self, message: Message, username: str):
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_1,
                DELAY_MSG_0,
                username,
                Button(TEXT_EGE_BTN_1, url=URL_EGE_BTN_1),
            )
        )
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message, EGE_MESSAGE_2, DELAY_MSG_20, username
            )
        )
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_3,
                DELAY_MSG_50,
                username,
                Button(TEXT_EGE_BTN_3, url=URL_EGE_BTN_3),
            )
        )
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_4,
                DELAY_MSG_80,
                username,
                Button(TEXT_EGE_BTN_4, url=URL_EGE_BTN_4),
            )
        )

    async def _handle_oge(self, message: Message, username: str):
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_1,
                DELAY_MSG_0,
                username,
                Button(TEXT_OGE_BTN_1, url=URL_OGE_BTN_1),
            )
        )
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message, OGE_MESSAGE_2, DELAY_MSG_20, username
            )
        )
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_3,
                DELAY_MSG_50,
                username,
                Button(TEXT_OGE_BTN_3, url=URL_OGE_BTN_3),
            )
        )
        asyncio.create_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_4,
                DELAY_MSG_80,
                username,
                Button(TEXT_OGE_BTN_4, url=URL_OGE_BTN_4),
            )
        )
