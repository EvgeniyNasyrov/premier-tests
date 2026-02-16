import pytest
import allure
from reqres_tests.test_data.data import complete_creds, not_existing_user_id
from reqres_tests.request_helper.api_call import api_call
from reqres_tests.utils.json_validator import validate_schema


@pytest.mark.positive
@allure.tag('API')
@allure.feature('API')
@allure.story('Регистрация / создание пользователя')
@allure.title('Успешное создание пользователя (POST)')
@allure.link('https://jsonplaceholder.typicode.com/')
@allure.label('jira_id', 'HOMEWORK-1583')
def test_register_successful(base_endpoint):
    response = api_call.send_request('post', base_endpoint, complete_creds)

    with allure.step('Статус ответа 201'):
        assert response.status_code == 201
    with allure.step('В ответе есть id'):
        assert 'id' in response.json()
    with allure.step('Валидация JSON schema'):
        validate_schema(response.json(), 'register_user.json')


@pytest.mark.negative
@allure.tag('API')
@allure.feature('API')
@allure.story('Получение пользователя')
@allure.title('Запрос несуществующего пользователя возвращает 404')
@allure.link('https://jsonplaceholder.typicode.com/')
@allure.label('jira_id', 'HOMEWORK-1583')
def test_register_unsuccessful(base_endpoint):
    response = api_call.send_request('get', base_url=f"{base_endpoint}/{not_existing_user_id}")

    with allure.step('Статус ответа 404'):
        assert response.status_code == 404
