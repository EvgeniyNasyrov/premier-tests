# Общие опции для всего набора тестов (API + UI)
import pytest


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome', help='Браузер: chrome или firefox')
    parser.addoption('--headless', action='store_true', default=False, help='Chrome в headless (без окна)')
