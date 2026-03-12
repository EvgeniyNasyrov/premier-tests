import allure
from selene import be
from selene.support.shared import browser

from premier_tests.pages.web.main_page import main_page

SEARCH_BTN = '//*[contains(@aria-label,"оиск") or contains(@title,"оиск") or contains(@class,"search")] | //a[contains(@href,"search")] | //*[contains(text(),"оиск")]'
SEARCH_INPUT = 'input[type="search"], input[placeholder*="оиск"], input[name="search"], input[type="text"]'
SEARCH_RESULT = '//*[contains(@class,"search") and (contains(@class,"result") or .//a)] | //*[contains(@class,"search")]//a | //main//section | //*[contains(@class,"result")] | //*[contains(@class,"content")]'


@allure.epic("Premier UI")
class TestSearch:
    @allure.story("Поиск")
    @allure.title("Поиск фильма по названию")
    @allure.feature("Поиск")
    @allure.tag("regress", "web", "normal")
    @allure.severity("normal")
    @allure.link("https://premier.one/", name="Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_find_movie_by_title(self):
        title = "Мажор"
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", SEARCH_BTN)).with_(timeout=10).should(be.visible).click()
        browser.element(SEARCH_INPUT).with_(timeout=5).type(title).press_enter()
        browser.element(("xpath", SEARCH_RESULT)).with_(timeout=12).should(be.visible)
