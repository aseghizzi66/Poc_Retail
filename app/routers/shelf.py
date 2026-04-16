from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import ShelfCheckRequest, ShelfCheckResponse, ProductResult
from app.models import ShelfMap, Product, ProductIngredient
from app.decision_engine import decide_status

router = APIRouter(prefix="/shelf", tags=["Totem"])

@router.post("/check", response_model=ShelfCheckResponse)
async def check_shelf(request: ShelfCheckRequest, db: Session = Depends(get_db)):
    shelf = db.query(ShelfMap).filter(ShelfMap.shelf_id == request.shelf_id).first()
    if not shelf or not shelf.products:
        raise HTTPException(status_code=404, detail="Shelf non trovato")

    ean_list = shelf.products
    safe = []
    warning = []
    unknown = []

    for item in ean_list:
        ean = item["ean"]
        position = item.get("position")
        shelf_row = item.get("shelf_row")

        product = db.query(Product).filter(Product.ean == ean).first()
        if not product:
            unknown.append(ProductResult(ean=ean, name="Non trovato", brand="", position=position, shelf_row=shelf_row, status="UNKNOWN", reasons=[]))
            continue

        # Usa parsing pre-computato
        ingredients = db.query(ProductIngredient).filter(ProductIngredient.product_ean == ean).all()
        parser_result = {
            "contains_matches": [{"token": i.token_original, "category": i.category, "severity": i.severity} for i in ingredients if not i.is_warning],
            "warning_matches": [{"token": i.token_original, "category": i.category, "severity": i.severity} for i in ingredients if i.is_warning],
            "unknown_tokens": [],
            "ingredients_missing": False
        }

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

        if decision.status == "SAFE":
            safe.append(result)
        elif decision.status == "WARNING":
            warning.append(result)
        else:
            unknown.append(result)

    return ShelfCheckResponse(
        shelf_id=request.shelf_id,
        safe_products=safe,
        warning_products=warning,
        unknown_products=unknown,
        total_products=len(ean_list),
        checked_at=datetime.utcnow().isoformat(),
        message=f"Analizzati {len(ean_list)} prodotti"
    )