from .common import *
import os
# change all of settings in here for deployment

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['dramoir.com', 'www.dramoir.com', '91.151.90.30', 'localhost']
CSRF_TRUSTED_ORIGINS = ['dramoir.com', 'www.dramoir.com', '91.151.90.30', 'localhost']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'movies_series'),
        'USER': os.environ.get('DB_USER', 'your_db_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_db_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
