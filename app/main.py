from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import product, shelf, totem

# Crea tabelle al boot
Base.metadata.create_all(bind=engine)

app = FastAPI(title="POC Retail Totem")

# 1. Configurazione CORS (Essenziale per evitare CORB)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Inclusione Router
app.include_router(product.router)
app.include_router(shelf.router)
app.include_router(totem.router)

# 3. Mount statico (SOLO per file accessori, non per l'HTML principale)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "✅ POC Retail Totem attiva",
        "totem_url": "/totem/",
        "docs": "/docs"
    }
