import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# Import dei componenti del database
from app.database import engine, Base
from app.routers import product, shelf, totem

# Crea le tabelle nel database all'avvio (se non esistono)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="POC Retail Totem")

# --- CONFIGURAZIONE CORS ---
# Risolve l'errore CORB permettendo la comunicazione tra frontend e backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# --- GESTIONE FILE STATICI ---
# Verifica che la cartella 'static' esista prima di montarla per evitare crash
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# --- INCLUSIONE ROUTER ---
# Assicurati che in questi file tu abbia usato 'router = APIRouter()'
app.include_router(product.router)
app.include_router(shelf.router)
app.include_router(totem.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Pagina di atterraggio rapida"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Retail Totem Backend</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background: 
#f4f4f9; }
                .card { background: white; padding: 20px; border-radius: 10px; display: inline-block; 
shadow: 0 4px 6px rgba(0,0,0,0.1); }
                a { color: #3498db; text-decoration: none; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>✅ Server Attivo</h1>
                <p>Il backend del POC è in esecuzione correttamente.</p>
                <hr>
                <p><a href="/totem/">👉 VAI ALL'INTERFACCIA TOTEM</a></p>
                <p><a href="/docs">📂 Documentazione API (Swagger)</a></p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    # Avvio del server sulla porta 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
