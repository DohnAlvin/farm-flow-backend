"""
Django settings for core project.
Modified for Farm Management System with JWT, Custom Auth, and Google Social Auth.
"""

import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# 🔒 Load environment variables from your .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔒 Now pulls from .env (and defaults to a dummy key just in case)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dummy-key-do-not-use-in-prod')

# 🔒 Debug is True locally, but False in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 🌐 Allow traffic from your local network and your future hosted domain
ALLOWED_HOSTS = ['*'] # We will lock this down to just your frontend URL later!

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Required for Social Auth

    # Third Party Apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Social Auth & Registration
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # Google Provider

    # Internal Apps
    'users',
    'farm_api',
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ☁️ Added WhiteNoise to serve CSS/JS in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

# ☁️ SMART DATABASE CONFIGURATION
# It uses SQLite locally, but automatically uses PostgreSQL on Render/Railway
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ☁️ STATIC FILES FOR PRODUCTION
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Where WhiteNoise collects files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CUSTOM FARM SYSTEM CONFIGURATIONS ---

# 🛡️ CORS SECURITY FIX
CORS_ALLOW_ALL_ORIGINS = False 
CORS_ALLOW_CREDENTIALS = True  # 🚨 Added this! Crucial for authentication/JWTs
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://farm-flow-frontend-five.vercel.app",  
    "https://farm-flow-frontend-au41c7pde-dohnalvins-projects.vercel.app", # 🚨 The specific Vercel URL!
]

# Tell Django to trust Vercel for form submissions (CSRF)
CSRF_TRUSTED_ORIGINS = [
    "https://farm-flow-frontend-five.vercel.app",
    "https://farm-flow-frontend-au41c7pde-dohnalvins-projects.vercel.app", # 🚨 Added here too!
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrPhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'VERIFIED_EMAIL': True,
    }
}

# --- ALLAUTH UPDATED SETTINGS ---
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 🚨 Explicitly tell allauth to login via email
ACCOUNT_USERNAME_REQUIRED = False        # 🚨 Tell allauth to stop asking for a username

# --- THE FIX FOR THE CUSTOM USER MODEL ---
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# Tell dj-rest-auth to use SimpleJWT instead of basic tokens
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'farm-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'farm-refresh',
}

REST_USE_JWT = True
# 🚨 CRITICAL FOR VERCEL + RENDER COOKIE SHARING
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True