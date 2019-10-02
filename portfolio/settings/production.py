from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1:8000', 'showcaseapp.azurewebsites.net']