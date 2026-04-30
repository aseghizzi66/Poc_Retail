from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.static_content import TOTEM_HTML

router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem():
    return TOTEM_HTML
