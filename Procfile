web: gunicorn --timeout 120 -k eventlet -w 1 wsgi:application
worker: celery -A app.tasks.celery worker --loglevel=info
beat: celery -A app.tasks.celery beat --loglevel=info

