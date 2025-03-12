web: python manage.py collectstatic && gunicorn django_snippets.wsgi
worker: celery -A django_snippets worker -E -l info