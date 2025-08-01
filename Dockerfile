FROM python:3.11-slim

# Копируем uv бинарники
COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/

WORKDIR /app

# Копируем только нужные файлы для кэширования
COPY pyproject.toml uv.lock* /app/

# Синхронизируем зависимости
RUN uv sync

# Копируем остальной проект
COPY . /app

# Запуск напрямую скрипта
CMD ["uv", "run", "python", "-m", "bot.tg_bot"]
