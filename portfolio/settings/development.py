from .base import *

SECRET_KEY = '^cc%7ak(_ee2de6o(-us%#emmf=%0(t+8^%7h8ukvp%ibvg!z!'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'

MEDIA_URL = '/uploads/'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(name)s:%(lineno)-4d %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'file',
        },
    },
    'loggers': {
        'student': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
        'teacher': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
        'preview': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
        'authentication': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}