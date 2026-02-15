"""
Проверка сценария мобильных тестов с мок-драйвером (без реального Appium/устройства).
Запуск: pytest tests/mobile/test_main_mock.py -v
"""
import pytest
from unittest.mock import MagicMock

from appium.webdriver.common.appiumby import AppiumBy
from premier_tests.pages.mobile.main_screen import MainScreen


@pytest.fixture
def mock_driver():
    """Драйвер-заглушка: find_element возвращает элемент с click/clear/send_keys."""
    driver = MagicMock()
    mock_element = MagicMock()
    driver.find_element.return_value = mock_element
    driver.implicitly_wait = MagicMock()
    driver.press_keycode = MagicMock()
    driver.page_source = "<mock><node>Праздники</node></mock>"
    return driver


def test_main_screen_is_main_visible(mock_driver):
    """MainScreen.is_main_visible не падает и возвращает True."""
    screen = MainScreen(mock_driver)
    assert screen.is_main_visible(timeout=5) is True


def test_main_screen_search_for_prazdniki(mock_driver):
    """MainScreen.search_for('Праздники') вызывает поиск и ввод текста."""
    screen = MainScreen(mock_driver)
    result = screen.search_for("Праздники", timeout=5)
    assert result is True
    mock_driver.find_element.assert_called()
    # Должны были вызвать send_keys с запросом
    mock_el = mock_driver.find_element.return_value
    mock_el.send_keys.assert_called_once_with("Праздники")
