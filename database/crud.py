from sqlalchemy.orm import Session

import database.models as models, schemas
    
    
def create_weather_request(db: Session, weather_request: schemas.WeatherRequestBase):
    db_weather_request = models.WeatherRequest(date=weather_request.date, headers=weather_request.headers)
    db.add(db_weather_request)
    db.commit()
    db.refresh(db_weather_request)
    return db_weather_request

def update_weather_request(db: Session, weather_request: schemas.WeatherRequestBase):
    db_weather_request = db.query(models.WeatherRequest).get(weather_request.id)
    db.add(db_weather_request)
    db.commit()
    db.refresh(db_weather_request)
    return db_weather_request

def get_weather_requests(db: Session, limit: int = 10):
    return db.query(models.WeatherRequest).order_by(models.WeatherRequest.id.desc()).limit(limit).all()