from ._base import *

ALLOWED_HOSTS = list(ENV('ALLOWED_HOSTS'))

DATABASES = {
    'default': {
        'ENGINE': ENV('DB_ENGINE'),
        'NAME': ENV('DB_NAME'),
        'USER': ENV('DB_USER'),
        'PORT': ENV('DB_PORT'),
        'PASSWORD': ENV('DB_PASSWORD'),
    }
}
