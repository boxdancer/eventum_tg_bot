import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.handlers import EgeHandler, OgeHandler
from constants.constants import (
    ExamType,
)
from logger_config import get_logger

logger = get_logger(__name__)


class ExamFlowHandler:
    def __init__(self, scheduler, owner_id: str):
        self.scheduler = scheduler
        self.owner_id = owner_id
        self.tasks = []
        self.handlers = {
            ExamType.EGE: EgeHandler(scheduler, self),
            ExamType.OGE: OgeHandler(scheduler, self),
        }

    def track_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)

    async def handle_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query:
            return
        await query.answer()
        user_choice = query.data
        username = query.from_user.name
        message = query.message

        msg = f"{username} chose: {user_choice}"
        await context.bot.send_message(chat_id=self.owner_id, text=msg)
        logger.info(msg)

        handler = self.handlers.get(user_choice)
        if handler:
            await handler.handle(message, username)
