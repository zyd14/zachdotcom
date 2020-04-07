from dataclasses import dataclass
from datetime import datetime

from flask import Request
from pymongo import MongoClient
from pytz import timezone
import requests

@dataclass
class OpenWeatherData:
    pass

def get_weather_nws():
    """ Only returns data in html format"""
    req = requests.get("https://national-weather-service.p.rapidapi.com/stations",
                       headers={"x-rapidapi-host": "national-weather-service.p.rapidapi.com",
                                "x-rapidapi-key": "f6e50008e6mshdf2ebe445cd3e74p145b4fjsnaa068668587d"})
    print(req)
    content = req.content.decode('utf-8')
    import json
    content_loaded = json.loads(content.replace('\n', ''))
    print(content_loaded)

    return req


def get_open_weather_map():
    req = requests.get("https://community-open-weather-map.p.rapidapi.com/weather",
                       headers={"x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
                                "x-rapidapi-key": "f6e50008e6mshdf2ebe445cd3e74p145b4fjsnaa068668587d"},
                       params={'q': 'seattle'}
                       )
    import json
    data = json.loads(req.text)

    openweather = get_weather_db()
    dumps = openweather['dumps']
    m_id = dumps.insert_one(data).inserted_id

    dump_to_file(req)


def dump_to_file(req: Request):
    now = get_file_date()
    with open(f'dumps/test_open_weather_dump_{now}.txt', 'w') as d_out:
        d_out.write(req.text)

def init_weather_db():
    client = MongoClient()
    weather_db = client.weather_data

def get_weather_db():
    client = MongoClient()
    weather_db = client['weather_data']
    return weather_db


def get_file_date():
    return datetime.now(tz=timezone('UCT'))

if __name__ == '__main__':
    get_open_weather_map()
