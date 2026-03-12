import allure
import pytest
from selene import be, have
from selene.support.shared import browser

from premier_tests.pages.web.main_page import main_page


@allure.epic("Premier UI")
class TestBasePage:
    @allure.story("Главная страница")
    @allure.title("Главная страница отображается")
    @allure.feature("Главная")
    @allure.tag("smoke", "regress", "web", "critical")
    @allure.severity("critical")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    @pytest.mark.smoke
    def test_open_base_page(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", '//header | //*[contains(@class,"header")]')).should(have.text("PREMIER"))

    @allure.story("Страница контента")
    @allure.title("Страница контента отображается")
    @allure.feature("Контент")
    @allure.tag("regress", "web", "normal")
    @allure.severity("normal")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    @pytest.mark.smoke
    def test_open_movie_page(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(
            (
                "xpath",
                '//main | //section | //*[contains(@class,"section") or contains(@class,"slider") or contains(@class,"content")]',
            )
        ).with_(timeout=8).should(be.visible)

    @allure.story("Промо")
    @allure.title("Промо-страница отображается")
    @allure.feature("Промо")
    @allure.tag("regress", "web", "normal")
    @allure.severity("normal")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    @pytest.mark.smoke
    def test_open_promo_page(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(
            (
                "xpath",
                '//section[@data-qa-selector="promo-slider"] | //*[contains(@class,"promo")] | //*[contains(text(),"Подключить")] | //*[contains(.,"1") and contains(.,"₽")]',
            )
        ).with_(timeout=6).should(be.visible)
