from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import product, shelf, totem

# 1. Inizializzazione Database: Crea le tabelle all'avvio
Base.metadata.create_all(bind=engine)

app = FastAPI(title="POC Retail Totem")

# 2. Configurazione CORS
# Questa sezione è vitale per evitare il blocco CORB. 
# Permette al browser di inviare e ricevere JSON in sicurezza.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)

# 3. Inclusione dei Router[cite: 3, 4]
# L'ordine è importante: i router devono essere registrati prima dei file statici.
app.include_router(product.router)
app.include_router(shelf.router)
app.include_router(totem.router)

# 4. Mount dei file statici[cite: 3, 4]
# Rimuoviamo html=True per evitare che il browser preferisca il file fisico totem.html 
# rispetto alla rotta dinamica /totem/ definita nel router.
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Endpoint di benvenuto con i link principali[cite: 3, 4]"""
    return {
        "message": "✅ POC Retail Totem attiva",
        "totem_url": "/totem/",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    # Avvio del server su porta 8000[cite: 3, 4]
    uvicorn.run(app, host="0.0.0.0", port=8000)