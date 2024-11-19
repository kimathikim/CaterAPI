  web: gunicorn --timeout 120 -k eventlet -w 3  wsgi:application
  worker: su nobody -s /bin/sh -c 'celery -A app.tasks.celery worker --loglevel=info'
  beat: su nobody -s /bin/sh -c 'celery -A app.tasks.celery beat --loglevel=info'
