from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ShelfMap

router = APIRouter(prefix="/totem", tags=["Totem"])

@router.get("/", response_class=HTMLResponse)
async def get_totem(db: Session = Depends(get_db)):
    # Recupera gli scaffali
    shelves = db.query(ShelfMap).all()
    shelf_options = "".join([f'<option value="{s.shelf_id}">{s.name}</option>' for s in shelves])

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Totem - Supermercato</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f4f6f9; }}
    .container {{ max-width: 1100px; margin: 40px auto; background: white; border-radius: 16px; 
box-shadow: 0 15px 35px rgba(0,0,0,0.1); overflow: hidden; }}
    .header {{ background: #2c3e50; color: white; padding: 30px; text-align: center; }}
    .main {{ padding: 40px; }}
    .filters {{ margin-bottom: 30px; }}
    .filter-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 
12px; }}
    .filter-btn {{
      padding: 16px;
      border: 2px solid #ccc;
      background: white;
      border-radius: 12px;
      text-align: center;
      cursor: pointer;
      font-size: 16px;
    }}
    .filter-btn.active {{ background: #3498db; color: white; border-color: #3498db; }}
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
    .showall-btn {{ background: #2980b9; color: white; }}
    .reset-btn {{ background: #7f8c8d; color: white; }}
    .product {{
      display: flex;
      align-items: center;
      gap: 18px;
      padding: 15px 0;
      border-bottom: 1px solid #eee;
    }}
    .product img {{ width: 75px; height: 75px; border-radius: 10px; object-fit: cover; }}
    .product-info {{ flex: 1; }}
    .product-name {{ font-weight: 600; font-size: 17px; }}
    .product-brand {{ color: #555; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🛒 Totem Intelligente</h1>
      <p>Seleziona le tue restrizioni alimentari</p>
    </div>
    <div class="main">
      <div class="filters">
        <h3>Cosa vuoi evitare?</h3>
        <div class="filter-grid" id="filters"></div>
      </div>

      <select id="shelfSelect" style="width:100%; padding:16px; font-size:17px; margin:20px 0; 
border-radius:12px;">
        {shelf_options}
      </select>

      <button class="search-btn" onclick="checkShelf()">🔍 Cerca prodotti compatibili</button>
      <button class="showall-btn" onclick="showAllProducts()">📋 Mostra tutti i prodotti</button>
      <button class="reset-btn" onclick="resetFilters()">🔄 Reset filtri</button>

      <div id="results" style="margin-top:40px;"></div>
    </div>
  </div>

  <script>
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

    function checkShelf() {{ alert("Funzione in fase di test. Usa 'Mostra tutti i prodotti' per ora."); 
}}
    function showAllProducts() {{ alert("Funzione in fase di test."); }}
    function resetFilters() {{ selected = []; renderFilters(); 
document.getElementById('results').innerHTML = ''; }}

    renderFilters();
  </script>
</body>
</html>"""
    return html
