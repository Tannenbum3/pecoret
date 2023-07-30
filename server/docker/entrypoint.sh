#!/bin/bash

if [ ! -f "/app/conf/production.py" ]; then
    touch /app/conf/__init__.py
    cp docker/local_settings.template.py /app/conf/production.py
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# import vulnerability templates
if [ ! -f "/app/resources/templates/vulnerability-templates/categories.yaml" ]; then
    echo "Cloning default templates..."
fi

python manage.py import_vulnerability_templates /app/resources/templates/vulnerability-templates

# echo "Update checklists"
# python manage.py update_checklists

# create superuser
echo "Create superuser"
python manage.py createsuperuser --noinput

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 pecoret.wsgi