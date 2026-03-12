import allure
import pytest
from allure_commons.types import Severity
from selene import be
from selene.support.shared import browser

from premier_tests.pages.web.main_page import main_page

LOGIN_BTN = '//a[contains(.,"Войти")] | //button[contains(.,"Войти")] | //*[contains(text(),"Войти") and (self::a or self::button or @role="button" or parent::a or parent::button)] | //*[@role="button" and contains(.,"Войти")]'
EMAIL_INPUT = '//input[@type="email"] | //input[@name="email"] | //*[@data-testid="email"] | //input[contains(@placeholder,"mail") or contains(@placeholder,"почт") or contains(@placeholder,"e-mail")]'
CONTINUE_BTN = '//button[@type="submit"] | //*[@data-testid="continue"] | //button[contains(.,"Далее") or contains(.,"Продолжить") or contains(.,"Войти")]'
AUTH_PANEL = '//*[contains(@class,"auth") or contains(@class,"modal") or contains(@class,"panel")] | //*[@data-testid="auth-panel"]'
ERROR_MSG = '//*[contains(@class,"error") or contains(@class,"invalid")] | //*[@data-testid="error"] | //*[contains(text(),"Неверн") or contains(text(),"ошибк") or contains(text(),"invalid") or contains(text(),"Введите")]'


@allure.epic("Premier UI")
class TestRegistrationForm:
    @pytest.mark.positive
    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Регистрация / Вход")
    @allure.title("Вход с корректным email")
    @allure.severity(Severity.CRITICAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_registration_with_valid_email(self, generate_email):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", LOGIN_BTN)).with_(timeout=10).should(be.visible).click()
        browser.element(("xpath", EMAIL_INPUT)).with_(timeout=6).should(be.visible).type(generate_email)
        browser.element(("xpath", CONTINUE_BTN)).with_(timeout=5).click()
        browser.element(("xpath", AUTH_PANEL)).with_(timeout=5).should(be.visible)

    @pytest.mark.negative
    @allure.tag("UI")
    @allure.feature("UI")
    @allure.story("Регистрация / Вход")
    @allure.title("Вход с некорректным email")
    @allure.severity(Severity.CRITICAL)
    @allure.link("https://premier.one/", name="Онлайн-кинотеатр Premier")
    @allure.label("jira_id", "HOMEWORK-1583")
    def test_registration_with_invalid_email(self):
        browser.open("/")
        main_page._close_promo_if_present()
        browser.element(("xpath", LOGIN_BTN)).with_(timeout=10).should(be.visible).click()
        invalid_email = "test@gmailcom"
        browser.element(("xpath", EMAIL_INPUT)).with_(timeout=6).should(be.visible).type(invalid_email)
        browser.element(("xpath", CONTINUE_BTN)).with_(timeout=5).click()
        browser.element(("xpath", ERROR_MSG)).with_(timeout=5).should(be.visible)
