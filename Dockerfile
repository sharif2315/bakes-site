# ----------- Stage 1: Node Build -----------
FROM node:20-slim AS frontend-builder

WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./
RUN npm install

# Copy all frontend files and build
COPY . .
RUN npm run build


# ----------- Stage 2: Python Runtime -----------
FROM python:3.12-slim-bookworm

# Add wagtail user
RUN useradd wagtail

WORKDIR /app
EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install Python dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Copy Django project files
COPY --chown=wagtail:wagtail . .

# Copy built frontend assets from Node stage
COPY --from=frontend-builder /app/assets /app/static/dist

# Collect static files
RUN python manage.py collectstatic --noinput

USER wagtail


CMD set -xe; python manage.py migrate --noinput; gunicorn core.wsgi:application
