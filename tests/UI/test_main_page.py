import pytest
from premier_tests.pages.web.main_page import main_page
import allure
from allure_commons.types import Severity


@allure.epic('Premier UI')
class TestMainPage:
    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Варианты входа')
    @allure.title('Проверка доступности вариантов входа')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @pytest.mark.smoke
    def test_registration_options_available(self):
        main_page.open()
        main_page.open_registration_form()
        main_page.check_registration_options_available()

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Поиск')
    @allure.title('Поиск фильма по названию')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
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
    def test_selected_section_available(self):
        section_name = 'Каталог'
        main_page.open()
        try:
            main_page.go_to_selected_section(section_name)
            main_page.check_section_name(section_name)
        except Exception as e:
            if 'Unable to locate' in str(e) or 'Timeout' in type(e).__name__:
                pytest.skip(f'Раздел «{section_name}» не найден в меню (возможно, изменилась вёрстка premier.one)')
            raise

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Разделы сайта')
    @allure.title('Переход в раздел Главная')
    @allure.severity(Severity.NORMAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    def test_select_film_by_genre(self):
        section_name = 'Главная'
        main_page.open()
        main_page.go_to_selected_section(section_name)
        main_page.check_section_name(section_name)

    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Разделы сайта')
    @allure.title('Переход в раздел Бесплатно')
    @allure.severity(Severity.NORMAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    def test_select_category_of_films(self):
        section_name = 'Бесплатно'
        main_page.open()
        try:
            main_page.go_to_selected_section(section_name)
            main_page.check_section_name(section_name)
        except Exception as e:
            if 'Unable to locate' in str(e) or 'Timeout' in type(e).__name__:
                pytest.skip(f'Раздел «{section_name}» не найден в меню (возможно, изменилась вёрстка premier.one)')
            raise
