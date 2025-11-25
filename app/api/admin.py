from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import verify_admin, create_session, require_admin
from app.models.message import Message
from app.core.database import get_db

router = APIRouter(tags=["Admin"])
templates = Jinja2Templates(directory="templates")

# ---- Login (GET)
@router.get("/admin/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

# ---- Login (POST)
@router.post("/admin/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if verify_admin(username, password):
        session = create_session(username)
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(key="session", value=session, httponly=True, max_age=86400)
        return response

    return templates.TemplateResponse(
        "admin_login.html",
        {"request": request, "error": "Credenciales inválidas"}
    )

@router.get("/admin")
async def admin_home(request: Request, db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message).order_by(Message.created_at.desc()))
    messages = result.scalars().all()
    return templates.TemplateResponse("admin_home.html", {"request": request, "messages": messages})

# ---- Logout
@router.get("/admin/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("session")
    return response