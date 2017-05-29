release: python website/manage.py migrate --noinput
web: python website/daphne_cli.py project.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v1
worker: python website/manage.py runworker -v1
queue: cd website && celery -A project worker -l info
# MAKE SURE ONLY ONE BEAT INSTANCE EXISTS!!!
beat: cd website && celery -A project beat -l info -S django
