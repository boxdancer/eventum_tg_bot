# 🤖 Telegram Bot – Setup & Run Instructions

This repository contains a Telegram bot powered by Python 3.11 and managed with [uv](https://github.com/astral-sh/uv). You can run it locally or inside Docker.

---

## 🔐 1. Environment Setup

Create a `.env` file in the project root with your Telegram bot token:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OWNER_ID=111111111  # Bot sends notifications to owner
```
To figure out what your OWNER_ID is, you could use @GetMyIDBot on Telegram for example.

---

## 🚀 2. Run Locally (via `uv`)

Make sure you have [`uv`](https://github.com/astral-sh/uv) installed:

```bash
uv sync
uv run python bot/tg_bot.py
```

---

## 🐳 3. Run with Docker (Recommended)

Make sure Docker and Docker Compose are installed, then run:

```bash
docker compose up -d --build
```

This will:

- Build the Docker image
- Start the bot container named `tg-bot`
- Load environment variables from `.env`

To view logs:

```bash
docker compose logs -f
```

To stop the bot:

```bash
docker compose down
```

---

## 📝 Notes

- All static resources (like images) are located in `constants/static`.
- The main entry point is `bot/tg_bot.py`.
- Use `.env` to configure runtime secrets and tokens.
