import logging


def get_logger(name: str) -> logging.Logger:
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        )

    # Подавляем мусор от сторонних библиотек
    for noisy_logger in ["telegram", "httpx", "apscheduler"]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    return logging.getLogger(name)
