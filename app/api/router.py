from fastapi import APIRouter
from . import messages, admin

router = APIRouter()

router.include_router(messages.router)
router.include_router(admin.router)
