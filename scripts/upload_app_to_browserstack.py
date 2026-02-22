"""
Загрузка APK/XAPK Premier в BrowserStack App Automate.
BrowserStack принимает .apk, .aab и .xapk (единственный из облаков с поддержкой XAPK).
Берёт BSTACK_USERNAME, BSTACK_ACCESS_KEY из .env.
Использование:
  python scripts/upload_app_to_browserstack.py          # загрузить первый найденный .apk или .xapk
  python scripts/upload_app_to_browserstack.py --xapk    # загрузить только .xapk (если есть в корне)
"""
import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_env = PROJECT_ROOT / ".env"
if _env.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env)
    except Exception:
        pass

# BrowserStack принимает .apk, .aab, .xapk (Android). По умолчанию приоритет у .apk.
APK_NAMES = (
    "gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk",
    "premier_aptoide.apk",
    "premier_from_xapk.apk",
    "gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk",
    "premier.apk",
    "premier2.apk",
    "gpm-tnt-premier.apk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure-2.xapk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure.xapk",
    "gpm-tnt-premier.xapk",
    "premier.xapk",
)
# Только .xapk — для загрузки именно XAPK в BrowserStack (LambdaTest/Sauce XAPK не принимают).
XAPK_NAMES = tuple(n for n in APK_NAMES if n.lower().endswith(".xapk"))
UPLOAD_URL = "https://api-cloud.browserstack.com/app-automate/upload"

# APK и XAPK — ZIP-архивы; первые байты должны быть PK
APK_MAGIC = b"PK"


def check_apk_valid(path: Path) -> bool:
    """Проверка, что файл похож на валидный APK/XAPK (ZIP, начинается с PK)."""
    try:
        with open(path, "rb") as f:
            return f.read(len(APK_MAGIC)) == APK_MAGIC
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Загрузка APK/XAPK в BrowserStack App Automate")
    parser.add_argument(
        "--xapk",
        action="store_true",
        help="Искать только .xapk в корне (BrowserStack — единственное облако, принимающее XAPK)",
    )
    parser.add_argument(
        "--app",
        metavar="FILE",
        help="Загрузить конкретный файл из корня (например premier_aptoide.apk)",
    )
    args = parser.parse_args()
    username = os.getenv("BSTACK_USERNAME") or os.getenv("USER_NAME")
    key = os.getenv("BSTACK_ACCESS_KEY") or os.getenv("ACCESS_KEY")
    if not username or not key:
        print("Задайте BSTACK_USERNAME и BSTACK_ACCESS_KEY в .env", file=sys.stderr)
        sys.exit(1)

    apk_path = None
    if args.app:
        p = PROJECT_ROOT / args.app.strip()
        if p.is_file():
            apk_path = p
        else:
            print(f"Файл не найден: {p}", file=sys.stderr)
            sys.exit(1)
    else:
        names = XAPK_NAMES if args.xapk else APK_NAMES
        for name in names:
            p = PROJECT_ROOT / name
            if p.is_file():
                apk_path = p
                break
    if not apk_path:
        print(
            f"Файл не найден в корне. Положите один из: {names}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not check_apk_valid(apk_path):
        print(
            f"Файл {apk_path.name} не похож на валидный APK/XAPK (должен начинаться с 'PK', как ZIP).\n"
            "Проверь целостность: unzip -t " + str(apk_path) + "\n"
            "Если файл повреждён или это не APK/XAPK, BrowserStack вернёт 'Could not parse'.",
            file=sys.stderr,
        )
        sys.exit(1)

    import requests
    # Как в документации: multipart/form-data, параметр file. Без явного MIME — пусть сервер определяет по расширению .apk
    with open(apk_path, "rb") as f:
        file_content = f.read()
    # custom_id по доке: A–Z, a–z, 0–9, ., -, _ (лимит 100 символов)
    r = requests.post(
        UPLOAD_URL,
        auth=(username, key),
        files={"file": (apk_path.name, file_content, "application/octet-stream")},
        data={"custom_id": "PremierApp"},
        timeout=300,
    )

    if r.status_code != 200:
        print(f"Ошибка {r.status_code}: {r.text}", file=sys.stderr)
        if r.status_code == 422:
            print(
                "\nВозможные причины 422 / 'Could not parse':\n"
                "1) Файл повреждён или не APK — проверь: unzip -t " + str(apk_path) + "\n"
                "2) Это .aab (Android App Bundle) переименованный в .apk — загружай как .aab или собери APK из AAB.\n"
                "3) Исчерпаны бесплатные минуты или сработала защита BrowserStack — см. support.",
                file=sys.stderr,
            )
        sys.exit(1)

    data = r.json()
    app_url = data.get("app_url")
    if not app_url:
        print(f"Нет app_url в ответе: {data}", file=sys.stderr)
        sys.exit(1)

    print("APK загружен в BrowserStack.")
    print("Добавь в .env:")
    print(f"BSTACK_APP={app_url}")
    print()
    print("Затем запуск мобильных тестов: pytest tests/mobile/ -v --context=bstack")


if __name__ == "__main__":
    main()
