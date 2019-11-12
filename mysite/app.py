import logging
from logging.config import dictConfig

from flask import Flask, has_request_context, request
from flask.logging import default_handler
from flask_bootstrap import Bootstrap

from mysite import public

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def create_app(config_object='mysite.settings'):
    app = Flask('Zachdotcom')
    app.config.from_object(config_object)
    formatter = RequestFormatter(
        '[%(asctime)s] [%(remote_addr)s] requested %(url)s\n'
        '[%(levelname)s] in %(module)s: %(message)s'
    )
    default_handler.setFormatter(formatter)

    register_exensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)

def register_exensions(app):
    Bootstrap(app)

if __name__ == '__main__':
    app = create_app()
    app.run()