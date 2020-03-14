from flask import Blueprint, request, render_template, current_app

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")

@blueprint.route("/", methods=["GET"])
def home():
    current_app.logger.info('Got to home page')
    page_content = current_app.config.get('CONTENT_MAP').load_page_content('public/home.html')
    return render_template('public/home.html', **page_content)

