from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ShelfMap

# Usiamo APIRouter, NON FastAPI() qui dentro
router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem(db: Session = Depends(get_db)):
    shelves = db.query(ShelfMap).all()
    
    # Generazione dinamica delle opzioni della select
    shelf_options = "".join([f'<option value="{s.shelf_id}">{s.name}</option>' for s in shelves])

    html_template = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Totem Intelligente</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: 
#f4f7f6; color: #333; }
    .container { max-width: 800px; margin: 40px auto; background: white; border-radius: 20px; 
box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; }
    .header { background: #2c3e50; color: white; padding: 40px 20px; text-align: center; }
    .main { padding: 30px; }
    .filter-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 
15px; margin-bottom: 30px; }
    .filter-btn {
      padding: 15px; border: 2px solid #e0e0e0; background: white; border-radius: 12px;
      text-align: center; cursor: pointer; transition: all 0.3s; font-weight: 600;
    }
    .filter-btn.active { background: #3498db; color: white; border-color: #3498db; transform: 
scale(1.05); }
    select { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid #ddd; font-size: 16px; 
margin-bottom: 20px; }
    button {
      width: 100%; padding: 15px; margin: 10px 0; font-size: 16px; border: none;
      border-radius: 10px; cursor: pointer; font-weight: bold; transition: opacity 0.2s;
    }
    .search-btn { background: #27ae60; color: white; }
    .reset-btn { background: #e74c3c; color: white; }
    #results { margin-top: 30px; padding: 20px; border-top: 1px solid #eee; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🛒 Totem Smart Shop</h1>
      <p>Configura i tuoi filtri alimentari</p>
    </div>
    <div class="main">
      <h3>Escludi ingredienti:</h3>
      <div class="filter-grid" id="filters"></div>

      <label>Seleziona Scaffale:</label>
      <select id="shelfSelect">
        {{SHELF_OPTIONS}}
      </select>

      <button class="search-btn" onclick="checkShelf()">🔍 Avvia Ricerca</button>
      <button class="reset-btn" onclick="resetFilters()">🔄 Reset</button>

      <div id="results"></div>
    </div>
  </div>

  <script>
    const filtersList = ["latte", "glutine", "soia", "uova", "arachidi"];
    let selected = [];

    function renderFilters() {
      const container = document.getElementById('filters');
      container.innerHTML = '';
      filtersList.forEach(f => {
        const btn = document.createElement('div');
        btn.className = `filter-btn ${selected.includes(f) ? 'active' : ''}`;
        btn.textContent = f.toUpperCase();
        btn.onclick = () => {
          if (selected.includes(f)) selected = selected.filter(x => x !== f);
          else selected.push(f);
          renderFilters();
        };
        container.appendChild(btn);
      });
    }

    function resetFilters() {
      selected = [];
      renderFilters();
      document.getElementById('results').innerHTML = '';
    }

    async function checkShelf() {
      const shelfId = document.getElementById('shelfSelect').value;
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = `<p>Cerco prodotti nello scaffale <b>${shelfId}</b> senza: 
<b>${selected.join(', ') || 'nessun filtro'}</b>...</p>`;
      
      // Esempio di chiamata fetch futura:
      // const response = await fetch(`/api/products?shelf=${shelfId}&exclude=${selected.join(',')}`);
    }

    renderFilters();
  </script>
</body>
</html>"""
    
    return html_template.replace("{{SHELF_OPTIONS}}", shelf_options)
