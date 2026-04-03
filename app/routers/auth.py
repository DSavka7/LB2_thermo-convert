from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
api_router = APIRouter(prefix="/api")


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ================= HTML =================

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_form(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "").strip()

    if not username or not password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Всі поля обов'язкові"})

    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Невірні дані"})

    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=30 * 60)
    return response


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_form(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "").strip()

    if not username or not password:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Всі поля обов'язкові"})

    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Користувач вже існує"})

    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password, role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse("/auth/login", status_code=303)


@router.get("/logout")
@router.post("/logout")
async def logout():
    response = RedirectResponse("/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response

# ================= API =================

@api_router.post("/register")
async def api_register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(data.password)
    user = User(username=data.username, hashed_password=hashed_password, role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}


@api_router.post("/login")
async def api_login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}