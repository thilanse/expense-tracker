#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn expense_tracker.wsgi:application --bind 0.0.0.0:8000