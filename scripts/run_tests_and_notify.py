"""
Запуск тестов и отправка результата в Telegram.
Токен и chat_id берутся из .env или переменных окружения.
Использование:
  python scripts/run_tests_and_notify.py                    # все тесты
  python scripts/run_tests_and_notify.py -- -v --headless   # все тесты, браузер без окна (быстрее)
  python scripts/run_tests_and_notify.py -- tests/API/ -v   # только API (самый быстрый прогон)
  python scripts/run_tests_and_notify.py -- tests/UI/ -v   # только UI
  # Два прогона для диплома (разные отчёты и скриншоты):
  python scripts/run_tests_and_notify.py --alluredir allure-results-api --label "API" -- tests/API/ -v
  python scripts/run_tests_and_notify.py --alluredir allure-results-ui --label "UI" -- tests/UI/ -v --headless
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# корень проекта (родитель scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Загрузить .env
_env = PROJECT_ROOT / ".env"
if _env.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env)
    except Exception:
        pass

DEFAULT_ALLUREDIR = "allure-results"


def _parse_script_args(argv=None):
    """Парсит аргументы скрипта до '--'; возвращает (alluredir, label, pytest_args)."""
    argv = argv or sys.argv
    alluredir = DEFAULT_ALLUREDIR
    label = None
    if "--" in argv:
        sep = argv.index("--")
        before = argv[1:sep]
        pytest_args = argv[sep + 1:]
    else:
        before = argv[1:]
        pytest_args = []
    for arg in before:
        if arg.startswith("--alluredir="):
            alluredir = arg.split("=", 1)[1].strip()
        elif arg.startswith("--label="):
            label = arg.split("=", 1)[1].strip()
    return alluredir, label, pytest_args


def run_pytest(pytest_args=None, alluredir=None):
    alluredir = alluredir or DEFAULT_ALLUREDIR
    cmd = [
        sys.executable, "-m", "pytest",
        "-v", "--tb=short",
        f"--alluredir={alluredir}", "--clean-alluredir",
    ]
    if pytest_args:
        cmd.extend(pytest_args)
    t0 = time.perf_counter()
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=3600,
    )
    duration = time.perf_counter() - t0
    return result.returncode, result.stdout + result.stderr, duration


def parse_summary(output: str):
    """Из вывода pytest извлечь строку вида 'X passed, Y failed, Z skipped'."""
    passed = re.search(r"(\d+)\s+passed", output)
    failed = re.search(r"(\d+)\s+failed", output)
    skipped = re.search(r"(\d+)\s+skipped", output)
    parts = []
    if passed:
        parts.append(f"{passed.group(1)} passed")
    if failed:
        parts.append(f"{failed.group(1)} failed")
    if skipped:
        parts.append(f"{skipped.group(1)} skipped")
    if parts:
        return ", ".join(parts)
    return "Прогон завершён"


def parse_counts(output: str):
    """(passed, failed, skipped)."""
    p = int(m.group(1)) if (m := re.search(r"(\d+)\s+passed", output)) else 0
    f = int(m.group(1)) if (m := re.search(r"(\d+)\s+failed", output)) else 0
    s = int(m.group(1)) if (m := re.search(r"(\d+)\s+skipped", output)) else 0
    return p, f, s


def main():
    alluredir, label, pytest_args = _parse_script_args()
    exit_code, output, duration = run_pytest(pytest_args, alluredir=alluredir)
    summary = parse_summary(output)
    report_hint = f"allure serve {alluredir}"
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        sys.path.insert(0, str(PROJECT_ROOT))
        passed, failed, skipped = parse_counts(output)
        total = passed + failed + skipped
        project_name = f"Premier Tests · {label}" if label else "Premier Tests"
        # Та же «красивая» карточка с круговым прогрессом, что и в run_diploma_runs
        if label and total > 0:
            from scripts.telegram_notify import send_telegram_rich
            send_telegram_rich(
                environment=label,
                duration_sec=duration,
                total=total,
                passed=passed,
                failed=failed,
                skipped=skipped,
                report_link=report_hint,
                project_name=project_name,
            )
        else:
            from scripts.telegram_notify import send_telegram
            status = "OK" if exit_code == 0 else "FAILED"
            send_telegram(f"{project_name}\n\n{summary}\n\nStatus: {status}\n\n{report_hint}")
    else:
        print("TELEGRAM_* не заданы — уведомление не отправляется.")
    print(output)
    print(f"\n--- Отчёт: {report_hint}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
