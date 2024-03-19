#!/bin/sh

rm db.sqlite3

./manage.py makemigrations blink_app
./manage.py migrate
./manage.py loaddata fixtures

