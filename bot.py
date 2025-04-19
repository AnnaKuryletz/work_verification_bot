import os
import time
from telegram import Bot
from dotenv import load_dotenv
from work_verification import fetch_review_attempts
from log_handler import setup_logging, send_log_to_telegram
import traceback

logger = setup_logging()


def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    dvmn_token = os.getenv("DVMN_TOKEN")

    bot = Bot(token=bot_token)

    logger.info("Бот начал работу!")

    while True:
        try:
            new_attempts = fetch_review_attempts(dvmn_token)
            if isinstance(new_attempts, list):
                for attempts in new_attempts:
                    lesson_title = attempts.get("lesson_title", "Неизвестный урок")
                    lesson_url = attempts.get("lesson_url", "")
                    is_negative = attempts.get("is_negative", True)

                    if is_negative:
                        negative_message = f"У вас проверили работу: '{lesson_title}'!\n\nК сожалению нашлись ошибки.\nСсылка на работу {lesson_url}"
                        bot.send_message(chat_id=chat_id, text=negative_message)
                        logger.info(
                            f"Отправлено сообщение о негативной проверке для урока: {lesson_title}"
                        )
                    else:
                        positive_message = f"У вас проверили работу: '{lesson_title}'!\n\nПреподавателю всё понравилось, можно приступать к следующему уроку!\nСсылка на работу {lesson_url}"
                        bot.send_message(chat_id=chat_id, text=positive_message)
                        logger.info(
                            f"Отправлено сообщение о позитивной проверке для урока: {lesson_title}"
                        )

        except Exception as e:
            error_message = f"❗ Ошибка: {str(e)}\n{traceback.format_exc()}"
            logger.error(f"Ошибка при получении или обработке данных: {str(e)}")
            send_log_to_telegram(error_message)

        time.sleep(2)


if __name__ == "__main__":
    main()
