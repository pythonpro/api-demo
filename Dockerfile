FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/python", "backend/manage.py", "runserver", "0.0.0.0:8000"]