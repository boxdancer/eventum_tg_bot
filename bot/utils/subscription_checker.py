from telegram import Bot, Message
from telegram.constants import ParseMode

from bot.utils.button import Button
from constants.constants import (
    CHECK_SUBSCRIPTION_CHANNEL,
    SUBSCRIPTION_REQUIRED_MESSAGE,
)
from logger_config import get_logger

logger = get_logger(__name__)

ALLOWED_STATUSES = {"member", "administrator", "creator"}


async def is_subscribed(bot: Bot, user_id: int, channel_username: str) -> bool:
    """Check if user is subscribed to the channel."""
    try:
        if not channel_username.startswith("@"):
            channel_username = f"@{channel_username}"
        
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        result = member.status in ALLOWED_STATUSES
        
        logger.info("Subscription: user=%d, status=%s, ok=%s", user_id, member.status, result)
        return result
    except Exception as e:
        logger.error("Subscription check failed: %s", e)
        return False


async def send_subscription_required(message: Message):
    """Send subscription required message with channel button."""
    button = Button("Подписаться на канал", url=CHECK_SUBSCRIPTION_CHANNEL)
    await message.reply_text(
        text=SUBSCRIPTION_REQUIRED_MESSAGE,
        reply_markup=Button.create_markup([[button]]),
        parse_mode=ParseMode.MARKDOWN_V2,
    )

