from pydantic import BaseModel, Json
from datetime import datetime


class WeatherRequestBase(BaseModel):
    date: datetime
    headers: dict

class WeatherRequest(WeatherRequestBase):
    id: int
    temperature: float | None
    
    class Config:
        orm_mode = True

class WeatherResponse(BaseModel):
    temperature: float
    response_time: datetime