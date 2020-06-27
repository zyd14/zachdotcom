import os

from flask import Blueprint, request, render_template, current_app, send_from_directory
import markdown
import markdown.extensions.fenced_code
import numpy as np
import pandas as pd

from flask_app.mysite.public.forms import PlantCount
from flask_app.mysite.public.utils import save_collection_entry, calculate_totals, load_init_df, \
    add_plant_record

blueprint = Blueprint("public", __name__, static_folder="../static", template_folder="../templates")
pd.set_option('max_colwidth', 60)
pd.set_option('precision', 0)
pd.set_option('chop_threshold', .5)


def add_blog_to_page(page_key: str, page_content: dict, file_name: str='', content_key: str='blog_post1', blog_path: str='') -> dict:
    """ Retrieve configuration defining where blog post is located and read it in as markdown, then render to page.

    Args:
        page_key:
        page_content:
        file_name:
        content_key:
        blog_path:

    Returns:
        dict of values to fill page template with
    """

    # Retrieve default blog path and file name if they weren't provided by caller
    if not blog_path:
        blog_path = current_app.config.get('BLOG_POSTS')
    if not file_name:
        try:
            file_name = page_content[content_key]
        except KeyError as ke:
            current_app.logger.exception(f'Exception occurred when finding post with key "{content_key}")')
            raise ke

    blog_in = open(os.path.join(blog_path, file_name), 'r').read()
    blog_md = markdown.markdown(blog_in, output_format='html4')

    if page_key in page_content:
        current_app.logger.info(f'Value for page_key {page_key} already exists in page_content. Value will be overridden')
    current_app.logger.info(f'page_key: {page_key}')
    page_content.update({page_key: blog_md})
    return page_content


@blueprint.route("/", methods=["GET"])
def home():
    current_app.logger.info('Got to home page')
    page_content = current_app.config.get('CONTENT_MAP').load_page_content('public/home.html')
    page_content = add_blog_to_page(file_name='home1.md', page_key='home_blurb', page_content=page_content)

    return render_template('public/home.html', **page_content)


@blueprint.route('/about_me', methods=['GET'])
def about_me():
    current_app.logger.info(['Got to about_me page'])
    page_content = current_app.config.get('CONTENT_MAP').load_page_content('public/about_me.html')
    page_content = add_blog_to_page(page_key='sidebar', page_content=page_content, content_key='sidebar')
    page_content = add_blog_to_page(page_key='aboutme_blurb', page_content=page_content, content_key='blog_post1')
    current_app.logger.info(f'page_content: {page_content.keys()}')
    return render_template('public/about_me.html', **page_content)


@blueprint.route('/blog', methods=['GET'])
def blog():
    current_app.logger.info(['Got to blog page'])
    page_content = current_app.config.get('CONTENT_MAP').load_page_content('public/blog.html')
    page_content = add_blog_to_page(file_name='post1.md', page_key='blog', page_content=page_content)

    return render_template('public/blog.html', **page_content)


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
