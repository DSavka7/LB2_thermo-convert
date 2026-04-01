from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.repositories.conversion_repo import ConversionRepository
from app.services.conversion_service import ConversionService

templates = Jinja2Templates(directory="app/templates")

repo = ConversionRepository()
service = ConversionService(repo)


router = APIRouter()


api_router = APIRouter(prefix="/api")


# ================= HTML =================

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history_count": len(service.get_history()),
        "celsius": ""
    })


@router.post("/")
async def convert(request: Request):
    form = await request.form()
    value = form.get("celsius")

    try:
        celsius = float(value)

        if not -273.15 <= celsius <= 1000:
            raise ValueError

        result = service.convert(celsius)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "history_count": len(service.get_history()),
            "celsius": celsius
        })

    except:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Некоректне значення!",
            "history_count": len(service.get_history()),
            "celsius": value
        })


@router.get("/history")
async def history_page(request: Request):
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": service.get_history()
    })


@router.post("/history/clear")
async def clear_history():
    service.clear_history()
    return RedirectResponse("/history", status_code=303)


# ================= API =================

class ConvertRequest(BaseModel):
    celsius: float


@api_router.post("/convert")
async def api_convert(data: ConvertRequest):
    return service.convert(data.celsius)


@api_router.get("/history")
async def api_history():
    return service.get_history()


@api_router.delete("/history")
async def api_clear():
    service.clear_history()
    return {"message": "History cleared"}