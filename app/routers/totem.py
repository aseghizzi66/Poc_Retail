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
  <title>Totem Intelligente</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin:0; background:#f0f2f5; }}
    .container {{ max-width:1100px; margin:40px auto; background:white; border-radius:16px; box-shadow:0 10px 40px rgba(0,0,0,0.1); }}
    .header {{ background:#2c3e50; color:white; padding:30px; text-align:center; }}
    .main {{ padding:40px; }}
    .filter-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(150px,1fr)); gap:10px; }}
    .filter-btn {{ padding:15px; border:2px solid #ddd; background:white; border-radius:10px; text-align:center; cursor:pointer; }}
    .filter-btn.active {{ background:#3498db; color:white; }}
    button {{ width:100%; padding:16px; margin:10px 0; font-size:17px; border:none; border-radius:10px; cursor:pointer; }}
    .search-btn {{ background:#27ae60; color:white; }}
    .showall-btn {{ background:#2980b9; color:white; }}
    .product {{ display:flex; flex-direction:column; padding:12px 0; border-bottom:1px solid #eee; }}
    .product-main {{ display:flex; gap:15px; align-items:center; }}
    .product img {{ width:70px; height:70px; border-radius:10px; object-fit:cover; }}
    .toggle-ing {{ background:none; border:none; color:#3498db; font-size:13px; cursor:pointer; padding:4px 0; margin:0; width:auto; text-align:left; }}
    .ingredients {{ display:none; font-size:13px; color:#555; margin-top:6px; padding:8px; background:#f8f9fa; border-radius:6px; line-height:1.5; }}
    .ingredients.visible {{ display:block; }}
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
      <button onclick="resetFilters()">🔄 Reset filtri</button>

      <div id="results" style="margin-top:30px;"></div>
    </div>
  </div>

  <script>
    let selected = [];
    const filtersList = ["latte","glutine","soia","uova","arachidi","olio_palma","zucchero"];

    function renderFilters() {{
      const container = document.getElementById('filters');
      container.innerHTML = '';
      filtersList.forEach(f => {{
        const btn = document.createElement('div');
        btn.className = `filter-btn ${{selected.includes(f) ? 'active' : ''}}`;
        btn.textContent = f.charAt(0).toUpperCase() + f.slice(1);
        btn.onclick = () => {{
          if (selected.includes(f)) selected = selected.filter(x => x !== f);
          else selected.push(f);
          renderFilters();
        }};
        container.appendChild(btn);
      }});
    }}

    async function checkShelf() {{
      const shelfId = document.getElementById('shelfSelect').value;
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '<p>Caricamento...</p>';

      try {{
        const res = await fetch('/shelf/check', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ shelf_id: shelfId, filters: selected, strict_mode: false }})
        }});
        const data = await res.json();
        renderResults(data);
      }} catch(e) {{
        resultsDiv.innerHTML = '<p style="color:red;">Errore di connessione</p>';
      }}
    }}

    async function showAllProducts() {{
      const shelfId = document.getElementById('shelfSelect').value;
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '<p>Caricamento...</p>';

      try {{
        const res = await fetch('/shelf/check', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ shelf_id: shelfId, filters: [], strict_mode: false }})
        }});
        const data = await res.json();
        renderResults(data);
      }} catch(e) {{
        resultsDiv.innerHTML = '<p style="color:red;">Errore di connessione</p>';
      }}
    }}

    function renderResults(data) {{
      const div = document.getElementById('results');
      let html = `<h3>Risultati per ${{data.shelf_id || 'Scaffale'}} (${{data.safe_products ? data.safe_products.length : 0}} sicuri)</h3>`;

      if (data.safe_products && data.safe_products.length > 0) {{
        data.safe_products.forEach((p, idx) => {{
          const imgSrc = p.image_url || `https://picsum.photos/id/${{Math.floor(Math.random()*300)+1}}/70/70`;
          const ingId = `ing-${{idx}}`;
          const ingHtml = p.ingredients_raw
            ? `<button class="toggle-ing" onclick="toggleIng('${{ingId}}')">📋 Ingredienti</button>
               <div class="ingredients" id="${{ingId}}">${{p.ingredients_raw}}</div>`
            : '';
          html += `<div class="product">
            <div class="product-main">
              <img src="${{imgSrc}}" onerror="this.src='https://picsum.photos/id/1/70/70'">
              <div><strong>${{p.brand}}</strong><br>${{p.name}}</div>
            </div>
            ${{ingHtml}}
          </div>`;
        }});
      }} else {{
        html += `<p>Nessun prodotto compatibile trovato.</p>`;
      }}
      div.innerHTML = html;
    }}

    function toggleIng(id) {{
      const el = document.getElementById(id);
      el.classList.toggle('visible');
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