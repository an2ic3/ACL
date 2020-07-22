ARG DBMS="mariadb"
ARG AUTH="openldap"

FROM python:3.9.0-alpine as builder
ARG DBMS
ARG AUTH

# set work directory
WORKDIR /usr/src/app

RUN apk update \
 && apk add gcc python3-dev musl-dev jpeg-dev zlib-dev

# install database dependencies
RUN if [[ "${DBMS}" == "postgres" ]]; then apk add postgresql-dev; fi
RUN if [[ "${AUTH}" == "openldap" ]]; then apk add build-base openldap-dev; fi

# install dependencies
COPY rqmts/ rqmts
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r rqmts/requirements.txt
RUN if [[ "${DBMS}" == "postgres" ]]; then pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r rqmts/requirements.postgres.txt; fi
RUN if [[ "${DBMS}" == "mariadb" ]]; then pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r rqmts/requirements.mariadb.txt; fi
RUN if [[ "${AUTH}" == "openldap" ]]; then pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r rqmts/requirements.openldap.txt; fi

FROM python:3.9.0-alpine
ARG DBMS
ARG AUTH
ENV DBMS=${DBMS}

# app config
ENV SQL_USER=acl SQL_DATABASE=acl ALLOWED_HOSTS='0.0.0.0' DEBUG=0

# create the app user and directories
ENV HOME=/home/app APP_HOME=/home/app/web
RUN mkdir -p $HOME \
 && mkdir -p $APP_HOME \
 && addgroup -S app \
 && adduser -S app -G app \
 && mkdir -p "${APP_HOME}/app/media"
WORKDIR $APP_HOME

# install dependencies
RUN apk update \
 && apk add libpq

# install database dependencies
RUN if [[ "${DBMS}" == "postgres" ]]; then apk add postgresql-dev; fi
RUN if [[ "${AUTH}" == "openldap" ]]; then apk add build-base openldap-dev; fi

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

ENTRYPOINT "${APP_HOME}/entrypoint.sh"
EXPOSE 8000
USER app
