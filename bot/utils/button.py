from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Button:
    def __init__(
        self, text: str, url: str | None = None, callback_data: str | None = None
    ):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        if not (url or callback_data):
            raise ValueError("Button must have either 'url' or 'callback_data'")

    def to_telegram(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            self.text, url=self.url, callback_data=self.callback_data
        )

    @staticmethod
    def create_markup(buttons: list[list["Button"]]) -> InlineKeyboardMarkup:
        keyboard = [[button.to_telegram() for button in row] for row in buttons]
        return InlineKeyboardMarkup(keyboard)
