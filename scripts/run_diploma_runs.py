"""
Три отдельных прогона для диплома: API, UI, Mobile.
Каждый прогон — свой Allure-отчёт и своё уведомление в Telegram (картинка + ссылка на отчёт).
Использование:
  python scripts/run_diploma_runs.py              # API → UI → Mobile
  python scripts/run_diploma_runs.py --no-notify  # без Telegram, только отчёты
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

_env = PROJECT_ROOT / ".env"
if _env.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env)
    except Exception:
        pass

SUITES = [
    {"alluredir": "allure-results-api", "label": "API", "pytest_args": ["tests/API/", "-v"]},
    {"alluredir": "allure-results-ui", "label": "UI", "pytest_args": ["tests/UI/", "-v", "--headless"]},
    {"alluredir": "allure-results-mobile", "label": "Mobile", "pytest_args": ["tests/mobile/test_main.py", "-v"]},
]


def parse_summary(output: str) -> str:
    parts = []
    for pattern, name in [(r"(\d+)\s+passed", "passed"), (r"(\d+)\s+failed", "failed"), (r"(\d+)\s+skipped", "skipped")]:
        m = re.search(pattern, output)
        if m:
            parts.append(f"{m.group(1)} {name}")
    return ", ".join(parts) if parts else "Прогон завершён"


def parse_counts(output: str) -> tuple[int, int, int]:
    """Возвращает (passed, failed, skipped)."""
    passed = int(m.group(1)) if (m := re.search(r"(\d+)\s+passed", output)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+)\s+failed", output)) else 0
    skipped = int(m.group(1)) if (m := re.search(r"(\d+)\s+skipped", output)) else 0
    return passed, failed, skipped


def run_one_suite(alluredir: str, label: str, pytest_args: list) -> tuple[int, str, float, int, int, int]:
    """Возвращает (exit_code, summary_text, duration_sec, passed, failed, skipped)."""
    cmd = [
        sys.executable, "-m", "pytest",
        "-v", "--tb=short",
        f"--alluredir={alluredir}", "--clean-alluredir",
        *pytest_args,
    ]
    start = time.perf_counter()
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=3600)
    duration = time.perf_counter() - start
    out = result.stdout + result.stderr
    print(out)
    summary = parse_summary(out)
    passed, failed, skipped = parse_counts(out)
    return result.returncode, summary, duration, passed, failed, skipped


def report_link_for_suite(alluredir: str) -> str:
    """Ссылка на отчёт: в Jenkins — URL сборки/allure, локально — команда allure serve."""
    build_url = os.getenv("BUILD_URL")
    if build_url:
        return f"{build_url.rstrip('/')}/allure"
    return f"allure serve {alluredir}"


def send_telegram_rich_suite(
    environment: str,
    alluredir: str,
    duration_sec: float,
    passed: int,
    failed: int,
    skipped: int,
) -> None:
    if not os.getenv("TELEGRAM_BOT_TOKEN") or not os.getenv("TELEGRAM_CHAT_ID"):
        return
    sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.telegram_notify import send_telegram_rich
    total = passed + failed + skipped
    if total == 0:
        total = 1
    comment = os.getenv("TELEGRAM_COMMENT")
    project_name = f"Premier Tests · {environment}"
    send_telegram_rich(
        environment=environment,
        duration_sec=duration_sec,
        total=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        report_link=report_link_for_suite(alluredir),
        project_name=project_name,
        comment=comment,
    )


def main():
    do_notify = "--no-notify" not in sys.argv
    exit_codes = []

    for i, suite in enumerate(SUITES, 1):
        print("\n" + "=" * 60)
        print(f"Прогон {i}: {suite['label']}")
        print("=" * 60)
        code, summary, duration, p, f, s = run_one_suite(
            suite["alluredir"],
            suite["label"],
            suite["pytest_args"],
        )
        exit_codes.append(code)
        if do_notify:
            send_telegram_rich_suite(
                environment=suite["label"],
                alluredir=suite["alluredir"],
                duration_sec=duration,
                passed=p,
                failed=f,
                skipped=s,
            )

    print("\n" + "=" * 60)
    print("Три прогона для диплома завершены")
    print("=" * 60)
    for suite in SUITES:
        print(f"  {suite['label']:8} allure serve {suite['alluredir']}")
    print("=" * 60)

    sys.exit(0 if all(c == 0 for c in exit_codes) else 1)


if __name__ == "__main__":
    main()
