import asyncio
import logging
import os
from io import BytesIO

from dotenv import load_dotenv
from telegram import (
    Update,
    Bot,
    BotCommand,
    Message,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    Application,
)

from bot.handlers.exam_flow import ExamFlowHandler
from bot.utils.button import Button
from bot.utils.message_scheduler import MessageScheduler
from constants.constants import (
    GREETING_MESSAGE,
    EGE_MESSAGE_3,
    EGE_MESSAGE_4,
    ExamType,
    OGE_MESSAGE_3,
    OGE_MESSAGE_4,
    GREETING_PHOTO,
)

# Logger setup
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Loading envs
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
        self.exam_flow = ExamFlowHandler(self.scheduler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = [
            [
                Button(text=ExamType.OGE, callback_data=ExamType.OGE),
                Button(text=ExamType.EGE, callback_data=ExamType.EGE),
            ]
        ]
        reply_markup = Button.create_markup(buttons)
        # Direct message to the bot owner about potential customer
        msg = f"/start triggered by user: @{update.message.chat.username}"
        await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        if update.message:
            await update.message.reply_photo(
                photo=BytesIO(GREETING_PHOTO),
                caption=GREETING_MESSAGE,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            logger.warning(msg)

    async def handle_inline_choice(self, update, context):
        await self.exam_flow.handle_choice(update, context)

    async def send_delayed_message(
        self,
        message: Message,
        text: str,
        delay: int,
        username: str,
        button: Button | None = None,
    ):
        await asyncio.sleep(delay)
        reply_markup = None
        if button:
            reply_markup = Button.create_markup([[button]])
        await message.reply_text(
            text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
        )
        logger.warning(
            "Message delivered to user: %s after %d min", username, delay // 60
        )

    async def send_delayed_photo(
        self,
        message: Message,
        text: str,
        photo: BytesIO,
        delay: int,
        username: str,
        button: Button | None = None,
    ):
        await asyncio.sleep(delay)
        reply_markup = None
        if button:
            reply_markup = Button.create_markup([[button]])
        await message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        logger.warning(
            "Photo with text delivered to user: %s after %d min",
            username,
            delay // 60,
        )

    async def run(self):
        # Skip messages while bot offline
        pending_updates = await self.bot.get_updates()
        logger.warning(
            "❗ Messages skipped while bot inactive: %s", len(pending_updates)
        )

        await self.bot.set_my_commands(
            [
                BotCommand(command="start", description="Начать заново"),
                BotCommand(command="plan_oge", description="План ОГЭ"),
                BotCommand(command="plan_ege", description="План ЕГЭ"),
                BotCommand(command="test_oge", description="Тест ОГЭ"),
                BotCommand(command="test_ege", description="Тест ЕГЭ"),
            ]
        )

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("plan_oge", self.plan_oge))
        self.application.add_handler(CommandHandler("plan_ege", self.plan_ege))
        self.application.add_handler(CommandHandler("test_oge", self.test_oge))
        self.application.add_handler(CommandHandler("test_ege", self.test_ege))
        self.application.add_handler(CallbackQueryHandler(self.handle_inline_choice))

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)

        logger.warning("🟢 Telegram bot started...")
        await asyncio.Event().wait()

    async def plan_oge(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(OGE_MESSAGE_3, parse_mode=ParseMode.MARKDOWN_V2)

    async def plan_ege(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(EGE_MESSAGE_3, parse_mode=ParseMode.MARKDOWN_V2)

    async def test_oge(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(OGE_MESSAGE_4, parse_mode=ParseMode.MARKDOWN_V2)

    async def test_ege(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(EGE_MESSAGE_4, parse_mode=ParseMode.MARKDOWN_V2)


if __name__ == "__main__":
    bot_handler = BotHandler(TOKEN)
    asyncio.run(bot_handler.run())
