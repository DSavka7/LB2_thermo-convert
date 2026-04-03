from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from app.routers.converter import router, api_router
from app.routers.auth import router as auth_router, api_router as auth_api_router
from app.routers.admin import router as admin_router

from app.db import Base, engine
from app.models.user import User
from app.models.conversion import DbConversion

app = FastAPI(title="ThermoConvert")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(api_router)
app.include_router(auth_router, prefix="/auth")
app.include_router(auth_api_router)
app.include_router(admin_router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/auth/login", status_code=303)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)