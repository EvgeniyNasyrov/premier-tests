"""
Мобильные тесты Premier (Appium, Android).
"""
import allure
import pytest

from premier_tests.pages.mobile.main_screen import MainScreen


@allure.epic('Premier Mobile')
@allure.feature('Android')
@pytest.mark.timeout(60)
class TestPremierMobile:
    @allure.title('Приложение Premier запускается')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_app_launches(self, mobile_driver):
        driver = mobile_driver
        assert driver is not None
        assert driver.current_context is not None

    @allure.title('Главный экран отображается')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_screen_visible(self, mobile_driver):
        screen = MainScreen(mobile_driver)
        screen.close_promo_banner()
        assert screen.is_main_visible(timeout=8) is True

    @allure.title('Закрытие баннеров при входе в приложение')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_banners_on_launch(self, mobile_driver):
        """После закрытия баннеров фикстурой проверяется отображение главного экрана."""
        screen = MainScreen(mobile_driver)
        assert screen.is_main_visible(timeout=8) is True
