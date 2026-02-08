import pytest
import allure
from allure_commons.types import Severity
from premier_tests.pages.web.main_page import main_page
from premier_tests.pages.web.registration_form import registration_form


@allure.epic('Premier UI')
class TestRegistrationForm:
    @pytest.mark.positive
    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Регистрация / Вход')
    @allure.title('Вход с корректным email')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    def test_registration_with_valid_email(self, generate_email):
        try:
            main_page.open()
            main_page.open_registration_form()
            registration_form.enter_email(generate_email)
            registration_form.check_registration_result()
        except Exception as e:
            if 'ERR_CONNECTION_RESET' in str(e) or 'net::ERR_' in str(e):
                pytest.skip(f'Сетевая ошибка при загрузке premier.one (нестабильное соединение): {e!s}')
            raise

    @pytest.mark.negative
    @allure.tag('UI')
    @allure.feature('UI')
    @allure.story('Регистрация / Вход')
    @allure.title('Вход с некорректным email')
    @allure.severity(Severity.CRITICAL)
    @allure.link('https://premier.one/', name='Онлайн-кинотеатр Premier')
    def test_registration_with_invalid_email(self):
        main_page.open()
        main_page.open_registration_form()
        invalid_email = 'test@gmailcom'
        registration_form.enter_email(invalid_email)
        registration_form.check_registration_result(email_valid=False)
