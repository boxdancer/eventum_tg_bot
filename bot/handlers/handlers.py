from .base_exam_handler import IExamHandler
from constants.constants import (
    EGE_MESSAGE_1,
    TEXT_EGE_BTN_1,
    URL_EGE_BTN_1,
    DELAY_MSG_0,
    DELAY_MSG_20,
    EGE_MESSAGE_2,
    EGE_MESSAGE_3,
    TEXT_EGE_BTN_3,
    DELAY_MSG_50,
    URL_EGE_BTN_3,
    EGE_MESSAGE_4,
    DELAY_MSG_80,
    URL_EGE_BTN_4,
    TEXT_EGE_BTN_4,
    OGE_MESSAGE_1,
    TEXT_OGE_BTN_1,
    URL_OGE_BTN_1,
    OGE_MESSAGE_2,
    OGE_MESSAGE_3,
    TEXT_OGE_BTN_3,
    URL_OGE_BTN_3,
    URL_OGE_BTN_4,
    TEXT_OGE_BTN_4,
    OGE_MESSAGE_4,
)
from ..utils.button import Button

from logger_config import get_logger

logger = get_logger(__name__)


class EgeHandler(IExamHandler):
    def __init__(self, scheduler, exam_flow):
        self.scheduler = scheduler
        self.exam_flow = exam_flow

    async def handle(self, message, username):
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_1,
                DELAY_MSG_0,
                username,
                Button(TEXT_EGE_BTN_1, url=URL_EGE_BTN_1),
            )
        )
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_2,
                DELAY_MSG_20,
                username,
            )
        )
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_3,
                DELAY_MSG_50,
                username,
                Button(TEXT_EGE_BTN_3, url=URL_EGE_BTN_3),
            )
        )
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                EGE_MESSAGE_4,
                DELAY_MSG_80,
                username,
                Button(TEXT_EGE_BTN_4, url=URL_EGE_BTN_4),
            )
        )


class OgeHandler(IExamHandler):
    def __init__(self, scheduler, exam_flow):
        self.scheduler = scheduler
        self.exam_flow = exam_flow

    async def handle(self, message, username):
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_1,
                DELAY_MSG_0,
                username,
                Button(TEXT_OGE_BTN_1, url=URL_OGE_BTN_1),
            )
        )
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_2,
                DELAY_MSG_20,
                username,
            )
        )
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_3,
                DELAY_MSG_50,
                username,
                Button(TEXT_OGE_BTN_3, url=URL_OGE_BTN_3),
            )
        )
        self.exam_flow.track_task(
            self.scheduler.send_delayed_message(
                message,
                OGE_MESSAGE_4,
                DELAY_MSG_80,
                username,
                Button(TEXT_OGE_BTN_4, url=URL_OGE_BTN_4),
            )
        )
