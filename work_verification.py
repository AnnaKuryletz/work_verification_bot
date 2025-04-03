import requests
import asyncio


async def work_verification():
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": "Token 0a825180eb5de7f543503fa7ead0985579f2c83d"}
    params = {}

    while True:
        try:
            response = await asyncio.to_thread(
                requests.get, url, headers=headers, params=params, timeout=90
            )
            response.raise_for_status()
            verification_report = response.json()

            if (
                "new_attempts" in verification_report
                and verification_report["new_attempts"]
            ):

                return verification_report[
                    "new_attempts"
                ]  

            if "last_attempt_timestamp" in verification_report:
                params["timestamp"] = verification_report["last_attempt_timestamp"]

        except requests.exceptions.ReadTimeout:
            print("Сервер не ответил за 90 секунд. Отправляю новый запрос...")
        except requests.exceptions.ConnectionError:
            print("Нет соединения с интернетом")

        await asyncio.sleep(2)
