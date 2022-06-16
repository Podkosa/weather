from datetime import datetime
import asyncio
import typing

from fastapi import Request, Depends, APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from database import crud
from database.base import get_db
from weather_requests import schemas,  external_requests

router = APIRouter()

@router.get("/weather", response_model=schemas.WeatherResponse)
async def weather(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    request_time = datetime.utcnow()
    weather_request = schemas.WeatherRequestBase(date=request_time, headers=request.headers)
    weather_request = crud.create_weather_request(db=db, weather_request=weather_request)
    
    try:
        temperature = await asyncio.wait_for(external_requests.get_weather(), timeout=2)
        weather_request.temperature = temperature
        background_tasks.add_task(crud.update_weather_request, db=db, weather_request=weather_request)
        return {'temperature':temperature, 'response_time':datetime.utcnow()}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=503, detail='Resource is temporarily overloaded. Please try again later.')

@router.get("/data", response_model=typing.List[schemas.WeatherRequest])
async def data(limit: int = 10,  db: Session = Depends(get_db)):
    weather_requests = crud.get_weather_requests(db, limit=limit)
    return weather_requests