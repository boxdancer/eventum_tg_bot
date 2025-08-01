import asyncio
import logging
from io import BytesIO
from telegram import Message
from telegram.constants import ParseMode

from bot.utils.button import Button

logger = logging.getLogger(__name__)


class MessageScheduler:
    @staticmethod
    async def send_delayed_message(
        message: Message,
        text: str,
        delay: int,
        username: str,
        button: Button | None = None,
    ):
        await asyncio.sleep(delay)
        reply_markup = Button.create_markup([[button]]) if button else None
        await message.reply_text(
            text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2
        )
        logger.info("Message delivered to user: %s after %d min", username, delay // 60)

    @staticmethod
    async def send_delayed_photo(
        message: Message,
        text: str,
        photo: BytesIO,
        delay: int,
        username: str,
        button: Button | None = None,
    ):
        await asyncio.sleep(delay)
        reply_markup = Button.create_markup([[button]]) if button else None
        await message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        logger.info("Photo delivered to user: %s after %d min", username, delay // 60)
