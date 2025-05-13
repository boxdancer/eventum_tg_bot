import logging
import os
import asyncio
import enum

from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class ExamType(str, enum.Enum):
    OGE = "ОГЭ"
    EGE = "ЕГЭ"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[ExamType.OGE, ExamType.EGE]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    msg = "Привет! 👋 Добро пожаловать! Какой экзамен сдаешь? :)"
    await update.message.reply_text(msg, reply_markup=reply_markup)
    logger.warning("Message shown to user: %s", msg)


async def send_delayed_message(update: Update, message: str, delay: int):
    await asyncio.sleep(delay)
    await update.message.reply_text(message)
    logger.warning("Сообщение отправлено через %d секунд: %s", delay, message)


async def handle_exam_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text

    if user_choice == ExamType.EGE.value:
        # Отправляем первое сообщение сразу
        await update.message.reply_text("Вот первый файл")
        logger.warning("Первое сообщение отправлено.")

        # Создаем асинхронную задачу для второго сообщения с задержкой
        asyncio.create_task(send_delayed_message(update, "Вот второй файл", 60))

    else:
        # В случае, если пользователь выбрал "ОГЭ", можно добавить другую логику
        await update.message.reply_text(f"Вы выбрали {user_choice}.")
        logger.warning("Выбор пользователя: %s", user_choice)


async def main():
    bot = Bot(token=TOKEN)

    # Получаем список накопленных апдейтов
    pending_updates = await bot.get_updates()
    logger.warning("❗ Пропущено входящих сообщений: %s", len(pending_updates))

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Обработчик для ответа на выбор экзамена
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_exam_choice))

    # Запускаем по шагам, чтобы избежать ошибок с event loop
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    logger.warning("🟢 Telegram бот запущен...")

    # Бесконечно держим бота активным
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
