from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import engine, Base
from app.routers import product, shelf

# Crea le tabelle automaticamente (solo per POC)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Retail POC - Totem Shelf Check",
    description="Parser ingredienti + Decision Engine + Shelf Check per totem in negozio",
    version="1.0.0"
)

# CORS per test e frontend kiosk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrazione router
app.include_router(product.router)
app.include_router(shelf.router)

@app.get("/")
async def root():
    return {
        "message": "✅ POC Retail Totem attiva e funzionante!",
        "endpoints": {
            "Parser": "/product/parse",
            "Shelf Check (Totem)": "/shelf/check",
            "Docs": "/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)