import enum
import os
from typing import NamedTuple


class ExamType(str, enum.Enum):
    OGE = "ОГЭ"
    EGE_PROFILE = "ЕГЭ профиль"
    EGE_BASE = "ЕГЭ база"


MATERIAL_CALLBACK_PREFIX = "material:"


class MaterialKey(str, enum.Enum):
    # ЕГЭ профиль
    EGE_PROFILE_1 = "ege_profile_1"
    EGE_PROFILE_3 = "ege_profile_3"
    EGE_PROFILE_4 = "ege_profile_4"
    # ЕГЭ база
    EGE_BASE_1 = "ege_base_1"
    EGE_BASE_3 = "ege_base_3"
    EGE_BASE_4 = "ege_base_4"
    # ОГЭ
    OGE_1 = "oge_1"
    OGE_3 = "oge_3"
    OGE_4 = "oge_4"


class Command(str, enum.Enum):
    START = "start"
    ADMIN = "admin"
    PLAN_OGE = "plan_oge"
    PLAN_EGE_PROFILE = "plan_ege_profile"
    PLAN_EGE_BASE = "plan_ege_base"
    TEST_OGE = "test_oge"
    TEST_EGE_PROFILE = "test_ege_profile"
    TEST_EGE_BASE = "test_ege_base"
    FREE_VIDEOLESSON = "free_videolesson"


# Command descriptions for bot menu
COMMAND_DESCRIPTIONS = {
    Command.START: "Начать заново",
    Command.PLAN_OGE: "План ОГЭ",
    Command.PLAN_EGE_PROFILE: "План ЕГЭ профиль",
    Command.PLAN_EGE_BASE: "План ЕГЭ база",
    Command.TEST_OGE: "Тест ОГЭ",
    Command.TEST_EGE_PROFILE: "Тест ЕГЭ профиль",
    Command.TEST_EGE_BASE: "Тест ЕГЭ база",
    Command.FREE_VIDEOLESSON: "Бесплатный видеоурок",
}


class Material(NamedTuple):
    message: str
    button_text: str
    url: str


# Message Delay Constants Minutes
DELAY_MSG_0 = 0
DELAY_MSG_20 = 20 * 60 * 1
DELAY_MSG_50 = 50 * 60 * 1
DELAY_MSG_80 = 80 * 60 * 1
DELAY_MSG_90 = 90 * 60 * 1


# Absolute path for dir /constants/static
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


def __prepare_photo_data(file_name: str):
    file_path = os.path.join(STATIC_DIR, f"{file_name}.png")
    with open(file_path, "rb") as photo:
        return photo.read()


SUBSCRIPTION_REQUIRED_MESSAGE = (
    "🔒 *Для доступа к материалам необходимо подписаться на наш канал\\!*\n\n"
    r"После подписки нажми на кнопку снова\."
)

# Photos
GREETING_PHOTO = __prepare_photo_data("GREETING_PHOTO")

# Message Text Constants
GREETING_MESSAGE = (
    r"Привет\! Я *Наташа Целина*, репетитор по математике для школьников с 5 по 11 класс\."
    r" Мой ТГ канал\: \@celina\_math\. Присоединяйся, там много полезного контента по подготовке\!"
    r" Какой экзамен сдаёшь\?"
)

# ЕГЭ профиль messages
EGE_PROFILE_MESSAGE_1 = r"""*Вот обещанный файл по стереометрии, в нём:*
✅ только нужные формулы для задания 3 и 14
✅ я рассказала как удобно строить объёмные фигуры
✅ в конце тебя ждёт список задач для отработки

*Почему тебе стоит прямо сейчас открыть этот материал:*
• задание 3 и 14 школьники часто пропускают, т\.к\. не понимают геометрию
• ученики совершают ошибки, потому что просто зубрят без понимания"""
TEXT_EGE_PROFILE_BTN_1 = "Вся необходимая стереометрия"
URL_EGE_PROFILE_BTN_1 = (
    "https://www.buildin.ai/share/c1f84b25-3f47-4b20-86e8-4a7a6bec51ea?code=LJYE9L"
)

