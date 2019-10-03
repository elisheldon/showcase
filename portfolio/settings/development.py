from .base import *

SECRET_KEY = '^cc%7ak(_ee2de6o(-us%#emmf=%0(t+8^%7h8ukvp%ibvg!z!'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}