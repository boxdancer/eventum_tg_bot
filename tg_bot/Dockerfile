FROM python:3.11

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копируем только pyproject.toml для установки зависимостей
COPY pyproject.toml .

# Настройка Poetry и установка только "main" зависимостей (без dev)
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Копируем остальной код
COPY . .

# Стартовая команда по умолчанию
CMD ["python3", "tg_bot.py"]