EGE_PROFILE_MESSAGE_2 = r"""*Знаешь, почему чаще сливают баллы в стереометрии?*
– не вспомнили формулы
– забыли из чего состоит фигура
– записали не ту формулу объёма
– не поняли как построить фигуру
_А теперь представь, только на этих задачах можно_ __потерять 4 балла\!__
*Мой подход \= не зубрить, а понять логически задачу\!* 
Не забудь прочитать файл👆"""

EGE_PROFILE_MESSAGE_3 = r"""*Ты не поверишь, сколько сильных учеников сдуваются ближе к экзамену\.* _Почему?_
• потому что они не понимают, где они и куда идут
• «вроде решаю варианты, но пробники пишу плохо»
• «формулы есть, а уверенности — нет», «вдруг попадется то, чего я не решал или будет сложный вариант»

*Вот тебе пошаговый план подготовки к ЕГЭ профиль, который я даю ученикам:*
✅ Темы выстроены от простых к сложным, чтобы сразу не выгореть из\-за трудного материала
✅ Перечислена вся необходимая теория 
✅ Примеры заданий, которые реально будут на ЕГЭ профиль
✨ _Этот файл — твой маршрут\._ Он спасает от бардака в голове и срыва при стрессе\."""
TEXT_EGE_PROFILE_BTN_3 = "План подготовки"
URL_EGE_PROFILE_BTN_3 = (
    "https://www.buildin.ai/share/f9b58133-3ee5-416e-8d2b-fec4198e96f1?code=LJYE9L"
)

EGE_PROFILE_MESSAGE_4 = r"""*Давай проверим на сколько ты готов к ЕГЭ профиль?*
Пройди реальный тест и узнай:
💫Где _ты теряешь баллы_
💫Над чем стоит поработать и сделать акцент

_Почему важно пройти тест?_
— Ты можешь быть неплох\(а\) в математике, но сливать баллы на мелких ошибках
— Или сидишь на 40 баллах и не понимаешь, как прыгнуть выше
— Или вообще, откладываешь подготовку, потому что не знаешь, с чего начать
_Этот тест — это не проверка знаний ради галочки\._ *Это шаг к системе\.* После него я отправлю тебе разбор ошибок и рекомендации, как двигаться дальше\. 
__Присылай фото с решением:__ @natashkatse"""
TEXT_EGE_PROFILE_BTN_4 = "Пройти тест"
URL_EGE_PROFILE_BTN_4 = (
    "https://drive.google.com/file/d/1s2ol2mLqPuHfv-R0YywTnY9yHFmwND3p/view?usp=drive_link"
)

# ЕГЭ база messages
EGE_BASE_MESSAGE_1 = r"""*Вот обещанный файл по стереометрии, в нём:*
✅ только нужные формулы для задания 11 и 13
✅ я рассказала как удобно строить объёмные фигуры
✅ в конце тебя ждёт список задач для отработки

*Почему тебе стоит прямо сейчас открыть этот материал:*
• задание 11 и 13 школьники часто пропускают, т\.к\. не понимают геометрию
• ученики совершают ошибки, потому что просто зубрят без понимания"""
TEXT_EGE_BASE_BTN_1 = "Вся необходимая стереометрия"
URL_EGE_BASE_BTN_1 = "https://www.buildin.ai/share/c1f84b25-3f47-4b20-86e8-4a7a6bec51ea?code=LJYE9L"

