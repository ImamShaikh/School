"""
Django settings for govind project.
Render-ready: PostgreSQL + WhiteNoise + env-based secrets.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# ---------------------------------------------------------------------------
# BASE DIR
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# CORE SETTINGS  (all sensitive values read from environment variables)
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-6qx3hmpk4j*or4m(t$p%1^*l3*(s4a-ljnp#h$eo)ko%t-b9i0'  # fallback for dev only
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    '127.0.0.1,localhost'
).split(',')

# Trust Render's reverse proxy for HTTPS redirects
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://127.0.0.1:8000,http://localhost:8000'
).split(',')


# ---------------------------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',            # Cloudinary SDK
    'cloudinary_storage',   # Django storage backend — must come BEFORE staticfiles
    'school',
    'Appadmin',
]


# ---------------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # must be right after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ---------------------------------------------------------------------------
# URLS / WSGI
# ---------------------------------------------------------------------------
ROOT_URLCONF = 'govind.urls'
WSGI_APPLICATION = 'govind.wsgi.application'


# ---------------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ---------------------------------------------------------------------------
# DATABASE  — PostgreSQL via DATABASE_URL (Render injects this automatically)
# Falls back to local SQLite when DATABASE_URL is not set (useful for quick
# local testing without PostgreSQL installed).
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production / Render:  DATABASE_URL is set automatically
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,        # persistent connections (seconds)
            conn_health_checks=True,
            ssl_require=True,        # Render PostgreSQL requires SSL
        )
    }
else:
    # Local development fallback — keep your MySQL connection here so
    # running locally still works without any extra setup.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME':     os.environ.get('DB_NAME',     'govindschool'),
            'HOST':     os.environ.get('DB_HOST',     'localhost'),
            'USER':     os.environ.get('DB_USER',     'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'Imam@123'),
            'PORT':     os.environ.get('DB_PORT',     '3306'),
        }
    }


# ---------------------------------------------------------------------------
# PASSWORD VALIDATORS
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# INTERNATIONALISATION
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# STATIC FILES  (WhiteNoise serves them on Render — unchanged)
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ---------------------------------------------------------------------------
# CLOUDINARY  —  Persistent media storage (images survive Render restarts)
# ---------------------------------------------------------------------------
# Read CLOUDINARY_URL from the environment (Render dashboard / local .env).
# Format:  cloudinary://API_KEY:API_SECRET@CLOUD_NAME
# NEVER hardcode credentials here.
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')

if CLOUDINARY_URL:
    import cloudinary
    cloudinary.config(
        cloudinary_url=CLOUDINARY_URL,
        secure=True,   # Always deliver images over HTTPS
    )
    _MEDIA_BACKEND = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Fallback: local filesystem.
    # Uploads will be lost on Render restart — set CLOUDINARY_URL to fix this.
    import warnings
    warnings.warn(
        "CLOUDINARY_URL is not set. Media uploads will use the local filesystem. "
        "Set CLOUDINARY_URL in your .env (local) or Render Environment Variables (production).",
        stacklevel=2,
    )
    _MEDIA_BACKEND = 'django.core.files.storage.FileSystemStorage'

# WhiteNoise handles STATIC files; Cloudinary handles MEDIA (user uploads).
STORAGES = {
    "default": {
        "BACKEND": _MEDIA_BACKEND,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# MEDIA FILES  (served via Cloudinary CDN in production)
# MEDIA_ROOT / MEDIA_URL are used only for local dev when CLOUDINARY_URL is
# not yet configured.
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django-cloudinary-storage settings
CLOUDINARY_STORAGE = {
    'MEDIA_TAG': 'govind-ashramshala',   # Tags all uploads; useful for Cloudinary filtering
}



# ---------------------------------------------------------------------------
# SECURITY HEADERS  (only enforced when DEBUG=False)
# ---------------------------------------------------------------------------
if DEBUG:
    # Local development
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

else:
    # Production
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'


# ---------------------------------------------------------------------------
# DEFAULT PK
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
