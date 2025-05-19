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
    OGE_MESSAGE_4, TEXT_EGE_BTN_1, URL_EGE_BTN_1, TEXT_EGE_BTN_3, URL_EGE_BTN_3, TEXT_OGE_BTN_1, URL_OGE_BTN_1,
    TEXT_OGE_BTN_3, URL_OGE_BTN_3, TEXT_OGE_BTN_4, URL_OGE_BTN_4, TEXT_EGE_BTN_4, URL_EGE_BTN_4,
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


class Button:
    def __init__(self, text: str, url: str | None = None, callback_data: str | None = None):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        if not (url or callback_data):
            raise ValueError("Button must have either 'url' or 'callback_data'")

    def to_telegram(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(self.text, url=self.url, callback_data=self.callback_data)

    @staticmethod
    def create_markup(buttons: list[list["Button"]]) -> InlineKeyboardMarkup:
        keyboard = [[button.to_telegram() for button in row] for row in buttons]
        return InlineKeyboardMarkup(keyboard)


class BotHandler:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)
        self.application: Application = ApplicationBuilder().token(self.token).build()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = [
            [
                Button(text=ExamType.OGE, callback_data=ExamType.OGE),
                Button(text=ExamType.EGE, callback_data=ExamType.EGE)
            ]
        ]
        reply_markup = Button.create_markup(buttons)
        # Direct message to the bot owner about potential customer
        msg = f"/start triggered by user: @{update.message.chat.username}"
        await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        if update.message:
            await update.message.reply_text(GREETING_MESSAGE, reply_markup=reply_markup)
            logger.warning(msg)

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
                        message=message,
                        text=EGE_MESSAGE_1,
                        delay=DELAY_MSG_0,
                        username=username,
                        button=Button(
                            text=TEXT_EGE_BTN_1,
                            url=URL_EGE_BTN_1,
                        )
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message, text=EGE_MESSAGE_2, delay=DELAY_MSG_20, username=username,
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message,
                        text=EGE_MESSAGE_3,
                        delay=DELAY_MSG_50,
                        username=username,
                        button=Button(
                            text=TEXT_EGE_BTN_3,
                            url=URL_EGE_BTN_3,
                        )
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message,
                        text=EGE_MESSAGE_4,
                        delay=DELAY_MSG_80,
                        username=username,
                        button=Button(
                            text=TEXT_EGE_BTN_4,
                            url=URL_EGE_BTN_4,
                        )
                    )
                )
            case ExamType.OGE:
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message,
                        text=OGE_MESSAGE_1,
                        delay=DELAY_MSG_0,
                        username=username,
                        button=Button(
                            text=TEXT_OGE_BTN_1,
                            url=URL_OGE_BTN_1,
                        )
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message, text=OGE_MESSAGE_2, delay=DELAY_MSG_20, username=username,
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message,
                        text=OGE_MESSAGE_3,
                        delay=DELAY_MSG_50,
                        username=username,
                        button=Button(
                            text=TEXT_OGE_BTN_3,
                            url=URL_OGE_BTN_3,
                        )
                    )
                )
                asyncio.create_task(
                    self.send_delayed_message(
                        message=message,
                        text=OGE_MESSAGE_4,
                        delay=DELAY_MSG_80,
                        username=username,
                        button=Button(
                            text=TEXT_OGE_BTN_4,
                            url=URL_OGE_BTN_4,
                        )
                    )
                )

    async def send_delayed_message(
        self, message: Message, text: str, delay: int, username: str, button: Button | None = None
    ):
        await asyncio.sleep(delay)
        reply_markup = None
        if button:
            reply_markup = Button.create_markup([[button]])
        await message.reply_text(text, reply_markup=reply_markup)
        logger.warning("Message delivered to user: %s after %d min", username, delay // 60)

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
