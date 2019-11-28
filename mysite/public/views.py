
from mysite.hello import NameForm
from flask import Blueprint, request, render_template, current_app, session, redirect, url_for

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")

@blueprint.route("/", methods=["GET", "POST"])
def home():
    current_app.logger.info('Got to home page')
    if 'name' not in session:
        session['name'] = 'Stranger'
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('public.home'))
    return render_template('public/home.html', form=form, name=session.get('name'))

