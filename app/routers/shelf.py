from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import ShelfCheckRequest, ShelfCheckResponse, ProductResult
from app.models import ShelfMap, Product, ProductIngredient
from app.decision_engine import decide_status

router = APIRouter(prefix="/shelf", tags=["Totem"])

@router.post("/check", response_model=ShelfCheckResponse)
@router.post("/check/", response_model=ShelfCheckResponse)
async def check_shelf(request: ShelfCheckRequest, db: Session = Depends(get_db)):
    # 1. Recupero lo scaffale
    shelf = db.query(ShelfMap).filter(ShelfMap.shelf_id == request.shelf_id).first()
    
    if not shelf:
        print(f"DEBUG: Scaffale {request.shelf_id} non trovato")
        raise HTTPException(status_code=404, detail="Shelf non trovato")

    # 2. Controllo se ci sono prodotti nello scaffale
    ean_list = shelf.products if isinstance(shelf.products, list) else []
    print(f"DEBUG: Lo scaffale {request.shelf_id} contiene {len(ean_list)} EAN")
    
    safe = []
    warning = []
    unknown = []

    for item in ean_list:
        ean = item.get("ean")
        if not ean: continue
        
        # 3. Cerco il prodotto nel catalogo
        product = db.query(Product).filter(Product.ean == ean).first()
        
        # 4. Cerco gli ingredienti/allergeni nel database
        ingredients = db.query(ProductIngredient).filter(ProductIngredient.product_ean == ean).all()
        print(f"DEBUG: EAN {ean} - Ingredienti trovati nel DB: {len(ingredients)}")
        
        # Costruzione del parser_result per il decision_engine
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
            "ingredients_missing": (len(ingredients) == 0)
        }

        # 5. Eseguo la logica di filtraggio con i filtri dell'utente
        decision = decide_status(parser_result, request.filters, request.strict_mode)
        print(f"DEBUG: EAN {ean} - Status deciso: {decision.status} (Filtri attivi: {request.filters})")

        res_item = ProductResult(
            ean=ean,
            name=product.name if product else "Sconosciuto",
            brand=product.brand if product else "",
            position=item.get("position"),
            shelf_row=item.get("shelf_row"),
            status=decision.status,
            reasons=decision.reasons
        )

        # 6. Distribuzione nelle liste di risposta
        if decision.status == "SAFE":
            safe.append(res_item)
        elif decision.status == "WARNING":
            warning.append(res_item)
        else:
            unknown.append(res_item)

    print(f"DEBUG FINALE: Safe: {len(safe)}, Warning: {len(warning)}, Unknown/Unsafe: {len(unknown)}")

    return ShelfCheckResponse(
        shelf_id=request.shelf_id,
        safe_products=safe,
        warning_products=warning,
        unknown_products=unknown,
        total_products=len(ean_list),
        checked_at=datetime.utcnow().isoformat(),
        message=f"Analizzati {len(ean_list)} prodotti"
    )