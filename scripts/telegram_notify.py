"""
Отправка результата прогона тестов в Telegram.
Токен и chat_id берутся из переменных окружения или из файла .env в корне проекта.
Использование:
  # Заполните .env (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) или export переменные
  python scripts/telegram_notify.py "5 passed, 2 failed in 120s"
  # Rich-формат как в Okko (из скриптов run_diploma_runs / run_tests_and_notify)
"""
import io
import os
import sys

# Загрузить .env из корня проекта (родитель каталога scripts/)
try:
    from pathlib import Path
    _root = Path(__file__).resolve().parent.parent
    _env = _root / ".env"
    if _env.exists():
        from dotenv import load_dotenv
        load_dotenv(_env)
except Exception:
    pass


def _format_duration(seconds: float) -> str:
    """Формат 00:02:06.289"""
    m = int(seconds // 60)
    s = seconds % 60
    return f"00:{m:02d}:{s:06.3f}"


def make_progress_image(passed: int, total: int, size: int = 200, project_name: str = "Premier Tests") -> bytes | None:
    """Белая карточка как в референсе: название проекта, донат-чарт (светло-зелёный + тонкий серый сегмент), число, квадратик + «X passed»."""
    if total <= 0:
        total = 1
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    try:
        card_radius = 16
        pad = 20
        title_h = 36
        circle_size = 140
        badge_width = 100
        # Вся карточка: белый фон, заголовок + блок (круг + бейдж)
        total_width = pad * 2 + circle_size + 12 + badge_width
        total_height = pad * 2 + title_h + 12 + circle_size
        card_bg = (255, 255, 255)
        img = Image.new("RGB", (total_width, total_height), card_bg)
        draw = ImageDraw.Draw(img)
        try:
            draw.rounded_rectangle((0, 0, total_width - 1, total_height - 1), radius=card_radius, fill=card_bg)
        except TypeError:
            draw.rectangle((0, 0, total_width - 1, total_height - 1), fill=card_bg)

        # Заголовок карточки — название проекта, тёмный текст на белом
        font_title = None
        for path in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            try:
                font_title = ImageFont.truetype(path, 18)
                break
            except OSError:
                continue
        if font_title is None:
            font_title = ImageFont.load_default()
        title_color = (40, 40, 43)
        draw.text((pad, pad), project_name, fill=title_color, font=font_title)

        # Блок с чартом: круг (донат) + справа квадратик и «X passed»
        chart_y0 = pad + title_h + 12
        box = [pad, chart_y0, pad + circle_size, chart_y0 + circle_size]
        light_green = (200, 230, 201)
        gray_segment = (240, 240, 240)
        # Донат: почти весь круг светло-зелёный, тонкий сегмент сверху — серый
        draw.ellipse(box, fill=light_green)
        if passed < total:
            gap_angle = 360 * (1 - passed / total)
            draw.pieslice(box, start=-90, end=-90 + gap_angle, fill=gray_segment)
        # Число в центре круга
        font_big = None
        for path in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            try:
                font_big = ImageFont.truetype(path, 52)
                break
            except OSError:
                continue
        if font_big is None:
            font_big = ImageFont.load_default()
        num_text = str(passed)
        try:
            bbox = draw.textbbox((0, 0), num_text, font=font_big)
        except AttributeError:
            bbox = (0, 0, len(num_text) * 12, 24)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        cx = pad + circle_size // 2
        cy = chart_y0 + circle_size // 2
        draw.text((cx - tw // 2, cy - th // 2 - 2), num_text, fill=(40, 40, 43), font=font_big)

        # Справа: маленький светло-зелёный квадрат + текст «X passed»
        sq_x = pad + circle_size + 12
        sq_y = chart_y0 + (circle_size - 28) // 2
        square_color = (200, 230, 201)
        draw.rectangle((sq_x, sq_y, sq_x + 20, sq_y + 20), fill=square_color)
        passed_text = f"{passed} passed"
        font_small = None
        for path in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            try:
                font_small = ImageFont.truetype(path, 20)
                break
            except OSError:
                continue
        if font_small is None:
            font_small = ImageFont.load_default()
        try:
            tb = draw.textbbox((0, 0), passed_text, font=font_small)
        except AttributeError:
            tb = (0, 0, len(passed_text) * 8, 18)
        tw2 = tb[2] - tb[0]
        th2 = tb[3] - tb[1]
        draw.text((sq_x + 20 + 6, sq_y + (20 - th2) // 2), passed_text, fill=(40, 40, 43), font=font_small)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return None


def send_telegram(text: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID не заданы. Уведомление не отправлено.")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    verify_ssl = os.getenv("SSL_CERTIFICATE_VERIFY", "1") != "0"
    try:
        import requests
        r = requests.post(
            url,
            data={"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
            timeout=10,
            verify=verify_ssl,
        )
        if r.status_code != 200:
            print(f"Ошибка Telegram API: {r.status_code} {r.reason}")
            return False
        return True
    except requests.exceptions.SSLError as e:
        print(f"Ошибка SSL. Попробуйте: export SSL_CERTIFICATE_VERIFY=0 (только для доверенной сети)")
        print(f"Подробнее: {e}")
        return False
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


def send_telegram_rich(
    *,
    environment: str,
    duration_sec: float,
    total: int,
    passed: int,
    failed: int = 0,
    skipped: int = 0,
    report_link: str,
    project_name: str = "Premier Tests",
    comment: str | None = None,
) -> bool:
    """
    Отправка уведомления в стиле Okko: картинка с круговым прогрессом + блок Results
    (Environment, Duration, Total scenarios, Total passed %, ссылка на отчёт).
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID не заданы. Уведомление не отправлено.")
        return False
    verify_ssl = os.getenv("SSL_CERTIFICATE_VERIFY", "1") != "0"
    pct = (100 * passed / total) if total else 0
    duration_str = _format_duration(duration_sec)
    lines = [
        f"<b>Results:</b>",
        f"<b>Environment:</b> {environment}",
    ]
    if comment:
        lines.append(f"<b>Comment:</b> {comment}")
    report_line = f'<a href="{report_link}">Report</a>' if report_link.startswith("http") else report_link
    lines.extend([
        f"<b>Duration:</b> {duration_str}",
        f"<b>Total scenarios:</b> {total}",
        f"<b>Total passed:</b> {passed} ({pct:.0f} %)",
        f"<b>Report available at the link:</b>",
        report_line,
    ])
    caption = f"<b>{project_name}</b>\n\n" + "\n".join(lines)
    if len(caption) > 1024:
        caption = caption[:1020] + "..."

    try:
        import requests
        progress_png = make_progress_image(passed, total, project_name=project_name)
        if not progress_png:
            print("Подсказка: для картинки с круговым прогрессом установите Pillow: pip install Pillow")
        if progress_png:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            r = requests.post(
                url,
                data={"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"},
                files={"photo": ("progress.png", progress_png, "image/png")},
                timeout=15,
                verify=verify_ssl,
            )
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            r = requests.post(
                url,
                data={
                    "chat_id": chat_id,
                    "text": caption,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=10,
                verify=verify_ssl,
            )
        if r.status_code != 200:
            print(f"Ошибка Telegram API: {r.status_code} {r.reason}")
            return False
        return True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


def main():
    if len(sys.argv) > 1:
        summary = "\n".join(sys.argv[1:]).replace("\\n", "\n")
    else:
        summary = "Прогон тестов завершён (итог не передан)."
    title = "Premier Tests"
    text = f"{title}\n\n{summary}"
    ok = send_telegram(text)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
