TOTEM_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Totem Intelligente</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 20px; }
    .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 12px; shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .filter-btn { display: inline-block; padding: 10px; margin: 5px; border: 1px solid #ccc; cursor: pointer; border-radius: 8px; }
    .filter-btn.active { background: #3498db; color: white; border-color: #3498db; }
    .product { border-bottom: 1px solid #eee; padding: 10px 0; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🛒 Totem Intelligente</h1>
    <div id="filters"></div>
    <select id="shelfSelect" style="width:100%; padding:10px; margin: 10px 0;">
        <option value="store_001-A12-R2">Biscotti e Snack - Ripiano 2</option>
        <option value="store_001-A12-R1">Prodotti Free-From - Ripiano 1</option>
    </select>
    <button onclick="checkShelf()" style="width:100%; padding:10px; background:#27ae60; color:white; border:none; border-radius:8px;">Cerca con filtri</button>
    <div id="results"></div>
  </div>

  <script>
    const filtersList = ["latte","glutine","soia","uova","arachidi"];
    let selected = [];

    function renderFilters() {
      const container = document.getElementById('filters');
      container.innerHTML = '';
      filtersList.forEach(f => {
        const btn = document.createElement('div');
        btn.className = `filter-btn ${selected.includes(f) ? 'active' : ''}`;
        btn.textContent = f;
        btn.onclick = () => {
          if (selected.includes(f)) selected = selected.filter(i => i !== f);
          else selected.push(f);
          renderFilters();
        };
        container.appendChild(btn);
      });
    }

    async function checkShelf() {
      const shelfId = document.getElementById('shelfSelect').value;
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = 'Caricamento...';
      try {
        const res = await fetch('/shelf/check', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({shelf_id: shelfId, filters: selected, strict_mode: false})
        });
        const data = await res.json();
        let html = '<h3>Risultati:</h3>';
        data.safe_products.forEach(p => {
          html += `<div class="product"><strong>${p.brand}</strong> - ${p.name}</div>`;
        });
        resultsDiv.innerHTML = html;
      } catch(e) {
        resultsDiv.innerHTML = 'Errore di connessione.';
      }
    }
    renderFilters();
  </script>
</body>
</html>"""