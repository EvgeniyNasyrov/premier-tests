import allure
from reqres_tests.utils.logger import send_request_logger


class ApiCall:
    @staticmethod
    @allure.step('Отправить API запрос')
    def send_request(method, base_url=None, payload=None, **kwargs):
        url = base_url or kwargs.get('base_url')
        # reqres.in ожидает JSON, не form-data
        req_kwargs = {**kwargs}
        if payload is not None:
            req_kwargs['json'] = payload
        response = send_request_logger(method=method.upper(), url=url, **req_kwargs)
        return response


api_call = ApiCall()
