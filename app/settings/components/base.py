# -*- coding: utf-8 -*-
import os
import sys
import posixpath


SECRET_KEY = env('SECRET_KEY')

FILER_DEBUG = DEBUG
ALLOWED_HOSTS = ['*',]

# this fixes strange behaviour when running app through gunicorn
DEBUG_TOOLBAR_PATCH_SETTINGS = False

SITE_URL = env('SITE_URL', default='http://localhost:8080/')
SITE_ID = env.int('SITE_ID', default=1)


LOCALE_PATHS = [root('locale')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


LANGUAGES = [
    ('en', _('English')),
    #('de', _('German')),
]

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'


##################################################################
# applications
##################################################################
INSTALLED_APPS = [

    #'django_slick_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    #'django.contrib.sites',
    #'django.contrib.sitemaps',
    'django.contrib.humanize',
    #
    'channels',
    'storages',
    'compressor',
    'turbolinks',
    'raven.contrib.django.raven_compat',
    'django_celery_beat',

    # authentication
    'authtools',
    'auth_extra',

    # api
    'api_extra',
    'rest_framework',
    'rest_framework.authtoken',

    # project apps
    'mixdown',

]


##################################################################
# middleware
##################################################################
MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'turbolinks.middleware.TurbolinksMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

##################################################################
# database
##################################################################

##################################################################
# authentication
##################################################################
AUTH_USER_MODEL = 'auth_extra.User'

# TODO: make dynamic
LOGIN_URL = '/account/login/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.email.EmailAuth',
    'django.contrib.auth.backends.ModelBackend',
)

# LOGIN_REDIRECT_URL = '/account/pick-up/'

##################################################################
# email settings
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


##################################################################
# turbolinks
# note: turbolinks does not work with gulp's browserSync
##################################################################
TURBOLINKS_ENABLED = True


##################################################################
# settings export
##################################################################
SETTINGS_EXPORT = [
    'DEBUG',
    'TURBOLINKS_ENABLED',
    'SITE_URL',
    'CHANNELS_ENABLED',
]

##################################################################
# API
##################################################################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

##################################################################
# Remote API (OBP)
##################################################################

REMOTE_API_BASE_URL = env('REMOTE_API_BASE_URL', default='https://www.openbroadcast.org')
REMOTE_API_USER = env('REMOTE_API_USER', default='peter')
REMOTE_API_KEY = env('REMOTE_API_KEY', default='peter')

