import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from work_verification import work_verification


async def main():
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    if not TOKEN:
        raise ValueError("BOT_TOKEN не найден в .env файле!")
    if not CHAT_ID:
        raise ValueError("CHAT_ID не найден в .env файле!")

    bot = Bot(token=TOKEN)
    while True:
        new_attempts = await work_verification()
        if isinstance(new_attempts, list):
            for attempts in new_attempts:
                lesson_title = attempts.get("lesson_title", "Неизвестный урок")
                lesson_url = attempts.get("lesson_url", "")
                is_negative = attempts.get("is_negative", True)
                if is_negative:
                    negative_message = f"У вас проверили работу: '{lesson_title}'!\n\nК сожалению нашлись ошибки.\nСсылка на работу {lesson_url}"
                    await bot.send_message(chat_id=CHAT_ID, text=negative_message)
                else:
                    positive_message = f"У вас проверили работу: '{lesson_title}'!\n\nПреподавателю всё понравилось, можно приступать к следующему уроку!\nСсылка на работу {lesson_url}"
                    await bot.send_message(chat_id=CHAT_ID, text=positive_message)


if __name__ == "__main__":
    asyncio.run(main())
