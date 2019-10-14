from .base import *

SECRET_KEY = '^cc%7ak(_ee2de6o(-us%#emmf=%0(t+8^%7h8ukvp%ibvg!z!'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/uploads/'

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.15', 'localhost',]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')