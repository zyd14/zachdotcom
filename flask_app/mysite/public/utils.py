import pandas as pd
from flask import current_app
from flask_wtf import FlaskForm
from pandas import DataFrame
from pymongo import MongoClient

from flask_app.mysite.fakestuff import mock_garden_log
from flask_app.mysite.public.views import GARDEN_LOG_PATH


def clean_column_names(df: DataFrame) -> DataFrame:
    df.columns = [name.strip().replace('/n', '').replace(' ', '_').lower() for name in df.columns]
    return df


def convert_to_int(x):
    try:
        return int(x)
    except Exception as exc:
        return x


def save_collection_entry(collection: str, entry: dict):
    client = MongoClient()
    plant_count_db = client['plant_count_db']
    plant_count_col = plant_count_db[collection]
    plant_count_col.insert_one(entry)


def get_all_plant_entries() -> pd.DataFrame:
    client = MongoClient()
    plant_count_db = client['plant_count_db']
    plant_count_col = plant_count_db['counts']

    return pd.concat([record['data'] for record in plant_count_col.find()])


def calculate_totals(garden_df: pd.DataFrame) -> pd.DataFrame:
    plant_types = garden_df['type'].unique()

    plant_totals = {'type': [],
                    'total': []}
    for p_type in plant_types:
        plant_totals['type'].append(p_type)
        plant_totals['total'].append(sum(int(p) for p in garden_df[garden_df['type'] == p_type]['count'].dropna()))

    return pd.DataFrame(plant_totals)


def load_init_df() -> pd.DataFrame:
    garden_df = mock_garden_log(path=GARDEN_LOG_PATH)
    garden_df = utils.clean_column_names(garden_df)
    current_app.config['garden_df'] = garden_df
    garden_df['count'] = garden_df['count'].apply(convert_to_int)
    return garden_df


def add_plant_record(form: FlaskForm, df: pd.DataFrame) -> pd.DataFrame:
    new_row = pd.DataFrame({'type': [form.data['plant_type']],
                            'species': [form.data['species']],
                            'count': [form.data['count']],
                            'germinated': [form.data['germinated']],
                            'location': [form.data['location']],
                            'date_started': [form.data['date_started']],
                            'last_updated': [form.data['date_updated']]})

    return pd.concat([df, new_row], ignore_index=True)