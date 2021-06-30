import pyowm
from pyowm.utils.config import get_default_config
import json

with open("secret.json", "rt") as file:
    keys = json.loads(file.read())
    weather_key = keys["weather_key"]

owm = pyowm.OWM(api_key=weather_key)
mgr = owm.weather_manager()
config_dict = get_default_config()
config_dict['language'] = 'ru'

temp_sensation = {
    -30: 'очень холодно',
    -25: 'очень холодно',
    -20: 'очень холодно',
    -15: 'очень холодно',
    -10: 'очень холодно',
    -5: 'очень холодно',
    0: 'очень холодно',
    5: 'зябко',
    10: 'прохладно',
    15: 'тепло',
    20: 'хорошо',
    25: 'жарко',
    30: 'невыносимо жарко'
}
wind_sensation = {
    30: 'очень сильный',
    25: 'очень сильный',
    20: 'очень сильный',
    15: 'очень сильный',
    10: 'сильный',
    5: 'слабый',
    0: 'небольшой',
}


def get_weather_data(city):
    """Функция определения погоды"""
    observation = mgr.weather_at_place(city)
    w = observation.weather
    temp = int(w.temperature('celsius')['temp'])
    wind = int(w.wind()['speed'])
    temp_rounded = round(temp / 5) * 5  # ощущение температуры
    wind_rounded = round(wind / 5) * 5  # ощущение ветра
    return f"В городе {city.title()} сейчас {temp} градусов\n\nНа улице сейчас {temp_sensation[temp_rounded]}," \
           f" {wind_sensation[wind_rounded]} ветер, {w.detailed_status}"
