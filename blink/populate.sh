#!/bin/sh

rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 populate.py