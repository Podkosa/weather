from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from weather_requests import endpoints
from database import models
from database.base import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Weather')
app.include_router(endpoints.router, prefix='')

@app.get('/')
async def redirect_to_docs():
    return RedirectResponse("/docs")