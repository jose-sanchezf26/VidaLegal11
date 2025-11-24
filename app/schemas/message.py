from pydantic import BaseModel, EmailStr

class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    content: str

class MessageOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    content: str

    class Config:
        orm_mode = True
