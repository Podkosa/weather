import os

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/db.sqlite3"

# External weather services (API)
API_KEYS = {
    'openweather': os.getenv('API_KEY_OPENWEATHER'),
    'weatherbit': os.getenv('API_KEY_WEATHERBIT'),
    'accuweather': os.getenv('API_KEY_ACCUWEATHER'),
}
# Openweather and Weatherbit are flexibile with the city name, accuweather is hardcoded for Moscow.
CITY = 'moscow'
WEATHER_URL = {
    'openweather':f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEYS["openweather"]}&units=metric',
    'weatherbit':f'http://api.weatherbit.io/v2.0/current?city={CITY}&key={API_KEYS["weatherbit"]}',
    'accuweather':f'http://dataservice.accuweather.com/currentconditions/v1/294021?apikey={API_KEYS["accuweather"]}'
}