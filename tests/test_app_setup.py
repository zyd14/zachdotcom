
from flask_app.backend.weatherdata import get_weather_db
from flask_app.mysite.public.utils import get_all_plant_entries, load_init_df

from pymongo import MongoClient

class TestMongoClient:


    def test_get_weather_db(self):
        data = get_weather_db()
        assert data

    def test_get_glant_counts(self):
        data = get_all_plant_entries()
        assert data

    def test_load_data(self):
        data = load_init_df()
        client = MongoClient()
        for i, row in enumerate(data.itertuples()):
            pass
