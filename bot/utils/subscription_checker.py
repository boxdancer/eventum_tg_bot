import os
import re
from functools import wraps

from constants.constants import SUBSCRIPTION_REQUIRED_MESSAGE
from logger_config import get_logger
from telegram import Bot, Message, Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from bot.utils.button import Button

logger = get_logger(__name__)

ALLOWED_STATUSES = {"member", "administrator", "creator"}


def subscription_channel() -> str:
    username = os.getenv("SUBSCRIPTION_CHANNEL", "").strip().removeprefix("@")
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        raise ValueError("SUBSCRIPTION_CHANNEL must contain a public Telegram username")
    return username


def requires_subscription(func):
    """Decorator that checks subscription before executing command handler."""

    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        message = update.effective_message
        user = update.effective_user
        if message is None or user is None:
            return
        if not await is_subscribed(context.bot, user.id):
            await send_subscription_required(message)
            return
        return await func(self, update, context, *args, **kwargs)

    return wrapper


async def is_subscribed(bot: Bot, user_id: int) -> bool:
    """Check if user is subscribed to the channel."""
    channel = f"@{subscription_channel()}"
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        result = member.status in ALLOWED_STATUSES

        logger.info("Subscription: user=%d, status=%s, ok=%s", user_id, member.status, result)
        return result
    except TelegramError as e:
        logger.error("Subscription check failed: %s", e)
        return False


async def send_subscription_required(message: Message):
    """Send subscription required message with channel button."""
    button = Button("Подписаться на канал", url=f"https://t.me/{subscription_channel()}")
    await message.reply_text(
        text=SUBSCRIPTION_REQUIRED_MESSAGE,
        reply_markup=Button.create_markup([[button]]),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
