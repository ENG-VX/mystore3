import os

from .common import *

DEBUG = True

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-development-only',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mystore3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    }
}