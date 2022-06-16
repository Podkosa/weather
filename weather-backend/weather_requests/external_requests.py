import asyncio
import aiohttp
from fastapi import HTTPException

from config import WEATHER_URL


async def get_weather() -> float:
    '''External request to a public weather APIs, specified in `config`.
    Returns temperature (`float`).'''

    results = await asyncio.gather(
        *[asyncio.create_task(api_request(site, url)) for site, url in WEATHER_URL.items()]
    )
    for result in results:
        if result:
            match result['site']:
                case 'openweather':
                    return result['json']['main']['temp']
                case 'weatherbit':
                    return result['json']['data'][0]['temp']
                case 'accuweather':
                    return result['json'][0]['Temperature']['Metric']['Value']
    raise HTTPException(status_code=504, detail="External weather services are unavailable. Please try again later.")
        
async def api_request(site: str, url: str):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                json = await response.json()
                return {'json': json, 'site': site}