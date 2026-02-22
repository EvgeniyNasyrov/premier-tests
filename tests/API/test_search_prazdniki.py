"""
API-тест: поиск сериала «Праздники».
Используется JSONPlaceholder GET /posts как эндпоинт со списком контента (проверка ответа 200 и непустой список).
"""
import allure
from reqres_tests.request_helper.api_call import api_call


@allure.tag('API')
@allure.feature('API')
@allure.story('Поиск контента')
@allure.title('Поиск сериала «Праздники» — API возвращает список результатов')
@allure.link('https://jsonplaceholder.typicode.com/')
@allure.label('jira_id', 'HOMEWORK-1583')
def test_search_series_prazdniki(search_endpoint):
    """Запрос к API списка контента (аналог поиска): статус 200, в ответе непустой список с полем title."""
    response = api_call.send_request('get', base_url=search_endpoint)

    with allure.step('Статус ответа 200'):
        assert response.status_code == 200
    with allure.step('В ответе — список'):
        data = response.json()
        assert isinstance(data, list), 'Ожидался список (результаты поиска)'
    with allure.step('Список не пустой'):
        assert len(data) > 0, 'Ожидались результаты поиска'
    with allure.step('Элементы содержат поле title (название)'):
        first = data[0]
        assert 'title' in first, 'В элементе результата ожидалось поле title'
