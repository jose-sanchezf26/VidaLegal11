from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from sqlalchemy import select, delete
from app.schemas.message import MessageCreate
from sqlalchemy.exc import SQLAlchemyError


async def get_all_messages(db: AsyncSession):
    result = await db.execute(select(Message).order_by(Message.created_at.desc()))
    return result.scalars().all()

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
    
async def delete_message(db: AsyncSession, message_id: int):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalars().first()

    if not message:
        return None

    await db.delete(message)
    await db.commit()

    return message