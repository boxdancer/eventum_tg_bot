from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.utils.button import Button
from bot.utils.subscription_checker import is_subscribed, send_subscription_required
from constants.constants import MATERIAL_CALLBACK_PREFIX, MATERIALS, MaterialKey
from logger_config import get_logger

logger = get_logger(__name__)


async def handle_material_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle material callback: material:{MaterialKey}"""
    query = update.callback_query
    if not query or not query.data.startswith(MATERIAL_CALLBACK_PREFIX):
        return

    await query.answer()

    try:
        material_key = MaterialKey(query.data.removeprefix(MATERIAL_CALLBACK_PREFIX))
    except ValueError:
        logger.warning("Unknown material: %s", query.data)
        return

    if not await is_subscribed(context.bot, query.from_user.id):
        await send_subscription_required(query.message)
        return

    material = MATERIALS[material_key]
    await query.message.reply_text(
        text=material.message,
        reply_markup=Button.create_markup(
            [[Button(material.button_text, url=material.url)]]
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
