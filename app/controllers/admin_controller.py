from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.models.conversion import DbConversion

templates = Jinja2Templates(directory="app/templates")


async def admin_panel(request: Request, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    users = db.query(User).all()
    total_conversions = db.query(DbConversion).count()

    stats = [
        {
            "user": user,
            "conversions_count": db.query(DbConversion).filter(DbConversion.user_id == user.id).count(),
        }
        for user in users
    ]

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": users,
        "total_users": len(users),
        "total_conversions": total_conversions,
        "stats": stats,
        "current_user": admin,
    })


async def clear_all_history(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db.query(DbConversion).delete()
    db.commit()
    return RedirectResponse("/admin", status_code=303)