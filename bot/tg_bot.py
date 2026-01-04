import asyncio
import os
from io import BytesIO
from functools import partial

from dotenv import load_dotenv
from telegram import Update, Bot, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    Application,
)

from bot.handlers.exam_flow import ExamFlowHandler
from bot.handlers.material_handler import handle_material_callback
from bot.utils.button import Button
from bot.utils.message_scheduler import MessageScheduler
from bot.utils.subscription_checker import is_subscribed, send_subscription_required
from constants.constants import (
    GREETING_MESSAGE,
    GREETING_PHOTO,
    ExamType,
    CHECK_SUBSCRIPTION_CHANNEL_USERNAME,
    MATERIALS,
    COMMAND_MATERIALS,
    COMMAND_DESCRIPTIONS,
    MaterialKey,
    Command,
)
from logger_config import get_logger

logger = get_logger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")


class BotHandler:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)
        self.application: Application = ApplicationBuilder().token(self.token).build()
        self.scheduler = MessageScheduler()
        self.exam_flow = ExamFlowHandler(self.scheduler, owner_id=OWNER_ID)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = [[
            Button(text=ExamType.OGE, callback_data=ExamType.OGE),
            Button(text=ExamType.EGE_PROFILE, callback_data=ExamType.EGE_PROFILE),
            Button(text=ExamType.EGE_BASE, callback_data=ExamType.EGE_BASE),
        ]]
        
        msg = f"/start triggered by user: @{update.message.chat.username}"
        await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        
        await update.message.reply_photo(
            photo=BytesIO(GREETING_PHOTO),
            caption=GREETING_MESSAGE,
            reply_markup=Button.create_markup(buttons),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        logger.info(msg)

    async def handle_material_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, material_key: MaterialKey
    ):
        """Generic handler for material commands with subscription check."""
        if not await is_subscribed(context.bot, update.message.from_user.id, CHECK_SUBSCRIPTION_CHANNEL_USERNAME):
            await send_subscription_required(update.message)
            return

        material = MATERIALS[material_key]
        await update.message.reply_text(
            text=material.message,
            reply_markup=Button.create_markup([[Button(material.button_text, url=material.url)]]),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    async def run(self):
        pending_updates = await self.bot.get_updates()
        logger.info("❗ Messages skipped while bot inactive: %s", len(pending_updates))

        await self.bot.set_my_commands([
            BotCommand(command=cmd, description=desc)
            for cmd, desc in COMMAND_DESCRIPTIONS.items()
        ])

        self.application.add_handler(CommandHandler(Command.START, self.start))
        
        # Register material commands dynamically
        for cmd, material_key in COMMAND_MATERIALS.items():
            handler = partial(self.handle_material_command, material_key=material_key)
            self.application.add_handler(CommandHandler(cmd, handler))

        self.application.add_handler(CallbackQueryHandler(self.exam_flow.handle_choice))
        self.application.add_handler(
            CallbackQueryHandler(handle_material_callback, pattern="^material:")
        )

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)

        logger.info("🟢 Telegram bot started...")
        await asyncio.Event().wait()


if __name__ == "__main__":
    bot_handler = BotHandler(TOKEN)
    asyncio.run(bot_handler.run())
