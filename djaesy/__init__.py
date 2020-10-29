from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from djaesy.layouts import USER_CREATE_EDIT_LAYOUT


settings.DJAESY_PAGE_TITLE_PREFIX = 'DJAESY | '
settings.DJAESY_PAGE_TITLE_SUFFIX = ''

required_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.contenttypes',
    'rest_framework',
    'rest_framework.authtoken',
    # 'django_cleanup.apps.CleanupConfig',
    'crispy_forms',
    'dal',
    'dal_select2',
    'leaflet',
    'django_filters',
    'easy_thumbnails',
    'image_cropping',
]

for app in required_apps:
    if not app in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.append(app)

settings.DJAESY_USER_MENU = getattr(settings, 'DJAESY_USER_MENU', True)

settings.DJAESY_USER_CREATE_FORM = getattr(settings, 'DJAESY_USER_CREATE_FORM', 'djaesy.UserCreationForm')
settings.DJAESY_USER_UPDATE_FORM = getattr(settings, 'DJAESY_USER_UPDATE_FORM', 'djaesy.UserUpdateForm')
settings.DJAESY_USER_CREATE_LAYOUT = getattr(settings, 'DJAESY_USER_CREATE_LAYOUT', USER_CREATE_EDIT_LAYOUT)
settings.DJAESY_USER_UPDATE_LAYOUT = getattr(settings, 'DJAESY_USER_UPDATE_LAYOUT', USER_CREATE_EDIT_LAYOUT)

settings.DJAESY_WEBPACK_FOLDER = getattr(settings, 'DJAESY_WEBPACK_FOLDER', 'webpack')

# settings.CITIES_LOCALES = ['pt-br',]
# settings.CITIES_POSTAL_CODES = ['BR',]

settings.CRISPY_TEMPLATE_PACK = 'bootstrap4'
settings.MENU_SELECT_PARENTS = True

settings.MIDDLEWARE += (
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'djaesy.middleware.ChangePassword',
    # 'djaesy.middleware.UrlRouter'
)

settings.X_FRAME_OPTIONS = 'SAMEORIGIN'

settings.DJAESY_PERMISSIONS = 'djaesy.permissions'
settings.AUTH_USER_MODEL = 'djaesy.User'
settings.STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

settings.DJAESY_USER_TYPES = getattr(
    settings,
    'DJAESY_USER_TYPES', (
        ('admin', _('Administrador')),
        ('operator', _('Operador')),
        ('guest', _('Visitante'))
    )
)

settings.DJAESY_DEFAULT_USER_TYPE = getattr(settings, 'DJAESY_DEFAULT_USER_TYPE', 'operator')

settings.LOGIN_URL = '/login'
settings.LOGOUT_REDIRECT_URL = '/'
settings.LOGIN_REDIRECT_URL = '/'

settings.APPLICATION_PAGE_TITLE_PREFIX = 'DJAESY '

settings.LEAFLET_CONFIG = {
    'SRID': 4326,
    'PLUGINS': {
        'prugin': {
            'css': ['https://unpkg.com/@geoman-io/leaflet-geoman-free@latest/dist/leaflet-geoman.css', '/root/path/to/stylesheet.css'],
            'js': 'https://unpkg.com/@geoman-io/leaflet-geoman-free@latest/dist/leaflet-geoman.min.js',
            'auto-include': True,
        },
    }
}
