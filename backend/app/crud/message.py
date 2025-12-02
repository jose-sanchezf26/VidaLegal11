from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.schemas.message import MessageCreate
from sqlalchemy.exc import SQLAlchemyError

async def create_message(db: AsyncSession, message: MessageCreate, category: str):
    new_msg = Message(
        name=message.name,
        email=message.email,
        content=message.content,
        category=category
    )
    db.add(new_msg)
    try:
        await db.commit()
        await db.refresh(new_msg)
        return new_msg
    except SQLAlchemyError as e:
        await db.rollback()
        # Aquí decides: loguear, re-lanzar, devolver None, etc.
        raise e