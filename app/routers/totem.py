# app/routers/totem.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.static_content import TOTEM_HTML # Importa dal file corretto

router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem():
    # Restituisce la stringa HTML definita in static_content.py[cite: 1, 2]
    return HTMLResponse(content=TOTEM_HTML)
