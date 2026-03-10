import pytest
import allure
from allure_commons.types import Severity
from selenium.common.exceptions import TimeoutException, WebDriverException

from premier_tests.pages.web.main_page import main_page
from premier_tests.pages.web.registration_form import registration_form
from tests.ui.ui_skip import skip_reason_for_ui_exception


@allure.epic('Premier UI')
class TestRegistrationForm:
    @pytest.mark.positive
    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Регистрация / Вход')
    @allure.title('Вход с корректным email')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_registration_with_valid_email(self, generate_email):
        try:
            main_page.open()
            main_page.open_registration_form()
            registration_form.enter_email(generate_email)
            registration_form.check_registration_result()
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e, kind='login')
            if reason:
                pytest.skip(reason)
            raise

    @pytest.mark.negative
    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Регистрация / Вход')
    @allure.title('Вход с некорректным email')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_registration_with_invalid_email(self):
        try:
            main_page.open()
            main_page.open_registration_form()
            invalid_email = 'test@gmailcom'
            registration_form.enter_email(invalid_email)
            registration_form.check_registration_result(email_valid=False)
        except (TimeoutException, WebDriverException) as e:
            reason = skip_reason_for_ui_exception(e, kind='login')
            if reason:
                pytest.skip(reason)
            raise
