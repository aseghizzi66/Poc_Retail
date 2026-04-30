# app/routers/totem.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.static_content import TOTEM_HTML

router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem():
    # Aggiungiamo esplicitamente il charset per evitare ambiguità nel browser
    return HTMLResponse(content=TOTEM_HTML, status_code=200, media_type="text/html; charset=utf-8")[cite: 1]