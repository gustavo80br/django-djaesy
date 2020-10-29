#
# Example of settings_[env].py file
#
# Customize this file as you need
#
# Create a settings_dev.py file for development settings
# Create a settings_staging.py for staging settings
# Create a settings_production.py for production settings
#
# To select which settings to use, create a file called __[env]__.py
#
#   __dev__.py -> Development environment, will use settings_dev.py
#   __staging__.py -> Staging environment, will use settings_stating.py
#   __production__.py -> Production environment, will use settings_production.py
#
# In the last line of the settings.py file, import django_env_settings, like this:
#
#   >> from django_env_settings import *
#
# Have fun!
#

import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Environment Allowed Hosts
ALLOWED_HOSTS = ['djaesy.ddns.net', '172.32.255.99']

# Environment Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

LOCALE_PATHS = [
    '/code/djaesy/translations',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'djaesy',
        'USER': 'dbuser',
        'PASSWORD': 'dbpass',
        'HOST': 'postgres_djaesy',
        'PORT': '5432',
    },
}

MONGO_DATABASES = {
    'mongoi3t': {
        'host': '172.20.0.50',
        'port': 27017,
        'database': 'djaesy',
        'user': 'djaesyapis',
        'password': 'HDwege4s3duNSFD3'
    }
}

STATIC_ROOT = '/static'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = '/static_media'
MEDIA_URL = '/media/'

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/logs/django-debug.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_FROM = 'i3Track <contato@djaesy.com.br>'
EMAIL_BASE_URL = 'http://djaesy.ddns.net'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# Add any other settings.py variable below this line, will override the default value in settings.py