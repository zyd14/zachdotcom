import numpy as np
import os
import pandas as pd

from flask import Blueprint, request, render_template, current_app


from flask_app.mysite.fakestuff import mock_garden_log

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")
pd.set_option('max_colwidth', 40)
pd.set_option('precision', 4)
pd.set_option('chop_threshold', .5)


@blueprint.route("/", methods=["GET"])
def home():
    current_app.logger.info('Got to home page')
    page_content = current_app.config.get('CONTENT_MAP').load_page_content('public/home.html')
    return render_template('public/home.html', **page_content)

@blueprint.route("/gardening", methods=["GET"])
def gardening():
    path = os.path.join(os.path.split(os.path.split(os.path.dirname(os.path.realpath('__name__')))[0])[0], 'tests/test_files/garden_log.csv')
    mock_df = mock_garden_log(path=path).replace(np.nan, 'Null').style.set_properties(**{'background-color': 'black','color': 'lawngreen','border-color': 'white'})
    tables = [mock_df.render()]
    return render_template('public/gardening.html', tables=tables)
