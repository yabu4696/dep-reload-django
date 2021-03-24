#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python3 manage.py flush --no-input
python3 manage.py showmigrations
python3 manage.py makemigrations
python3 manage.py migrate 
python3 manage.py showmigrations
# DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
# DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
# DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
# python3 manage.py createsuperuser --noinput
cd ca_camera
ls -l
cd migrations
ls -l
cd /workspace

gunicorn config.wsgi --bind=0.0.0.0:8800 -D
celery -A config worker --pool=solo -B -l info
exec "$@"