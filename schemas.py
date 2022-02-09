from pydantic import BaseModel
from datetime import datetime

class WeatherRequestBase(BaseModel):
    date: datetime
    headers: dict