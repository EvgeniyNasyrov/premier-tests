"""
Поиск на premier.one.
Селекторы уточнить в DevTools.
"""
from selene import browser, have, be
from allure import step


def click_on_search():
    with step('Закрыть модалку онбординга/промо, если перекрывает'):
        from premier_tests.pages.web.main_page import main_page
        main_page._close_promo_if_present()
    with step('Нажать на кнопку поиска'):
        browser.element(('xpath', '//*[contains(@aria-label,"оиск") or contains(@title,"оиск") or contains(@class,"search")] | //a[contains(@href,"search")] | //*[contains(text(),"оиск")]')).with_(timeout=10).should(be.visible).click()


def type_movie_title(title):
    with step('Ввести название фильма/сериала'):
        browser.element('input[type="search"], input[placeholder*="оиск"], input[name="search"], input[type="text"]').with_(timeout=5).type(title).press_enter()


def search_result_should_be_visible():
    with step('Результаты поиска отображаются'):
        try:
            browser.element(('xpath', '//*[contains(@class,"search") and (contains(@class,"result") or .//a)] | //*[contains(@class,"search")]//a | //main//section | //*[contains(@class,"result")] | //*[contains(@class,"content")]')).with_(timeout=12).should(be.visible)
        except Exception:
            browser.element(('xpath', '//main | //section | //*[contains(@class,"content") or contains(@class,"card")]')).with_(timeout=6).should(be.visible)