EGE_BASE_MESSAGE_3 = r"""*Ты не поверишь, сколько сильных учеников сдуваются ближе к экзамену\.* _Почему?_
• потому что они не понимают, где они и куда идут
• «вроде решаю варианты, но пробники пишу плохо»
• «формулы есть, а уверенности — нет», «вдруг попадется то, чего я не решал или будет сложный вариант»

*Вот тебе пошаговый план подготовки к базовому ЕГЭ, который я даю ученикам:*
✅ Темы выстроены от простых к сложным, чтобы сразу не выгореть из\-за трудного материала
✅ Перечислена вся необходимая теория 
✅ Примеры заданий, которые реально будут на базовом ЕГЭ
✨ _Этот файл — твой маршрут\._ Он спасает от бардака в голове и срыва при стрессе\."""
TEXT_EGE_BASE_BTN_3 = "План подготовки"
URL_EGE_BASE_BTN_3 = "https://www.buildin.ai/share/a3744d8b-a13a-405e-9e08-8e368d32883a?code=LJYE9L"

EGE_BASE_MESSAGE_4 = r"""*Давай проверим на сколько ты готов к базовому ЕГЭ?*
Пройди реальный тест и узнай:
💫Где _ты теряешь баллы_
💫Над чем стоит поработать и сделать акцент

_Почему важно пройти тест?_
— Ты можешь быть неплох\(а\) в математике, но сливать баллы на мелких ошибках
— Или вообще, откладываешь подготовку, потому что не знаешь, с чего начать
_Этот тест — это не проверка знаний ради галочки\._ *Это шаг к системе\.* После него я отправлю тебе разбор ошибок и рекомендации, как двигаться дальше\. 
__Присылай фото с решением:__ @natashkatse"""
TEXT_EGE_BASE_BTN_4 = "Пройти тест"
URL_EGE_BASE_BTN_4 = (
    "https://drive.google.com/file/d/1vW3voXGUtaafiQxItaQeO4kjF5BBk_YG/view?usp=drive_link"
)

OGE_MESSAGE_1 = r""" *Вот обещанный файл по «Шинам», в нём:*
✅ собраны и решены все прототипы, которые могут попасться в номерах с 1 по 5
✅ лайфхаки с уже готовыми формулами
✅ в конце тебя ждёт список задач для отработки

_Почему тебе стоит прямо сейчас открыть этот материал:_
• задание с 1 по 5 школьники часто пропускают, т\.к\. не понимают как решать
• ученики совершают ошибки, потому невнимательно читают условия и пытаются вызубрить формулы"""
TEXT_OGE_BTN_1 = "Файл по шинам"
URL_OGE_BTN_1 = "https://www.buildin.ai/share/29eca5bd-2765-4566-8119-bbf9c370af34?code=LJYE9L"

OGE_MESSAGE_2 = r"""*Знаешь, почему чаще сливают баллы в первых пяти номерах?*
– заранее не разобрали номера
– не вспомнили формулы из геометрии
– забыли как решаются прототипы
– невнимательно прочитали условие
_А теперь представь, только на этих задачах_ __можно потерять 5 баллов\!__ Это больше половины проходного😱
*Мой подход \= не зубрить, а понять логически задачу\!* 
Не забудь прочитать файл👆"""

OGE_MESSAGE_3 = r"""*Ты не поверишь, сколько сильных учеников сдуваются ближе к экзамену\.* _Почему?_
— потому что они не понимают, где они и куда идут
— «вроде решаю варианты, но пробники пишу плохо»
— «формулы есть, а уверенности — нет», «вдруг попадется то, чего я не решал или будет сложный вариант»

*Вот тебе пошаговый план подготовки к ОГЭ, который я даю ученикам:*
✅ Темы выстроены от простых к сложным, чтобы сразу не выгореть из\-за трудного материала
✅ Перечислена вся необходимая теория 
✅ Примеры заданий, которые реально будут на ОГЭ
✨ _Этот файл — твой маршрут\._ Он спасает от бардака в голове и срыва при стрессе\. """
TEXT_OGE_BTN_3 = "План подготовки"
URL_OGE_BTN_3 = "https://www.buildin.ai/share/fd1d6aec-174e-472e-9233-011744fe0328?code=LJYE9L"

