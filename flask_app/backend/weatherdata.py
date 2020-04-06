import requests

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

    print(req)

if __name__ == '__main__':
    get_open_weather_map()