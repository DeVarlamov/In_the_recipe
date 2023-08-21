import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-#muy!1d6ix0wc%%++s6b6)un3s8+a)mm@9&0pmrv3y0%y-ww07'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig',
    'api.apps.ApiConfig',
    'colorfield',
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

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}


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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.User'

STATIC_URL = '/static/'
STATIC_ROOT = '/static/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserRegistrationSerializer',
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
}

# ------------------------------------------------------------------------------
#                             Постоянные константы
# ------------------------------------------------------------------------------
CHARACTER_LENGTH = 150
MAXIMUM_LENGTH = 200
LENGTH_FOR_MAIL = 254
LENGTH_FOR_COLOR = 7
MINIMUM_TIME = int(1)

INGREDIENT_UNITS = (
    ('г', 'граммы'),
    ('стакан', 'стакан'),
    ('по вкусу', 'по вкусу'),
    ('ст. л.', 'столовая ложка'),
    ('шт.', 'штука'),
    ('мл', 'миллилитры'),
    ('кг', 'килограммы'),
    ('л', 'литры'),
    ('ч. л.', 'чайная ложка'),
    ('банка', 'банка'),
    ('пакетик', 'пакетик'),
    ('пучок', 'пучок'),
    ('лист', 'лист'),
    ('зубчик', 'зубчик'),
    ('бутылка', 'бутылка'),
    ('пакет', 'пакет'),
    ('головка', 'головка'),
    ('корень', 'корень'),
    ('брусок', 'брусок'),
    ('кусочек', 'кусочек'),
    ('щепотка', 'щепотка'),
    ('брусочек', 'брусочек'),
    ('долька', 'долька'),
    ('чашка', 'чашка'),
    ('стебель', 'стебель'),
    ('пластинка', 'пластинка'),
    ('крошка', 'крошка'),
    ('кисточка', 'кисточка')
)
