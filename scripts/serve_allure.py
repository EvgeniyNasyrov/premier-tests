"""
Открыть Allure-отчёт в браузере — оттуда удобно снимать скриншоты (Overview, Suites, тесты).

Нужен установленный Allure CLI: https://docs.qameta.io/allure/#_installing_a_commandline

Использование:
  python scripts/serve_allure.py                    # allure-results
  python scripts/serve_allure.py allure-results-ui
  python scripts/serve_allure.py allure-results-api
  python scripts/serve_allure.py allure-results-mobile
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_DIR = "allure-results"


def main():
    alluredir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    path = PROJECT_ROOT / alluredir
    if not path.exists():
        print(f"Каталог не найден: {path}")
        print(f"Сначала запустите тесты с --alluredir={alluredir}")
        print("Пример: pytest tests/UI/ -v --alluredir=allure-results-ui --headless")
        sys.exit(1)

    print("Allure Report")
    print("-------------")
    print("Отчёт откроется в браузере по адресу вида http://localhost:XXXXX")
    print("Снимайте скриншоты с этой страницы: Overview (круг с %, тренд), Suites, тесты.")
    print()

    subprocess.run(["allure", "serve", alluredir], cwd=PROJECT_ROOT)


if __name__ == "__main__":
    main()
