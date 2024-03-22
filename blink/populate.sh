#!/bin/sh

rm db.sqlite3
python3 manage.py makemigrations blink_app
python3 manage.py migrate blink_app
python3 manage.py migrate --run-syncdb
python3 populate.py