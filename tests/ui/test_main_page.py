import allure
import pytest
from allure_commons.types import Severity
from selene import be
from selene.support.shared import browser

from premier_tests.pages.web.main_page import main_page

LOGIN_BTN = '//a[contains(.,"Войти")] | //button[contains(.,"Войти")] | //*[contains(text(),"Войти") and (self::a or self::button or @role="button" or parent::a or parent::button)] | //*[@role="button" and contains(.,"Войти")]'
REG_OPTIONS = '//*[contains(@class,"modal") or contains(@class,"auth") or contains(@class,"login") or contains(@class,"popup")] | //form | //input[@type="email" or @type="tel" or @name="email" or @name="phone"]'
SEARCH_BTN = '//*[contains(@aria-label,"оиск") or contains(@title,"оиск") or contains(@class,"search") or contains(@data-qa,"search")] | //a[contains(@href,"search")] | //*[contains(text(),"оиск") and (self::a or self::button or @role="button")] | //*[contains(.,"Поиск") and (self::a or self::button)]'
SEARCH_INPUT = 'input[type="search"], input[placeholder*="оиск"], input[name="search"]'


def _section_xpath(section_name: str) -> str:
    parts = [
        f'//header//a[contains(.,"{section_name}")]',
        f'//nav//a[contains(.,"{section_name}")]',
        f'//*[contains(@class,"header") or contains(@class,"nav") or contains(@class,"menu")]//a[contains(.,"{section_name}")]',
        f'//a[contains(normalize-space(),"{section_name}")]',
        f'//*[contains(text(),"{section_name}")]/ancestor::a[1]',
        f'//*[@role="link" and contains(.,"{section_name}")]',
        f'//*[contains(.,"{section_name}")]/parent::a',
        f'//button[contains(.,"{section_name}")]',
        f'//*[contains(.,"{section_name}") and (self::a or self::button or @role="button" or @role="link")]',
    ]
    return " | ".join(parts)


@allure.epic("Premier UI")
class TestMainPage:
    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Варианты входа")
    @allure.title("Проверка доступности вариантов входа")
    @allure.severity(Severity.CRITICAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    @pytest.mark.smoke
    def test_registration_options_available(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", LOGIN_BTN)).with_(timeout=10).should(be.visible).click()
        browser.element(("xpath", REG_OPTIONS)).with_(timeout=3).should(be.visible)

    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Поиск")
    @allure.title("Поиск фильма по названию")
    @allure.severity(Severity.CRITICAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_search_film_by_title(self):
        film_title_for_search = "Мажор"
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", SEARCH_BTN)).with_(timeout=10).should(be.visible).click()
        browser.element(SEARCH_INPUT).with_(timeout=8).should(be.visible).type(film_title_for_search).press_enter()
        browser.element(("xpath", f'//*[contains(.,"{film_title_for_search}")]')).with_(timeout=8).should(be.visible)

    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Разделы сайта")
    @allure.title("Переход в выбранный раздел (Каталог)")
    @allure.severity(Severity.CRITICAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_selected_section_available(self):
        section_name = "Каталог"
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", _section_xpath(section_name))).with_(timeout=10).should(be.visible).click()
        browser.element(
            (
                "xpath",
                f'//*[contains(text(),"{section_name}") or contains(.,"{section_name}")] | //main | //section | //*[contains(@class,"content")]',
            )
        ).with_(timeout=6).should(be.visible)

    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Разделы сайта")
    @allure.title("Переход в раздел Главная")
    @allure.severity(Severity.NORMAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_select_film_by_genre(self):
        section_name = "Главная"
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", _section_xpath(section_name))).with_(timeout=10).should(be.visible).click()
        browser.element(
            (
                "xpath",
                f'//*[contains(text(),"{section_name}") or contains(.,"{section_name}")] | //main | //section | //*[contains(@class,"content")]',
            )
        ).with_(timeout=6).should(be.visible)

    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Разделы сайта")
    @allure.title("Переход в раздел Бесплатно")
    @allure.severity(Severity.NORMAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_select_category_of_films(self):
        section_name = "Бесплатно"
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", _section_xpath(section_name))).with_(timeout=10).should(be.visible).click()
        browser.element(
            (
                "xpath",
                f'//*[contains(text(),"{section_name}") or contains(.,"{section_name}")] | //main | //section | //*[contains(@class,"content")]',
            )
        ).with_(timeout=6).should(be.visible)

    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Поиск в каталоге")
    @allure.title("Поиск сериала «Праздники» в каталоге")
    @allure.severity(Severity.CRITICAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_search_series_prazdniki(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", SEARCH_BTN)).with_(timeout=10).should(be.visible).click()
        browser.element(SEARCH_INPUT).with_(timeout=8).should(be.visible).type("Праздники").press_enter()
        browser.element(("xpath", '//*[contains(.,"Праздники")]')).with_(timeout=8).should(be.visible)
