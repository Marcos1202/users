from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST':'localhost',
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIRS = [BASE_DIR.child('static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

#email
#activar envios de mails
EMAIL_USE_TLS = True
#Tipo de correo
EMAIL_HOST = 'smtp.gmail.com'
#correo de backend
EMAIL_HOST_USER = get_secret("E-MAIL")
#password
EMAIL_HOST_PASSWORD = get_secret("E-MAIL_PASS")
#puerto
EMAIL_PORT = 587