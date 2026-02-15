"""
Загрузка APK Premier в LambdaTest (TestMu AI) Real Device Cloud.
Берёт LT_USERNAME, LT_ACCESS_KEY из .env, ищет premier2.apk / premier.apk и др. в корне.
Документация: https://www.lambdatest.com/support/docs/application-setup-via-api/
Использование: python scripts/upload_app_to_lambdatest.py
"""
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

# Приоритет: APK 2.80 (apkmirror), затем Aptoide и др.
APK_NAMES = (
    "gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk",
    "premier_aptoide.apk",
    "premier_from_xapk.apk",
    "premier.apk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure-2.xapk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure.xapk",
    "premier2.apk",
    "gpm-tnt-premier.apk",
    "gpm-tnt-premier.xapk",
    "premier.xapk",
)
UPLOAD_URL = "https://manual-api.lambdatest.com/app/upload/realDevice"
APK_MAGIC = b"PK"


def check_apk_valid(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(len(APK_MAGIC)) == APK_MAGIC
    except Exception:
        return False


def main():
    username = os.getenv("LT_USERNAME") or os.getenv("LAMBDATEST_USERNAME")
    key = os.getenv("LT_ACCESS_KEY") or os.getenv("LAMBDATEST_ACCESS_KEY")
    if not username or not key:
        print("Задайте LT_USERNAME и LT_ACCESS_KEY в .env (можно взять на https://accounts.lambdatest.com/security)", file=sys.stderr)
        sys.exit(1)

    apk_path = None
    for name in APK_NAMES:
        p = PROJECT_ROOT / name
        if p.is_file():
            apk_path = p
            break
    if not apk_path:
        print(f"APK не найден в корне. Положите один из: {APK_NAMES}", file=sys.stderr)
        sys.exit(1)

    if not check_apk_valid(apk_path):
        print(f"Файл {apk_path.name} не похож на валидный APK (должен начинаться с PK).", file=sys.stderr)
        sys.exit(1)

    import requests
    with open(apk_path, "rb") as f:
        file_content = f.read()
    r = requests.post(
        UPLOAD_URL,
        auth=(username, key),
        files={"appFile": (apk_path.name, file_content, "application/vnd.android.package-archive")},
        data={"name": "PremierApp"},
        timeout=300,
    )

    if r.status_code != 200:
        print(f"Ошибка {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    data = r.json()
    app_url = data.get("app_url") or data.get("App URL") or data.get("App_URL")
    if not app_url:
        print(f"В ответе нет app_url. Ответ: {data}", file=sys.stderr)
        sys.exit(1)

    print("APK загружен в LambdaTest (TestMu AI).")
    print("Добавь в .env:")
    print(f"LT_APP={app_url}")
    print()
    print("Запуск мобильных тестов: pytest tests/mobile/ -v --context=lambdatest")


if __name__ == "__main__":
    main()
