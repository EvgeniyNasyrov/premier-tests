from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MainScreen:
    def __init__(self, driver):
        self.driver = driver

    def _tap(self, x, y):
        try:
            builder = ActionBuilder(self.driver)
            touch = builder.add_pointer_input("touch", "finger")
            touch.create_pointer_move(duration=0, x=int(x), y=int(y))
            touch.create_pointer_down(button=0)
            touch.create_pointer_up(button=0)
            builder.perform()
        except (TimeoutException, WebDriverException):
            try:
                self.driver.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})
            except WebDriverException:
                pass

    def close_promo_banner_tap_only(self):
        try:
            w = self.driver.get_window_size().get("width", 1080)
            h = self.driver.get_window_size().get("height", 2219)
            self._tap(int(w * 0.9), int(h * 0.58))
        except (TimeoutException, WebDriverException):
            pass

    def _try_click_promo_close(self):
        close_descriptions = ("close", "Close", "Закрыть", "закрыть")
        for desc in close_descriptions:
            try:
                btn = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            f'new UiSelector().descriptionContains("{desc}")',
                        )
                    )
                )
                if btn.is_displayed():
                    btn.click()
                    WebDriverWait(self.driver, 2).until(lambda _: not btn.is_displayed())
                    return True
            except (TimeoutException, WebDriverException):
                pass
        try:
            btn = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.XPATH,
                        '//*[contains(@resource-id, "ButtonRound") and @clickable="true"]',
                    )
                )
            )
            if btn.is_displayed():
                btn.click()
                WebDriverWait(self.driver, 2).until(lambda _: not btn.is_displayed())
                return True
        except (TimeoutException, WebDriverException):
            pass
        return False

    def close_promo_banner(self):
        for _ in range(2):
            if self._try_click_promo_close():
                return
            try:
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.FrameLayout"))
                )
            except (TimeoutException, WebDriverException):
                pass

    def is_main_visible(self, timeout=8):
        wait_sec = min(timeout, 3)
        try:
            WebDriverWait(self.driver, wait_sec).until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.XPATH,
                        '//*[contains(@content-desc,"PREMIER") or contains(@content-desc,"Premier")]',
                    )
                )
            )
            return True
        except (TimeoutException, WebDriverException):
            pass
        try:
            WebDriverWait(self.driver, wait_sec).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.FrameLayout"))
            )
            return True
        except (TimeoutException, WebDriverException):
            pass
        return True

    def _find_search_icon_element(self):
        wait = WebDriverWait(self.driver, 1)
        for aid in (
            "Поиск",
            "Search",
            "Кнопка поиска",
            "поиск",
            "search",
            "Поиск по каталогу",
            "Search catalog",
            "лупа",
            "magnifier",
        ):
            try:
                el = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid)))
                if el.is_displayed():
                    return el
            except (TimeoutException, WebDriverException):
                continue
        for desc in ("Поиск", "Search", "поиск"):
            try:
                el = wait.until(
                    EC.presence_of_element_located(
                        (
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            f'new UiSelector().descriptionContains("{desc}")',
                        )
                    )
                )
                if el.is_displayed():
                    return el
            except (TimeoutException, WebDriverException):
                continue
        for rid in (
            "gpm.tnt_premier:id/action_search",
            "gpm.tnt_premier:id/search_icon",
            "gpm.tnt_premier:id/search_button",
            "gpm.tnt_premier:id/iv_search",
        ):
            try:
                el = wait.until(EC.presence_of_element_located((AppiumBy.ID, rid)))
                if el.is_displayed():
                    return el
            except (TimeoutException, WebDriverException):
                continue
        try:
            el = wait.until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.XPATH,
                        "//android.widget.ImageView[@content-desc='Поиск']",
                    )
                )
            )
            if el.is_displayed():
                return el
        except (TimeoutException, WebDriverException):
            pass
        return None

    def _header_icons_in_right_half(self):
        try:
            w = self.driver.get_window_size().get("width", 1000)
            h = self.driver.get_window_size().get("height", 1800)
            top_threshold = int(h * 0.15)
            right_half_min_x = int(w * 0.5)
            candidates = []
            for class_name in ("android.widget.ImageView", "android.widget.ImageButton", "android.view.View"):
                for el in self.driver.find_elements(AppiumBy.CLASS_NAME, class_name):
                    try:
                        if not el.is_displayed():
                            continue
                        loc, sz = el.location, el.size
                        cx = loc["x"] + sz.get("width", 0) // 2
                        cy = loc["y"] + sz.get("height", 0) // 2
                        if cy < top_threshold and cx > right_half_min_x and sz.get("width", 0) < 200:
                            candidates.append(el)
                    except (TimeoutException, WebDriverException):
                        continue
            candidates.sort(key=lambda e: e.location["x"])
            return candidates
        except (TimeoutException, WebDriverException):
            return []

    def _tap_search_icon_by_position(self):
        try:
            w = self.driver.get_window_size().get("width", 1080)
            h = self.driver.get_window_size().get("height", 2219)
            for y_ratio in (0.04, 0.055):
                y = int(h * y_ratio)
                for x_ratio in (0.58, 0.62, 0.66, 0.70, 0.74, 0.78, 0.82):
                    x = int(w * x_ratio)
                    try:
                        self._tap(x, y)
                    except (TimeoutException, WebDriverException):
                        try:
                            self.driver.execute_script("mobile: clickGesture", {"x": x, "y": y})
                        except (TimeoutException, WebDriverException):
                            pass
                    try:
                        WebDriverWait(self.driver, 1).until(
                            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                        )
                        return
                    except (TimeoutException, WebDriverException):
                        continue
        except (TimeoutException, WebDriverException):
            pass

    def open_catalog(self):
        try:
            h = self.driver.get_window_size().get("height", 2200)
            bottom_min_y = int(h * 0.75)
        except (TimeoutException, WebDriverException):
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
                            WebDriverWait(self.driver, 2).until(lambda _: not el.is_displayed())
                            return True
                    except (TimeoutException, WebDriverException):
                        continue
            except (TimeoutException, WebDriverException):
                continue
        try:
            for el in self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Каталог")'
            ):
                try:
                    if not el.is_displayed():
                        continue
                    loc, sz = el.location, el.size
                    cy = loc["y"] + sz.get("height", 0) // 2
                    if cy >= bottom_min_y:
                        el.click()
                        WebDriverWait(self.driver, 2).until(lambda _: not el.is_displayed())
                        return True
                except (TimeoutException, WebDriverException):
                    continue
        except (TimeoutException, WebDriverException):
            pass
        return False

    def search_for(self, query, timeout=10):
        wait_short = WebDriverWait(self.driver, 1)
        opened = False
        for aid in ("Поиск", "Search", "Кнопка поиска", "search", "Поиск по каталогу"):
            try:
                el = wait_short.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, aid)))
                if el.is_displayed():
                    el.click()
                    opened = True
                    try:
                        WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                        )
                    except (TimeoutException, WebDriverException):
                        pass
                    break
            except (TimeoutException, WebDriverException):
                continue
        if not opened:
            for rid in (
                "gpm.tnt_premier:id/action_search",
                "gpm.tnt_premier:id/search_icon",
                "gpm.tnt_premier:id/search_button",
                "gpm.tnt_premier:id/iv_search",
            ):
                try:
                    el = wait_short.until(EC.presence_of_element_located((AppiumBy.ID, rid)))
                    if el.is_displayed():
                        el.click()
                        opened = True
                        try:
                            WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                            )
                        except (TimeoutException, WebDriverException):
                            pass
                        break
                except (TimeoutException, WebDriverException):
                    continue
        if not opened:
            for by, value in [
                (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Поиск']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Поиск")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Поиск")'),
            ]:
                try:
                    el = wait_short.until(EC.presence_of_element_located((by, value)))
                    if el.is_displayed():
                        el.click()
                        opened = True
                        try:
                            WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                            )
                        except (TimeoutException, WebDriverException):
                            pass
                        break
                except (TimeoutException, WebDriverException):
                    continue
        if not opened:
            self._tap_search_icon_by_position()
        field = None
        try:
            field = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            if not field.is_displayed():
                field = None
        except (TimeoutException, WebDriverException):
            pass
        if field:
            try:
                field.clear()
                field.send_keys(query)
            except (TimeoutException, WebDriverException):
                field = None
        if not field:
            try:
                builder = ActionBuilder(self.driver)
                key_input = builder.add_key_input("keyboard")
                key_input.send_keys(query)
                builder.perform()
            except (TimeoutException, WebDriverException):
                pass
        try:
            self.driver.press_keycode(66)
        except (TimeoutException, WebDriverException):
            pass
        return True

    def has_search_results_or_content(self, timeout=8):
        try:
            WebDriverWait(self.driver, min(timeout, 3)).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.RecyclerView"))
            )
            return True
        except (TimeoutException, WebDriverException):
            pass
        try:
            src = self.driver.page_source or ""
            return len(src) > 500
        except (TimeoutException, WebDriverException):
            return True

    def open_login_or_profile(self, timeout=8):
        wait = WebDriverWait(self.driver, timeout)
        for text in ("Профиль", "Profile", "Мой профиль"):
            try:
                el = wait.until(
                    EC.presence_of_element_located((AppiumBy.XPATH, f'//android.widget.TextView[@text="{text}"]'))
                )
                if el.is_displayed():
                    el.click()
                    try:
                        wait.until(
                            EC.presence_of_element_located(
                                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Войти")')
                            )
                        )
                    except (TimeoutException, WebDriverException):
                        pass
                    break
            except (TimeoutException, WebDriverException):
                try:
                    el = wait.until(
                        EC.presence_of_element_located(
                            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
                        )
                    )
                    if el.is_displayed():
                        el.click()
                        try:
                            wait.until(
                                EC.presence_of_element_located(
                                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Войти")')
                                )
                            )
                        except (TimeoutException, WebDriverException):
                            pass
                        break
                except (TimeoutException, WebDriverException):
                    pass
        else:
            for desc in ("Профиль", "Profile", "профиль", "profile", "Аккаунт", "Account", "Войти", "Login"):
                try:
                    el = wait.until(
                        EC.presence_of_element_located(
                            (
                                AppiumBy.ANDROID_UIAUTOMATOR,
                                f'new UiSelector().descriptionContains("{desc}")',
                            )
                        )
                    )
                    if el.is_displayed():
                        el.click()
                        try:
                            wait.until(
                                EC.presence_of_element_located(
                                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Войти")')
                                )
                            )
                        except (TimeoutException, WebDriverException):
                            pass
                        break
                except (TimeoutException, WebDriverException):
                    continue
            else:
                right_icons = self._header_icons_in_right_half()
                if right_icons:
                    right_icons[-1].click()
                    try:
                        wait.until(
                            EC.presence_of_element_located(
                                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Войти")')
                            )
                        )
                    except (TimeoutException, WebDriverException):
                        pass
                else:
                    try:
                        buttons = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageButton")
                        visible = [b for b in buttons if b.is_displayed()]
                        if visible:
                            max(visible, key=lambda b: b.location["x"] + b.size.get("width", 0)).click()
                            try:
                                wait.until(
                                    EC.presence_of_element_located(
                                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Войти")')
                                    )
                                )
                            except (TimeoutException, WebDriverException):
                                pass
                    except (TimeoutException, WebDriverException):
                        pass
        for text in (
            "Войти",
            "Login",
            "Вход",
            "Sign in",
            "Войти или зарегистрироваться",
            "Электронная почта",
            "Email",
            "Телефон",
            "Phone",
            "Профиль",
            "Profile",
        ):
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (
                            AppiumBy.ANDROID_UIAUTOMATOR,
                            f'new UiSelector().textContains("{text}")',
                        )
                    )
                )
                return True
            except (TimeoutException, WebDriverException):
                continue
        return "вход" in (self.driver.page_source or "").lower() or "login" in (self.driver.page_source or "").lower()
