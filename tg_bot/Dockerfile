FROM python:3.11

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копируем pyproject.toml для зависимостей
COPY tg_bot/pyproject.toml ./tg_bot/pyproject.toml

# Устанавливаем зависимости
WORKDIR /app/tg_bot
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Возвращаемся в корень и копируем всё
WORKDIR /app
COPY . .

# Делаем constants доступным
ENV PYTHONPATH=/app

# Запуск
CMD ["python3", "tg_bot/tg_bot.py"]
