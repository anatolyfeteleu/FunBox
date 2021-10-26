from .base import *  # NOQA


# GENERAL
# --------------------------------------------------------------------------------------------------
DEBUG = True

ALLOWED_HOSTS = ['*']

# Celery configuration
# --------------------------------------------------------------------------------------------------
USE_CELERY = False

# Debug toolbar
# --------------------------------------------------------------------------------------------------
INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    '192.168.192.1',
]

# Logging
# --------------------------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'django.db.backends': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'visit.clients': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
