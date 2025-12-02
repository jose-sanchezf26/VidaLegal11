from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageOut
from app.crud.message import create_message
from app.core.classifier import classify_message

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/api/contacto", response_model=MessageOut)
async def send_message(name: str = Form(...), email: str = Form(...), content: str = Form(...), db: AsyncSession = Depends(get_db)):
    try:
        message = MessageCreate(name=name, email=email, content=content)
        category = classify_message(content)
        msg = await create_message(db, message, category)
        return msg
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="No se pudo almacenar el mensaje, inténtalo más tarde")