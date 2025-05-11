import logging
import os
import asyncio

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Привет! 👋 Добро пожаловать, как и обещал вот твои файлы :)"
    await update.message.reply_text(msg)
    logger.warning("Message shown to user: %s", msg)

async def main():
    bot = Bot(token=TOKEN)

    # Получаем список накопленных апдейтов
    pending_updates = await bot.get_updates()
    logger.warning("❗ Пропущено входящих сообщений: %s", len(pending_updates))

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Запускаем по шагам, чтобы избежать ошибок с event loop
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    logger.warning("🟢 Telegram бот запущен...")

    # Бесконечно держим бота активным
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

