#!/bin/sh

if [ "${SQL_ENGINE}" != "django.db.backends.sqlite3" ]; then
    dbms="${SQL_ENGINE##*.}"
    echo "Waiting for ${dbms}..."

    while ! nc -z "${SQL_HOST}" "${SQL_PORT}"; do
        sleep 0.1
    done

    echo "${dbms} started"
fi

python manage.py migrate

# shellcheck disable=SC2198
if [ -z "${@}" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  python manage.py "${@}"
fi