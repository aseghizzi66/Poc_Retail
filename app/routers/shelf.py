from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import ShelfCheckRequest, ShelfCheckResponse, ProductResult
from app.models import ShelfMap, Product, ProductIngredient
from app.decision_engine import decide_status

router = APIRouter(prefix="/shelf", tags=["Totem"])

@router.post("/check", response_model=ShelfCheckResponse)
async def check_shelf(request: ShelfCheckRequest, db: Session = Depends(get_db)):
    # 1. Cerca lo scaffale nel database[cite: 5, 6]
    shelf = db.query(ShelfMap).filter(ShelfMap.shelf_id == request.shelf_id).first()
    
    # DEBUG: Verifica se lo scaffale esiste
    if not shelf:
        print(f"DEBUG ERROR: Scaffale {request.shelf_id} non trovato nel DB")[cite: 6]
        raise HTTPException(status_code=404, detail=f"Shelf {request.shelf_id} non trovato")[cite: 5, 6]

    # 2. Estrai la lista prodotti[cite: 5, 6]
    ean_list = shelf.products or []
    print(f"DEBUG: Scaffale {request.shelf_id} contiene {len(ean_list)} prodotti")[cite: 6]
    
    if not ean_list:
        return ShelfCheckResponse(
            shelf_id=request.shelf_id,
            safe_products=[],
            warning_products=[],
            unknown_products=[],
            total_products=0,
            checked_at=datetime.utcnow().isoformat(),
            message="Lo scaffale è vuoto nel database"[cite: 6]
        )

    safe = []
    warning = []
    unknown = []

    for item in ean_list:
        ean = item.get("ean")
        position = item.get("position")
        shelf_row = item.get("shelf_row")

        # 3. Cerca l'anagrafica prodotto[cite: 5, 6]
        product = db.query(Product).filter(Product.ean == ean).first()
        if not product:
            print(f"DEBUG: Prodotto EAN {ean} non trovato in anagrafica")[cite: 6]
            unknown.append(ProductResult(
                ean=ean, name="Non trovato", brand="", 
                position=position, shelf_row=shelf_row, 
                status="UNKNOWN", reasons=["Prodotto non censito"]
            ))[cite: 5, 6]
            continue

        # 4. Recupera gli ingredienti/allergeni associati[cite: 5, 6]
        ingredients = db.query(ProductIngredient).filter(ProductIngredient.product_ean == ean).all()
        
        # Costruzione del pacchetto dati per il motore di decisione[cite: 5, 6]
        parser_result = {
            "contains_matches": [
                {"token": i.token_original, "category": i.category, "severity": i.severity} 
                for i in ingredients if not i.is_warning
            ],
            "warning_matches": [
                {"token": i.token_original, "category": i.category, "severity": i.severity} 
                for i in ingredients if i.is_warning
            ],
            "unknown_tokens": [],
            "ingredients_missing": len(ingredients) == 0[cite: 5, 6]
        }

        # 5. Applica i filtri utente[cite: 5, 6]
        decision = decide_status(parser_result, request.filters, request.strict_mode)

        result = ProductResult(
            ean=ean,
            name=product.name,
            brand=product.brand or "",
            position=position,
            shelf_row=shelf_row,
            status=decision.status,
            reasons=decision.reasons
        )

        # 6. Smista il prodotto nella categoria corretta[cite: 5, 6]
        if decision.status == "SAFE":
            safe.append(result)[cite: 5, 6]
        elif decision.status == "WARNING":
            warning.append(result)[cite: 5, 6]
        else:
            # Include i casi UNSAFE e quelli con ingredienti mancanti (UNKNOWN)[cite: 5, 6]
            unknown.append(result)[cite: 5, 6]

    print(f"DEBUG RESULT: Safe: {len(safe)}, Warning: {len(warning)}, Unknown/Unsafe: {len(unknown)}")[cite: 6]

    return ShelfCheckResponse(
        shelf_id=request.shelf_id,
        safe_products=safe,
        warning_products=warning,
        unknown_products=unknown,
        total_products=len(ean_list),
        checked_at=datetime.utcnow().isoformat(),
        message=f"Analizzati {len(ean_list)} prodotti"[cite: 5, 6]
    )