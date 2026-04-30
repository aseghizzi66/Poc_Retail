from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import product, shelf, totem   # ← Import corretto

app = FastAPI(title="POC Retail Totem")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta static (opzionale, lo teniamo per sicurezza)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Includi i router
app.include_router(product.router)
app.include_router(shelf.router)
app.include_router(totem.router)        # ← Ora funziona

@app.get("/")
async def root():
    return {
        "message": "✅ POC Retail Totem attiva",
        "totem_url": "/totem/",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
