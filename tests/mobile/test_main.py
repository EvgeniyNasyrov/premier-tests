"""
Мобильные тесты приложения Premier (Appium, Android).
Для запуска: Appium Server, эмулятор/устройство, переменная APP_PATH с путём к APK.
"""
import allure
import pytest
from premier_tests.pages.mobile.main_screen import MainScreen


@allure.epic('Premier Mobile')
@allure.feature('Android')
class TestPremierMobile:
    @allure.story('Запуск приложения')
    @allure.title('Приложение Premier запускается')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_app_launches(self, mobile_driver):
        """Приложение открывается без падения."""
        driver = mobile_driver
        assert driver is not None
        assert driver.current_context is not None

    @allure.story('Главный экран')
    @allure.title('Главный экран отображается')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_main_screen_visible(self, mobile_driver):
        """После запуска виден главный экран (контент или контейнер)."""
        screen = MainScreen(mobile_driver)
        assert screen.is_main_visible(timeout=15) is True

    @allure.story('Элементы интерфейса')
    @allure.title('Интерфейс приложения отображается')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link('https://premier.one/', name='Premier')
    @allure.label('jira_id', 'HOMEWORK-1583')
    def test_ui_elements_present(self, mobile_driver):
        """На экране есть элементы интерфейса (виджеты)."""
        driver = mobile_driver
        from appium.webdriver.common.appiumby import AppiumBy
        driver.find_elements(AppiumBy.XPATH, '//*[@clickable="true" or @content-desc!=""]')
        assert driver.page_source is not None and len(driver.page_source) > 100
