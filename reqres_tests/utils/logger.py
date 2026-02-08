import time
import requests
import logging
import json
import allure
from curlify import to_curl

# Повтор при ConnectionError (обход нестабильности SSL/сокетов на Python 3.14)
MAX_REQUEST_RETRIES = 3
RETRY_DELAY_SEC = 0.5


def send_request_logger(method, url, **kwargs):
    with allure.step(f'{method} {url}'):
        for attempt in range(MAX_REQUEST_RETRIES):
            try:
                response = requests.request(method=method, url=url, **kwargs)
                break
            except requests.exceptions.ConnectionError:
                if attempt == MAX_REQUEST_RETRIES - 1:
                    raise
                time.sleep(RETRY_DELAY_SEC * (attempt + 1))

        curl = to_curl(response.request)
        logging.info(curl)
        logging.info(f'status code: {response.status_code}')
        allure.attach(body=curl, name='curl', attachment_type=allure.attachment_type.TEXT, extension='txt')

        try:
            allure.attach(
                body=json.dumps(response.json(), indent=4),
                name='response',
                attachment_type=allure.attachment_type.JSON,
                extension='json'
            )
        except json.JSONDecodeError:
            response_text = response.text if response.text is not None else 'No content'
            allure.attach(
                body=response_text,
                name='response',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt'
            )

        return response
