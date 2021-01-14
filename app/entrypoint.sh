#!/bin/sh

# check if required environment variables exist:
# shellcheck disable=SC2153
if [ -z "${SQL_HOST}" ]; then
  echo "You need to specify SQL_HOST"
  exit 1
fi

# set environment variables for database configuration (engine / port)
case ${DBMS} in
"mariadb")
  export SQL_ENGINE=django.db.backends.mysql
  export SQL_PORT=3306
  ;;
"postgres")
  export SQL_ENGINE=django.db.backends.postgres
  export SQL_PORT=5432
  ;;
"sqlite3")
  export SQL_ENGINE=django.db.backends.sqlite3
  ;;
*)
  echo "Error DBMS=${DBMS} is undefined!"
  exit 1
  ;;
esac

# wait for database
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
  if [ "${DEBUG}" != 0 ]; then
    gunicorn acl.wsgi:application --bind 0.0.0.0:8000 --log-level DEBUG
  else
    gunicorn acl.wsgi:application --bind 0.0.0.0:8000
  fi
else
  exec "${@}"
fi
