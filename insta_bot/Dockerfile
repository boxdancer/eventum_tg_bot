FROM python:3.11

WORKDIR /app

# Установка Poetry
RUN pip install poetry

COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-root --only main

COPY . .

CMD ["python3", "insta_bot.py"]