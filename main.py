from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.converter import router, api_router

app = FastAPI(title="ThermoConvert")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
app.include_router(api_router)
