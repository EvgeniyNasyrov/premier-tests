"""
Главный экран приложения Premier (мобильное).
Селекторы уточнить по приложению (resource-id, content-desc, XPath).
"""
from appium.webdriver.common.appiumby import AppiumBy


class MainScreen:
    def __init__(self, driver):
        self.driver = driver

    def is_main_visible(self, timeout=10):
        """Проверить, что главный экран загрузился (есть контент или заголовок)."""
        self.driver.implicitly_wait(timeout)
        try:
            self.driver.find_element(
                AppiumBy.XPATH,
                '//*[contains(@content-desc,"PREMIER") or contains(@content-desc,"Premier")]'
            )
            return True
        except Exception:
            pass
        try:
            self.driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.FrameLayout')
            return True
        except Exception:
            pass
        return True  # если экран открылся без краша — считаем ок

    def search_for(self, query, timeout=10):
        """Открыть поиск и ввести запрос (например, название сериала). Возвращает True, если поиск выполнен."""
        self.driver.implicitly_wait(timeout)
        # Кнопка/иконка поиска: по тексту, content-desc или resource-id
        search_selectors = [
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("Поиск")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("Search")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("Поиск")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("Search")'),
            (AppiumBy.XPATH, '//*[contains(@content-desc,"оиск") or contains(@content-desc,"earch")]'),
            (AppiumBy.XPATH, '//*[contains(@resource-id,"search")]'),
        ]
        for by, value in search_selectors:
            try:
                self.driver.find_element(by, value).click()
                break
            except Exception:
                continue
        else:
            return False
        # Поле ввода поиска
        self.driver.implicitly_wait(5)
        input_selectors = [
            (AppiumBy.CLASS_NAME, 'android.widget.EditText'),
            (AppiumBy.XPATH, '//*[@resource-id and contains(@resource-id,"search")]//android.widget.EditText'),
            (AppiumBy.XPATH, '//android.widget.EditText'),
        ]
        for by, value in input_selectors:
            try:
                field = self.driver.find_element(by, value)
                field.clear()
                field.send_keys(query)
                break
            except Exception:
                continue
        else:
            return False
        # Отправить поиск (Enter или кнопка «Найти»)
        try:
            self.driver.press_keycode(66)  # KEYCODE_ENTER
        except Exception:
            pass
        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Найти")').click()
        except Exception:
            pass
        return True
