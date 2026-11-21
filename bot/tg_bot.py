import os
import re
from functools import partial
from io import BytesIO

from constants.admin import ADMIN_CALLBACK_PREFIX
from constants.constants import (
    COMMAND_DESCRIPTIONS,
    COMMAND_MATERIALS,
    FREE_VIDEOLESSON_MESSAGE,
    GREETING_MESSAGE,
    GREETING_PHOTO,
    MATERIAL_CALLBACK_PREFIX,
    MATERIALS,
    Command,
    ExamType,
    MaterialKey,
)
from dotenv import load_dotenv
from logger_config import get_logger
from telegram import BotCommand, Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.audience import Audience
from bot.handlers.admin import AdminHandler
from bot.handlers.exam_flow import ExamFlowHandler
from bot.handlers.material_handler import handle_material_callback
from bot.utils.button import Button
from bot.utils.message_scheduler import MessageScheduler
from bot.utils.subscription_checker import requires_subscription, subscription_channel

logger = get_logger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")


class BotHandler:
    def __init__(self, token: str, owner_id: int):
        self.audience = Audience()
        self.owner_id = owner_id
        self.admin = AdminHandler(self.audience, owner_id)
        self.exam_flow = ExamFlowHandler(MessageScheduler(), owner_id, self.audience)
        self.application = (
            ApplicationBuilder()
            .token(token)
            .post_init(self.post_init)
            .post_stop(self.post_stop)
            .post_shutdown(self.post_shutdown)
            .build()
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        if message is None:
            return
        user = update.effective_user
        if message.chat.type == ChatType.PRIVATE and user and user.id:
            await self.audience.save_user(user)

        buttons = [
            [
                Button(text=ExamType.OGE, callback_data=ExamType.OGE),
                Button(text=ExamType.EGE_PROFILE, callback_data=ExamType.EGE_PROFILE),
                Button(text=ExamType.EGE_BASE, callback_data=ExamType.EGE_BASE),
            ]
        ]

        msg = f"/start triggered by user: @{message.chat.username}"
        await context.bot.send_message(chat_id=self.owner_id, text=msg)

        await message.reply_photo(
            photo=BytesIO(GREETING_PHOTO),
            caption=GREETING_MESSAGE,
            reply_markup=Button.create_markup(buttons),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        logger.info(msg)

    @requires_subscription
    async def handle_material_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        material_key: MaterialKey,
    ):
        """Generic handler for material commands."""
        message = update.effective_message
        if message is None:
            return
        material = MATERIALS[material_key]
        await message.reply_text(
            text=material.message,
            reply_markup=Button.create_markup([[Button(material.button_text, url=material.url)]]),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    @requires_subscription
    async def free_videolesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /free_videolesson command."""
        message = update.effective_message
        if message is None:
            return
        await message.reply_text(
            text=FREE_VIDEOLESSON_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    async def post_init(self, application: Application):
        await self.audience.open()
        await application.bot.set_my_commands(
            [
                BotCommand(command=cmd, description=desc)
                for cmd, desc in COMMAND_DESCRIPTIONS.items()
            ]
        )

    async def post_stop(self, application: Application):
        await self.admin.stop()
        await self.exam_flow.stop()

    async def post_shutdown(self, application: Application):
        await self.audience.close()

    def run(self):
        self.application.add_handler(CommandHandler(Command.START, self.start))
        self.application.add_handler(
            CommandHandler(Command.FREE_VIDEOLESSON, self.free_videolesson)
        )

        for cmd, material_key in COMMAND_MATERIALS.items():
            handler = partial(self.handle_material_command, material_key=material_key)
            self.application.add_handler(CommandHandler(cmd, handler))

        exam_choices = "|".join(re.escape(exam.value) for exam in ExamType)
        self.application.add_handler(
            CallbackQueryHandler(self.exam_flow.handle_choice, pattern=rf"\A(?:{exam_choices})\Z")
        )
        self.application.add_handler(
            CallbackQueryHandler(handle_material_callback, pattern=f"^{MATERIAL_CALLBACK_PREFIX}")
        )
        self.application.add_handler(CommandHandler(Command.ADMIN, self.admin.open))
        self.application.add_handler(
            CallbackQueryHandler(self.admin.callback, pattern=f"^{ADMIN_CALLBACK_PREFIX}")
        )
        self.application.add_handler(
            MessageHandler(
                filters.ChatType.PRIVATE
                & ~filters.COMMAND
                & (
                    filters.TEXT
                    | filters.PHOTO
                    | filters.Document.ALL
                    | filters.VIDEO
                    | filters.ANIMATION
                    | filters.AUDIO
                    | filters.VOICE
                    | filters.VIDEO_NOTE
                ),
                self.admin.receive_message,
            )
        )
        self.application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    subscription_channel()
    if not OWNER_ID or not OWNER_ID.isascii() or not OWNER_ID.isdecimal() or int(OWNER_ID) <= 0:
        raise ValueError("OWNER_ID must be a positive numeric Telegram user ID")
    BotHandler(TOKEN, int(OWNER_ID)).run()
