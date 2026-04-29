from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ParseRequest, ParseResponse
from app.parser import parse_ingredients
from app.services.product_lookup import ProductLookupService
from app.models import Dictionary

router = APIRouter(prefix="/product", tags=["Parser"])

@router.post("/parse", response_model=ParseResponse)
async def parse_product(request: ParseRequest, db: Session = Depends(get_db)):
    if request.ean:
        lookup = ProductLookupService(db)
        product_data = lookup.get_or_fetch_product(request.ean)
        raw_text = product_data["ingredients_raw"]
    else:
        raw_text = request.ingredients_raw

    if not raw_text:
        raise HTTPException(status_code=400, detail="Nessun testo ingredienti fornito")

    # Carica il dizionario
    rows = db.query(Dictionary).all()
    dictionary = {}
    for row in rows:
        if row.category not in dictionary:
            dictionary[row.category] = {"terms": [], "severity": row.severity}
        dictionary[row.category]["terms"].append(row.term.lower())

    parse_result = parse_ingredients(raw_text, dictionary)

    return ParseResponse(
        ean=request.ean,
        status="PROCESSED",
        contains_matches=parse_result.get("contains_matches", []),
        warning_matches=parse_result.get("warning_matches", []),
        unknown_tokens=parse_result.get("unknown_tokens", []),
        ingredients_missing=parse_result.get("ingredients_missing", False),
        raw_text=raw_text
    )
