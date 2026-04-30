from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.static_content import TOTEM_HTML  #

router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem():
    # Usando HTMLResponse, il browser riceve il tipo di contenuto corretto[cite: 1]
    return HTMLResponse(content=TOTEM_HTML)