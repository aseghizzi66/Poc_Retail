from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import product, shelf

app = FastAPI(title="POC Retail Totem")

# CORS - Configurazione molto permissiva per POC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Monta i file statici DOPO il middleware CORS
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Router
app.include_router(product.router)
app.include_router(shelf.router)

@app.get("/")
async def root():
    return {
        "message": "✅ POC Retail Totem attiva sul cloud",
        "totem": "/static/totem.html",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
