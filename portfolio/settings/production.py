from .base import *
from boto3.session import Session

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DJANGO_DEBUG']

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION_NAME = 'us-west-2'
AWS_STORAGE_BUCKET_NAME = 'showcase-s3-bucket'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'portfolio.storage_backends.StaticStorage'

MEDIA_LOCATION = 'uploads'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'portfolio.storage_backends.PublicMediaStorage'

EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['SES_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SES_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Showcase <noreply@showcaseedu.com>'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        'handlers': ['console'],
    },
    'formatters': {
        'aws': {
            'format': u"%(name)s:%(lineno)-4d %(levelname)-8s %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'watchtower': {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
                     'boto3_session': boto3_session,
                     'log_group': 'Showcase',
                     'stream_name': 'ShowcaseStream',
            'formatter': 'aws',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'aws',
        }
    },
    'loggers': {
        'student': {
            'level': 'INFO',
            'handlers': ['watchtower'],
            'propagate': False,
        },
        'teacher': {
            'level': 'INFO',
            'handlers': ['watchtower'],
            'propagate': False,
        },
        'preview': {
            'level': 'INFO',
            'handlers': ['watchtower'],
            'propagate': False,
        },
        'authentication': {
            'level': 'INFO',
            'handlers': ['watchtower'],
            'propagate': False,
        },
    },
}