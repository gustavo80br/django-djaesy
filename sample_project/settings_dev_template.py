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

# SECURITY WARNING: don't run with debug turned on in production!
import os

DEBUG = True

# Environment Allowed Hosts
ALLOWED_HOSTS = ['*']

# Environment Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if os.name == 'nt':
    pg_local = 'localhost'
    mongo_local = 'localhost'
    mongo_staging = 'djaesy.ddns.net'
else:
    pg_local = 'postgres_djaesy'
    mongo_local = 'mongo_i3t'
    mongo_staging = 'djaesy.ddns.net'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'djaesy',
        'USER': 'postgres',
        'PASSWORD': 'dbpass',
        'HOST': pg_local,
        'PORT': '5432',
    },
}

MONGO_DATABASES = {
    # 'mongoi3t': {
    #     'host': mongo_local,
    #     'port': 27017,
    #     'database': 'djaesy',
    #     'user': 'djaesyapis',
    #     'password': '123quatro'
    # },
    'mongoi3t': {
        'host': mongo_staging,
        'port': 27017,
        'database': 'djaesy',
        'user': 'djaesyapis',
        'password': 'HDwege4s3duNSFD3'
    }
}

if os.name == 'nt':
    OSGEO4W = r"D:\Dev\virtualenvs\djaesy\Lib\site-packages\osgeo"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\data\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\data\proj"
    os.environ['PATH'] = OSGEO4W + r";" + os.environ['PATH']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/logs/django-debug.log',
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #.console.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_FROM = 'i3Track <contato@djaesy.com.br>'
EMAIL_BASE_URL = 'http://localhost:8000'

# Add any other settings.py variable below this line, will override the default value in settings.py
