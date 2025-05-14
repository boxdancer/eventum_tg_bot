import logging
import os
import asyncio
import enum

from telegram import (
    Update,
    Bot,
    InlineKeyboardMarkup,
    InlineKeyboardButton, BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Константы задержка перед отправкой
DELAY_MSG_MIN_20 = 4
DELAY_MSG_MIN_40 = 8


# Типы экзаменов
class ExamType(str, enum.Enum):
    OGE = "ОГЭ"
    EGE = "ЕГЭ"


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(text=ExamType.OGE, callback_data=ExamType.OGE),
            InlineKeyboardButton(text=ExamType.EGE, callback_data=ExamType.EGE),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = "Привет! 👋 Добро пожаловать! Какой экзамен сдаешь? :)"
    await update.message.reply_text(msg, reply_markup=reply_markup)
    logger.warning("/start command triggered by user: %s", update.message.chat.username)


# Отложенное сообщение
async def send_delayed_message(message, text: str, delay: int, user: str):
    await asyncio.sleep(delay)
    await message.reply_text(text)
    logger.warning("Cообщение отправлено пользователю: %s спустя: %d с", user, delay)


# Обработка нажатий на inline-кнопки
async def handle_inline_choice(update: Update, *args, **kwargs):
    query = update.callback_query
    await query.answer()

    user_choice = query.data

    match user_choice:
        case ExamType.EGE:
            await query.message.reply_text("Вот первый файл ЕГЭ")
            logger.warning("Первое сообщение ЕГЭ отправлено пользователю: %s", query.from_user.name)
            asyncio.create_task(
                send_delayed_message(query.message, "Вот второй файл ЕГЭ", DELAY_MSG_MIN_20, query.from_user.name))
            asyncio.create_task(
                send_delayed_message(query.message, "Вот третий файл ЕГЭ", DELAY_MSG_MIN_40, query.from_user.name))
        case ExamType.OGE:
            await query.message.reply_text("Вот первый файл ОГЭ")
            logger.warning("Первое сообщение ОГЭ отправлено пользователю: %s", query.from_user.name)
            asyncio.create_task(
                send_delayed_message(query.message, "Вот второй файл ОГЭ", DELAY_MSG_MIN_20, query.from_user.name))
            asyncio.create_task(
                send_delayed_message(query.message, "Вот третий файл ОГЭ", DELAY_MSG_MIN_40, query.from_user.name))
        case _:
            pass


# Главная точка входа
async def main():
    bot = Bot(token=TOKEN)

    # Проверка накопленных апдейтов
    pending_updates = await bot.get_updates()
    logger.warning("❗ Пропущено входящих сообщений: %s", len(pending_updates))

    await bot.set_my_commands([
        BotCommand(command="start", description="Начать заново"),
        # Можно добавить другие команды тут
    ])

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_inline_choice))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    logger.warning("🟢 Telegram бот запущен...")

    # Поддержка бота в активном состоянии
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
