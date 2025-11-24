from tempfile import template
from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageOut
from app.crud.message import create_message

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/contacto", response_model=MessageOut)
async def send_message(request: Request, name: str = Form(...), email: str = Form(...), content: str = Form(...), db: AsyncSession = Depends(get_db)):
    message = MessageCreate(name=name, email=email, content=content)
    msg = await create_message(db, message)
    return templates.TemplateResponse("index.html", {"request": request})