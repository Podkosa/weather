from datetime import datetime
import asyncio

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import models, crud
from database.base import SessionLocal, engine
import schemas
from external_requests import get_weather
from endpoints import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Weather')
app.include_router(router, prefix='')

@app.get('/')
async def redirect_to_docs():
    return RedirectResponse("/docs")