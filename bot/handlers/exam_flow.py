import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.handlers import EgeHandler, OgeHandler
from bot.utils.subscription_checker import is_subscribed, send_subscription_required
from constants.constants import ExamType, CHECK_SUBSCRIPTION_CHANNEL_USERNAME
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

        user_id = query.from_user.id
        user_choice = query.data

        if not await is_subscribed(context.bot, user_id, CHECK_SUBSCRIPTION_CHANNEL_USERNAME):
            await send_subscription_required(query.message)
            return

        await context.bot.send_message(
            chat_id=self.owner_id,
            text=f"{query.from_user.name} chose: {user_choice}",
        )

        handler = self.handlers.get(user_choice)
        if handler:
            await handler.handle(query.message, query.from_user.name)
