from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-tl=)s2b@0&(+^s!2rni9iqxs@@p68et4&_@f7v+-_ll5&$1sm+'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'movies_series',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
BASE_URL = "http://127.0.0.1:8000"
