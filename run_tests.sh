#!/usr/bin/env bash
# Запуск тестов Premier (активируйте venv: source .venv/bin/activate)
set -e
cd "$(dirname "$0")"

if [ "$1" = "--api-only" ]; then
  echo "=== Только API-тесты (без браузера) ==="
  pytest tests/API/ -v "${@:2}"
else
  echo "=== Все тесты (API + UI, нужен Chrome). Для только API: $0 --api-only ==="
  pytest -v "$@"
fi
