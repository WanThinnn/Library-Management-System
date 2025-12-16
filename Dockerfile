# Build Tailwind assets separately to keep runtime image slim
FROM node:20-alpine AS tailwind-builder
WORKDIR /app/theme/static_src

COPY src/theme/static_src/package*.json ./
RUN npm ci

COPY src/theme/static_src/ ./
RUN npm run build

# Final runtime image
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=LibraryManagementSystem.settings

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

COPY src/ /app/
COPY --from=tailwind-builder /app/theme/static/css/dist /app/theme/static/css/dist

RUN mkdir -p /app/data /app/staticfiles

RUN python manage.py collectstatic --noinput || true

RUN chmod -R 755 /app && \
    chmod -R 777 /app/data

EXPOSE 8000

CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn LibraryManagementSystem.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
