from functools import partial
import numpy as np
import os
import pandas as pd
from flask import Blueprint, request, render_template, current_app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, AnyOf

from flask_app.mysite.fakestuff import mock_garden_log
from flask_app.mysite.public import utils

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")
pd.set_option('max_colwidth', 60)
#pd.set_option('max_rows', 30)
pd.set_option('precision', 0)
pd.set_option('chop_threshold', .5)

@blueprint.route("/", methods=["GET"])
def home():
    current_app.logger.info('Got to home page')
    page_content = current_app.config.get('CONTENT_MAP').load_page_content('public/home.html')
    return render_template('public/home.html', **page_content)


@blueprint.route("/gardening", methods=["GET", "POST"])
def gardening():

    if 'garden_df' not in current_app.config:
        garden_df = load_init_df()
    else:
        garden_df = current_app.config['garden_df']

    styles = [
        dict(
            props=[
                ('border-collapse', 'separate'),
                ('border-spacing', '5px 35px'),
                ('border', 'solid')
            ]
        ),
        # dict(
        #     selector='td',
        #     props=[
        #         ('border', 'solid')
        #     ]
        # )

    ]

    out_df = garden_df.copy()
    out_df['count'] = out_df['count'].replace(np.nan, 'Null')
    garden_df_style = out_df.style\
        .set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'grey'})\
        .set_table_styles(styles)\
        .hide_index()
    tables = [garden_df_style.render()]
    #tables = [garden_df.to_html(index=False)]

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
    plant_totals_syntax = plant_totals_df.style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'grey'}).hide_index()
    plant_totals_syntax.background_gradient(subset=['total'], cmap='BuGn')
    form = PlantCount(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        return render_template('public/gardening.html', tables=tables, plant_totals=plant_totals_syntax.render(), form=form)

    return render_template('public/gardening.html', tables=tables, plant_totals=plant_totals_syntax.render(), form=form)

from wtforms import StringField, Form, Field, SubmitField, IntegerField, DateField, SelectField, ValidationError
from datetime import datetime
import pytz

def load_init_df() -> pd.DataFrame:
    path = os.path.join(os.path.split(os.path.split(os.path.dirname(os.path.realpath('__name__')))[0])[0],
                        'tests/test_files/garden_log.csv')
    garden_df = mock_garden_log(path=path)
    garden_df = utils.clean_column_names(garden_df)
    current_app.config['garden_df'] = garden_df
    garden_df['count'] = garden_df['count'].apply(convert_to_int)
    return garden_df

def convert_to_int(x):
    try:
        return int(x)
    except Exception as exc:
        return x

def add_plant_record(form: FlaskForm, df: pd.DataFrame) -> pd.DataFrame:
    pass


class PlantCount(FlaskForm):
    species = StringField('Plant species', validators=[DataRequired()])
    count = IntegerField('Number of plants', validators=[DataRequired()])
    location = StringField('Indoor / Outdoor', default='Indoor', validators=[partial(AnyOf, values=['Indoor', 'Outdoor'])()])
    date = DateField(default=datetime.now(tz=pytz.timezone('UTC')))
    submit = SubmitField(label='Submit')
