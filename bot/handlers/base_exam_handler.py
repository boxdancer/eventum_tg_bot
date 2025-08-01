from abc import ABC, abstractmethod
from telegram import Message


class IExamHandler(ABC):
    @abstractmethod
    async def handle(self, message: Message, username: str):
        pass
