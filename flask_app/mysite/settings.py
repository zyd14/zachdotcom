import os
from flask_app.mysite.utils import PageContentMapper

ENV = os.getenv('ZACHDOTCOM_ENV', 'dev')
DEBUG = os.getenv('ZACHDOTCOM_DEBUG', True)
CONTENT_MAP = PageContentMapper()
