# File sets up the django environment, used by other scripts that need to
# execute in django land
import os

import django

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = 'sample_project.settings'

import sys

sys.path += [os.path.join(BASE_DIR, 'sample_project')]


def boot_django():

    # try:
    #     import gdal
    #     gdal_path = Path(gdal.__file__)
    #     OSGEO4W = os.path.join(gdal_path.parent, 'osgeo')
    #     os.environ["OSGEO4W_ROOT"] = OSGEO4W
    #     os.environ["GDAL_DATA"] = os.path.join(OSGEO4W, "data", "gdal")
    #     os.environ["PROJ_LIB"] = os.path.join(OSGEO4W, "data", "proj")
    #     os.environ["PATH"] = OSGEO4W + ";" + os.environ["PATH"]
    #     GEOS_LIBRARY_PATH = str(os.path.join(OSGEO4W, "geos_c.dll"))
    #     GDAL_LIBRARY_PATH = str(os.path.join(OSGEO4W, "gdal301.dll"))
    # except ImportError:
    #     GEOS_LIBRARY_PATH = None
    #     GDAL_LIBRARY_PATH = None

    # settings.configure(
    #
    #     DEBUG=True,
    #     ALLOWED_HOSTS=['*'],
    #     BASE_DIR=BASE_DIR,
    #
    #     DATABASES={
    #         "default": {
    #             "ENGINE": "django.db.backends.sqlite3",
    #             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    #         }
    #     },
    #
    #     INSTALLED_APPS=(
    #
    #         'django.contrib.admin',
    #         'django.contrib.auth',
    #         'django.contrib.contenttypes',
    #         'django.contrib.sessions',
    #         'django.contrib.messages',
    #         'django.contrib.staticfiles',
    #
    #         'rest_framework',
    #         'rest_framework.authtoken',
    #
    #         'dal',
    #         'dal_select2',
    #         'django_filters',
    #         'crispy_forms',
    #         'easy_thumbnails',
    #         'image_cropping',
    #
    #         "djaesy",
    #     ),
    #     TIME_ZONE="UTC",
    #     USE_TZ=True,
    #
    #     # DJAESY_USER_ROLE_CLASS='djaesy.User',
    #     # DJAESY_USER_MENU=True,
    #
    #     # DJAESY_USER_CREATE_LAYOUT = USER_CREATE_EDIT_LAYOUT,
    #     # DJAESY_USER_UPDATE_LAYOUT = USER_CREATE_EDIT_LAYOUT,
    #     # DJAESY_USER_CREATE_FORM = 'accounts.AccountsUserCreationForm',
    #     # DJAESY_USER_UPDATE_FORM = 'accounts.AccountsUserUpdateForm',
    #     # DJAESY_USER_LIST_VIEW = 'accounts.AccountsUserList',
    #     # DJAESY_USER_UPDATE_VIEW = 'accounts.AccountsUserUpdate',
    #     # DJAESY_USER_CREATE_VIEW = 'accounts.AccountsUserCreate',
    #     # DJAESY_USER_ROLE_CLASS = 'accounts.UserProfile'
    #
    #     MIDDLEWARE=[
    #         'django.middleware.security.SecurityMiddleware',
    #         'whitenoise.middleware.WhiteNoiseMiddleware',
    #         'django.contrib.sessions.middleware.SessionMiddleware',
    #         'django.middleware.locale.LocaleMiddleware',
    #         'django.middleware.common.CommonMiddleware',
    #         'django.middleware.csrf.CsrfViewMiddleware',
    #         'django.contrib.auth.middleware.AuthenticationMiddleware',
    #         'django.contrib.messages.middleware.MessageMiddleware',
    #         'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #     ],
    #
    #     ROOT_URLCONF='sample_project.urls',
    #
    #     TEMPLATES=[
    #         {
    #             'BACKEND': 'django.template.backends.django.DjangoTemplates',
    #             'DIRS': [os.path.join(BASE_DIR, 'templates')]
    #             ,
    #             'APP_DIRS': True,
    #             'OPTIONS': {
    #                 'context_processors': [
    #                     'django.template.context_processors.debug',
    #                     'django.template.context_processors.request',
    #                     'django.contrib.auth.context_processors.auth',
    #                     'django.contrib.messages.context_processors.messages',
    #                 ],
    #             },
    #         },
    #     ],
    #
    #     AUTH_PASSWORD_VALIDATORS=[
    #         {
    #             'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    #         },
    #         {
    #             'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #         },
    #         {
    #             'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    #         },
    #         {
    #             'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    #         },
    #     ],
    #
    #     LOGIN_URL='/login',
    #     LOGIN_REDIRECT_URL='/',
    #     LOGOUT_REDIRECT_URL='/',
    #
    #     GEOS_LIBRARY_PATH=GEOS_LIBRARY_PATH,
    #     GDAL_LIBRARY_PATH=GDAL_LIBRARY_PATH
    # )

    django.setup()
