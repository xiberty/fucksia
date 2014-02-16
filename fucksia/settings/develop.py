# -*- encoding: utf-8 -*-
from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

# Email ------------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST, EMAIL_PORT = '127.0.0.1', 1025  # Work with maildump
DEFAULT_FROM_EMAIL = 'admin@xiberty.com'

INSTALLED_APPS += (
    # 'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PANELS = (
    # 'debug_toolbar.panels.version.VersionDebugPanel',
    # 'debug_toolbar.panels.timer.TimerDebugPanel',
    # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    # 'debug_toolbar.panels.headers.HeaderDebugPanel',
    # 'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    # 'debug_toolbar.panels.template.TemplateDebugPanel',
    # 'debug_toolbar.panels.sql.SQLDebugPanel',
)


def custom_show_toolbar(request):
    if request.path.startswith('/admin'):
        return False
    return True


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': True,
    'TAG': 'div',
    'ENABLE_STACKTRACES': True
}

try:
    from .local import *
except ImportError:
    pass