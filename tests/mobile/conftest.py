"""
Мобильные тесты (Appium, Android) — приложение Premier.
Локально: --context=local (Appium + APK в корне).
Облако: --context=bstack (BrowserStack), lambdatest (LambdaTest), sauce (Sauce Labs), testingbot (TestingBot).
Переменные см. .env.example.
Таймаут подключения к облаку: MOBILE_CONNECT_TIMEOUT=45 (сек) — при отсутствии ответа быстрый skip.
"""
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from datetime import datetime
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# Поддерживаются .apk и .xapk (первый найденный в списке)
# Приоритет: APK 2.80 (apkmirror), затем остальные
APK_NAMES_IN_ROOT = (
    'gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk',
    'premier_aptoide.apk',
    'premier_from_xapk.apk',
    'premier.apk',
    'PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure-2.xapk',
    'PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure.xapk',
    'premier2.apk',
    'gpm-tnt-premier.apk',
    'gpm-tnt-premier.xapk',
    'premier.xapk',
)


def pytest_addoption(parser):
    parser.addoption(
        '--context',
        action='store',
        default=os.getenv('MOBILE_CONTEXT', 'local'),
        help='Контекст: local, bstack, lambdatest, sauce, testingbot (TestingBot)',
    )
    parser.addoption('--app', action='store', default=os.getenv('APP_PATH'), help='Путь к APK (для local)')
    parser.addoption(
        '--remote',
        action='store',
        default=os.getenv('REMOTE_URL'),
        help='URL Appium (local: 127.0.0.1:4723) или BrowserStack hub',
    )


