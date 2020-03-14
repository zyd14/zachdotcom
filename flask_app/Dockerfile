FROM python:3.6.8-alpine3.9

ENV MONGODB_DATABASE = "zachdb"
ENV MONGODB_USERNAME = $mongodb_username
ENV MONGODB_PASSWORD = $mongodb_password
ENV MONGODB_HOSTNAME = "mongodb"
ENV APP_ENV = "dev"
ENV APP_DEBUG = "True"
ENV APP_PORT = 5000

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www

RUN mkdir /var/www/flask_app
COPY . /var/www/flask_app

RUN pip install -r /var/www/flask_app/requirements.txt
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]