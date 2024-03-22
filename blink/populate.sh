#!/bin/sh

# rm db.sqlite3

# ./manage.py makemigrations blink_app
# ./manage.py migrate
# ./manage.py loaddata fixtures

rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 populate.py