import allure
from premier_tests.pages.web.base_page import open_main_page
from premier_tests.pages.web.search import (
    click_on_search,
    type_movie_title,
    search_result_should_be_visible,
)


@allure.epic('Premier UI')
class TestSearch:
    @allure.story('Поиск')
    @allure.title('Поиск фильма по названию')
    @allure.feature('Поиск')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    def test_find_movie_by_title(self):
        title = 'Мажор'
        open_main_page()
        click_on_search()
        type_movie_title(title)
        search_result_should_be_visible()
