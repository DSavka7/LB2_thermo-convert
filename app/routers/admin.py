from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.models.conversion import DbConversion

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/admin")


@router.get("/")
async def admin_panel(request: Request, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    users = db.query(User).all()
    total_conversions = db.query(DbConversion).count()

    # Статистика по користувачах
    stats = []
    for user in users:
        conv_count = db.query(DbConversion).filter(DbConversion.user_id == user.id).count()
        stats.append({
            "user": user,
            "conversions_count": conv_count
        })

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": users,
        "total_users": len(users),
        "total_conversions": total_conversions,
        "stats": stats,
    })


@router.post("/clear-all")
async def clear_all_history(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db.query(DbConversion).delete()
    db.commit()
    return RedirectResponse("/admin", status_code=303)