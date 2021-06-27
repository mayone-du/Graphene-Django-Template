# 概要

app 内はアプリ用のサンプル
それ以外はプロジェクト用のサンプル

## セットアップ

- docker-compose up --build
- docker-compose exec app bash
- cd src
- django-admin startproject sampleproject .
- python manage.py startapp sampleapp
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver 0.0.0.0:8000
