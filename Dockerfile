FROM python:3.14.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_PYTHON_DOWNLOADS=never
ENV UV_PYTHON=python3.14.3

WORKDIR /skin-system

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /app/logs /var/log/nginx

EXPOSE 5050

CMD ["sh", "-c", "nginx -g 'daemon off;' & uv run uvicorn run:app --workers 4 --host 127.0.0.1 --port 5000 --access-log"]
