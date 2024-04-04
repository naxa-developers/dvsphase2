python manage.py collectstatic --no-input
#python manage.py compilemessages -l ne -l en
python manage.py migrate --no-input
gunicorn dvs.wsgi:application --bind 0.0.0.0:8000 --workers 5 --timeout 600

