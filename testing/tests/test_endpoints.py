import random
from ..setup import client, test_db

def test_weather_endpoint(test_db):
    response = client.get("/weather")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_data_endpoint(test_db):
    response = client.get("/data", params={'n':random.randint(0, 100)})
    assert response.status_code == 200
    assert type(response.json()) == list