OGE_MESSAGE_4 = r"""*Давай проверим на сколько ты готов к ОГЭ?*
Пройди реальный тест и узнай:
— Где ты теряешь баллы
— Над чем стоит поработать и сделать акцент

_Почему важно пройти тест?_
— Ты можешь быть неплох в математике, но сливать баллы на мелких ошибках
— Решаешь ОГЭ на 2 и не понимаешь, как прыгнуть выше
— Или вообще, откладываешь подготовку, потому что не знаешь, с чего начать
_Этот тест — это не проверка знаний ради галочки\._ *Это шаг к системе\.* После него я отправлю тебе разбор ошибок и рекомендации, как двигаться дальше\. 
__Присылай фото с решением:__ @natashkatse"""
TEXT_OGE_BTN_4 = "Пройти тест"
URL_OGE_BTN_4 = (
    "https://drive.google.com/file/d/1d131NqQ8XfIW0l4wUDuGmJHog8BWvfpl/view?usp=drive_link"
)

# Free videolesson message (no button, text only)
FREE_VIDEOLESSON_MESSAGE = r"""У меня есть для тебя *бесплатный видеоурок*, который поможет разобраться с одной важной темой по математике и убрать пробелы, из\-за которых чаще всего возникают ошибки\.

Этот урок я отдаю лично, чтобы понимать, кому он действительно нужен\.

Напиши мне в личные сообщения @natashkatse слово *УРОК* — вышлю доступ 🎯"""

# Materials: MaterialKey -> Material(message, button_text, url)
MATERIALS = {
    # ЕГЭ профиль
    MaterialKey.EGE_PROFILE_1: Material(
        EGE_PROFILE_MESSAGE_1, TEXT_EGE_PROFILE_BTN_1, URL_EGE_PROFILE_BTN_1
    ),
    MaterialKey.EGE_PROFILE_3: Material(
        EGE_PROFILE_MESSAGE_3, TEXT_EGE_PROFILE_BTN_3, URL_EGE_PROFILE_BTN_3
    ),
    MaterialKey.EGE_PROFILE_4: Material(
        EGE_PROFILE_MESSAGE_4, TEXT_EGE_PROFILE_BTN_4, URL_EGE_PROFILE_BTN_4
    ),
    # ЕГЭ база
    MaterialKey.EGE_BASE_1: Material(EGE_BASE_MESSAGE_1, TEXT_EGE_BASE_BTN_1, URL_EGE_BASE_BTN_1),
    MaterialKey.EGE_BASE_3: Material(EGE_BASE_MESSAGE_3, TEXT_EGE_BASE_BTN_3, URL_EGE_BASE_BTN_3),
    MaterialKey.EGE_BASE_4: Material(EGE_BASE_MESSAGE_4, TEXT_EGE_BASE_BTN_4, URL_EGE_BASE_BTN_4),
    # ОГЭ
    MaterialKey.OGE_1: Material(OGE_MESSAGE_1, TEXT_OGE_BTN_1, URL_OGE_BTN_1),
    MaterialKey.OGE_3: Material(OGE_MESSAGE_3, TEXT_OGE_BTN_3, URL_OGE_BTN_3),
    MaterialKey.OGE_4: Material(OGE_MESSAGE_4, TEXT_OGE_BTN_4, URL_OGE_BTN_4),
}

# Command -> MaterialKey
COMMAND_MATERIALS = {
    Command.PLAN_OGE: MaterialKey.OGE_3,
    Command.PLAN_EGE_PROFILE: MaterialKey.EGE_PROFILE_3,
    Command.PLAN_EGE_BASE: MaterialKey.EGE_BASE_3,
    Command.TEST_OGE: MaterialKey.OGE_4,
    Command.TEST_EGE_PROFILE: MaterialKey.EGE_PROFILE_4,
    Command.TEST_EGE_BASE: MaterialKey.EGE_BASE_4,
}
