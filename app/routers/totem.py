import json
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
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; background: #f0f4f8; min-height: 100vh; }}

    /* HEADER */
    .header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: white; padding: 32px 24px; text-align: center;
    }}
    .header h1 {{ font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }}
    .header p {{ margin-top: 6px; opacity: 0.75; font-size: 15px; }}

    /* LAYOUT */
    .container {{ max-width: 960px; margin: 0 auto; padding: 28px 20px 60px; }}

    /* SECTION LABELS */
    .section-label {{
      font-size: 11px; font-weight: 600; letter-spacing: 1px;
      text-transform: uppercase; color: #94a3b8; margin-bottom: 12px;
    }}

    /* SHELF SELECTOR */
    .shelf-tabs {{ display: flex; gap: 10px; margin-bottom: 28px; flex-wrap: wrap; }}
    .shelf-tab {{
      padding: 10px 20px; border: 2px solid #e2e8f0; border-radius: 50px;
      background: white; cursor: pointer; font-size: 14px; font-weight: 500;
      color: #475569; transition: all .2s;
    }}
    .shelf-tab.active {{
      background: #1a1a2e; border-color: #1a1a2e; color: white;
    }}

    /* FILTER CHIPS */
    .filters-wrap {{ background: white; border-radius: 16px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }}
    .filter-grid {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }}
    .filter-chip {{
      display: flex; align-items: center; gap: 6px;
      padding: 9px 16px; border: 2px solid #e2e8f0; border-radius: 50px;
      background: white; cursor: pointer; font-size: 14px; font-weight: 500;
      color: #475569; transition: all .18s; user-select: none;
    }}
    .filter-chip:hover {{ border-color: #94a3b8; }}
    .filter-chip.active {{
      background: #fee2e2; border-color: #fca5a5; color: #dc2626; font-weight: 600;
    }}
    .filter-chip .chip-icon {{ font-size: 16px; }}
    .active-badge {{
      display: inline-flex; align-items: center; justify-content: center;
      background: #dc2626; color: white; border-radius: 50px;
      font-size: 11px; font-weight: 700; min-width: 20px; height: 20px;
      padding: 0 5px; margin-left: 8px;
    }}

    /* ACTION BUTTONS */
    .actions {{ display: flex; gap: 10px; margin-bottom: 28px; flex-wrap: wrap; }}
    .btn {{
      flex: 1; min-width: 140px; padding: 14px 20px; border: none; border-radius: 12px;
      font-size: 15px; font-weight: 600; cursor: pointer; transition: all .18s;
      display: flex; align-items: center; justify-content: center; gap: 8px;
    }}
    .btn-primary {{ background: #16a34a; color: white; }}
    .btn-primary:hover {{ background: #15803d; }}
    .btn-secondary {{ background: #2563eb; color: white; }}
    .btn-secondary:hover {{ background: #1d4ed8; }}
    .btn-ghost {{ background: white; color: #64748b; border: 2px solid #e2e8f0; }}
    .btn-ghost:hover {{ border-color: #94a3b8; }}

    /* SPINNER */
    .spinner {{
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; padding: 60px; gap: 16px; color: #94a3b8;
    }}
    .spin {{
      width: 40px; height: 40px; border: 4px solid #e2e8f0;
      border-top-color: #2563eb; border-radius: 50%;
      animation: spin .7s linear infinite;
    }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

    /* RESULTS HEADER */
    .results-header {{
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 16px; flex-wrap: wrap; gap: 8px;
    }}
    .results-title {{ font-size: 17px; font-weight: 700; color: #1e293b; }}
    .results-count {{
      background: #dcfce7; color: #16a34a; font-weight: 700;
      font-size: 13px; padding: 4px 12px; border-radius: 50px;
    }}

    /* PRODUCT GRID */
    .product-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }}
    .product-card {{
      background: white; border-radius: 14px; overflow: hidden;
      box-shadow: 0 1px 4px rgba(0,0,0,.07);
      transition: box-shadow .2s, transform .2s;
    }}
    .product-card:hover {{ box-shadow: 0 6px 20px rgba(0,0,0,.12); transform: translateY(-2px); }}
    .card-body {{ display: flex; gap: 14px; padding: 16px; align-items: flex-start; }}
    .card-img {{
      width: 80px; height: 80px; border-radius: 10px;
      object-fit: cover; flex-shrink: 0; background: #f1f5f9;
    }}
    .card-info {{ flex: 1; min-width: 0; }}
    .card-brand {{ font-size: 12px; color: #94a3b8; font-weight: 500; margin-bottom: 3px; }}
    .card-name {{ font-size: 15px; font-weight: 600; color: #1e293b; line-height: 1.3; }}
    .card-footer {{
      border-top: 1px solid #f1f5f9; padding: 10px 16px;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .toggle-btn {{
      background: none; border: none; color: #2563eb; font-size: 13px;
      font-weight: 500; cursor: pointer; padding: 0; display: flex;
      align-items: center; gap: 4px;
    }}
    .toggle-btn svg {{ transition: transform .2s; }}
    .toggle-btn.open svg {{ transform: rotate(180deg); }}
    .ing-panel {{
      max-height: 0; overflow: hidden; transition: max-height .3s ease;
    }}
    .ing-panel.open {{ max-height: 300px; }}
    .ing-text {{
      font-size: 12.5px; color: #64748b; line-height: 1.6;
      padding: 0 16px 14px; border-top: 1px solid #f1f5f9; padding-top: 10px;
    }}

    /* EMPTY STATE */
    .empty-state {{
      text-align: center; padding: 60px 20px; color: #94a3b8;
    }}
    .empty-state .icon {{ font-size: 48px; margin-bottom: 12px; }}
    .empty-state p {{ font-size: 16px; }}

    /* ERROR */
    .error-msg {{
      background: #fee2e2; color: #dc2626; border-radius: 12px;
      padding: 16px; text-align: center; font-weight: 500;
    }}
  </style>
</head>
<body>

  <div class="header">
    <h1>🛒 Totem Intelligente</h1>
    <p>Seleziona le restrizioni alimentari e scopri i prodotti compatibili</p>
  </div>

  <div class="container">

    <!-- SHELF SELECTOR -->
    <div class="section-label">Seleziona il ripiano</div>
    <div class="shelf-tabs" id="shelfTabs"></div>

    <!-- FILTERS -->
    <div class="filters-wrap">
      <div class="section-label" style="margin-bottom:0;">
        Cosa vuoi evitare?
        <span class="active-badge" id="activeBadge" style="display:none"></span>
      </div>
      <div class="filter-grid" id="filters"></div>
    </div>

    <!-- ACTIONS -->
    <div class="actions">
      <button class="btn btn-primary" onclick="checkShelf()">
        <span>🔍</span> Cerca con filtri
      </button>
      <button class="btn btn-secondary" onclick="showAllProducts()">
        <span>📋</span> Mostra tutti
      </button>
      <button class="btn btn-ghost" onclick="resetFilters()">
        <span>🔄</span> Reset
      </button>
    </div>

    <!-- RESULTS -->
    <div id="results"></div>

  </div>

  <script>
    let selected = [];
    let currentShelf = '';

    const filtersList = [
      {{ key: "latte",     icon: "🥛", label: "Latte" }},
      {{ key: "glutine",   icon: "🌾", label: "Glutine" }},
      {{ key: "soia",      icon: "🫘", label: "Soia" }},
      {{ key: "uova",      icon: "🥚", label: "Uova" }},
      {{ key: "arachidi",  icon: "🥜", label: "Arachidi" }},
      {{ key: "olio_palma",icon: "🌴", label: "Olio di palma" }},
      {{ key: "zucchero",  icon: "🍬", label: "Zucchero" }},
    ];

    const shelves = {json.dumps([{"id": s.shelf_id, "name": s.name} for s in shelves])};

    function initShelfTabs() {{
      const container = document.getElementById('shelfTabs');
      shelves.forEach((s, i) => {{
        const tab = document.createElement('div');
        tab.className = 'shelf-tab' + (i === 0 ? ' active' : '');
        tab.textContent = s.name;
        tab.dataset.id = s.id;
        tab.onclick = () => {{
          document.querySelectorAll('.shelf-tab').forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          currentShelf = s.id;
        }};
        container.appendChild(tab);
        if (i === 0) currentShelf = s.id;
      }});
    }}

    function renderFilters() {{
      const container = document.getElementById('filters');
      container.innerHTML = '';
      filtersList.forEach(f => {{
        const chip = document.createElement('div');
        chip.className = 'filter-chip' + (selected.includes(f.key) ? ' active' : '');
        chip.innerHTML = `<span class="chip-icon">${{f.icon}}</span>${{f.label}}`;
        chip.onclick = () => {{
          if (selected.includes(f.key)) selected = selected.filter(x => x !== f.key);
          else selected.push(f.key);
          renderFilters();
        }};
        container.appendChild(chip);
      }});
      const badge = document.getElementById('activeBadge');
      if (selected.length > 0) {{
        badge.style.display = 'inline-flex';
        badge.textContent = selected.length;
      }} else {{
        badge.style.display = 'none';
      }}
    }}

    async function fetchShelf(filters) {{
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = `<div class="spinner"><div class="spin"></div><span>Analisi in corso...</span></div>`;
      try {{
        const res = await fetch('/shelf/check', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ shelf_id: currentShelf, filters, strict_mode: false }})
        }});
        const data = await res.json();
        renderResults(data, filters.length > 0);
      }} catch(e) {{
        resultsDiv.innerHTML = `<div class="error-msg">⚠️ Errore di connessione. Riprova.</div>`;
      }}
    }}

    function checkShelf()    {{ fetchShelf(selected); }}
    function showAllProducts() {{ fetchShelf([]); }}

    function renderResults(data, filtered) {{
      const div = document.getElementById('results');
      const products = data.safe_products || [];
      const shelfName = shelves.find(s => s.id === data.shelf_id)?.name || data.shelf_id;

      let html = `<div class="results-header">
        <div class="results-title">${{shelfName}}</div>
        <div class="results-count">${{products.length}} ${{filtered ? 'compatibili' : 'prodotti'}}</div>
      </div>`;

      if (products.length === 0) {{
        html += `<div class="empty-state">
          <div class="icon">🔍</div>
          <p>Nessun prodotto compatibile con i filtri selezionati.</p>
        </div>`;
      }} else {{
        html += `<div class="product-grid">`;
        products.forEach((p, idx) => {{
          const imgSrc = p.image_url || `https://picsum.photos/id/${{(idx % 50) + 1}}/80/80`;
          const ingId = `ing-${{idx}}`;
          const hasIng = !!p.ingredients_raw;
          html += `
          <div class="product-card">
            <div class="card-body">
              <img class="card-img" src="${{imgSrc}}" onerror="this.src='https://images.openfoodfacts.org/images/icons/dist/packaging.svg'" alt="${{p.name}}">
              <div class="card-info">
                <div class="card-brand">${{p.brand || ''}}</div>
                <div class="card-name">${{p.name}}</div>
              </div>
            </div>
            ${{hasIng ? `
            <div class="card-footer">
              <button class="toggle-btn" id="btn-${{ingId}}" onclick="toggleIng('${{ingId}}')">
                📋 Ingredienti
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </button>
            </div>
            <div class="ing-panel" id="${{ingId}}">
              <div class="ing-text">${{p.ingredients_raw}}</div>
            </div>` : ''}}
          </div>`;
        }});
        html += `</div>`;
      }}
      div.innerHTML = html;
    }}

    function toggleIng(id) {{
      const panel = document.getElementById(id);
      const btn = document.getElementById('btn-' + id);
      panel.classList.toggle('open');
      btn.classList.toggle('open');
    }}

    function resetFilters() {{
      selected = [];
      renderFilters();
      document.getElementById('results').innerHTML = '';
    }}

    initShelfTabs();
    renderFilters();
  </script>
</body>
</html>"""
    return html