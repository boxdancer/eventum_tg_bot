from constants.constants import MATERIAL_CALLBACK_PREFIX, MATERIALS, MaterialKey
from logger_config import get_logger
from telegram import Message, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.utils.button import Button
from bot.utils.subscription_checker import is_subscribed, send_subscription_required

logger = get_logger(__name__)


async def handle_material_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle material callback: material:{MaterialKey}"""
    query = update.callback_query
    if query is None or query.data is None or not query.data.startswith(MATERIAL_CALLBACK_PREFIX):
        return

    await query.answer()
    message = query.message
    if not isinstance(message, Message):
        return

    try:
        material_key = MaterialKey(query.data.removeprefix(MATERIAL_CALLBACK_PREFIX))
    except ValueError:
        logger.warning("Unknown material: %s", query.data)
        return

    if not await is_subscribed(context.bot, query.from_user.id):
        await send_subscription_required(message)
        return

    material = MATERIALS[material_key]
    await message.reply_text(
        text=material.message,
        reply_markup=Button.create_markup([[Button(material.button_text, url=material.url)]]),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
