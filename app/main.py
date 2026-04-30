from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.database import engine, Base
from app.routers import product, shelf, totem

app = FastAPI(title="POC Retail Totem")

# CORS estremamente permissivo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Monta static
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Router
app.include_router(product.router)
app.include_router(shelf.router)
app.include_router(totem.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>✅ POC Retail Totem</h1>
    <p><a href="/totem/">Vai al Totem →</a></p>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
