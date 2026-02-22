"""
Базовые действия главной страницы Premier.
"""
from selene import browser, have, be
from allure import step


def open_main_page():
    with step('Открыть главную страницу'):
        browser.open('/')
    with step('Закрыть промо-окно, если открыто'):
        from premier_tests.pages.web.main_page import main_page
        main_page._close_promo_if_present()


def premier_header_should_be_visible():
    with step('Шапка сайта Premier отображается'):
        # В шапке есть «Сделано PREMIER» или «Войти»
        browser.element(('xpath', '//header | //*[contains(@class,"header")]')).should(have.text('PREMIER'))


def click_on_movie_preview():
    with step('Нажать на превью контента'):
        # Premier: карточки — ссылки с картинкой (широкий селектор под любую структуру)
        browser.element(('xpath', '//a[.//img][contains(@href,"/") and not(starts-with(@href,"#"))] | //a[contains(@href,"/watch") or contains(@href,"/movie") or contains(@href,"/film") or contains(@href,"/p/")]')).with_(timeout=10).should(be.visible).click()


def movie_title_should_be_visible():
    with step('Заголовок контента отображается'):
        browser.element('h1, [class*="title"]').should(be.visible)


def click_on_promo():
    with step('Нажать на промо-блок'):
        browser.element(('xpath', '//section[@data-qa-selector="promo-slider"]//a | //*[contains(@class,"w-promo")]//a | //button[contains(text(),"Подключить")]')).with_(timeout=6).should(be.visible).click()


def check_promo_title():
    with step('Проверить заголовок промо'):
        browser.element(('xpath', '//*[contains(text(),"1₽") or contains(text(),"PREMIER") or contains(text(),"RUTUBE")]')).should(be.visible)


def check_promo_button():
    with step('Проверить кнопку промо'):
        browser.element(('xpath', '//button[contains(text(),"Подключить")] | //*[contains(text(),"Подключить")]')).should(be.visible)
