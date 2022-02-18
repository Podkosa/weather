import aiohttp
from fastapi import HTTPException

from config import WEATHER_URL


async def get_weather() -> float:
    '''External request to a public weather API, specified in `config`.
    Returns temperature (`float`).'''
    
    # To test the timeout uncomment the next 2 lines
    # import asyncio
    # await asyncio.sleep(3)

    for site, url in WEATHER_URL.items():
        json = await api_request(url)
        if json is not None:
            if site == 'openweather':
                return json['main']['temp']
            elif site == 'weatherbit':
                return json['data'][0]['temp']
            elif site == 'accuweather':
                return json[0]['Temperature']['Metric']['Value']
    raise HTTPException(status_code=504, detail="External weather services are unavailable. Please try again later.")
        
    
async def api_request(url):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=0.5)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                json = await response.json()
                return json