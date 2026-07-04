FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_NO_DEV=1 \
    ENVIRONMENT=prod 

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

WORKDIR /app

# Dependencias
COPY pyproject.toml uv.lock /app/
RUN uv sync --locked

COPY . .

RUN mkdir -p /app/uploads /app/logs

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE $PORT

CMD ["/app/entrypoint.sh"]