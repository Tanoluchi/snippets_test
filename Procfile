web: python manage.py collectstatic && gunicorn django_snippets.wsgi
worker: celery -A django_snippets worker -l info -n my_celery_worker@%h