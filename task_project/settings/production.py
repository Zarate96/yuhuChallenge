from environs import Env
from .base import *

env = Env()
env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['http://test.hzcode.mx/','test.hzcode.mx','74.208.123.242']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  
    "http://test.fronted.hzcode.mx",
    "http://test.fronted.hzcode.mx/",
]

CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME', default=''),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default=''),
        'PORT': env('DB_PORT', default=''),
    }
}

