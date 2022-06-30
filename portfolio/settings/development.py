from .base import *
from boto3.session import Session
from django.db.backends.oracle.base import DatabaseOperations
DatabaseOperations.max_name_length = lambda s: 120 # Without this, Django attempts to query truncated table names within the Oracle DB 

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': os.environ['ORACLE_NAME'],
        'USER': os.environ['ORACLE_USERNAME'],
        'PASSWORD': os.environ['ORACLE_PASSWORD'],
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

boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)