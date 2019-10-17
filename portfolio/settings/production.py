from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DJANGO_DEBUG']

ALLOWED_HOSTS = ['127.0.0.1', 'showcase-env.pb9jd7myyh.us-west-2.elasticbeanstalk.com', 'www.showcaseedu.com', 'showcaseedu.com', '192.168.1.15', 'localhost']

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
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-us-west-2-315679056419'
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