from functools import partial
import numpy as np
import os
import pandas as pd

from flask import Blueprint, request, render_template, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, AnyOf

from flask_app.mysite.fakestuff import mock_garden_log
from flask_app.mysite.public import utils

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
    garden_df = mock_garden_log(path=path)
    mock_df = garden_df.style.set_properties(**{'background-color': 'black','color': 'lawngreen','border-color': 'white'})
    tables = [mock_df.render()]

    garden_df = utils.clean_column_names(garden_df)
    plant_types = garden_df['type'].unique()
    species_types = garden_df['species'].unique()

    plant_totals = {'type': [],
                    'total': []}
    for p_type in plant_types:
        df = garden_df[garden_df['type'] == p_type]['count']
        plant_totals['type'].append(p_type)
        plant_totals['total'].append(sum(int(p) for p in garden_df[garden_df['type'] == p_type]['count'].dropna()))

    plant_totals_df = pd.DataFrame(plant_totals)
    #sorted_plant_totals = plant_totals_df.sort_values(by=['total'], axis=1)
    #species_totals = {s_type: len(garden_df[garden_df['species'] == s_type]) for s_type in species_types}
    plat_totals_styles = plant_totals_df.style.set_properties(**{'background-color': 'black', 'color': 'lawngreen', 'border-color': 'white'})
    form = PlantCount()
    return render_template('public/gardening.html', tables=tables, plant_totals=plat_totals_styles.render(), form=form)

from wtforms import StringField, Field, SubmitField, IntegerField, DateField, SelectField, ValidationError
from datetime import datetime
import pytz


class PlantCount(FlaskForm):
    species = StringField('Plant species', validators=[DataRequired])
    count = IntegerField('Number of plants', validators=[DataRequired])
    location = StringField('Indoor / Outdoor', default='Indoor', validators=[partial(AnyOf, values=['Indoor', 'Outdoor'])])
    date = DateField(default=datetime.now(tz=pytz.timezone('UTC')))
