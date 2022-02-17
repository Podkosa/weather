#Normally not hardcoded
API_KEYS = {
    'openweather':'bc8058e81b58367caa9769b06d109692',
    'weatherbit':'18b0482a647240d4a801ea0a9d18bc1a',
    'accuweather':'FwM79Zba9fc5a89TMoMFFtn2oqK1ernt',
}

#Openweather and Weatherbit are flexibile with the city name, accuweather is hardcoded for Moscow.
CITY = 'moscow'
WEATHER_URL = {
    'openweather':f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEYS["openweather"]}&units=metric',
    'weatherbit':f'http://api.weatherbit.io/v2.0/current?city={CITY}&key={API_KEYS["weatherbit"]}',
    'accuweather':f'http://dataservice.accuweather.com/currentconditions/v1/294021?apikey={API_KEYS["accuweather"]}'
}

#Options: openweather, weatherbit, accuweather
WEATHER_SERVICE = 'accuweather'

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/db.sqlite3"