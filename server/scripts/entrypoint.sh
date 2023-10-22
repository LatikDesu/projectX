#!/bin/bash

APP_HOST=${HOST:-0.0.0.0}
APP_PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/app/server/logging.ini}

export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
export APP_MODULE=${APP_MODULE:-"server.wsgi:application"}

sleep 10

# Проверяем, были ли миграции выполнены
if [ ! -f /app/server/scripts/migrations_done ]; then
    /app/server/scripts/migrations.sh
    touch /app/server/scripts/migrations_done
fi

# Проверяем, был ли createsuperuser выполнен
if [ ! -f /app/server/scripts/createsuperuser_done ]; then
    /app/server/scripts/createsuperuser.sh
    touch /app/server/scripts/createsuperuser_done
fi

# Проверяем, было ли loaddata выполнено
if [ ! -f /app/server/scripts/loaddata_done ]; then
    /app/server/scripts/loaddata.sh
    touch /app/server/scripts/loaddata_done
fi

/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm --bind "${APP_HOST}:${APP_PORT}" --log-config $LOG_CONFIG "$APP_MODULE"
