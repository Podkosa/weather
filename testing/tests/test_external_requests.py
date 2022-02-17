import pytest

from weather_requests import external_requests
from config import WEATHER_URL

@pytest.mark.asyncio
async def test_weather_endpoint():
    temperature = await external_requests.get_weather()
    assert type(temperature) == float or temperature == None

@pytest.mark.asyncio
async def test_api_request():
    for url in WEATHER_URL.values():
        response = await external_requests.api_request(url)
        assert response