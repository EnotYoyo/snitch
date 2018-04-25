#!/bin/bash
export PGPASSWORD="$POSTGRES_PASSWORD"
export SNITCH_DB_URI="postgresql+psycopg2://$SNITCH_DB_USER:$SNITCH_DB_PASSWORD@db/$SNITCH_DB_NAME"

TIMEOUT=5
until psql -h "db" -U "postgres" -c "select 1" > /dev/null 2>&1 || [ $TIMEOUT -eq 0 ]; do
  echo "Waiting for postgres server, $((TIMEOUT--)) remaining attempts..."
  sleep 3
done

# create user and database
psql -h "db" -U "postgres" \
    -c "CREATE USER $SNITCH_DB_USER PASSWORD '$SNITCH_DB_PASSWORD';"

psql -h "db" -U "postgres" \
    -c "CREATE DATABASE "$SNITCH_DB_NAME" OWNER $SNITCH_DB_USER;"

psql -h "db" -U "postgres" -d "$SNITCH_DB_NAME" \
    -c "CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;";

unset PGPASSWORD
unset POSTGRES_PASSWORD

cd /srv/snitch/src
/srv/snitch/.env/bin/pip install -r requirements.txt
/srv/snitch/.env/bin/python setup.py install
export FLASK_APP=snitch.py
/srv/snitch/.env/bin/python -m flask db upgrade
/srv/snitch/.env/bin/python -m flask run --host=0.0.0.0