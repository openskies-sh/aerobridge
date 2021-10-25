#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


# Load data 
echo "Loading data from Fixture"
python manage.py loaddata fixtures/initial_data.json
# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000