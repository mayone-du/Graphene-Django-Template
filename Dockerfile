FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN \
  mkdir /src && \
  cd /src && \
  pip install --upgrade pip && \
  pip install \
  django \
  graphene-django \
  graphene-file-upload \
  pillow \
  django-cors-headers \
  django-filter \
  django-graphql-jwt \
  python-decouple \
  psycopg2-binary \
  gunicorn

WORKDIR /src