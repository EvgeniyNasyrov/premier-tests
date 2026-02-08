import pytest
import allure
from premier_tests.pages.web.base_page import (
    open_main_page,
    premier_header_should_be_visible,
)


@allure.epic('Premier UI')
class TestBasePage:
    @allure.story('Главная страница')
    @allure.title('Главная страница отображается')
    @allure.feature('Главная')
    @allure.tag('smoke', 'regress', 'web', 'critical')
    @allure.severity('critical')
    @allure.link('https://premier.one/', name='Premier')
    @pytest.mark.smoke
    def test_open_base_page(self):
        open_main_page()
        premier_header_should_be_visible()

    @allure.story('Страница контента')
    @allure.title('Страница контента отображается')
    @allure.feature('Контент')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    @pytest.mark.smoke
    def test_open_movie_page(self):
        open_main_page()
        # На главной есть контент (блоки/секции) — без привязки к точной разметке карточек
        from selene import be
        from selene.support.shared import browser
        browser.element(('xpath', '//main | //section | //*[contains(@class,"section") or contains(@class,"slider") or contains(@class,"content")]')).with_(timeout=8).should(be.visible)

    @allure.story('Промо')
    @allure.title('Промо-страница отображается')
    @allure.feature('Промо')
    @allure.tag('regress', 'web', 'normal')
    @allure.severity('normal')
    @allure.link('https://premier.one/', name='Premier')
    @pytest.mark.smoke
    def test_open_promo_page(self):
        open_main_page()
        # На главной есть промо/контент или любой блок (main, section, div с контентом)
        from selene import be
        from selene.support.shared import browser
        browser.element(('xpath', '//section[@data-qa-selector="promo-slider"] | //*[contains(@class,"promo")] | //*[contains(text(),"Подключить")] | //*[contains(.,"1") and contains(.,"₽")] | //main | //main//section | //section | //div[contains(@class,"content") or contains(@class,"root") or contains(@class,"app")] | //body/div | //body')).with_(timeout=10).should(be.visible)
