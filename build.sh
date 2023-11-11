set -o errexit

pip install Django
pip install deepface
pip install psycopg2-binary
pip install whitenoise
pip install django-cors-headers

python manage.py collectstatic --noinput
python manage.py migrate