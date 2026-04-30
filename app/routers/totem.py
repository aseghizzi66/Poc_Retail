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
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f0f2f5; }}
    .container {{ max-width: 1000px; margin: 40px auto; background: white; border-radius: 16px; 
box-shadow: 0 15px 40px rgba(0,0,0,0.1); }}
    .header {{ background: #2c3e50; color: white; padding: 30px; text-align: center; }}
    .main {{ padding: 40px; }}
    .filter-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 
12px; }}
    .filter-btn {{
      padding: 16px;
      border: 2px solid #ddd;
      background: white;
      border-radius: 12px;
      text-align: center;
      cursor: pointer;
    }}
    .filter-btn.active {{ background: #3498db; color: white; }}
    button {{
      width: 100%;
      padding: 18px;
      margin: 12px 0;
      font-size: 18px;
      border: none;
      border-radius: 12px;
      cursor: pointer;
    }}
    .search-btn {{ background: #27ae60; color: white; }}
    .showall-btn {{ background: #3498db; color: white; }}
    .reset-btn {{ background: #7f8c8d; color: white; }}
    .product {{
      display: flex;
      gap: 15px;
      padding: 15px 0;
      border-bottom: 1px solid #eee;
      align-items: center;
    }}
    .product img {{ width: 75px; height: 75px; border-radius: 10px; object-fit: cover; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🛒 Totem Intelligente</h1>
      <p>Seleziona le tue esigenze alimentari</p>
    </div>
    <div class="main">
      <h3>Cosa vuoi evitare?</h3>
      <div class="filter-grid" id="filters"></div>

      <select id="shelfSelect" style="width:100%; padding:16px; margin:25px 0; font-size:17px;">
        {shelf_options}
      </select>

      <button class="search-btn" onclick="checkShelf()">🔍 Cerca con filtri</button>
      <button class="showall-btn" onclick="showAllProducts()">📋 Mostra tutti i prodotti</button>
      <button class="reset-btn" onclick="resetFilters()">🔄 Reset filtri</button>

      <div id="results" style="margin-top:40px;"></div>
    </div>
  </div>

  <script>
    alert("✅ Totem caricato correttamente!\\n\\nPer ora usa 'Mostra tutti i prodotti' (i filtri sono 
in fase di test).");
    const filtersList = ["latte","glutine","soia","uova","arachidi","olio_palma"];
    let selected = [];

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

    function checkShelf() {{ alert("Funzione filtri in fase di sviluppo."); }}
    function showAllProducts() {{ alert("Mostra tutti i prodotti - Funzione in fase di test."); }}
    function resetFilters() {{ selected = []; renderFilters(); 
document.getElementById('results').innerHTML = ''; }}

    renderFilters();
  </script>
</body>
</html>"""
    return html
