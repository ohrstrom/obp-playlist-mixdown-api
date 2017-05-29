# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import dj_database_url

# rather naive way to detect heroku environment
if os.environ.get('HOME') == '/app':

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    ##################################################################
    # database settings from heroku env
    ##################################################################
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
        },
    }

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

    ##################################################################
    # queues
    ##################################################################
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379') + '/6'
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379') + '/6'
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERYD_CHDIR = "/app/website"


    ##################################################################
    # media storage on s3
    ##################################################################
    DEFAULT_FILE_STORAGE = 'project.storage.MediaRootS3BotoStorage'

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
    # heroku config:set DJANGO_STATIC_HOST=s3-eu-west-1.amazonaws.com
    AWS_S3_HOST = os.environ.get('AWS_S3_HOST', 's3-eu-west-1.amazonaws.com')
    AWS_AUTO_CREATE_BUCKET = True
    AWS_HEADERS = {
        'Cache-Control': 'public, max-age=86400',
    }
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SECURE_URLS = True
    AWS_REDUCED_REDUNDANCY = False
    AWS_IS_GZIPPED = False


    ##################################################################
    # staticfiles through whitenose & cloud front
    ##################################################################
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_MAX_AGE = 60


    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = False

    COMPRESS_OFFLINE_CONTEXT = {
        'template': 'base.html',
    }

    # heroku config:set DJANGO_STATIC_HOST=https://d2ko6bbh8aq9i.cloudfront.net
    STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
    STATIC_URL = STATIC_HOST + '/static/'


    ##################################################################
    # redis connection for matching
    ##################################################################
    MATCHING_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    MATCHING_REDIS_DB = 4


    ##################################################################
    # email configuration (sendgrid)
    ##################################################################
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    #EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'
    #BANDIT_EMAIL = 'jonas+hoodeenie@anorg.net'

    SENDGRID_EVENTS_IGNORE_MISSING = True

    ##################################################################
    # deliver emails via task queue
    ##################################################################
    NOTIFICATION_EMAIL_RUN_ASYNC = True


    ##################################################################
    # cache
    ##################################################################
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
        'cachalot': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    CACHALOT_CACHE = 'cachalot'
    CACHALOT_ENABLED = True


    ##################################################################
    # analytics
    ##################################################################
    GOOGLE_ANALYTICS_CODE = os.environ.get('GOOGLE_ANALYTICS_CODE', None)


    ##################################################################
    # tools
    ##################################################################
    LOADERIO_TOKEN = os.environ.get('LOADERIO_TOKEN', None)

    RAVEN_DSN = os.environ.get('RAVEN_DSN', None)
    if RAVEN_DSN:
        RAVEN_CONFIG = {
            'dsn': RAVEN_DSN,
        }


    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {'custom-tag': 'x'},
            },
        },
        'loggers': {},
    }
