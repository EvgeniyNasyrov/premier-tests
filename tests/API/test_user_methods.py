import allure
from reqres_tests.test_data.data import data_for_post, data_for_update
from reqres_tests.request_helper.api_call import api_call
from reqres_tests.utils.json_validator import validate_schema


@allure.tag('API')
@allure.feature('API')
@allure.story('Создание пользователя')
@allure.title('Создать пользователя')
@allure.link('https://jsonplaceholder.typicode.com/')
@allure.label('jira_id', 'HOMEWORK-1583')
def test_create_user(base_endpoint):
    response = api_call.send_request('post', base_url=base_endpoint, payload=data_for_post)

    with allure.step('Статус 201'):
        assert response.status_code == 201
    with allure.step('Данные совпадают'):
        assert response.json()["name"] == data_for_post["name"]
        assert response.json()["email"] == data_for_post["email"]
    with allure.step('Валидация schema'):
        validate_schema(response.json(), 'create_user.json')


@allure.tag('API')
@allure.feature('API')
@allure.story('Обновление пользователя')
@allure.title('Обновить пользователя')
@allure.link('https://jsonplaceholder.typicode.com/')
@allure.label('jira_id', 'HOMEWORK-1583')
def test_update_user(base_endpoint):
    response = api_call.send_request('put', base_url=f"{base_endpoint}/1", payload=data_for_update)

    with allure.step('Статус 200'):
        assert response.status_code == 200
    with allure.step('Данные обновлены'):
        assert response.json()["name"] == data_for_update["name"]
        assert response.json()["email"] == data_for_update["email"]
    with allure.step('Валидация schema'):
        validate_schema(response.json(), 'update_user.json')


@allure.tag('API')
@allure.feature('API')
@allure.story('Удаление пользователя')
@allure.title('Удалить пользователя')
@allure.link('https://jsonplaceholder.typicode.com/')
@allure.label('jira_id', 'HOMEWORK-1583')
def test_delete_user(base_endpoint):
    response = api_call.send_request('delete', base_url=f"{base_endpoint}/1")

    # JSONPlaceholder для DELETE возвращает 200, не 204
    with allure.step('Статус 200 или 204'):
        assert response.status_code in (200, 204)
