import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from bot.audience import Audience
from bot.handlers.handlers import EgeProfileHandler, EgeBaseHandler, OgeHandler
from bot.utils.subscription_checker import is_subscribed, send_subscription_required
from constants.audience import AudienceCategory
from constants.constants import ExamType


class ExamFlowHandler:
    def __init__(self, scheduler, owner_id: int, audience: Audience):
        self.scheduler = scheduler
        self.owner_id = owner_id
        self.audience = audience
        self.tasks = set()
        self.handlers = {
            ExamType.EGE_PROFILE: (
                EgeProfileHandler(scheduler, self),
                AudienceCategory.EGE,
            ),
            ExamType.EGE_BASE: (EgeBaseHandler(scheduler, self), AudienceCategory.EGE),
            ExamType.OGE: (OgeHandler(scheduler, self), AudienceCategory.OGE),
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
        user_choice = query.data
        flow = self.handlers.get(user_choice)
        if flow is None:
            return
        await query.answer()
        user_id = query.from_user.id

        if not await is_subscribed(context.bot, user_id):
            await send_subscription_required(query.message)
            return

        handler, category = flow
        await self.audience.set_category(user_id, category)

        await context.bot.send_message(
            chat_id=self.owner_id,
            text=f"{query.from_user.name} chose: {user_choice}",
        )

        await handler.handle(query.message, query.from_user.name)
