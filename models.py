from database import Base
from sqlalchemy import Column, Integer, DateTime, Float, JSON

class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    headers = Column(JSON)
    temperature = Column(Float)