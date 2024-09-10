FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /skin-system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /app/logs /var/log/nginx

EXPOSE 5050 5000

CMD ["sh", "-c", "nginx -g 'daemon off;' & gunicorn -w 4 -b 127.0.0.1:5000 --access-logfile /app/logs/access.log --error-logfile /app/logs/error.log run:app"]


