"""
Верхнее меню разделов Premier.
Селекторы под premier.one — при необходимости замените.
"""
from selene import browser, have, be
from allure import step


class TopMenu:
    # Premier: Главная, Каталог, Бесплатно, ТВ-каналы, Спорт, Детям
    title = 'h1, [class*="page-title"], [class*="title"], main, [class*="content"]'

    # Ссылка в шапке/наве или любой кликабельный элемент с текстом раздела
    _nav_link = (
        '//header//a[contains(.,"{0}")] | //nav//a[contains(.,"{0}")] '
        '| //*[contains(@class,"header") or contains(@class,"nav") or contains(@class,"menu")]//a[contains(.,"{0}")] '
        '| //a[contains(normalize-space(),"{0}")] '
        '| //*[contains(text(),"{0}")]/ancestor::a[1] '
        '| //*[@role="link" and contains(.,"{0}")] '
        '| //*[contains(text(),"{0}")]/parent::a | //*[contains(text(),"{0}")]/parent::*[self::a or self::button] '
        '| //button[contains(.,"{0}")] '
        '| //*[contains(.,"{0}") and (self::a or self::button or @role="button" or @role="link")]'
    )

    @staticmethod
    def click_on_movies():
        with step('Нажать на раздел "Главная"'):
            browser.element(('xpath', TopMenu._nav_link.format('Главная'))).with_(timeout=10).should(be.visible).click()

    def check_movies_title(self):
        with step('Проверить, что раздел загрузился'):
            browser.element(('xpath', '//h1 | //*[contains(@class,"title")] | //main | //*[contains(@class,"content")]')).with_(timeout=8).should(be.visible)

    @staticmethod
    def click_on_serials():
        with step('Нажать на раздел "Бесплатно"'):
            browser.element(('xpath', TopMenu._nav_link.format('Бесплатно'))).with_(timeout=10).should(be.visible).click()

    def check_serials_title(self):
        with step('Проверить, что раздел Бесплатно загрузился'):
            browser.element(('xpath', '//*[contains(text(),"Бесплатно")] | //h1 | //main | //*[contains(@class,"content")]')).with_(timeout=8).should(be.visible)

    @staticmethod
    def click_on_catalog():
        with step('Нажать на раздел "Каталог"'):
            browser.element(('xpath', TopMenu._nav_link.format('Каталог'))).with_(timeout=10).should(be.visible).click()

    def check_catalog_title(self):
        with step('Проверить, что раздел Каталог загрузился'):
            browser.element(('xpath', '//*[contains(text(),"Каталог")] | //h1 | //main | //*[contains(@class,"content")]')).with_(timeout=8).should(be.visible)
