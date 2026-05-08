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

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Totem</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin:0; background:#f0f2f5; }}
    .container {{ max-width:1000px; margin:40px auto; background:white; border-radius:16px; box-shadow:0 10px 40px rgba(0,0,0,0.1); }}
    .header {{ background:#2c3e50; color:white; padding:30px; text-align:center; }}
    .main {{ padding:40px; }}
    .filter-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(150px,1fr)); gap:10px; }}
    .filter-btn {{ padding:15px; border:2px solid #ddd; background:white; border-radius:10px; text-align:center; cursor:pointer; }}
    .filter-btn.active {{ background:#3498db; color:white; }}
    button {{ width:100%; padding:16px; margin:10px 0; font-size:17px; border:none; border-radius:10px; cursor:pointer; }}
    .search-btn {{ background:#27ae60; color:white; }}
    .showall-btn {{ background:#2980b9; color:white; }}
    .product {{ display:flex; gap:15px; padding:12px 0; border-bottom:1px solid #eee; }}
    .product img {{ width:70px; height:70px; border-radius:10px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🛒 Totem Intelligente</h1>
    </div>
    <div class="main">
      <h3>Cosa vuoi evitare?</h3>
      <div class="filter-grid" id="filters"></div>

      <select id="shelfSelect" style="width:100%;padding:15px;margin:20px 0;font-size:16px;">
        {shelf_options}
      </select>

      <button class="search-btn" onclick="checkShelf()">🔍 Cerca con filtri</button>
      <button class="showall-btn" onclick="showAllProducts()">📋 Mostra tutti i prodotti</button>
      <button onclick="resetFilters()">🔄 Reset</button>

      <div id="results" style="margin-top:30px;"></div>
    </div>
  </div>

  <script>
    let selected = [];

    const filters = ["latte","glutine","soia","uova","arachidi","olio_palma"];

    function renderFilters() {{
      const div = document.getElementById('filters');
      div.innerHTML = '';
      filters.forEach(f => {{
        const b = document.createElement('div');
        b.className = `filter-btn ${selected.includes(f) ? 'active' : ''}`;
        b.textContent = f;
        b.onclick = () => {{ 
          if (selected.includes(f)) selected = selected.filter(x=>x!==f);
          else selected.push(f);
          renderFilters();
        }};
        div.appendChild(b);
      }});
    }}

    async function checkShelf() {{
      const shelf = document.getElementById('shelfSelect').value;
      const resDiv = document.getElementById('results');
      resDiv.innerHTML = '<p>Caricamento...</p>';

      const resp = await fetch('/shelf/check', {{
        method: 'POST',
        headers: {{'Content-Type':'application/json'}},
        body: JSON.stringify({{shelf_id: shelf, filters: selected, strict_mode: false}})
      }});
      const data = await resp.json();
      renderResults(data);
    }}

    async function showAllProducts() {{
      const shelf = document.getElementById('shelfSelect').value;
      const resDiv = document.getElementById('results');
      resDiv.innerHTML = '<p>Caricamento...</p>';

      const resp = await fetch('/shelf/check', {{
        method: 'POST',
        headers: {{'Content-Type':'application/json'}},
        body: JSON.stringify({{shelf_id: shelf, filters: [], strict_mode: false}})
      }});
      const data = await resp.json();
      renderResults(data);
    }}

    function renderResults(data) {{
      const div = document.getElementById('results');
      let html = `<h3>Risultati (${data.safe_products.length} sicuri)</h3>`;
      data.safe_products.forEach(p => {{
        html += `<div class="product">
          <img src="https://picsum.photos/id/${Math.floor(Math.random()*300)+1}/70/70">
          <div><strong>${p.brand}</strong><br>${p.name}</div>
        </div>`;
      }});
      div.innerHTML = html;
    }}

    function resetFilters() {{
      selected = [];
      renderFilters();
      document.getElementById('results').innerHTML = '';
    }}

    renderFilters();
  </script>
</body>
</html>"""
    return html