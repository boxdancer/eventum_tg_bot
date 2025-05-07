from instagrapi import Client
from dotenv import load_dotenv
import os
import json
import time

# Загрузка .env
load_dotenv()
USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")
POST_SHORTCODE = os.getenv("INSTA_POST_SHORTCODE")
TG_BOT_LINK = os.getenv("TELEGRAM_BOT_LINK")

# Файл, где будут храниться ID уже обработанных комментариев
LOG_FILE = "sent_log.json"

# Загрузка обработанных комментов
def load_sent_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_sent_log(sent_ids):
    with open(LOG_FILE, "w") as f:
        json.dump(list(sent_ids), f)

def main():
    print("🔐 Вход в Instagram...")
    cl = Client()
    cl.login(USERNAME, PASSWORD)

    sent_log = load_sent_log()
    print("✅ Бот запущен. Слежу за комментариями...")

    while True:
        try:
            media_id = cl.media_pk_from_url(f"https://www.instagram.com/p/{POST_SHORTCODE}/")
            comments = cl.media_comments(media_id)

            for comment in comments:
                if comment.text.strip() == "+" and str(comment.pk) not in sent_log:
                    reply = f"Привет, вот как и обещал — ссылка на Telegram бота 👉 {TG_BOT_LINK}"
                    cl.direct_send(text=reply, user_ids=[comment.user.pk])
                    print(f"💬 Ответил {comment.user.username}: {reply}")
                    sent_log.add(str(comment.pk))
                    save_sent_log(sent_log)

        except Exception as e:
            print(f"⚠️ Ошибка: {e}")

        time.sleep(5)  # Проверка раз в минуту

if __name__ == "__main__":
    main()
