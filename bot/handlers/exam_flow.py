import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.handlers import EgeHandler, OgeHandler
from constants.constants import (
    ExamType,
)


class ExamFlowHandler:
    def __init__(self, scheduler):
        self.scheduler = scheduler
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

        handler = self.handlers.get(user_choice)
        if handler:
            await handler.handle(message, username)
