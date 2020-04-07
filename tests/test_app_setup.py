
from flask_app.backend.weatherdata import get_weather_db

class TestMongoClient:


    def test_get_weather_db(self):
        data = get_weather_db()
        assert data