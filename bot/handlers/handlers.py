from .base_exam_handler import IExamHandler
from constants.constants import (
    EGE_MESSAGE_1,
    EGE_MESSAGE_2,
    EGE_MESSAGE_3,
    EGE_MESSAGE_4,
    OGE_MESSAGE_1,
    OGE_MESSAGE_2,
    OGE_MESSAGE_3,
    OGE_MESSAGE_4,
    TEXT_EGE_BTN_1,
    TEXT_EGE_BTN_3,
    TEXT_EGE_BTN_4,
    TEXT_OGE_BTN_1,
    TEXT_OGE_BTN_3,
    TEXT_OGE_BTN_4,
    DELAY_MSG_0,
    DELAY_MSG_20,
    DELAY_MSG_50,
    DELAY_MSG_80,
    MaterialKey,
)
from ..utils.button import Button


class BaseExamHandler(IExamHandler):
    """Base handler for exam flow with message sequence."""
    
    messages: list = []  # [(msg_text, delay, btn_text, MaterialKey), ...]

    def __init__(self, scheduler, exam_flow):
        self.scheduler = scheduler
        self.exam_flow = exam_flow

    async def handle(self, message, username):
        for msg_text, delay, btn_text, material_key in self.messages:
            button = Button(btn_text, callback_data=f"material:{material_key}") if btn_text else None
            self.exam_flow.track_task(
                self.scheduler.send_delayed_message(message, msg_text, delay, username, button)
            )


class EgeHandler(BaseExamHandler):
    messages = [
        (EGE_MESSAGE_1, DELAY_MSG_0, TEXT_EGE_BTN_1, MaterialKey.EGE_1),
        (EGE_MESSAGE_2, DELAY_MSG_20, None, None),
        (EGE_MESSAGE_3, DELAY_MSG_50, TEXT_EGE_BTN_3, MaterialKey.EGE_3),
        (EGE_MESSAGE_4, DELAY_MSG_80, TEXT_EGE_BTN_4, MaterialKey.EGE_4),
    ]


class OgeHandler(BaseExamHandler):
    messages = [
        (OGE_MESSAGE_1, DELAY_MSG_0, TEXT_OGE_BTN_1, MaterialKey.OGE_1),
        (OGE_MESSAGE_2, DELAY_MSG_20, None, None),
        (OGE_MESSAGE_3, DELAY_MSG_50, TEXT_OGE_BTN_3, MaterialKey.OGE_3),
        (OGE_MESSAGE_4, DELAY_MSG_80, TEXT_OGE_BTN_4, MaterialKey.OGE_4),
    ]
