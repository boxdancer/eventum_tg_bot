# Telegram-бот

Бот работает на Python 3.11, `python-telegram-bot` 20.x и PostgreSQL. Точка входа — `bot/tg_bot.py`, зависимости управляются через `uv`.

## Запуск в Docker Compose

Создайте в корне проекта файл `.env`:

```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OWNER_ID=123456789
SUBSCRIPTION_CHANNEL=@celina_math
POSTGRES_USER=tg_bot
POSTGRES_PASSWORD=replace_with_a_strong_password
POSTGRES_DB=tg_bot
PGHOST=127.0.0.1
PGPORT=5831
```

`OWNER_ID` — числовой Telegram ID владельца. На этот аккаунт поступают уведомления, и с него доступна команда `/admin` в личном чате с ботом.

В `SUBSCRIPTION_CHANNEL` укажите username публичного канала или группы. Бот проверяет подписку на этот чат и использует его в кнопке «Подписаться на канал».

```sh
docker compose up -d --build
docker compose logs -f tg-bot
```

Compose передаёт боту адрес `postgres:5432` и ждёт готовности PostgreSQL. Точка входа контейнера выполняет `alembic upgrade head` перед запуском Python. Если миграция завершится ошибкой, polling не начнётся. Причину можно посмотреть в логах `tg-bot`.

На пустой базе первая ревизия создаёт таблицу `users`. Если таблица уже создана прежним SQL-скриптом, ревизия проверяет её структуру и регистрирует версию в `alembic_version` без пересоздания таблицы. На следующих релизах Alembic применяет только новые ревизии.

## Миграции

Для очередного релиза положите новую ревизию в `alembic/versions/` и обновите контейнер командой `docker compose up -d --build tg-bot`. Чтобы применить миграции отдельным шагом без запуска бота:

```sh
docker compose up -d --wait postgres
docker compose build tg-bot
docker compose run --rm --entrypoint .venv/bin/alembic tg-bot upgrade head
```

Для изменения схемы обновите модель в `bot/db/models.py` и создайте ревизию на базе, обновлённой до текущего `head`:

```sh
uv run alembic revision --autogenerate -m "describe schema change"
```

Проверьте сгенерированный файл перед выкатом. База хранится в томе `postgres-data`. `docker compose down` сохраняет данные, а опция `--volumes` удаляет их вместе с томом.

## Подключение из DBeaver

Чтобы поднять только базу, выполните `docker compose up -d --wait postgres`. Для подключения из DBeaver используйте `127.0.0.1:5831` (порт задаётся через `PGPORT`), а имя базы, пользователя и пароль возьмите из `.env`. PostgreSQL доступен на хосте через локальный интерфейс.

## Локальный запуск

При запуске Python напрямую бот подключается через `PGHOST` и `PGPORT` из `.env`. Для базы, поднятой через Compose, подходят значения из примера выше. Перед запуском Python примените миграции командой Alembic.

```sh
uv sync
uv run alembic upgrade head
uv run python -m bot.tg_bot
```

## Аудитория и рассылки

Бот записывает аудиторию с первого личного `/start` после обновления. В `/admin` доступны список пользователей и рассылка по категории и дате первого запуска. Одновременно выполняется одна рассылка. При остановке бота она прерывается, уже отправленные сообщения сохраняются у получателей.
