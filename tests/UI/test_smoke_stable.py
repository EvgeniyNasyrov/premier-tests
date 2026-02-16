"""
Шесть стабильных дымовых UI-тестов: загрузка premier.one и базовая проверка контента.
Минимум зависимостей от вёрстки — только body, main, заголовок страницы, ссылки.
"""
import pytest
import allure
from selene import browser, be
from premier_tests.pages.web.base_page import open_main_page


@allure.epic('Premier UI')
@allure.feature('Дымовые проверки')
class TestSmokeStable:
    @allure.story('Загрузка')
    @allure.title('Страница открывается и body виден')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_page_body_visible(self):
        open_main_page()
        browser.element('body').with_(timeout=10).should(be.visible)

    @allure.story('Загрузка')
    @allure.title('На странице есть основной контент (main или section)')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_page_has_main_or_section(self):
        open_main_page()
        el = browser.element(('xpath', '//main | //section | //*[contains(@class,"content") or contains(@class,"main")]'))
        el.with_(timeout=12).should(be.visible)

    @allure.story('Загрузка')
    @allure.title('Заголовок страницы содержит Premier')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_page_title_contains_premier(self):
        open_main_page()
        title = browser.driver.title or ''
        assert 'premier' in title.lower() or 'premier' in title, f'В title ожидался Premier, получено: {title!r}'

    @allure.story('Контент')
    @allure.title('На странице есть ссылки')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_page_has_links(self):
        open_main_page()
        links = browser.driver.find_elements('tag name', 'a')
        assert len(links) >= 1, f'На странице должна быть хотя бы одна ссылка, найдено: {len(links)}'

    @allure.story('Контент')
    @allure.title('Размер контента страницы достаточный')
    @allure.severity(allure.severity_level.MINOR)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_page_source_not_empty(self):
        open_main_page()
        source = browser.driver.page_source or ''
        assert len(source) > 2000, f'Страница подгрузилась не полностью: {len(source)} символов'

    @allure.story('Загрузка')
    @allure.title('URL главной страницы корректен')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_current_url_premier(self):
        open_main_page()
        url = browser.driver.current_url or ''
        assert 'premier' in url.lower(), f'Ожидался URL premier.one, получено: {url!r}'
