import pytest
import allure
from premier_tests.utils import attach
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.common.exceptions import WebDriverException
from faker import Faker


@pytest.fixture(scope='function', autouse=True)
def manage_browser(request):
    browser_name = request.config.getoption('--browser_name')
    headless = request.config.getoption('--headless', default=False)
    options = ChromeOptions() if browser_name.lower() == 'chrome' else FirefoxOptions()

    if browser_name.lower() == 'chrome':
        if headless:
            options.add_argument('--headless=new')
        # Опции, снижающие падения Chrome при запуске из Selenium
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--remote-debugging-port=0')

    driver_class = webdriver.Chrome if browser_name.lower() == 'chrome' else webdriver.Firefox
    try:
        browser.config.driver = driver_class(options=options)
    except WebDriverException as e:
        if 'session not created' in str(e).lower() or 'chrome' in str(e).lower():
            pytest.skip(f'Браузер не запустился в данном окружении (CI/песочница): {e!s}')
        raise
    browser.config.base_url = "https://premier.one"
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    report = getattr(request.node, 'rep_call', None)
    if report and report.failed:
        with allure.step('Добавить скриншот'):
            attach.add_screenshot(browser)
        with allure.step('Добавить логи браузера'):
            if browser_name == 'chrome':
                attach.add_logs(browser)
        with allure.step('Добавить HTML'):
            attach.add_html(browser)

    browser.quit()


@pytest.fixture
def generate_email():
    fake = Faker()
    return fake.email()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, 'rep_' + report.when, report)
