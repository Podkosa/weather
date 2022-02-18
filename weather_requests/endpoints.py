from datetime import datetime
import asyncio
import typing

from fastapi import Request, Depends, APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from database import crud
from database.base import get_db
import weather_requests.schemas as schemas
from .external_requests import get_weather

router = APIRouter()

#As per test conditions, returns only the temperature and response time. If needed, can be modified to return more info.
@router.get("/weather", response_model=schemas.WeatherResponse)
async def weather(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    request_time = datetime.utcnow()
    weather_request = schemas.WeatherRequestBase(date=request_time, headers=request.headers)
    weather_request = crud.create_weather_request(db=db, weather_request=weather_request)
    
    try:
        temperature = await asyncio.wait_for(get_weather(), timeout=2)
        if temperature is not None and type(temperature) == float:
            weather_request.temperature = temperature
            background_tasks.add_task(crud.update_weather_request, db=db, weather_request=weather_request)
            return {'temperature':temperature, 'response_time':datetime.utcnow()}
        raise HTTPException (status_code=200, detail="External weather services are unavailable. Please try again later.")
    except asyncio.TimeoutError:
        raise HTTPException (status_code=200, detail='Resource is temporarily overloaded. Please try again later.')

@router.get("/data", response_model=typing.List[schemas.WeatherRequest])
async def data(limit: int = 10,  db: Session = Depends(get_db)):
    weather_requests = crud.get_weather_requests(db, limit=limit)
    return weather_requests