from datetime import datetime
import asyncio

from fastapi import Request, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from database import crud
from database.base import get_db
import schemas
from .external_requests import get_weather

router = APIRouter()

#As per test conditions, returns only the temperature and response time. If needed, can be modified to return more info.
@router.get("/weather")
async def weather(request: Request, db: Session = Depends(get_db)):
    request_time = datetime.utcnow()
    weather_request = schemas.WeatherRequestBase(date=request_time, headers=request.headers)
    weather_request = crud.create_weather_request(db=db, weather_request=weather_request)
    try:
        temperature = await asyncio.wait_for(get_weather(), timeout=2)
        if temperature is not None:
            weather_request.temperature = temperature
            weather_request = crud.update_weather_request(db=db, weather_request=weather_request)
            return {'temperature':temperature, 'response_time':datetime.utcnow()}
        return {'error':'External temperature request was unsuccessful. Please try again later.'}
    except asyncio.TimeoutError:
        return {'error':'Resource is temporarily overloaded. Please try again later.'}

@router.get("/data")
async def data(limit: int = 10,  db: Session = Depends(get_db)):
    weather_requests = crud.get_weather_requests(db, limit=limit)
    return weather_requests