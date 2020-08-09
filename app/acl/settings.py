"""
Django settings for acl project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import random

from string import punctuation, digits, ascii_letters


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', repr(''.join([
    random.SystemRandom().choice(ascii_letters + digits + punctuation) for i in range(
        random.randint(45, 50)
    )])
))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1 0.0.0.0').split(' ')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.acl_manager.apps.AclManagerConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.basicauth.BasicAuthMiddleware'
]

ROOT_URLCONF = 'acl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'acl.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = 'static/'

MEDIA_ROOT = os.environ['ACL_FILE_PATH']


APPEND_SLASH = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# LDAP
if os.environ.get('LDAP_URI', False):
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType

    AUTH_LDAP_SERVER_URI = os.environ['LDAP_URI']
    AUTH_LDAP_BIND_DN = os.environ['LDAP_BIND_DN']
    AUTH_LDAP_BIND_PASSWORD = os.environ['LDAP_BIND_PASS']
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        os.environ['LDAP_USERS'],
        ldap.SCOPE_SUBTREE,
        '(uid=%(user)s)',
    )
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        os.environ['LDAP_GROUPS'],
        ldap.SCOPE_SUBTREE,
        '(objectClass=groupOfUniqueNames)',
    )
    AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType(name_attr='cn')

    AUTH_LDAP_REQUIRE_GROUP = os.environ['LDAP_GROUP']

    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        'is_active': os.environ['LDAP_GROUP'],
        'is_staff': os.environ['LDAP_SUPERGROUP'],
        'is_superuser': os.environ['LDAP_SUPERGROUP'],
    }

    AUTH_LDAP_GROUP_CACHE_TIMEOUT = 0
    AUTH_LDAP_CACHE_GROUPS = 0
    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    AUTH_LDAP_FIND_GROUP_PERMS = True
    AUTH_LDAP_CACHE_TIMEOUT = 0

    AUTHENTICATION_BACKENDS += ['django_auth_ldap.backend.LDAPBackend']

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
}


# Custom
SCHEDULE_UPDATE_TIME = os.environ.get('SCHEDULE_UPDATE_TIME', 15)  # in Minutes
PROXY_CONTAINER = os.environ.get('PROXY_CONTAINER', 'main_nginx_1')
