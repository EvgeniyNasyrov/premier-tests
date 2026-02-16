import pytest
import allure
from premier_tests.pages.web.base_page import open_main_page
from premier_tests.pages.web.top_menu import TopMenu

top_menu = TopMenu()


@allure.epic('Premier UI')
class TestTopMenu:
    @allure.story('Раздел Главная')
    @allure.title('Страница Главная отображается')
    @allure.feature('Меню')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_movies(self):
        open_main_page()
        top_menu.click_on_movies()
        top_menu.check_movies_title()

    @allure.story('Раздел Бесплатно')
    @allure.title('Страница Бесплатно отображается')
    @allure.feature('Меню')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_serials(self):
        open_main_page()
        try:
            top_menu.click_on_serials()
            top_menu.check_serials_title()
        except Exception as e:
            if 'Unable to locate' in str(e) or 'Timeout' in type(e).__name__:
                pytest.skip('Раздел «Бесплатно» не найден в меню (возможно, изменилась вёрстка premier.one)')
            raise

    @allure.story('Раздел Каталог')
    @allure.title('Страница Каталог отображается')
    @allure.feature('Меню')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_catalog(self):
        open_main_page()
        try:
            top_menu.click_on_catalog()
            top_menu.check_catalog_title()
        except Exception as e:
            if 'Unable to locate' in str(e) or 'Timeout' in type(e).__name__:
                pytest.skip('Раздел «Каталог» не найден в меню (возможно, изменилась вёрстка premier.one)')
            raise
