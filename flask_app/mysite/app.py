import datetime as dt
import logging
from logging.config import dictConfig

from flask import has_request_context, request
from flask.logging import default_handler
import logging

from flask import Flask, render_template

from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flaskext.markdown import Markdown


dictConfig({'version': 1,
            'formatters': {'default': {
                'class': 'flask_app.mysite.settings.RequestFormatter',
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



def create_app(config_object='flask_app.mysite.settings'):
    _app = Flask('Zachdotcom')
    _app.config.from_object(config_object)
    register_extensions(_app)
    register_blueprints(_app)
    register_errorhandlers(_app)

    return _app


def register_blueprints(this_app):
    import flask_app.mysite.public as public
    this_app.register_blueprint(public.views.blueprint)


def register_extensions(this_app):
    Bootstrap(this_app)
    PyMongo(this_app)
    Markdown(this_app)


def register_errorhandlers(this_app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        this_app.errorhandler(errcode)(render_error)
    return None


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
