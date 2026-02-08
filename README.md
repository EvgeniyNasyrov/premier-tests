# Дипломный проект: автотесты онлайн-кинотеатра Premier

Проект по автоматизации тестирования сайта [Premier](https://premier.one/) и API [Reqres](https://reqres.in/), по образцу дипломов Okko и Ivi.

## Стек

- **Python 3.10–3.12** (на 3.14 возможны ошибки SSL при API-запросах; добавлен повтор запроса при ConnectionError)
- **pytest** — запуск тестов
- **Selene** — UI (Selenium)
- **requests** — API
- **Allure** — отчёты
- **Faker** — тестовые данные
- **jsonschema** — валидация ответов API


## Структура

```
premier-tests/
├── premier_tests/          # код под Premier (UI)
│   ├── pages/web/         # страницы и компоненты
│   └── utils/             # attach, path
├── reqres_tests/          # хелперы для API (reqres.in)
│   ├── request_helper/
│   ├── test_data/
│   └── utils/
├── tests/
│   ├── UI/                # UI-тесты Premier
│   └── API/               # API-тесты reqres.in
├── schemas/               # JSON Schema для API
├── requirements.txt
├── pytest.ini
└── README.md
```

## Установка

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

### UI-тесты (Premier)

```bash
# все UI-тесты
pytest tests/UI/

# с указанием браузера (по умолчанию chrome)
pytest tests/UI/ --browser_name=firefox
```

### API-тесты (Reqres)

```bash
pytest tests/API/
```

### Все тесты (полный прогон)

```bash
# 1. Активировать окружение
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Запустить всё: API (5) + UI (14)
pytest -v

# или через скрипт
./run_tests.sh
```

Если Chrome падает или не открывает окно — запускайте в headless (без окна, стабильнее):
```bash
pytest -v --headless
```

Только API (без браузера, работает в любом окружении, включая CI):
```bash
pytest tests/API/ -v
```

### Allure-отчёт

```bash
pytest
allure serve allure-results
```

## Реализованные проверки

### UI (Premier)

- Доступность вариантов входа (форма входа)
- Поиск по названию
- Переход в разделы (Фильмы, Сериалы, Каталог)
- Выбор по жанру и категории
- Регистрация/вход с валидным и невалидным email
- Отображение главной, страницы контента, промо
- Поиск фильма по названию (отдельный сценарий)

### API (Reqres.in)

- Успешная и неуспешная регистрация
- Создание пользователя
- Обновление пользователя
- Удаление пользователя