#!/bin/bash

APP_PORT=${PORT:-8000}

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

/app/server/scripts/migrations.sh

/app/server/scripts/createsuperuser.sh

/app/server/scripts/loaddata.sh

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm server.wsgi:application --bind "0.0.0.0:${APP_PORT}"

