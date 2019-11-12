from flask import Blueprint, request, render_template, current_app

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")


@blueprint.route("/", methods=["GET"])
def home():
    current_app.logger.info('Got to home page')
    return render_template('home.html')

@blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@blueprint.errorhandler(500)
def internal_sever_error(e):
    return render_template('500.html'), 500
