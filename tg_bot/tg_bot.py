import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import (
    Update,
    Bot,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    Message,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    Application,
)

from constants.constants import (
    GREETING_MESSAGE,
    EGE_MESSAGE_1,
    EGE_MESSAGE_2,
    EGE_MESSAGE_3,
    DELAY_MSG_50,
    DELAY_MSG_20,
    DELAY_MSG_0,
    EGE_MESSAGE_4,
    DELAY_MSG_80,
    ExamType,
    OGE_MESSAGE_1,
    OGE_MESSAGE_2,
    OGE_MESSAGE_3,
    OGE_MESSAGE_4,
)

# Logger setup
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Loading envs
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")


class BotHandler:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)
        self.application: Application = ApplicationBuilder().token(self.token).build()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton(text=ExamType.OGE, callback_data=ExamType.OGE),
                InlineKeyboardButton(text=ExamType.EGE, callback_data=ExamType.EGE),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message:
            await update.message.reply_text(GREETING_MESSAGE, reply_markup=reply_markup)
            logger.warning("/start triggered by user: %s", update.message.chat.username)

    async def handle_inline_choice(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        if not query:
            return
        await query.answer()
        user_choice = query.data
        username = query.from_user.name
        message = query.message

        match user_choice:
            case ExamType.EGE:
                asyncio.create_task(
                    self.send_delayed_message(
                        message, EGE_MESSAGE_1, DELAY_MSG_0, username
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message, EGE_MESSAGE_2, DELAY_MSG_20, username
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message, EGE_MESSAGE_3, DELAY_MSG_50, username
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message, EGE_MESSAGE_4, DELAY_MSG_80, username
                    )
                )
            case ExamType.OGE:
                asyncio.create_task(
                    self.send_delayed_message(
                        message, OGE_MESSAGE_1, DELAY_MSG_0, username
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message, OGE_MESSAGE_2, DELAY_MSG_20, username
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message, OGE_MESSAGE_3, DELAY_MSG_50, username
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message, OGE_MESSAGE_4, DELAY_MSG_80, username
                    )
                )

    async def send_delayed_message(
        self, message: Message, text: str, delay: int, username: str
    ):
        await asyncio.sleep(delay)
        await message.reply_text(text)
        logger.warning("Message delivered to user: %s after %d s", username, delay)

    async def run(self):
        # Skip messages while bot offline
        pending_updates = await self.bot.get_updates()
        logger.warning(
            "❗ Messages skipped while bot inactive: %s", len(pending_updates)
        )

        await self.bot.set_my_commands(
            [
                BotCommand(command="start", description="Начать заново"),
            ]
        )

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.handle_inline_choice))

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)

        logger.warning("🟢 Telegram bot started...")
        await asyncio.Event().wait()


if __name__ == "__main__":
    bot_handler = BotHandler(TOKEN)
    asyncio.run(bot_handler.run())
