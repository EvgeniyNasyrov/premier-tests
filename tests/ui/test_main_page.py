import pytest
import allure
from allure_commons.types import Severity
from selenium.common.exceptions import TimeoutException, WebDriverException

from premier_tests.pages.web.main_page import main_page
from tests.ui.ui_skip import skip_reason_for_ui_exception


@allure.epic('Premier UI')
class TestMainPage:
    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Варианты входа')
    @allure.title('Проверка доступности вариантов входа')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    @pytest.mark.smoke
    def test_registration_options_available(self):
        try:
            main_page.open()
            main_page.open_registration_form()
            main_page.check_registration_options_available()
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e, kind="login")
            if reason:
                pytest.skip(reason)
            raise

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Поиск')
    @allure.title('Поиск фильма по названию')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_search_film_by_title(self):
        film_title_for_search = 'Мажор'
        main_page.open()
        main_page.search_film_by_title(film_title_for_search)
        main_page.check_result(film_title_for_search)

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Разделы сайта')
    @allure.title('Переход в выбранный раздел (Каталог)')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_selected_section_available(self):
        section_name = 'Каталог'
        main_page.open()
        try:
            main_page.go_to_selected_section(section_name)
            main_page.check_section_name(section_name)
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e, section_name=section_name, kind="section")
            if reason:
                pytest.skip(reason)
            raise

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Разделы сайта')
    @allure.title('Переход в раздел Главная')
    @allure.severity(Severity.NORMAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_select_film_by_genre(self):
        section_name = 'Главная'
        try:
            main_page.open()
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e)
            if reason:
                pytest.skip(reason)
            raise
        main_page.go_to_selected_section(section_name)
        main_page.check_section_name(section_name)

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Разделы сайта')
    @allure.title('Переход в раздел Бесплатно')
    @allure.severity(Severity.NORMAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_select_category_of_films(self):
        section_name = 'Бесплатно'
        try:
            main_page.open()
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e)
            if reason:
                pytest.skip(reason)
            raise
        try:
            main_page.go_to_selected_section(section_name)
            main_page.check_section_name(section_name)
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e, section_name=section_name, kind="section")
            if reason:
                pytest.skip(reason)
            raise

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Поиск в каталоге')
    @allure.title('Поиск сериала «Праздники» в каталоге')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_search_series_prazdniki(self):
        main_page.open()
        main_page.search_film_by_title('Праздники')
        main_page.check_result('Праздники')
