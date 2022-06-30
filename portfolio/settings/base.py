import os
import logging.config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_cleanup.apps.CleanupConfig',
    'storages',
    'student.apps.StudentConfig',
    'teacher.apps.TeacherConfig',
    'authentication.apps.AuthenticationConfig',
    'preview.apps.PreviewConfig',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'authentication.PortfolioUser'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = 'logoutUser'
LOGOUT_REDIRECT_URL = '/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'preview/static/'),
    os.path.join(BASE_DIR, 'authentication/static/'),
    os.path.join(BASE_DIR, 'student/static/'),
    os.path.join(BASE_DIR, 'teacher/static/'),
    os.path.join(BASE_DIR, 'static/'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.microsoft.MicrosoftOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '649627438525-pfmf65to8338qmvaeo4gre3mhasgf5at.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['GOOGLE_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]

SOCIAL_AUTH_MICROSOFT_GRAPH_KEY = '18c3c49f-bef0-495b-81bd-e0390698acf8'
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET = os.environ['AZURE_SECRET']

SOCIAL_AUTH_UUID_LENGTH = 3

# Logging Configuration

# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console',],
        },
    },
})