import requests
import asyncio
import os
from dotenv import load_dotenv


async def work_verification():
    url = "https://dvmn.org/api/long_polling/"
    token = os.getenv("DVMN_TOKEN")
    headers = {"Authorization": f"Token {token}"}
    params = {}
    connection_error_delay = 5
    while True:
        try:
            response = await asyncio.to_thread(
                requests.get, url, headers=headers, params=params, timeout=90
            )
            response.raise_for_status()
            verification_report = response.json()
            connection_error_delay = 5
            if (
                "new_attempts" in verification_report
                and verification_report["new_attempts"]
            ):

                return verification_report["new_attempts"]

            if "last_attempt_timestamp" in verification_report:
                params["timestamp"] = verification_report["last_attempt_timestamp"]

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print(
                f"Нет соединения с интернетом. Повтор через {connection_error_delay} сек."
            )
            await asyncio.sleep(connection_error_delay)
            connection_error_delay = min(connection_error_delay * 2, 300)

        await asyncio.sleep(2)
