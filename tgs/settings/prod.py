from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", None)
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY is empty, please check environment variables.")

# Database
DATABASES = {
    "default": dj_database_url.config(
        # default=DB_URL,
        default="postgres://postgres:pwd@db/tgs_db",
        conn_max_age=600,
    )
}

# Static files
STATIC_URL = "/assets/"
STATIC_ROOT = os.path.join(BASE_DIR, "public/assets")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# # HTTPS settings
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# # HSTS settings
# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True