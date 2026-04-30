from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.static_content import TOTEM_HTML

# Definiamo il router con il prefisso /totem
router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem():
    """
    Serve la pagina principale del Totem.
    Viene specificato il charset utf-8 e il media_type corretto per 
    prevenire errori di encoding e blocchi CORB.
    """
    return HTMLResponse(
        content=TOTEM_HTML, 
        status_code=200, 
        media_type="text/html; charset=utf-8"
    )