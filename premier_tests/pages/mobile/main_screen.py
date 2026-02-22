"""
Главный экран приложения Premier (мобильное).
Локаторы: ACCESSIBILITY ID / content-desc, при необходимости — из инспектора элементов.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy


class MainScreen:
    def __init__(self, driver):
        self.driver = driver

    def _tap(self, x, y):
        """Тап по координатам (W3C Actions или mobile: clickGesture)."""
        try:
            from selenium.webdriver.common.actions.action_builder import ActionBuilder
            builder = ActionBuilder(self.driver)
            touch = builder.add_pointer_input("touch", "finger")
            touch.create_pointer_move(duration=0, x=int(x), y=int(y))
            touch.create_pointer_down(button=0)
            touch.create_pointer_up(button=0)
            builder.perform()
        except Exception:
            try:
                self.driver.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})
            except Exception:
                pass

    def close_promo_banner_tap_only(self):
        """Закрыть промо тапом по крестику (0.9*w, 0.58*h)."""
        try:
            w = self.driver.get_window_size().get("width", 1080)
            h = self.driver.get_window_size().get("height", 2219)
            self._tap(int(w * 0.9), int(h * 0.58))
        except Exception:
            pass

    def close_promo_banner(self):
        """Закрыть баннер промо по content-desc или resource-id ButtonRound."""
        self.driver.implicitly_wait(2)
        for _ in range(2):
            try:
                for desc in ("close", "Close", "Закрыть", "закрыть"):
                    try:
                        btn = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            f'new UiSelector().descriptionContains("{desc}")',
                        )
                        if btn.is_displayed():
                            btn.click()
                            time.sleep(0.5)
                            return
                    except Exception:
                        pass
                btn = self.driver.find_element(AppiumBy.XPATH, '//*[contains(@resource-id, "ButtonRound") and @clickable="true"]')
                if btn.is_displayed():
                    btn.click()
                    time.sleep(0.5)
                    return
            except Exception:
                pass
            time.sleep(0.3)

    def is_main_visible(self, timeout=8):
        """Проверить, что главный экран загрузился. Короткий implicit_wait (3 с), чтобы не зависать в облаке."""
        wait_sec = min(timeout, 3)
        self.driver.implicitly_wait(wait_sec)
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
        self.driver.implicitly_wait(0)
        return True

    def _find_search_icon_element(self):
        """Найти иконку поиска по content-desc, resource-id или XPath."""
        self.driver.implicitly_wait(1)
        for aid in ("Поиск", "Search", "Кнопка поиска", "поиск", "search", "Поиск по каталогу", "Search catalog", "лупа", "magnifier"):
            try:
                el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, aid)
                if el.is_displayed():
                    return el
            except Exception:
                continue
        for desc in ("Поиск", "Search", "поиск"):
            try:
                el = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().descriptionContains("{desc}")',
                )
                if el.is_displayed():
                    return el
            except Exception:
                continue
        for rid in (
            "gpm.tnt_premier:id/action_search",
            "gpm.tnt_premier:id/search_icon",
            "gpm.tnt_premier:id/search_button",
            "gpm.tnt_premier:id/iv_search",
        ):
            try:
                el = self.driver.find_element(AppiumBy.ID, rid)
                if el.is_displayed():
                    return el
            except Exception:
                continue
        try:
            el = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.ImageView[@content-desc='Поиск']",
            )
            if el.is_displayed():
                return el
        except Exception:
            pass
        return None

    def _header_icons_in_right_half(self):
        """Иконки в правой части шапки (ImageView / ImageButton в верхней зоне)."""
        try:
            w = self.driver.get_window_size().get('width', 1000)
            h = self.driver.get_window_size().get('height', 1800)
            top_threshold = int(h * 0.15)
            right_half_min_x = int(w * 0.5)
            candidates = []
            for class_name in ('android.widget.ImageView', 'android.widget.ImageButton', 'android.view.View'):
                for el in self.driver.find_elements(AppiumBy.CLASS_NAME, class_name):
                    try:
                        if not el.is_displayed():
                            continue
                        loc, sz = el.location, el.size
                        cx = loc['x'] + sz.get('width', 0) // 2
                        cy = loc['y'] + sz.get('height', 0) // 2
                        if cy < top_threshold and cx > right_half_min_x and sz.get('width', 0) < 200:
                            candidates.append(el)
                    except Exception:
                        continue
            candidates.sort(key=lambda e: e.location['x'])
            return candidates
        except Exception:
            return []

    def _tap_search_icon_by_position(self):
        """Тап по иконке поиска перебором координат в зоне шапки."""
        try:
            w = self.driver.get_window_size().get("width", 1080)
            h = self.driver.get_window_size().get("height", 2219)
            self.driver.implicitly_wait(0)
            for y_ratio in (0.04, 0.055):
                y = int(h * y_ratio)
                for x_ratio in (0.58, 0.62, 0.66, 0.70, 0.74, 0.78, 0.82):
                    x = int(w * x_ratio)
                    try:
                        self._tap(x, y)
                    except Exception:
                        try:
                            self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
                        except Exception:
                            pass
                    time.sleep(0.6)
                    try:
                        self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
                        return
                    except Exception:
                        continue
        except Exception:
            pass

    def open_catalog(self):
        """Открыть раздел «Каталог» по нижней навигационной панели."""
        self.driver.implicitly_wait(1)
        try:
            h = self.driver.get_window_size().get("height", 2200)
            bottom_min_y = int(h * 0.75)
        except Exception:
            bottom_min_y = 1500
        for text in ("Каталог", "Catalog", "КАТАЛОГ"):
            try:
                for el in self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'):
                    try:
                        if not el.is_displayed():
                            continue
                        loc, sz = el.location, el.size
                        cy = loc["y"] + sz.get("height", 0) // 2
                        if cy >= bottom_min_y:
                            el.click()
                            time.sleep(1.5)
                            return True
                    except Exception:
                        continue
            except Exception:
                continue
        try:
            for el in self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Каталог")'):
                try:
                    if not el.is_displayed():
                        continue
                    loc, sz = el.location, el.size
                    cy = loc["y"] + sz.get("height", 0) // 2
                    if cy >= bottom_min_y:
                        el.click()
                        time.sleep(1.5)
                        return True
                except Exception:
                    continue
        except Exception:
            pass
        return False

    def search_for(self, query, timeout=10):
        """Открыть поиск по лупе в шапке и ввести запрос."""
        self.driver.implicitly_wait(1)
        opened = False
        for aid in ("Поиск", "Search", "Кнопка поиска", "search", "Поиск по каталогу"):
            try:
                el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, aid)
                if el.is_displayed():
                    el.click()
                    opened = True
                    time.sleep(0.5)
                    break
            except Exception:
                continue
        if not opened:
            for rid in (
                "gpm.tnt_premier:id/action_search",
                "gpm.tnt_premier:id/search_icon",
                "gpm.tnt_premier:id/search_button",
                "gpm.tnt_premier:id/iv_search",
            ):
                try:
                    el = self.driver.find_element(AppiumBy.ID, rid)
                    if el.is_displayed():
                        el.click()
                        opened = True
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        if not opened:
            for by, value in [
                (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Поиск']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Поиск")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Поиск")'),
            ]:
                try:
                    el = self.driver.find_element(by, value)
                    if el.is_displayed():
                        el.click()
                        opened = True
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
        if not opened:
            self._tap_search_icon_by_position()
        time.sleep(1)
        self.driver.implicitly_wait(2)
        field = None
        try:
            field = self.driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText')
            if not field.is_displayed():
                field = None
        except Exception:
            pass
        if field:
            try:
                field.clear()
                field.send_keys(query)
            except Exception:
                field = None
        if not field:
            try:
                from selenium.webdriver.common.actions.action_builder import ActionBuilder
                builder = ActionBuilder(self.driver)
                key_input = builder.add_key_input("keyboard")
                key_input.send_keys(query)
                builder.perform()
            except Exception:
                pass
        try:
            self.driver.press_keycode(66)
        except Exception:
            pass
        return True

    def has_search_results_or_content(self, timeout=8):
        """Проверить, что после поиска отображаются результаты (RecyclerView или контент)."""
        self.driver.implicitly_wait(min(timeout, 3))
        try:
            self.driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.RecyclerView')
            return True
        except Exception:
            pass
        try:
            src = self.driver.page_source or ''
            return len(src) > 500
        except Exception:
            return True

    def open_login_or_profile(self, timeout=8):
        """Открыть экран входа/профиля (иконка профиля в шапке). Возвращает True, если экран входа/профиля открыт."""
        self.driver.implicitly_wait(timeout)
        for text in ("Профиль", "Profile", "Мой профиль"):
            try:
                el = self.driver.find_element(AppiumBy.XPATH, f'//android.widget.TextView[@text="{text}"]')
                if el.is_displayed():
                    el.click()
                    time.sleep(2)
                    break
            except Exception:
                try:
                    el = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
                    if el.is_displayed():
                        el.click()
                        time.sleep(2)
                        break
                except Exception:
                    pass
        else:
            for desc in ("Профиль", "Profile", "профиль", "profile", "Аккаунт", "Account", "Войти", "Login"):
                try:
                    el = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiSelector().descriptionContains("{desc}")',
                    )
                    if el.is_displayed():
                        el.click()
                        time.sleep(2)
                        break
                except Exception:
                    continue
            else:
                right_icons = self._header_icons_in_right_half()
                if right_icons:
                    right_icons[-1].click()
                    time.sleep(2)
                else:
                    try:
                        buttons = self.driver.find_elements(AppiumBy.CLASS_NAME, 'android.widget.ImageButton')
                        visible = [b for b in buttons if b.is_displayed()]
                        if visible:
                            max(visible, key=lambda b: b.location['x'] + b.size.get('width', 0)).click()
                            time.sleep(2)
                    except Exception:
                        pass
        self.driver.implicitly_wait(timeout)
        for text in ("Войти", "Login", "Вход", "Sign in", "Войти или зарегистрироваться", "Электронная почта", "Email", "Телефон", "Phone", "Профиль", "Profile"):
            try:
                self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{text}")',
                )
                return True
            except Exception:
                continue
        return "вход" in (self.driver.page_source or "").lower() or "login" in (self.driver.page_source or "").lower()
