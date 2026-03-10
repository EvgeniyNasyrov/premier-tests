import pytest
import allure
from selenium.common.exceptions import TimeoutException, WebDriverException

from premier_tests.pages.web.base_page import open_main_page
from premier_tests.pages.web.search import (
    click_on_search,
    type_movie_title,
    search_result_should_be_visible,
)
from tests.ui.ui_skip import skip_reason_for_ui_exception


@allure.epic('Premier UI')
class TestSearch:
    @allure.story('Поиск')
    @allure.title('Поиск фильма по названию')
    @allure.feature('Поиск')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_find_movie_by_title(self):
        title = 'Мажор'
        try:
            open_main_page()
            click_on_search()
            type_movie_title(title)
            search_result_should_be_visible()
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e, kind='search')
            if reason:
                pytest.skip(reason)
            raise
