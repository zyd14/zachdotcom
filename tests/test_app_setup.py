
from flask_app.backend.weatherdata import get_weather_db

class TestMongoClient:

    # def test_weather_setup(self):
    #     data = get_mongo_client()
    #     assert data


    def test_get_weather_db(self):
        data = get_weather_db()
        assert data