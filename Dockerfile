FROM python:3.11-slim

# Копируем uv бинарники
COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/

WORKDIR /app

# Копируем только нужные файлы для кэширования
COPY pyproject.toml uv.lock* /app/

# Синхронизируем зависимости
RUN uv sync --locked --no-dev

# Копируем остальной проект
COPY . /app

ENTRYPOINT ["/bin/sh", "/app/docker/entrypoint.sh"]
CMD [".venv/bin/python", "-m", "bot.tg_bot"]
