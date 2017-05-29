release: python manage.py migrate --noinput
web: uwsgi --http :$PORT --module app.wsgi
