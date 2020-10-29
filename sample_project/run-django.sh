#!/bin/sh

# Wait for database ready

pip install -r /code/requirements.txt

cd /code

until python test_database.py; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

ENV=$(python get_environment.py)

echo "Environment detected: $ENV"

if test "$ENV" = "staging" -o "$ENV" = "production"
then
    python manage.py migrate
    python manage.py collectstatic --noinput
    gunicorn i3track.wsgi \
        --bind 0.0.0.0:8000 \
        --access-logfile /logs/gunicorn-access.log \
        --error-logfile /logs/gunicorn-error.log \
        --log-level debug \
        --worker-class eventlet \
        --workers 4 \
        --timeout 300

    # uvicorn --host 0.0.0.0 --port 8000 i3track.asgi:application
    # python manage.py runserver 0.0.0.0:8000
else
    if test "$ENV" = "dev"
    then
        echo "Starting development server"
        python manage.py migrate
        gunicorn i3track.wsgi \
            --bind 0.0.0.0:8000 \
            --access-logfile /logs/gunicorn-access.log \
            --error-logfile /logs/gunicorn-error.log \
            --log-level debug \
            --worker-class eventlet \
            --workers 4 \
            --timeout 300
        # uvicorn i3track.asgi:application
        # python manage.py runserver 0.0.0.0:8000
        # python manage.py runserver_plus 0.0.0.0:8000
    else
        exit 1
    fi
fi


