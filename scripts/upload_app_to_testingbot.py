"""
Загрузка APK Premier в TestingBot Storage.
TestingBot не принимает XAPK — скрипт при необходимости извлекает APK из XAPK, затем грузит.
Берёт TB_KEY, TB_SECRET из .env (ключи в Security Settings на testingbot.com).
Документация: https://testingbot.com/support/mobile/upload.html
Использование: python scripts/upload_app_to_testingbot.py
"""
import os
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_env = PROJECT_ROOT / ".env"
if _env.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(str(_env), override=True)
    except Exception:
        pass

PREMIER_FROM_XAPK = "premier_from_xapk.apk"
MAIN_APK_IN_XAPK = "gpm.tnt_premier.apk"
XAPK_NAMES = (
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure-2.xapk",
    "PREMIER - Сериалы, фильмы, шоу_2.117.1_APKPure.xapk",
    "gpm-tnt-premier.xapk",
    "premier.xapk",
)
# Приоритет: APK 2.80 (apkmirror), затем Aptoide и остальные
APK_NAMES = (
    "gpm.tnt_premier_2.80.0-5759187_minAPI24(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com.apk",
    "premier_aptoide.apk",
    PREMIER_FROM_XAPK,
    "premier.apk",
) + XAPK_NAMES + (
    "premier2.apk",
    "gpm-tnt-premier.apk",
)
UPLOAD_URL = "https://api.testingbot.com/v1/storage"
APK_MAGIC = b"PK"


def ensure_apk_from_xapk() -> bool:
    """Если premier_from_xapk.apk нет, извлечь из первого найденного .xapk. Возвращает True, если APK готов."""
    out = PROJECT_ROOT / PREMIER_FROM_XAPK
    if out.is_file():
        return True
    for name in XAPK_NAMES:
        xapk = PROJECT_ROOT / name
        if not xapk.is_file():
            continue
        try:
            with zipfile.ZipFile(xapk, "r") as z:
                if MAIN_APK_IN_XAPK not in z.namelist():
                    continue
                z.extract(MAIN_APK_IN_XAPK, PROJECT_ROOT)
            (PROJECT_ROOT / MAIN_APK_IN_XAPK).rename(out)
            print(f"Из XAPK извлечён {PREMIER_FROM_XAPK}", file=sys.stderr)
            return True
        except Exception as e:
            print(f"Ошибка извлечения из {name}: {e}", file=sys.stderr)
            continue
    return False


def check_apk_valid(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(len(APK_MAGIC)) == APK_MAGIC
    except Exception:
        return False


def main():
    ensure_apk_from_xapk()

    key = os.getenv("TB_KEY") or os.getenv("TESTINGBOT_KEY")
    secret = os.getenv("TB_SECRET") or os.getenv("TESTINGBOT_SECRET")
    if not key or not secret:
        print("Задайте TB_KEY и TB_SECRET в .env (Security Settings на testingbot.com)", file=sys.stderr)
        if not _env.exists():
            print(f"Файл .env не найден. Создайте {_env}", file=sys.stderr)
        else:
            if not key:
                print("В .env отсутствует: TB_KEY=ваш_key_из_testingbot", file=sys.stderr)
            if not secret:
                print("В .env отсутствует: TB_SECRET=ваш_secret_из_testingbot", file=sys.stderr)
            print("Формат в .env — без кавычек, без пробелов вокруг =:", file=sys.stderr)
            print("  TB_KEY=ваш_key_из_Security_Settings", file=sys.stderr)
            print("  TB_SECRET=ваш_secret_из_Security_Settings", file=sys.stderr)
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

    import requests
    with open(apk_path, "rb") as f:
        payload = f.read()
    r = requests.post(
        UPLOAD_URL,
        auth=(key, secret),
        files={"file": (apk_path.name, payload, "application/vnd.android.package-archive")},
        timeout=300,
    )

    if r.status_code not in (200, 201):
        print(f"Ошибка {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)

    data = r.json() if r.text else {}
    app_url = data.get("app_url")
    if not app_url:
        print(f"Нет app_url в ответе. Ответ: {r.text}", file=sys.stderr)
        sys.exit(1)

    print("APK загружен в TestingBot.")
    print("Добавь в .env:")
    print(f"TB_APP={app_url}")
    print()
    print("Запуск мобильных тестов: pytest tests/mobile/ -v --context=testingbot")

if __name__ == "__main__":
    main()
