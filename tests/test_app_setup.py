
from flask_app.backend.weatherdata import get_mongo_client

class TestMongoClient:

    def test_weather_setup(self):
        data = get_mongo_client()
        assert data

