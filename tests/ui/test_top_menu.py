import allure
from selene import be
from selene.support.shared import browser

from premier_tests.pages.web.main_page import main_page

NAV_LINK = (
    '//header//a[contains(.,"{0}")] | //nav//a[contains(.,"{0}")] '
    '| //*[contains(@class,"header") or contains(@class,"nav") or contains(@class,"menu")]//a[contains(.,"{0}")] '
    '| //a[contains(normalize-space(),"{0}")] '
    '| //*[contains(text(),"{0}")]/ancestor::a[1] '
    '| //*[@role="link" and contains(.,"{0}")] '
    '| //*[contains(text(),"{0}")]/parent::a | //*[contains(text(),"{0}")]/parent::*[self::a or self::button] '
    '| //button[contains(.,"{0}")] '
    '| //*[contains(.,"{0}") and (self::a or self::button or @role="button" or @role="link")]'
)
SECTION_CONTENT = '//h1 | //*[contains(@class,"title")] | //main | //*[contains(@class,"content")]'


@allure.epic("Premier UI")
class TestTopMenu:
    @allure.story("Раздел Главная")
    @allure.title("Страница Главная отображается")
    @allure.feature("Меню")
    @allure.tag("regress", "web", "normal")
    @allure.severity("normal")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_movies(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", NAV_LINK.format("Главная"))).with_(timeout=10).should(be.visible).click()
        browser.element(("xpath", SECTION_CONTENT)).with_(timeout=8).should(be.visible)

    @allure.story("Раздел Бесплатно")
    @allure.title("Страница Бесплатно отображается")
    @allure.feature("Меню")
    @allure.tag("regress", "web", "normal")
    @allure.severity("normal")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_serials(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", NAV_LINK.format("Бесплатно"))).with_(timeout=10).should(be.visible).click()
        browser.element(
            ("xpath", '//*[contains(text(),"Бесплатно")] | //h1 | //main | //*[contains(@class,"content")]')
        ).with_(timeout=8).should(be.visible)

    @allure.story("Раздел Каталог")
    @allure.title("Страница Каталог отображается")
    @allure.feature("Меню")
    @allure.tag("regress", "web", "normal")
    @allure.severity("normal")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_catalog(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", NAV_LINK.format("Каталог"))).with_(timeout=10).should(be.visible).click()
        browser.element(
            ("xpath", '//*[contains(text(),"Каталог")] | //h1 | //main | //*[contains(@class,"content")]')
        ).with_(timeout=8).should(be.visible)
