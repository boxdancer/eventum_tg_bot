from enum import StrEnum

from constants.audience import AudienceCategory
from constants.constants import Command

CALLBACK_SEPARATOR = ":"
ADMIN_CALLBACK_PREFIX = f"{Command.ADMIN.value}{CALLBACK_SEPARATOR}"
BROADCAST_DRAFT_KEY = "broadcast_draft"
AUDIENCE_PAGE_SIZE = 20
BROADCAST_DELAY_SECONDS = 1
DISPLAY_NAME_LIMIT = 65
DISPLAY_USERNAME_LIMIT = 32


class AdminAction(StrEnum):
    MENU = "menu"
    USERS = "users"
    BROADCAST = "broadcast"
    SEND = "send"
    CANCEL = "cancel"


class AudiencePeriod(StrEnum):
    ALL = "all"
    MONTH = "30"
    WEEK = "7"
    DAY = "1"


ALL_CATEGORIES = "all"
CATEGORY_LABELS = {
    ALL_CATEGORIES: "Все",
    AudienceCategory.OGE: "ОГЭ",
    AudienceCategory.EGE: "ЕГЭ",
}
PERIOD_LABELS = {
    AudiencePeriod.ALL: "Всё время",
    AudiencePeriod.MONTH: "30 дней",
    AudiencePeriod.WEEK: "7 дней",
    AudiencePeriod.DAY: "24 часа",
}


class AdminText:
    TITLE = "Админка"
    USERS = "Пользователи"
    BROADCAST = "Рассылка"
    MENU = "В меню"
    BACK = "Назад"
    NEXT = "Вперёд"
    CONFIRM = "Подтвердить рассылку"
    CANCEL = "Отмена"
    DENIED = "Доступ закрыт"
    CANCELLED = "Рассылка отменена."
    CHOOSE_CATEGORY = "Выберите категорию."
    CHOOSE_PERIOD = "Выберите период."
    NO_RECIPIENTS = "В сегменте нет получателей."
    ENTER_TEXT = (
        "Получателей сейчас: {count}. Отправьте текст рассылки одним сообщением."
    )
    PAGE = "Всего: {count} · Страница {page}/{pages}"
    NO_NAME = "Без имени"
    BUSY = "Рассылка уже выполняется. Повторите после её завершения."
    STARTED = "Рассылка запущена. Получателей: {count}."
    REPORT = "Рассылка завершена. Всего: {total}. Успешно: {sent}. Ошибок: {failed}."
