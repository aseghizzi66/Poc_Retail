from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ShelfMap

router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem(db: Session = Depends(get_db)):
    shelves = db.query(ShelfMap).all()
    shelf_options = "".join([f'<option value="{s.shelf_id}">{s.name}</option>' for s in shelves])

    html = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Totem Intelligente</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    body { font-family: 'Inter', Arial, sans-serif; margin: 0; background: #f4f6f9; }
    .container { max-width: 1100px; margin: 40px auto; background: white; border-radius: 20px; box-shadow: 0 15px 50px rgba(0,0,0,0.1); overflow: hidden; }
    .header { background: linear-gradient(90deg, #2c3e50, #3498db); color: white; padding: 35px; text-align: center; }
    .header h1 { margin: 0; font-size: 32px; }
    .main { padding: 40px; }
    .section-title { font-size: 18px; font-weight: 600; color: #2c3e50; margin-bottom: 15px; }
    .filter-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }
    .filter-btn {
      padding: 16px 20px;
      border: 2px solid #e2e8f0;
      background: white;
      border-radius: 12px;
      text-align: center;
      cursor: pointer;
      font-size: 16px;
      transition: all 0.2s;
    }
    .filter-btn:hover { border-color: #3498db; transform: translateY(-2px); }
    .filter-btn.active { background: #3498db; color: white; border-color: #3498db; }
    button {
      width: 100%;
      padding: 18px;
      margin: 12px 0;
      font-size: 18px;
      font-weight: 600;
      border: none;
      border-radius: 12px;
      cursor: pointer;
    }
    .search-btn { background: #27ae60; color: white; }
    .showall-btn { background: #2980b9; color: white; }
    .reset-btn { background: #95a5a6; color: white; }
    .product {
      display: flex;
      align-items: center;
      gap: 18px;
      padding: 15px 0;
      border-bottom: 1px solid #eee;
    }
    .product:last-child { border-bottom: none; }
    .product img { width: 75px; height: 75px; border-radius: 12px; object-fit: cover; }
    .product-info { flex: 1; }
    .product-name { font-weight: 600; font-size: 17px; }
    .product-brand { color: #666; }
    .no-results { text-align: center; padding: 60px 20px; color: #777; font-size: 18px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🛒 Totem Intelligente</h1>
      <p>Seleziona le tue esigenze e scopri i prodotti compatibili</p>
    </div>
    <div class="main">
      <div class="section-title">Cosa vuoi evitare?</div>
      <div class="filter-grid" id="filters"></div>

      <div class="section-title">Scegli lo scaffale</div>
      <select id="shelfSelect" style="width:100%; padding:16px; font-size:17px; border-radius:12px; margin-bottom:25px;">
        """ + shelf_options + """
      </select>

      <button class="search-btn" onclick="checkShelf()">🔍 Cerca con filtri</button>
      <button class="showall-btn" onclick="showAllProducts()">📋 Mostra tutti i prodotti</button>
      <button class="reset-btn" onclick="resetFilters()">🔄 Reset filtri</button>

      <div id="results" style="margin-top:40px;"></div>
    </div>
  </div>

  <script>
    const filtersList = ["latte","glutine","soia","uova","arachidi","olio_palma"];
    let selected = [];

    function renderFilters() {
      const container = document.getElementById('filters');
      container.innerHTML = '';
      filtersList.forEach(f => {
        const btn = document.createElement('div');
        btn.className = `filter-btn ${selected.includes(f) ? 'active' : ''}`;
        btn.textContent = f.charAt(0).toUpperCase() + f.slice(1);
        btn.onclick = () => {
          if (selected.includes(f)) selected = selected.filter(x => x !== f);
          else selected.push(f);
          renderFilters();
        };
        container.appendChild(btn);
      });
    }

    async function checkShelf() {
      const shelfId = document.getElementById('shelfSelect').value;
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '<p style="text-align:center;">Analisi in corso...</p>';

      try {
        const res = await fetch('/shelf/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ shelf_id: shelfId, filters: selected, strict_mode: false })
        });
        const data = await res.json();
        renderResults(data);
      } catch(e) {
        resultsDiv.innerHTML = '<p style="color:red; text-align:center;">Errore di connessione</p>';
      }
    }

    async function showAllProducts() {
      const shelfId = document.getElementById('shelfSelect').value;
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '<p style="text-align:center;">Caricamento di tutti i prodotti...</p>';

      try {
        const res = await fetch('/shelf/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ shelf_id: shelfId, filters: [], strict_mode: false })
        });
        const data = await res.json();
        renderResults(data);
      } catch(e) {
        resultsDiv.innerHTML = '<p style="color:red; text-align:center;">Errore di connessione</p>';
      }
    }

    function renderResults(data) {
      const div = document.getElementById('results');
      let html = `<h3 style="text-align:center;">Risultati per ${data.shelf_id || 'Scaffale'}</h3>`;

      if (data.safe_products && data.safe_products.length > 0) {
        html += `<h4 style="color:#27ae60;">✅ Prodotti Sicuri (${data.safe_products.length})</h4>`;
        data.safe_products.forEach(p => {
          html += `
            <div class="product">
              <img src="https://picsum.photos/id/${Math.floor(Math.random()*300)+1}/75/75" alt="">
              <div class="product-info">
                <div class="product-brand">${p.brand}</div>
                <div class="product-name">${p.name}</div>
              </div>
            </div>`;
        });
      } else {
        html += `<div class="no-results">Nessun prodotto compatibile trovato.<br><br>Prova "Mostra tutti i prodotti"</div>`;
      }
      div.innerHTML = html;
    }

    function resetFilters() {
      selected = [];
      renderFilters();
      document.getElementById('results').innerHTML = '';
    }

    renderFilters();
  </script>
</body>
</html>"""
    return html