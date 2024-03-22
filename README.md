# BLINK

A social media platform in which users may only post once a day.

## Description

BLINK - A social media platform in which users may only post once a day.
This limited posting forces users to make their posts count.
In addition, limited posting will result in a less saturated feed - highlighting what is important.
Posts on BLINK can be scheduled for release.
Ticking time bomb’ posts are designed to increase user engagement.

## Getting Started

The [BLINK](http://blinkwad2.eu.pythonanywhere.com/) project is hosted using [eu.pythonanywhere.com](https://eu.pythonanywhere.com/)

The app can also be run locally.
Clone the repository, install the dependencies and then from the 'blink' directory run
```
python manage.py runserver
```

### Dependencies
* python 3.10 (or above)
* django 2.1.5
* pillow 5.4.1
* bcrypt 4.1.2
* coverage 7.4.3
* requests 2.31.0

Install project depedencies from [requirements](./requirements.txt) file
```
pip install -r requirements.txt
```

### External sources

The `bcrypt` package was used to hash passwords.
Django's `messsages` framework was used to display success or error messages when a user tries to log in.
`Scss` was used to more easily compile into CSS.
Python's `datetime` library was used throughout for keeping track of various times.