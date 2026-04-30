from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import engine, Base
from app.routers import product, shelf

app = FastAPI(title="POC Retail Totem")

# Monta la cartella static
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi i router
app.include_router(product.router)
app.include_router(shelf.router)

@app.get("/")
async def root():
    return {
        "message": "✅ POC Retail Totem attiva!",
        "totem_interface": "/static/totem.html",
        "docs": "/docs"
    }

# Crea tabelle solo in ambiente locale (opzionale)
if os.getenv("ENV") != "production":
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
