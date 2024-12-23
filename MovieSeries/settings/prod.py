from .common import *
# change all of settings in here for deployment

DEBUG = True

SECRET_KEY = os.environ('SECRET_KEY')

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
