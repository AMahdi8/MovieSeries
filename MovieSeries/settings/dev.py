from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-tl=)s2b@0&(+^s!2rni9iqxs@@p68et4&_@f7v+-_ll5&$1sm+'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'movie_series',
    }
}
