from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.repositories.conversion_repo import ConversionRepository
from app.services.conversion_service import ConversionService
from app.db import get_db
from app.dependencies import get_current_user

templates = Jinja2Templates(directory="app/templates")

repo = ConversionRepository()
service = ConversionService(repo)

router = APIRouter()
api_router = APIRouter(prefix="/api")


# ================= HTML =================

@router.get("/")
async def index(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    history_count = len(service.get_history(db, current_user.id))

    return templates.TemplateResponse("index.html", {
        "request": request,
        "history_count": history_count,
        "celsius": "",
        "result": None,
        "error": None,
        "current_user": current_user,  # ← Важливо для адмін меню
    })


@router.post("/")
async def convert(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    form = await request.form()
    value = form.get("celsius", "").strip()

    try:
        celsius = float(value)

        if not (-273.15 <= celsius <= 1_000_000):
            raise ValueError("Out of range")

        result = service.convert(celsius, db, current_user.id)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "history_count": len(service.get_history(db, current_user.id)),
            "celsius": celsius,
            "error": None,
            "current_user": current_user,  # ← Важливо
        })

    except ValueError:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Введіть коректне числове значення температури.",
            "history_count": len(service.get_history(db, current_user.id)),
            "celsius": value,
            "result": None,
            "current_user": current_user,  # ← Важливо
        })


@router.get("/history")
async def history_page(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": service.get_history(db, current_user.id),
        "current_user": current_user,  # ← Важливо
    })


@router.post("/history/clear")
async def clear_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service.clear_history(db, current_user.id)
    return RedirectResponse("/history", status_code=303)


# ================= API =================

class ConvertRequest(BaseModel):
    celsius: float


@api_router.post("/convert")
async def api_convert(data: ConvertRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.convert(data.celsius, db, current_user.id)


@api_router.get("/history")
async def api_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.get_history(db, current_user.id)


@api_router.delete("/history")
async def api_clear(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service.clear_history(db, current_user.id)
    return {"message": "History cleared"}