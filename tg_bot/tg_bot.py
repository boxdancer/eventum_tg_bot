import logging
import os
import asyncio
import enum

from telegram import (
    Update,
    Bot,
    InlineKeyboardMarkup,
    InlineKeyboardButton, BotCommand,
    Message,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    Application,
)
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env")

# Константы задержки
DELAY_MSG_1 = 4
DELAY_MSG_2 = 8


class ExamType(str, enum.Enum):
    OGE = "ОГЭ"
    EGE = "ЕГЭ"


class BotHandler:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)
        self.application: Application = ApplicationBuilder().token(self.token).build()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[
            InlineKeyboardButton(text=ExamType.OGE, callback_data=ExamType.OGE),
            InlineKeyboardButton(text=ExamType.EGE, callback_data=ExamType.EGE),
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = "Привет! 👋 Добро пожаловать! Какой экзамен сдаешь? :)"
        if update.message:
            await update.message.reply_text(msg, reply_markup=reply_markup)
            logger.warning("/start triggered by user: %s", update.message.chat.username)

    async def handle_inline_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query:
            return
        await query.answer()
        user_choice = query.data
        username = query.from_user.name
        message = query.message

        match user_choice:
            case ExamType.EGE:
                asyncio.create_task(self.process_exam_choice(message, ExamType.EGE.value, username))
            case ExamType.OGE:
                asyncio.create_task(self.process_exam_choice(message, ExamType.OGE.value, username))

    async def process_exam_choice(self, message: Message, exam: str, username: str):
        await message.reply_text(f"Вот первый файл {exam}")
        logger.warning("Первое сообщение %s отправлено пользователю: %s", exam, username)

        asyncio.create_task(self.send_delayed_message(message, f"Вот второй файл {exam}", DELAY_MSG_1, username))
        asyncio.create_task(self.send_delayed_message(message, f"Вот третий файл {exam}", DELAY_MSG_2, username))

    async def send_delayed_message(self, message: Message, text: str, delay: int, username: str):
        await asyncio.sleep(delay)
        await message.reply_text(text)
        logger.warning("Сообщение отправлено пользователю: %s спустя %d сек", username, delay)

    async def run(self):
        # Очистка старых апдейтов
        pending_updates = await self.bot.get_updates()
        logger.warning("❗ Пропущено входящих сообщений: %s", len(pending_updates))

        await self.bot.set_my_commands([
            BotCommand(command="start", description="Начать заново"),
        ])

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.handle_inline_choice))

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)

        logger.warning("🟢 Telegram бот запущен...")
        await asyncio.Event().wait()


if __name__ == "__main__":
    bot_handler = BotHandler(TOKEN)
    asyncio.run(bot_handler.run())
