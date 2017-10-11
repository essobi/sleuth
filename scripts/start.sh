#!/bin/bash
# Wait until services have booted then migrate and boot Django server

echo "Waiting for Solr to boot"
bash scripts/wait.sh "Solr" "curl solr:8983/solr"
echo "Waiting for Postgres to boot"
bash scripts/wait.sh "Postgres" "pg_isready -h db -p 5432"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000