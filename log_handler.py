import logging
import sys
from telegram import Bot
import os


def send_log_to_telegram(message):
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    chat_id = os.getenv("CHAT_ID")
    bot.send_message(chat_id=chat_id, text=message)


class TelegramLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        send_log_to_telegram(log_entry)


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    log_handler = TelegramLogHandler()
    log_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logger.info("✅ Логирование настроено успешно!")
    return logger
