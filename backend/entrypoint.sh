#!/bin/sh
echo "Ejecutando migraciones"

alembic upgrade head

echo "Migraciones ejecutadas. Iniciando API."

uvicorn app.main:app --host 0.0.0.0 --port $PORT