FROM python:3.14-alpine AS build-base

# --- builder: compile uwsgi and install Python deps into a venv ---
FROM build-base AS builder

RUN apk add --no-cache \
    build-base \
    linux-headers \
    python3-dev \
 && pip install --no-cache-dir poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true \
 && poetry install --only main --with prod --no-interaction --no-root

# --- runtime: lean image with venv + app only ---
FROM build-base

RUN apk add --no-cache mailcap \
 && (getent group www-data >/dev/null || addgroup -g 82 -S www-data) \
 && (getent passwd www-data >/dev/null || adduser -u 82 -D -S -G www-data www-data)

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY docker/uwsgi.ini /app/uwsgi.ini
COPY manage.py /app/
COPY docker/ /app/docker
COPY tus/ /app/tus

# default settings are in MemberManagement
ENV DJANGO_SETTINGS_MODULE="tus.docker_settings"

### ALL THE CONFIGURATION

# The secret key used for django
ENV DJANGO_SECRET_KEY=""

# A comma-seperated list of allowed hosts
ENV DJANGO_ALLOWED_HOSTS="localhost"

# Database settings
## Use SQLITE out of the box
ENV DJANGO_DB_ENGINE="django.db.backends.sqlite3"
ENV DJANGO_DB_NAME="/data/db.sqlite3"
ENV DJANGO_DB_USER=""
ENV DJANGO_DB_PASSWORD=""
ENV DJANG_DB_HOST=""
ENV DJANGO_DB_PORT=""

# create data volume, and collect static files
RUN mkdir -p /var/www/static/ /data/ \
 && chown -R www-data:www-data /data/ \
 && DJANGO_SECRET_KEY=setup python manage.py collectstatic --noinput

# Volume and ports
USER www-data:www-data
VOLUME /data/
EXPOSE 8080

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/app/docker/uwsgi.ini"]
