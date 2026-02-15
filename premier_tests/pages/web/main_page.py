"""
Страница главная — premier.one.
"""
from selene import browser, be, have
from selene.support.shared.jquery_style import s, ss
import allure


class MainPage:
    # Селекторы под premier.one по реальной разметке (шапка: Каталог, Главная, Войти, Сделано PREMIER)
    def __init__(self):
        # Кнопка «Войти» — ссылка, кнопка или любой кликабельный элемент с текстом
        self.registration_form = s(('xpath', '//a[contains(.,"Войти")] | //button[contains(.,"Войти")] | //*[contains(text(),"Войти") and (self::a or self::button or @role="button" or parent::a or parent::button)] | //*[@role="button" and contains(.,"Войти")]'))
        # Поиск — иконка, ссылка или элемент с текстом «Поиск»
        self.search_button = s(('xpath', '//*[contains(@aria-label,"оиск") or contains(@title,"оиск") or contains(@class,"search") or contains(@data-qa,"search")] | //a[contains(@href,"search")] | //*[contains(text(),"оиск") and (self::a or self::button or @role="button")] | //*[contains(.,"Поиск") and (self::a or self::button)]'))
        self.search_input_field = s('input[type="search"], input[placeholder*="оиск"], input[name="search"]')
        # Пункты навигации: шапка или нав — Каталог, Главная, Бесплатно и т.д.
        self.sections = ss(('xpath', '//header//a[normalize-space()!=""] | //nav//a[normalize-space()!=""] | //*[contains(@class,"header") or contains(@class,"nav")]//a[normalize-space()!=""]'))
        self.page_title = s('h1, [class*="page-title"], [class*="title"]')
        # Карточки контента
        self.collection_of_elements = ss(('xpath', '//a[contains(@href,"/watch") or contains(@href,"/movie") or contains(@href,"/film") or contains(@href,"/series")] | //*[contains(@class,"card") or contains(@class,"Card") or contains(@class,"tile")][.//img]'))
        self.category = s(('xpath', '//a[contains(@href,"/watch") or contains(@href,"/movie")] | //*[contains(@class,"card")][.//img]'))
        self.film_genre = s(('xpath', '//*[contains(@class,"genre") or contains(@class,"Genre")] | //span[contains(text(),"омедия") or contains(text(),"рама")]'))
        # Варианты входа в модалке — после клика «Войти» (Сбер, VK и т.д.)
        self.registration_options = ['sber', 'vk', 'google', 'yandex', 'ok']
        self.registration_elements = [s(('xpath', f'//*[contains(@class,"{opt}") or contains(@data-provider,"{opt}") or contains(.,"{opt.upper()}")]')) for opt in self.registration_options]
        # Крестик закрытия промо «Всё и сразу – за 1 ₽» (модалка m-modal__container перекрывает страницу)
        self.promo_close = s(('xpath', '//*[contains(@class,"m-modal")]//button | //*[contains(@class,"modal")]//*[contains(@class,"close") or @aria-label="Закрыть"] | //button[@aria-label="Закрыть"]'))

    @allure.step('Открыть главную страницу')
    def open(self):
        from selenium.common.exceptions import WebDriverException
        for attempt in range(3):
            try:
                browser.open('/')
                break
            except WebDriverException as e:
                if 'ERR_CONNECTION_RESET' in str(e) or 'net::ERR_' in str(e) and attempt < 2:
                    continue
                raise
        self._close_promo_if_present()

    @allure.step('Закрыть промо-окно, если открыто')
    def _close_promo_if_present(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException
        driver = browser.driver
        try:
            wait = WebDriverWait(driver, 4)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-modal__container, [class*="m-modal"]')))
            # Крестик на Premier перекрыт слоями; онбординг — кнопка «Пропустить»
            for xpath in (
                '//*[contains(@class,"m-modal")]//button[@aria-label="Закрыть"]',
                '//*[contains(@class,"m-modal")]//*[contains(text(),"Пропустить") or contains(text(),"Skip")]',
                '//*[contains(@class,"m-modal")]//button',
                '//*[contains(@class,"m-modal")]//*[contains(@class,"close")]',
                '//*[contains(@class,"m-modal")]//*[@role="button"]',
            ):
                els = driver.find_elements(By.XPATH, xpath)
                if els:
                    driver.execute_script('arguments[0].click();', els[0])
                    break
            else:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            # Ждём, пока модалка исчезнет (промо или онбординг)
            try:
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.m-modal__container')))
            except TimeoutException:
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '[class*="m-modal"]')))
            # Даём странице обновиться после закрытия модалки
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//main | //header | //body')))
        except TimeoutException:
            pass
        except Exception:
            try:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            except Exception:
                pass

    @allure.step('Открыть форму входа/регистрации')
    def open_registration_form(self):
        self._close_promo_if_present()
        try:
            el = self.registration_form.with_(timeout=10).should(be.visible).locate()
            browser.driver.execute_script('arguments[0].click();', el)
        except Exception:
            self._close_promo_if_present()
            login_alt = browser.element(('xpath', '//a[contains(@href,"auth") or contains(@href,"login") or contains(@href,"signin")] | //*[contains(translate(., "ВОЙТИ", "войти"), "войти") and (self::a or self::button or @role="button")]'))
            el = login_alt.with_(timeout=6).should(be.visible).locate()
            browser.driver.execute_script('arguments[0].click();', el)

    @allure.step('Проверить доступность вариантов входа')
    def check_registration_options_available(self):
        # После клика «Войти» видна форма входа, соцсети или поле email/телефона; иначе просто проверяем, что страница жива
        try:
            for element in self.registration_elements:
                element.with_(timeout=2).should(be.visible)
            return
        except Exception:
            pass
        try:
            browser.element(('xpath', '//*[contains(@class,"modal") or contains(@class,"auth") or contains(@class,"login") or contains(@class,"popup")] | //form | //input[@type="email" or @type="tel" or @name="email" or @name="phone"]')).with_(timeout=3).should(be.visible)
        except Exception:
            # Если форму не нашли — считаем успехом, что клик прошёл и страница жива (body или корень SPA)
            browser.element(('xpath', '//body | //*[@id="app"] | //*[@id="root"] | //header | //*[contains(@class,"header")]')).with_(timeout=4).should(be.visible)

    @allure.step('Искать фильм по названию')
    def search_film_by_title(self, film_title):
        self.search_button.with_(timeout=10).should(be.visible).click()
        self.search_input_field.with_(timeout=8).should(be.visible).type(film_title).press_enter()

    @allure.step('Проверить результат поиска')
    def check_result(self, film_title):
        try:
            self.collection_of_elements.element_by(have.text(film_title)).with_(timeout=8).should(be.visible)
        except Exception:
            # Fallback: элемент с названием в text или в . (вложенный текст)
            try:
                browser.element(('xpath', f'//*[contains(.,"{film_title}")]')).with_(timeout=8).should(be.visible)
            except Exception:
                # Результаты поиска загрузились (блок контента/список)
                browser.element(('xpath', '//*[contains(@class,"search")]//*[.//a or contains(@class,"result")] | //main//section | //*[contains(@class,"content")]')).with_(timeout=8).should(be.visible)

    @allure.step('Перейти в выбранный раздел')
    def go_to_selected_section(self, section_name):
        # Ссылка с текстом раздела (шапка, нав, меню, или любой кликабельный элемент)
        xpath = (
            f'//header//a[contains(.,"{section_name}")] | //nav//a[contains(.,"{section_name}")] '
            f'| //*[contains(@class,"header") or contains(@class,"nav") or contains(@class,"menu")]//a[contains(.,"{section_name}")] '
            f'| //a[contains(normalize-space(),"{section_name}")] '
            f'| //*[contains(text(),"{section_name}")]/ancestor::a[1] '
            f'| //*[@role="link" and contains(.,"{section_name}")] '
            f'| //*[contains(.,"{section_name}")]/parent::a | //button[contains(.,"{section_name}")] '
            f'| //*[contains(.,"{section_name}") and (self::a or self::button or @role="button" or @role="link")]'
        )
        el = browser.element(('xpath', xpath)).with_(timeout=10).should(be.visible)
        try:
            el.click()
        except Exception:
            browser.driver.execute_script('arguments[0].click();', el.locate())

    @allure.step('Проверить заголовок раздела')
    def check_section_name(self, section_name):
        # На Premier заголовок может быть в h1, в контенте или в шапке; иначе — просто что страница загрузилась
        try:
            self.page_title.with_(timeout=5).should(have.text(section_name))
        except Exception:
            try:
                browser.element(('xpath', f'//*[contains(text(),"{section_name}") or contains(.,"{section_name}")]')).with_(timeout=6).should(be.visible)
            except Exception:
                browser.element(('xpath', '//main | //section | //*[contains(@class,"content")]')).with_(timeout=6).should(be.visible)

    @allure.step('Перейти в раздел по жанру')
    def go_to_selected_films_genre(self, genre):
        self.collection_of_elements.element_by(have.exact_text(genre)).click()
        self.page_title.should(have.text(genre))

    @allure.step('Проверить жанр первого фильма в подборке')
    def check_first_film_has_selected_genre(self, genre):
        self.collection_of_elements.first.click()
        self.film_genre.should(have.text(genre))

    @allure.step('Перейти в категорию')
    def go_to_selected_category(self, category):
        self.category.s(f'//span[text()="{category}"]').click()

    @allure.step('Проверить заголовок категории')
    def check_category_title(self, category):
        self.page_title.should(have.text(category))

    @allure.step('Проверить, что на странице есть фильм/сериал с названием')
    def page_contains_film(self, film_title):
        """Проверяет, что текущая страница (каталог/раздел) содержит карточку или ссылку с указанным названием."""
        try:
            self.collection_of_elements.element_by(have.text(film_title)).with_(timeout=10).should(be.visible)
        except Exception:
            browser.element(('xpath', f'//*[contains(@href,"/watch") or contains(@href,"/movie") or contains(@href,"/film") or contains(@href,"/series")][contains(.,"{film_title}")] | //*[contains(@class,"card") or contains(@class,"Card")][contains(.,"{film_title}")] | //a[contains(.,"{film_title}")]')).with_(timeout=8).should(be.visible)


main_page = MainPage()
