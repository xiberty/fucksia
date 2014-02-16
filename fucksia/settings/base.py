# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

location = lambda x: os.path.realpath(os.path.join(BASE_DIR, x))

ROOT_PATH = location('')
LOG_ROOT = location('../var/log')

SECRET_KEY = 'o33*3kj%q7mhijj@b57n8zuss(zt1!d7_vau%e!%2rmv%y^h1#'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',

    "compressor",
    'mobility',
    'crispy_forms',
    'django_nose',
    'django_extensions',
    'south',
    'gravatar',

    'fucksia.core',
    'fucksia.accounts',
    'fucksia.maker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fucksia.urls'

WSGI_APPLICATION = 'fucksia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': location('var/db/database.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish')
)

TIME_ZONE = 'America/La_Paz'

# Internacionalización
USE_I18N = True

# Localización
USE_L10N = True

LOCALE_PATHS = (
    location('fucksia/locales'),
)

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = location('public/static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = location('public/media/')

COMPRESS_ENABLED = False
COMPRESS_OUTPUT_DIR = ''

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

STATICFILES_DIRS = (
    location('fucksia/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_DIRS = (
    location('fucksia/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    #'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'fucksia.core.context_processors.website',
    'fucksia.core.context_processors.debug'
)

WEBSITE_NAME = 'Startup Django'
WEBSITE_DESCRIPTION = 'An easy to use start project for Django'
WEBSITE_AUTHOR = 'Victor Aguilar'
WEBSITE_BASE_URL = 'http://localhost:8000'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'accounts.User'