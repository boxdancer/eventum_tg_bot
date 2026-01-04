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
    DELAY_MSG_0,
    DELAY_MSG_20,
    DELAY_MSG_50,
    DELAY_MSG_80,
    MaterialKey,
    MATERIALS,
)
from ..utils.button import Button


class BaseExamHandler(IExamHandler):
    """Base handler for exam flow with message sequence."""
    
    messages: list = []  # [(msg_text, delay, MaterialKey), ...]

    def __init__(self, scheduler, exam_flow):
        self.scheduler = scheduler
        self.exam_flow = exam_flow

    async def handle(self, message, username):
        for msg_text, delay, material_key in self.messages:
            button = None
            if material_key:
                material = MATERIALS[material_key]
                button = Button(material.button_text, url=material.url)
            self.exam_flow.track_task(
                self.scheduler.send_delayed_message(message, msg_text, delay, username, button)
            )


class EgeHandler(BaseExamHandler):
    messages = [
        (EGE_MESSAGE_1, DELAY_MSG_0, MaterialKey.EGE_1),
        (EGE_MESSAGE_2, DELAY_MSG_20, None),
        (EGE_MESSAGE_3, DELAY_MSG_50, MaterialKey.EGE_3),
        (EGE_MESSAGE_4, DELAY_MSG_80, MaterialKey.EGE_4),
    ]


class OgeHandler(BaseExamHandler):
    messages = [
        (OGE_MESSAGE_1, DELAY_MSG_0, MaterialKey.OGE_1),
        (OGE_MESSAGE_2, DELAY_MSG_20, None),
        (OGE_MESSAGE_3, DELAY_MSG_50, MaterialKey.OGE_3),
        (OGE_MESSAGE_4, DELAY_MSG_80, MaterialKey.OGE_4),
    ]
