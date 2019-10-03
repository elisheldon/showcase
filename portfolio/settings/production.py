from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DJANGO_DEBUG']

ALLOWED_HOSTS = ['127.0.0.1:8000', 'showcase-env.pb9jd7myyh.us-west-2.elasticbeanstalk.com']

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