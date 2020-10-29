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
    python manage.py send_notifications
else
    if test "$ENV" = "dev"
    then
        python manage.py send_notifications
    else
        exit 1
    fi
fi


