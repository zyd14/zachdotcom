
from flask import Blueprint, render_template, current_app, session, redirect, url_for

from mysite.hello import NameForm
from mysite.models import db, User

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")

@blueprint.route("/", methods=["GET", "POST"])
def home():
    current_app.logger.info('Got to home page')

    if 'name' not in session:
        session['name'] = 'Stranger'

    form = NameForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('public.home'))

    return render_template('public/home.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


