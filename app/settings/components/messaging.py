import os

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379/5')],
        },
        "ROUTING": "app.routing.channel_routing",
    },
}

RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379'),
        'DB': 1,
        'DEFAULT_TIMEOUT': 500,
    },
}
