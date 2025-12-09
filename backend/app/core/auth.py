from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from itsdangerous import BadSignature
from .config import serializer, ADMIN_USER, ADMIN_PASS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- En producción deberías almacenar el pass encriptado.
# Pero para tu proyecto local es suficiente así:
def verify_admin(username: str, password: str) -> bool:
    return username == ADMIN_USER and password == ADMIN_PASS 

def create_session(username: str):
    return serializer.dumps({"user": username})

def read_session(session_cookie: str):
    try:
        return serializer.loads(session_cookie)
    except BadSignature:
        return None

def require_admin(request: Request):
    session = request.cookies.get("session")
    user = None

    if session:
        user = read_session(session)

    if not user:
        raise HTTPException(status_code=307, headers={"Location": "/admin/login"})

    return user
