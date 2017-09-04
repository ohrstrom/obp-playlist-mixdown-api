INTERNAL_IPS = (
    '127.0.0.1',
    '10.40.10.40',
)

DEBUG = True


TEMPLATES[0]['OPTIONS']['loaders'] = [
    'admin_tools.template_loaders.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
]


##################################################################
# db
##################################################################
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'com_example_api_local',
    #     'USER': 'ohrstrom',
    #     'HOST': '',
    # },
    'default': dj_database_url.config(default='sqlite:///app/data.sqlite3')
}


##################################################################
# cache
##################################################################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
CACHALOT_ENABLED = True
CACHALOT_CACHE = 'cachalot'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


##################################################################
# queues
##################################################################
CELERY_BROKER_URL = 'redis://localhost:6379/6'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/6'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']


##################################################################
# email
##################################################################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 60


COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

COMPRESS_OFFLINE_CONTEXT = {
    'template': 'base.html',
}


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
    #'devserver',
]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'devserver.middleware.DevServerMiddleware',
    #'base.middleware.profile.ProfileMiddleware',
]

DEBUG_TOOLBAR_PANELS = [

]

WERKZEUG_DEBUG_PIN = 'off'

DEVSERVER_MODULES = (
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)


from colorlog import ColoredFormatter
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(lineno)-4s [%(levelname)s] %(name)s: %(message)s'
        },
        'debug': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s %(lineno)-4s%(name)-24s %(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'bold_green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {

        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console',],
            'propagate': False
        },
        '': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': False
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False
        },
        'matching': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'notification': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'flatshare': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'dev': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
