from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import product, shelf, totem

# 1. Inizializzazione Database: Crea le tabelle se non esistono[cite: 4]
Base.metadata.create_all(bind=engine)

app = FastAPI(title="POC Retail Totem")

# 2. Configurazione CORS Avanzata
# Specifichiamo gli header per evitare che il browser blocchi le risposte JSON (CORB)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Accept", "Authorization"], # Header espliciti
    expose_headers=["*"],
)

# 3. Inclusione Router Dinamici
# È fondamentale includere i router PRIMA del mount statico per evitare sovrapposizioni
app.include_router(product.router)
app.include_router(shelf.router)
app.include_router(totem.router)

# 4. Mount Statico[cite: 3, 4]
# Montiamo la cartella 'static' senza l'opzione html=True per non scavalcare il router totem
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Punto di ingresso API con link diretti alle funzionalità[cite: 4]"""
    return {
        "message": "✅ POC Retail Totem attiva",
        "totem_url": "/totem/",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    # Avvio standard uvicorn[cite: 4]
    uvicorn.run(app, host="0.0.0.0", port=8000)