from flask import Blueprint, request, render_template, current_app

blueprint = Blueprint("public", __name__, static_folder="../static")

@blueprint.route("/", methods=["GET"])
def home():
    current_app.logger.info('Got to home page')
    