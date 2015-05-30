import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

INSTALLED_APPS = [
    'tests',
    'djublog',

    'django.contrib.auth',
    'django.contrib.contenttypes',
]

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = 'tests.urls'

SECRET_KEY = 'fake-key'

USE_TZ = True
