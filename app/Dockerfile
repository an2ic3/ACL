FROM python:3.8.3-alpine as builder

# set work directory
WORKDIR /usr/src/app

# install psycopg2 dependencies
RUN apk update \
 && apk add postgresql-dev gcc python3-dev musl-dev zlib-dev build-base openldap-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.8.3-alpine

# app config
ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_PORT=5432
ENV SQL_USER=acl
ENV SQL_DATABASE=acl
ENV ALLOWED_HOSTS='0.0.0.0'
ENV DEBUG=0

# create the app user
RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update \
 && apk add libpq build-base openldap-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

ENTRYPOINT "${APP_HOME}/entrypoint.sh"
EXPOSE 8000

# USER app
# TODO user app has no permission to use unix socket: docker.sock