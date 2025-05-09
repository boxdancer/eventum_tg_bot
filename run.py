import subprocess
import os
import sys

def run_bot(script_path):
    return subprocess.Popen([sys.executable, script_path])

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tg_bot_path = os.path.join(base_dir, "tg_bot", "tg_bot.py")
    insta_bot_path = os.path.join(base_dir, "insta_bot", "insta_bot.py")

    print("🚀 Запускаю Telegram-бота...")
    tg_proc = run_bot(tg_bot_path)

    print("🚀 Запускаю Instagram-бота...")
    insta_proc = run_bot(insta_bot_path)

    try:
        tg_proc.wait()
        insta_proc.wait()
    except KeyboardInterrupt:
        print("\n⛔️ Останавливаю ботов...")
        tg_proc.terminate()
        insta_proc.terminate()
