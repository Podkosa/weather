from sqlalchemy import Column, Integer, DateTime, Float, JSON

from database.database import Base


class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    headers = Column(JSON)
    temperature = Column(Float)