@pytest.fixture(scope='function')
def mobile_driver(request):
    from appium import webdriver
    from appium.options.android import UiAutomator2Options

    context = (request.config.getoption('--context', default='local') or 'local').lower()
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.new_command_timeout = 120

    if context == 'bstack':
        user = os.getenv('BSTACK_USERNAME') or os.getenv('USER_NAME')
        key = os.getenv('BSTACK_ACCESS_KEY') or os.getenv('ACCESS_KEY')
        app = os.getenv('BSTACK_APP') or os.getenv('APP')
        if not user or not key or not app:
            pytest.skip(
                'Для BrowserStack задайте BSTACK_USERNAME, BSTACK_ACCESS_KEY и BSTACK_APP в .env'
            )
        executor_url = 'https://hub.browserstack.com/wd/hub'
        options.set_capability('deviceName', os.getenv('DEVICE_NAME', 'Google Pixel 7'))
        options.set_capability('platformVersion', os.getenv('PLATFORM_VERSION', '13.0'))
        options.set_capability('app', app)
        options.set_capability(
            'bstack:options',
            {
                'projectName': 'Premier Android tests',
                'buildName': f"Premier mobile build {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                'sessionName': 'Premier Android tests',
                'userName': user,
                'accessKey': key,
                'idleTimeout': 300,
                'buildIdentifier': os.getenv('BUILD_NAME', 'premier-mobile'),
            },
        )
    elif context == 'lambdatest' or context == 'lt':
        user = os.getenv('LT_USERNAME') or os.getenv('LAMBDATEST_USERNAME')
        key = os.getenv('LT_ACCESS_KEY') or os.getenv('LAMBDATEST_ACCESS_KEY')
        app = os.getenv('LT_APP') or os.getenv('LAMBDATEST_APP')
        if not user or not key or not app:
            pytest.skip(
                'Для LambdaTest задайте LT_USERNAME, LT_ACCESS_KEY и LT_APP в .env. '
                'Сначала загрузи APK: python scripts/upload_app_to_lambdatest.py'
            )
        executor_url = f'https://{user}:{key}@mobile-hub.lambdatest.com/wd/hub'
        options.set_capability('deviceName', os.getenv('LT_DEVICE', 'Galaxy S23'))
        options.set_capability('platformVersion', os.getenv('LT_PLATFORM_VERSION', '13'))
        options.set_capability('app', app)
        options.set_capability('isRealMobile', True)
        options.set_capability('build', os.getenv('LT_BUILD', 'Premier mobile'))
        options.set_capability('name', 'Premier Android tests')
        options.set_capability('video', True)
        options.set_capability('network', False)
    elif context == 'sauce' or context == 'saucelabs':
        user = os.getenv('SAUCE_USERNAME')
        key = os.getenv('SAUCE_ACCESS_KEY')
        app = os.getenv('SAUCE_APP')
        if not user or not key or not app:
            pytest.skip(
                'Для Sauce Labs задайте SAUCE_USERNAME, SAUCE_ACCESS_KEY и SAUCE_APP в .env. '
                'Сначала загрузите APK: python scripts/upload_app_to_saucelabs.py'
            )
        region = os.getenv('SAUCE_REGION', 'us-west-1').lower()
        executor_url = f'https://{user}:{key}@ondemand.{region}.saucelabs.com:443/wd/hub'
        options.set_capability('app', app)
        options.set_capability('deviceName', os.getenv('SAUCE_DEVICE', 'Google Pixel 7 GoogleAPI Emulator'))
        options.set_capability('platformVersion', os.getenv('SAUCE_PLATFORM_VERSION', '13.0'))
        options.set_capability('sauce:options', {
            'name': 'Premier Android tests',
            'build': os.getenv('SAUCE_BUILD', 'Premier mobile'),
        })
    elif context == 'testingbot' or context == 'tb':
        key = os.getenv('TB_KEY') or os.getenv('TESTINGBOT_KEY')
        secret = os.getenv('TB_SECRET') or os.getenv('TESTINGBOT_SECRET')
        app = os.getenv('TB_APP') or os.getenv('TESTINGBOT_APP')
        if not key or not secret or not app:
            pytest.skip(
                'Для TestingBot задайте TB_KEY, TB_SECRET и TB_APP в .env. '
                'Сначала загрузите APK: python scripts/upload_app_to_testingbot.py'
            )
        executor_url = f'https://{key}:{secret}@hub.testingbot.com/wd/hub'
        options.set_capability('app', app)
        options.set_capability('deviceName', os.getenv('TB_DEVICE', 'Google Pixel 7'))
        options.set_capability('platformVersion', os.getenv('TB_PLATFORM_VERSION', '13.0'))
        options.set_capability('tb:options', {
            'name': 'Premier Android tests',
            'build': os.getenv('TB_BUILD', 'Premier mobile'),
        })
    else:
        # local: свой Appium и APK
        app_path = request.config.getoption('--app', default=None) or os.getenv('APP_PATH')
        if not app_path or not os.path.isfile(app_path):
            for name in APK_NAMES_IN_ROOT:
                candidate = PROJECT_ROOT / name
                if candidate.is_file():
                    app_path = str(candidate)
                    break
        executor_url = (
            request.config.getoption('--remote', default=None)
            or os.getenv('REMOTE_URL')
            or 'http://127.0.0.1:4723'
        )
        if not app_path or not os.path.isfile(app_path):
            pytest.skip(
                'APK/XAPK не найден. Положите gpm-tnt-premier.apk, premier.apk или .xapk в корень '
                'или задайте APP_PATH / --app'
            )
        options.app = app_path

    connect_timeout = int(os.getenv('MOBILE_CONNECT_TIMEOUT', '45'))
    try:
        cloud_contexts = ('bstack', 'lambdatest', 'lt', 'sauce', 'saucelabs', 'testingbot', 'tb')
        if context in cloud_contexts:
            with ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(webdriver.Remote, command_executor=executor_url, options=options)
                driver = fut.result(timeout=connect_timeout)
        else:
            driver = webdriver.Remote(command_executor=executor_url, options=options)
    except FuturesTimeoutError:
        pytest.skip(
            f'Облако не ответило за {connect_timeout} с. Задай MOBILE_CONNECT_TIMEOUT=90 для долгого ожидания.'
        )
    except Exception as e:
        pytest.skip(f'Не удалось подключиться к Appium/облаку или запустить приложение: {e}')

    from appium.webdriver.common.appiumby import AppiumBy
    import time

    # Диалог уведомлений «Allow PREMIER to send you notifications?» — нажать Don't allow
    driver.implicitly_wait(5)
    notification_closed = False
    try:
        deny = driver.find_element(AppiumBy.ID, 'com.android.permissioncontroller:id/permission_deny_button')
        if deny.is_displayed():
            deny.click()
            notification_closed = True
    except Exception:
        pass
    if not notification_closed:
        for text in ("Don't allow", "Не разрешать", "Allow", "Разрешить"):
            try:
                btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
                if btn.is_displayed():
                    btn.click()
                    break
            except Exception:
                pass
    time.sleep(0.5)
    driver.implicitly_wait(0)

    def _tap(drv, x, y):
        try:
            from selenium.webdriver.common.actions.action_builder import ActionBuilder
            builder = ActionBuilder(drv)
            touch = builder.add_pointer_input("touch", "finger")
            touch.create_pointer_move(duration=0, x=int(x), y=int(y))
            touch.create_pointer_down(button=0)
            touch.create_pointer_up(button=0)
            builder.perform()
        except Exception:
            try:
                drv.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})
            except Exception:
                pass

    def _close_promo_banner(drv):
        """Закрывает баннер «45 дней PREMIER за 1₽» крестиком (тап 0.9*w, 0.58*h или content-desc/ButtonRound)."""
        try:
            w = drv.get_window_size().get('width', 1080)
            h = drv.get_window_size().get('height', 2219)
            _tap(drv, int(w * 0.9), int(h * 0.58))
            time.sleep(0.3)
            return
        except Exception:
            pass
        for _ in range(1):
            try:
                for desc in ("close", "Close", "Закрыть"):
                    try:
                        btn = drv.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{desc}")')
                        if btn.is_displayed():
                            btn.click()
                            time.sleep(0.3)
                            return
                    except Exception:
                        pass
                try:
                    btn = drv.find_element(AppiumBy.XPATH, '//*[contains(@resource-id, "ButtonRound") and @clickable="true"]')
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(0.3)
                        return
                except Exception:
                    pass
                try:
                    w = drv.get_window_size().get('width', 1080)
                    h = drv.get_window_size().get('height', 2219)
                    _tap(drv, int(w * 0.9), int(h * 0.58))
                    time.sleep(0.3)
                    return
                except Exception:
                    pass
            except Exception:
                pass

    def _try_close_vpn(drv):
        for sel in ('new UiSelector().textContains("Продолжить с VPN")', 'new UiSelector().textContains("Продолжить")', 'new UiSelector().textContains("Continue with VPN")'):
            try:
                tx = drv.find_element(AppiumBy.ANDROID_UIAUTOMATOR, sel)
                if tx.is_displayed():
                    loc, sz = tx.location, tx.size
                    cy = loc['y'] + sz.get('height', 0) // 2
                    if cy > 200:
                        cx = loc['x'] + sz.get('width', 0) // 2
                        _tap(drv, cx, cy)
                        return True
            except Exception:
                pass
        try:
            w = drv.get_window_size().get('width', 1080)
            h = drv.get_window_size().get('height', 2219)
            _tap(drv, w // 2, int(h * 0.987))
        except Exception:
            pass
        return False

    # Пауза 5 с — дать баннеру появиться; закрыть промо крестиком, затем VPN (если есть).
    time.sleep(5)
    _close_promo_banner(driver)
    time.sleep(2)
    _try_close_vpn(driver)
    time.sleep(2)
    driver.implicitly_wait(0)

    yield driver
    driver.quit()
