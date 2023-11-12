release: python manage.py migrate
web: gunicorn Sentinel.wsgi:app --log-file