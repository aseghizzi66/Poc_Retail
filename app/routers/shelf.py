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
    shelf = db.query(ShelfMap).filter(ShelfMap.shelf_id == request.shelf_id).first()
    if not shelf:
        raise HTTPException(status_code=404, detail="Scaffale non trovato")

    products_data = shelf.products or []
    if isinstance(products_data, dict):
        products_data = products_data.get("products", [])

    safe = []
    warning = []
    unknown = []

    for item in products_data:
        ean = item.get("ean") if isinstance(item, dict) else str(item)
        if not ean: continue

        product = db.query(Product).filter(Product.ean == ean).first()
        ingredients = db.query(ProductIngredient).filter(ProductIngredient.product_ean == ean).all()

        parser_result = {
            "contains_matches": [{"token": i.token_original or "", "category": i.category or ""} for i in ingredients if not getattr(i, 'is_warning', False)],
            "warning_matches": [{"token": i.token_original or "", "category": i.category or ""} for i in ingredients if getattr(i, 'is_warning', False)],
            "unknown_tokens": [],
            "ingredients_missing": len(ingredients) == 0
        }

        decision = decide_status(parser_result, request.filters or [], getattr(request, 'strict_mode', False))

        res_item = ProductResult(
            ean=ean,
            name=product.name if product else "Sconosciuto",
            brand=product.brand if product else "",
            position=item.get("position") if isinstance(item, dict) else None,
            shelf_row=item.get("shelf_row") if isinstance(item, dict) else None,
            status=decision.status,
            reasons=decision.reasons,
            image_url=product.image_url if product else None
        )

        if decision.status == "SAFE":
            safe.append(res_item)
        elif decision.status == "WARNING":
            warning.append(res_item)
        else:
            unknown.append(res_item)

    return ShelfCheckResponse(
        shelf_id=request.shelf_id,
        safe_products=safe,
        warning_products=warning,
        unknown_products=unknown,
        total_products=len(products_data),
        checked_at=datetime.utcnow().isoformat(),
        message=f"Analizzati {len(products_data)} prodotti"
    )