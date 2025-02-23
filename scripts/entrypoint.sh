#!/bin/bash

# echo ">>> Waiting for Kafka to start..."
# .//wait-for-it.sh kafka:9092 -t 60

echo ">>> Waiting for Database to start..."
./scripts/wait-for-it.sh db:5432 -t 60

# echo ">>> Preparing media directories"
# mkdir media/
# mkdir media/vehicles

echo ">>> Make database migrations"
python3 ./manage.py makemigrations

echo ">>> Apply database migrations"
python3 ./manage.py migrate

# echo ">>> Load data from fixtures"
# python3 manage.py loaddata db/fixture.json

# echo ">>> Compile messages..."
# poetry run python manage.py compilemessages > logs/compilemessages.log

echo ">>> Starting server..."

if [ "$1" = "dev" ]; then
    echo ">> Running as developement server"
    python3 manage.py runserver 0.0.0.0:8000
else
    echo ">> Collecting static files..."
    python manage.py collectstatic --noinput

    # echo ">>> Populate database with dummy data"
    # python manage.py createdata

    echo ">> Running as production server"
    gunicorn tgs.wsgi -w 3 -b 0.0.0.0:8000
fi