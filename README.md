# 概要

app 内はアプリ用のサンプル
それ以外はプロジェクト用のサンプル

## セットアップ

- pipenv --python 3.9
- pipenv install hoge...
- pip freeze > requirements.txt
- docker-compose up --build
- docker-compose exec app bash
- cd src
- django-admin startproject sampleproject .
- python manage.py startapp sampleapp
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver 0.0.0.0:8000

### /.env

SECRET_KEY
DEBUG

DB_NAME
DB_USER
DB_HOST

CLOUDINARY_API_SECRET

EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWOR=
EMAIL_PORT

## デプロイ（Heroku）

- heroku config:push
  ...
- git push heroku master
- heroku run python3 manage.py migrate
- heroku run python3 manage.py createsuperuser
