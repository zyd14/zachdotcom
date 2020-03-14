FROM python:3.6

ENV MONGODB_DATABASE = "zachdb"
ENV MONGODB_USERNAME = $mongodb_username
ENV MONGODB_PASSWORD = $mongodb_password
ENV MONGODB_HOSTNAME = "mongodb"
ENV APP_ENV = "dev"
ENV APP_DEBUG = "True"
ENV APP_PORT = 5000

RUN mkdir flask_app
COPY . flask_app

RUN pip install -r requirements.txt