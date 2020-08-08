FROM python:3.8.3-alpine AS compile-image

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_PORT=5432
ENV SQL_USER=acl
ENV SQL_DATABASE=acl
ENV ALLOWED_HOSTS='0.0.0.0'
ENV DEBUG=0

# install psycopg2 dependencies
RUN apk update \
 && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev build-base openldap-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --user -r requirements.txt


FROM python:3.8.3-alpine AS build-image

COPY --from=compile-image /root/.local /root/.local

# copy project
COPY . .

EXPOSE 8000
ENV PATH=/root/.local/bin:$PATH
ENTRYPOINT '/usr/src/app/entrypoint.sh'

# TODO use gunicorn
CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000', '--insecure']
