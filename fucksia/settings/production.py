# -*- encoding; utf-8 -*-
from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

ADMINS = (
    ('admin', 'admin@example.com'),
)

COMPRESS_ENABLED = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

RAVEN_CONFIG = {
    'dsn': 'http://8033bd8732d541848a126d42da951ae3:a3f567381ab04a2799dd68251d3cb8ba@sentry.example.com:9000/1',
}

# Host and domains -------------------------------------------------------------

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Sessions ---------------------------------------------------------------------

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

try:
    from .local import *
except ImportError:
    pass