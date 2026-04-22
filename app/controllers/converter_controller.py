from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.repositories.conversion_repo import ConversionRepository
from app.services.conversion_service import ConversionService
from app.db import get_db
from app.dependencies import get_current_user
from app.utils.temperature import is_valid_celsius

templates = Jinja2Templates(directory="app/templates")

_repo = ConversionRepository()
_service = ConversionService(_repo)


# ── HTML handlers ──────────────────────────────────────────────────────────────

async def index(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    history_count = len(_service.get_history(db, current_user.id))
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history_count": history_count,
        "celsius": "",
        "result": None,
        "error": None,
        "current_user": current_user,
    })


async def convert(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    form = await request.form()
    raw = form.get("celsius", "").strip()

    def _render(*, result=None, error=None):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "history_count": len(_service.get_history(db, current_user.id)),
            "celsius": result.celsius if result else raw,
            "error": error,
            "current_user": current_user,
        })

    try:
        celsius = float(raw)
        if not is_valid_celsius(celsius):
            raise ValueError("Out of range")
        return _render(result=_service.convert(celsius, db, current_user.id))
    except ValueError:
        return _render(error="Введіть коректне числове значення температури.")


async def history_page(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": _service.get_history(db, current_user.id),
        "current_user": current_user,
    })


async def clear_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _service.clear_history(db, current_user.id)
    return RedirectResponse("/history", status_code=303)


# ── API handlers ───────────────────────────────────────────────────────────────

class ConvertRequest(BaseModel):
    celsius: float


async def api_convert(data: ConvertRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return _service.convert(data.celsius, db, current_user.id)


async def api_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return _service.get_history(db, current_user.id)


async def api_clear(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _service.clear_history(db, current_user.id)
    return {"message": "History cleared"}