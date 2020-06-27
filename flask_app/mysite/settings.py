import logging
import os

from flask import has_request_context, request
from flask_app.mysite.content import PageContentMapper
from flask.logging import default_handler

mysite_dir = os.path.realpath(os.path.dirname(__file__))

ENV = os.getenv('ZACHDOTCOM_ENV', 'dev')
DEBUG = os.getenv('ZACHDOTCOM_DEBUG', True)
CONTENT_MAP = PageContentMapper()
SECRET_KEY = os.urandom(32)
MONGO_URI = 'mongodb://localhost:27017/'
LOG_LEVEL = 'INFO'

BLOG_POSTS = os.path.join(mysite_dir, 'static/blogs')


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter(
        '[%(asctime)s] | [%(remote_addr)s] | requested %(url)s\n'
        '[%(levelname)s] in %(module)s: %(message)s | %(lineno)s '
    )
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(LOG_LEVEL)
default_handler.setFormatter(formatter)
