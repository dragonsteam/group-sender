import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()


def get_env(var_name, required=False):
    value = os.getenv(var_name)

    if required and not value:
        raise ImproperlyConfigured(f"The {var_name} environment variable is not set!")
    
    return value


BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = []
# SITE_ID = 1

SECRET_KEY                    = get_env('SECRET_KEY', required=True)
TELEGRAM_BOT_TOKEN            = get_env('TELEGRAM_BOT_TOKEN', required=True)
TELEGRAM_WEBHOOK_URL          = get_env('TELEGRAM_WEBHOOK_URL', required=True)
TELEGRAM_WEBHOOK_SECRET_TOKEN = get_env('TELEGRAM_WEBHOOK_SECRET_TOKEN', required=True)
TELEGRAM_API_ID               = get_env('TELEGRAM_API_ID', required=True)
TELEGRAM_API_HASH             = get_env('TELEGRAM_API_HASH', required=True)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    # 'rest_framework_simplejwt',
    # 'phonenumber_field',
    # apps
    'bot',
]

# AUTHENTICATION_BACKENDS = (
#     # Needed to login by username in Django admin, regardless of `allauth`
#     "django.contrib.auth.backends.ModelBackend",
#     # `allauth` specific authentication methods, such as login by e-mail
#     # "allauth.account.auth_backends.AuthenticationBackend",
# )

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "allauth.account.middleware.AccountMiddleware",
]

# AUTH_USER_MODEL = "accounts.User"

ROOT_URLCONF = 'tgs.urls'

WSGI_APPLICATION = 'tgs.wsgi.application'
# ASGI_APPLICATION = 'tgs.asgi.application'

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

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PERMISSION_CLASSES": (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.BasicAuthentication",
    ),
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 12,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'