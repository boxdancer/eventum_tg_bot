# Project Setup Instructions

To run this project, follow the steps below:

---

## 📦 1. Install Dependencies

Install the required libraries from `pyproject.toml`:

```bash
pip install -r requirements.txt  # or use poetry/uv if that's your tool
```

> Make sure you have Python and pip (or poetry/uv) properly installed.

---

## 🔐 2. Create a `.env` File

In the root of the repository, create a `.env` file with the following content:

```env
INSTA_USERNAME=your_instagram_username
INSTA_PASSWORD=your_instagram_password
INSTA_POST_SHORTCODE=C0d3ABC1  # example shortcode

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_BOT_LINK=https://t.me/your_bot_username
```

> Replace placeholders with your actual credentials and details.

---

## ✅ You're Ready!

After these steps, the project should be ready to run locally by:
```bash
python run.py
```
If you want to run bots in docker container, run in project root directory:
```bash
docker-compose up
```
---

### 🛠️ Notes

- The `INSTA_POST_SHORTCODE` refers to the unique code at the end of an Instagram post URL.
- Use a virtual environment for best practices.
