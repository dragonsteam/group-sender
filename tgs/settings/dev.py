from .base import *

DEBUG = True
SESSION_LOGIN = True
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # Allow credentials (cookies, authorization headers, etc.) to be sent with requests
# CORS_ALLOWED_ORIGINS = ['0.0.0.0']
# CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization'] # Allow specific headers in requests

# INSTALLED_APPS = INSTALLED_APPS + [
#     'monitoring',
# ]

STATIC_URL = 'assets/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "public/assets"),
    # os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Database
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    "default": dj_database_url.config(
        # mysql://USER:PASSWORD@HOST:PORT/NAME
        default="postgres://postgres:pwd@db/tgs_db",
        # default=DB_URL,
        conn_max_age=600,
        # conn_health_checks=True,
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60 * 24 * 365),
}