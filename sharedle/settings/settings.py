from .base_settings import *

SECRET_KEY = 'this is not the secret key, use your own'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
