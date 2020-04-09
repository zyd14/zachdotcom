import os

from flask import Blueprint, request, render_template, current_app
import numpy as np
import pandas as pd

from flask_app.mysite.public.forms import PlantCount
from flask_app.mysite.public.utils import save_collection_entry, calculate_totals, load_init_df, \
    add_plant_record

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")
pd.set_option('max_colwidth', 60)
# pd.set_option('max_rows', 30)
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
    plant_totals_df = calculate_totals(garden_df)
    out_df = garden_df.copy()
    out_df['count'] = out_df['count'].replace(np.nan, 'Null')
    garden_df_style = out_df.style \
        .set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'grey'}) \
        .set_table_styles(styles) \
        .hide_index()

    tables = [garden_df.to_html(index=False).replace('dataframe', 'table table-striped')]

    # sorted_plant_totals = plant_totals_df.sort_values(by=['total'], axis=1)
    # species_totals = {s_type: len(garden_df[garden_df['species'] == s_type]) for s_type in species_types}
    # plant_totals_syntax = plant_totals_df.style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'grey'}).hide_index()
    # plant_totals_syntax.background_gradient(subset=['total'], cmap='BuGn')
    # plant_totals_df.style.background_gradient(subset=['total'], cmap='BuGn')
    form = PlantCount(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        garden_df = add_plant_record(form, garden_df)
        save_collection_entry('count_records', form.data)
        current_app.config['garden_df'] = garden_df
        plant_totals_df = calculate_totals(garden_df)
        return render_template('public/gardeningdata.html', tables=tables,
                               plant_totals=plant_totals_df.to_html().replace('dataframe', 'table table-striped'),
                               form=form)

    return render_template('public/gardeningdata.html', tables=tables,
                           plant_totals=plant_totals_df.to_html(index=False).replace('dataframe',
                                                                                     'table table-striped'), form=form)


@blueprint.route("/gardening/blog", methods=["GET", "POST"])
def garden_blog():
    pass
