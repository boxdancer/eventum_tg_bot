from .base_exam_handler import IExamHandler
from constants.constants import (
    EGE_PROFILE_MESSAGE_1,
    EGE_PROFILE_MESSAGE_2,
    EGE_PROFILE_MESSAGE_3,
    EGE_PROFILE_MESSAGE_4,
    EGE_BASE_MESSAGE_1,
    EGE_BASE_MESSAGE_3,
    EGE_BASE_MESSAGE_4,
    OGE_MESSAGE_1,
    OGE_MESSAGE_2,
    OGE_MESSAGE_3,
    OGE_MESSAGE_4,
    FREE_VIDEOLESSON_MESSAGE,
    DELAY_MSG_0,
    DELAY_MSG_20,
    DELAY_MSG_50,
    DELAY_MSG_80,
    DELAY_MSG_90,
    MaterialKey,
    MATERIALS,
)
from ..utils.button import Button


class BaseExamHandler(IExamHandler):
    """Base handler for exam flow with message sequence."""
    
    messages: list = []  # [(msg_text, delay, MaterialKey | None), ...]

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


class EgeProfileHandler(BaseExamHandler):
    messages = [
        (EGE_PROFILE_MESSAGE_1, DELAY_MSG_0, MaterialKey.EGE_PROFILE_1),
        (EGE_PROFILE_MESSAGE_2, DELAY_MSG_20, None),
        (EGE_PROFILE_MESSAGE_3, DELAY_MSG_50, MaterialKey.EGE_PROFILE_3),
        (EGE_PROFILE_MESSAGE_4, DELAY_MSG_80, MaterialKey.EGE_PROFILE_4),
        (FREE_VIDEOLESSON_MESSAGE, DELAY_MSG_90, None),
    ]


class EgeBaseHandler(BaseExamHandler):
    messages = [
        (EGE_BASE_MESSAGE_1, DELAY_MSG_0, MaterialKey.EGE_BASE_1),
        (EGE_BASE_MESSAGE_3, DELAY_MSG_20, MaterialKey.EGE_BASE_3),
        (EGE_BASE_MESSAGE_4, DELAY_MSG_50, MaterialKey.EGE_BASE_4),
        (FREE_VIDEOLESSON_MESSAGE, DELAY_MSG_90, None),
    ]


class OgeHandler(BaseExamHandler):
    messages = [
        (OGE_MESSAGE_1, DELAY_MSG_0, MaterialKey.OGE_1),
        (OGE_MESSAGE_2, DELAY_MSG_20, None),
        (OGE_MESSAGE_3, DELAY_MSG_50, MaterialKey.OGE_3),
        (OGE_MESSAGE_4, DELAY_MSG_80, MaterialKey.OGE_4),
        (FREE_VIDEOLESSON_MESSAGE, DELAY_MSG_90, None),
    ]
