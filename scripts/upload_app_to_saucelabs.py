"""
Загрузка APK Premier в Sauce Labs App Storage.
Берёт SAUCE_USERNAME, SAUCE_ACCESS_KEY из .env, ищет в корне: premier_from_xapk.apk, premier.apk и др.
Документация: https://docs.saucelabs.com/mobile-apps/app-storage/
Использование: python scripts/upload_app_to_saucelabs.py
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

APK_NAMES = (
    "gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk",
    "premier_aptoide.apk",
    "premier_from_xapk.apk",
    "gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk",
    "premier.apk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure-2.xapk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure.xapk",
    "premier2.apk",
    "gpm-tnt-premier.apk",
    "gpm-tnt-premier.xapk",
    "premier.xapk",
)
# Регион: us-west-1, us-east-4, eu-central-1
API_REGIONS = {
    "us-west-1": "https://api.us-west-1.saucelabs.com",
    "us-east-4": "https://api.us-east-4.saucelabs.com",
    "eu-central-1": "https://api.eu-central-1.saucelabs.com",
}
APK_MAGIC = b"PK"


def check_apk_valid(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(len(APK_MAGIC)) == APK_MAGIC
    except Exception:
        return False


def main():
    username = os.getenv("SAUCE_USERNAME")
    key = os.getenv("SAUCE_ACCESS_KEY")
    if not username or not key:
        print("Задайте SAUCE_USERNAME и SAUCE_ACCESS_KEY в .env", file=sys.stderr)
        print("Регистрация: https://saucelabs.com/sign-up", file=sys.stderr)
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
        print(f"Файл {apk_path.name} не похож на валидный APK (ZIP/PK).", file=sys.stderr)
        sys.exit(1)

    region = os.getenv("SAUCE_REGION", "us-west-1").lower()
    base = API_REGIONS.get(region) or API_REGIONS["us-west-1"]
    upload_url = f"{base}/v1/storage/upload"

    import requests
    with open(apk_path, "rb") as f:
        payload = f.read()
    # Имя должно содержать расширение, иначе приложение не будет доступно для тестов
    name = apk_path.name

    r = requests.post(
        upload_url,
        auth=(username, key),
        files={"payload": (name, payload, "application/vnd.android.package-archive")},
        data={"name": name},
        timeout=300,
    )

    if r.status_code != 201:
        print(f"Ошибка {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    data = r.json()
    item = data.get("item") or {}
    file_id = item.get("id")
    if not file_id:
        print(f"Нет item.id в ответе: {data}", file=sys.stderr)
        sys.exit(1)

    # В capabilities передаём storage:file_id или storage:filename=...
    app_value = f"storage:{file_id}"
    print("APK загружен в Sauce Labs.")
    print("Добавь в .env:")
    print(f"SAUCE_APP={app_value}")
    print("(или SAUCE_APP=storage:filename=" + name + "  — будет использована последняя версия по имени)")
    print()
    print("Запуск мобильных тестов: pytest tests/mobile/ -v --context=sauce")

if __name__ == "__main__":
    main()
