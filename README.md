# Проект Web/Mobile тестирования онлайн-кинотеатра Premier + API

> [Premier](https://premier.one/) · [Reqres](https://reqres.in/) / [JSONPlaceholder](https://jsonplaceholder.typicode.com/)
<img width="1440" height="807" alt="Снимок экрана 2026-02-22 в 16 20 04" src="https://github.com/user-attachments/assets/1d4400d3-118e-4231-9575-add0f9ceda03" />


## Используемые технологии

- **Python 3.10+**, **pytest** — запуск тестов

- **Selene**, **Selenium** — UI (веб)
- **requests** — API
- **Allure** — отчёты
- **Faker** — тестовые данные, **jsonschema** — валидация API
- **Appium** — мобильные тесты (Android)
- **Jenkins** — CI: pipeline, Allure-отчёт, уведомления в Telegram
- **Allure TestOps** и **Jira** — опционально: загрузка результатов в TestOps,связь тест-кейсов с задачами Jira

## Тест-кейсы

**UI:**
* ✅ Проверка доступности вариантов входа
* ✅ Вход с корректным email
* ✅ Вход с некорректным email
* ✅ Переход в выбранный раздел (Каталог, Главная, Бесплатно)
* ✅ Поиск фильма по названию
* ✅ Поиск сериала «Праздники» в каталоге
* ✅ Дымовые проверки (загрузка страницы, контент, ссылки)

**Mobile:**
* ✅ Приложение Premier запускается
* ✅ Главный экран отображается
* ✅ Закрытие баннеров при входе в приложение

**API:**
* ✅ Создание пользователя (POST)
* ✅ Обновление пользователя
* ✅ Удаление пользователя
* ✅ Запрос несуществующего пользователя (404)
* ✅ Поиск контента (сериал «Праздники»)

---

## Запуск проекта в Jenkins

[Задача в Jenkins](https://jenkins.autotests.cloud/job/023-evgdnzh-premier_tests/) — ссылка на джобу на [jenkins.autotests.cloud](https://jenkins.autotests.cloud/).

Pipeline из репозитория: одна джоба. Параметры: **TEST_RUN** (`diploma` — три прогона API/UI/Mobile, три Allure-отчёта и три сообщения в Telegram; `api_only` — только API), **ALLURE_PROJECT_ID** (по умолчанию `5127` — ID проекта в Allure TestOps), **USE_BROWSERSTACK_MOBILE** (галочка — запускать мобильные в BrowserStack), **APP_PATH** (путь к APK, если без BrowserStack).

---

## Allure Report

Результаты выполнения тестов можно посмотреть в Allure-отчёте (локально: `allure serve allure-results-ui` и т.п.; в Jenkins — ссылка «Allure Report» на странице сборки).
<img width="1440" height="812" alt="Снимок экрана 2026-02-22 в 16 24 51" src="https://github.com/user-attachments/assets/fc78eaac-01b9-475c-b6f5-ba0d1870ad12" />

---

##  Интеграция с Allure TestOps

[Dashboard](https://allure.autotests.cloud/project/5127/dashboards)

<img width="1440" height="807" alt="Снимок экрана 2026-02-22 в 16 37 29" src="https://github.com/user-attachments/assets/cde926d8-f4be-4e3b-9e10-3e3083793c00" />

---

## Интеграция с Jira

Связь тест-кейсов и прогонов с задачами Jira настраивается в Allure TestOps (интеграция Jira + Issue mapping). В тестах — метка `allure.label('jira', 'KEY-123')`. В Jira отображаются прилинкованные тест-кейсы и лаунчи (плагин Allure TestOps for Jira).


<img width="1440" height="810" alt="Снимок экрана 2026-02-22 в 16 26 30" src="https://github.com/user-attachments/assets/3cf1dbe8-ef30-4cb6-9f1e-f0450059e6f9" />


---

## Оповещения в Telegram

После выполнения тестов в Telegram приходит сообщение с графиком (круг passed/failed) и информацией о тестовом прогоне. При прогоне `diploma` — три сообщения (API, UI, Mobile).

<img width="323" height="382" alt="API" src="https://github.com/user-attachments/assets/a414ae2f-7fc9-4da1-a97e-7a488ce92ad1" />

<img width="323" height="386" alt="UI" src="https://github.com/user-attachments/assets/d646b395-5cbb-43f5-a766-3b156e49fd15" />

<img width="322" height="388" alt="Mobile" src="https://github.com/user-attachments/assets/10a6d7c8-79b9-4039-9124-00fdc0d42eb5" />


---


## Структура проекта

```
premier-tests/
├── premier_tests/          # код под Premier
│   ├── pages/web/         # страницы и компоненты (UI)
│   ├── pages/mobile/      # экраны приложения (Android)
│   └── utils/             # path и хелперы
├── reqres_tests/           # хелперы и данные для API (request_helper, test_data, utils)
├── tests/
│   ├── UI/                # UI-тесты Premier (сайт)
│   ├── API/               # API-тесты (JSONPlaceholder)
│   └── mobile/            # мобильные тесты (Appium, Android): test_main.py, test_main_mock.py
├── scripts/               # run_diploma_runs.py, run_tests_and_notify.py, telegram_notify.py, serve_allure.py, upload_app_to_*.py
├── schemas/               # JSON-схемы для валидации API (create_user, register_user, update_user)
├── images/                # скриншоты для README (Allure, Telegram)
├── requirements.txt
├── pytest.ini
├── run_tests.sh
├── Jenkinsfile            # Pipeline: diploma / api_only, Allure, TestOps, Telegram
├── .env                   # не коммитится: TELEGRAM_*, BSTACK_*, APP_PATH и др.
└── README.md
```
