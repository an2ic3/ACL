#!/bin/sh

if [ "${SQL_ENGINE}" != "django.db.backends.sqlite3" ]; then
    dbms="${SQL_ENGINE##*.}"
    echo "Waiting for ${dbms}..."

    while ! nc -z "${SQL_HOST}" "${SQL_PORT}"; do
        sleep 0.1
    done

    # TODO test auth

    echo "${dbms} started"
fi

python manage.py migrate

# shellcheck disable=SC2198
if [ -z "${@}" ]; then
  gunicorn acl.wsgi:application --bind 0.0.0.0:8000
else
  exec "${@}"
fi
