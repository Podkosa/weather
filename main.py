from datetime import datetime
from database import SessionLocal, engine
import models, schemas, crud
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from external_requests import get_weather
import asyncio


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#As per test conditions, returns only the temperature and response time. If needed, can be modified to return more info.
@app.get("/weather")
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
        return 'External temperature request was unsuccessful. Please try again later.'
    except asyncio.TimeoutError:
        return 'Resource is temporarily overloaded. Please try again later.'

@app.get("/data")
async def data(n: int = 10,  db: Session = Depends(get_db)):
    weather_requests = crud.get_weather_requests(db, limit=n)
    return weather_requests