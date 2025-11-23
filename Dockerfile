# Pull official base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=LibraryManagementSystem.settings

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY src/requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Copy project
COPY src/ /app/

# Create directories for SQLite and static files
RUN mkdir -p /app/data /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Set permissions
RUN chmod -R 755 /app && \
    chmod -R 777 /app/data

# Expose port
EXPOSE 8000

# Run migrations and start gunicorn
CMD python manage.py migrate --noinput && \
    gunicorn LibraryManagementSystem.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
