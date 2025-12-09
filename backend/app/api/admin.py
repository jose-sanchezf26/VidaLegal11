from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import verify_admin, create_session, require_admin
from app.models.message import Message
from app.core.database import get_db
from app.crud.message import delete_message, get_all_messages

router = APIRouter(tags=["Admin"])
templates = Jinja2Templates(directory="templates")

# ---- Login (GET)
@router.get("/admin/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

# ---- Login (POST)
@router.post("/admin/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if verify_admin(username, password):
        session = create_session(username)
        response = JSONResponse({"success": True})
        response.set_cookie(key="session", value=session, httponly=True, max_age=86400)
        return response
    
    return JSONResponse(content={"success": False, "detail": "Credenciales inválidas"}, status_code=401)

@router.get("/admin/messages")
async def admin_messages(_ = Depends(require_admin)):
    return JSONResponse({"success": True})

def format_datetime(dt: datetime) -> str:
    return dt.strftime("%d/%m/%Y %H:%M")

@router.get("/admin/messages/all")
async def get_all_messages_endpoint(db: AsyncSession = Depends(get_db), _ = Depends(require_admin)):
    messages = await get_all_messages(db)
    # Convertir a lista de dicts para JSON
    return [
        {
            "id": m.id,
            "name": m.name,
            "email": m.email,
            "content": m.content,
            "category": m.category,
            "created_at": format_datetime(m.created_at)
        }
        for m in messages
    ]

@router.delete("/admin/messages/{message_id}")
async def delete_message_endpoint(message_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_message(db, message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")

    return {"status": "ok"}

# ---- Logout
@router.get("/admin/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("session")
    return response