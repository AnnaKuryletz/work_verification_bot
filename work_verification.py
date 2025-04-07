import requests
import time


def fetch_review_attempts(dvmn_token):
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {dvmn_token}"}
    params = {}
    connection_error_delay = 5

    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=90)
            response.raise_for_status()
            verification_report = response.json()

            connection_error_delay = 5

            if verification_report.get("new_attempts"):
                return verification_report["new_attempts"]

            if "last_attempt_timestamp" in verification_report:
                params["timestamp"] = verification_report["last_attempt_timestamp"]

        except requests.exceptions.ReadTimeout:
            pass

        except requests.exceptions.ConnectionError:
            print(
                f"Нет соединения с интернетом. Повтор через {connection_error_delay} сек."
            )
            time.sleep(connection_error_delay)
            connection_error_delay = min(connection_error_delay * 2, 300)

        time.sleep(2)
