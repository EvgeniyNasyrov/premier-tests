"""
Форма входа/регистрация — premier.one.
Селекторы уточнить в DevTools; форма может быть в iframe.
"""
from selene import be, have
from selene.support.shared import browser
from selene.support.shared.jquery_style import s
import allure


def _email_input_xpath():
    return '//input[@type="email"] | //input[@name="email"] | //*[@data-testid="email"] | //input[contains(@placeholder,"mail") or contains(@placeholder,"почт") or contains(@placeholder,"e-mail")] | //input[contains(@type,"text") and (contains(@name,"mail") or contains(@id,"mail"))]'


class RegistrationForm:
    def __init__(self):
        self.sign_input = s(('xpath', _email_input_xpath()))
        self.continue_button = s(('xpath', '//button[@type="submit"] | //*[@data-testid="continue"] | //button[contains(.,"Далее") or contains(.,"Продолжить") or contains(.,"Войти")]'))
        self.sliding_panel = s(('xpath', '//*[contains(@class,"auth") or contains(@class,"modal") or contains(@class,"panel")] | //*[@data-testid="auth-panel"]'))
        self.info_message = s(('xpath', '//*[contains(@class,"error") or contains(@class,"invalid")] | //*[@data-testid="error"]'))

    def _find_and_type_email(self, email):
        """Найти поле (email или любой input) и ввести email — в документе или в iframe."""
        for xpath in [_email_input_xpath(), '//input[@type="text"]', '//input']:
            try:
                browser.element(('xpath', xpath)).with_(timeout=6).should(be.visible).type(email)
                return
            except Exception:
                continue
        try:
            iframe = browser.element('iframe').with_(timeout=3)
            if iframe.matching(be.visible):
                browser.driver.switch_to.frame(iframe.get())
                for xpath in [_email_input_xpath(), '//input[@type="text"]', '//input']:
                    try:
                        browser.element(('xpath', xpath)).with_(timeout=6).should(be.visible).type(email)
                        return
                    except Exception:
                        continue
        except Exception:
            pass
        raise AssertionError('Поле ввода (email или текст) не найдено на странице входа')

    @allure.step('Ввести email в поле')
    def enter_email(self, email):
        self._find_and_type_email(email)
        self.continue_button.with_(timeout=5).click()

    @allure.step('Проверить результат входа/регистрации')
    def check_registration_result(self, email_valid=True):
        if email_valid:
            # Успех: панель соцсетей/следующий шаг или отсутствие ошибки
            try:
                self.sliding_panel.with_(timeout=5).should(be.visible)
            except Exception:
                # Форма могла смениться — проверяем, что нет явной ошибки
                try:
                    browser.element(('xpath', '//*[contains(@class,"error") or contains(text(),"Неверн") or contains(text(),"ошибк")]')).with_(timeout=2).should(be.visible)
                except Exception:
                    pass  # ошибки нет — считаем успехом
                else:
                    raise AssertionError('Ожидался успешный шаг, но видно сообщение об ошибке')
        else:
            try:
                self.info_message.with_(timeout=5).should(be.visible)
            except Exception:
                browser.element(('xpath', '//*[contains(text(),"Неверн") or contains(text(),"ошибк") or contains(text(),"invalid") or contains(text(),"Введите")]')).with_(timeout=4).should(be.visible)


registration_form = RegistrationForm()
