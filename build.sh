set -o errexit

pip install Django
pip install deepface
pip install psycopg2-binary

python manage.py collectstatic --noinput
python manage.py migrate