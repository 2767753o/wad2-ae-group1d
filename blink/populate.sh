#!/bin/sh

rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 populate.py