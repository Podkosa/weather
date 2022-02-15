import aiohttp

from config import WEATHER_SERVICE, WEATHER_URL


async def get_weather():
    # To test the timeout uncomment the next 2 lines
    # import asyncio
    # await asyncio.sleep(3)
    json = await api_request()
    if json is not None:
        if WEATHER_SERVICE == 'openweather':
            return json['main']['temp']
        if WEATHER_SERVICE == 'weatherbit':
            return json['data'][0]['temp']
        if WEATHER_SERVICE == 'accuweather':
            return json[0]['Temperature']['Metric']['Value']
    
async def api_request():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL[WEATHER_SERVICE]) as response:
            if response.status == 200:
                json = await response.json()
                return json