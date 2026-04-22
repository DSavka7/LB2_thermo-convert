from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from app.routes import all_routers
from app.db import Base, engine
from app.models import User, DbConversion  # noqa: F401 — register tables

app = FastAPI(title="ThermoConvert")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)

for router in all_routers:
    app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/auth/login", status_code=303)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)