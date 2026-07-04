#!/bin/sh
echo "Ejecutando migraciones"

uv run alembic upgrade head

echo "Migraciones ejecutadas. Iniciando API."

uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT