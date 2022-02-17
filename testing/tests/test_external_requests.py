import pytest

from weather_requests import external_requests

@pytest.mark.asyncio
async def test_weather_endpoint():
    temperature = await external_requests.get_weather()
    assert type(temperature) == float or temperature == None

@pytest.mark.asyncio
async def test_api_request():
    dummy_url = 'not a url'
    response = await external_requests.api_request(dummy_url)
    assert response == None