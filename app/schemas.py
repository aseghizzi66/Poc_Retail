from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ParseRequest(BaseModel):
    ean: Optional[str] = None
    ingredients_raw: Optional[str] = None

class MatchItem(BaseModel):
    token: str
    category: str
    severity: str
    confidence: float

class ParseResponse(BaseModel):
    ean: Optional[str]
    status: str
    contains_matches: List[MatchItem]
    warning_matches: List[MatchItem]
    unknown_tokens: List[str]
    ingredients_missing: bool
    raw_text: Optional[str]
    message: Optional[str] = None

class DecisionRequest(BaseModel):
    parser_result: Dict[str, Any]
    user_blacklist: List[str]
    strict_mode: bool = False

class DecisionResponse(BaseModel):
    status: str
    reasons: List[str]
    details: List[dict]
    message: Optional[str] = None

class ShelfCheckRequest(BaseModel):
    shelf_id: str
    filters: List[str]
    strict_mode: bool = False

class ProductResult(BaseModel):
    ean: str
    name: str
    brand: str
    position: Optional[int] = None
    shelf_row: Optional[int] = None
    status: str
    reasons: List[str]

class ShelfCheckResponse(BaseModel):
    shelf_id: str
    safe_products: List[ProductResult]
    warning_products: List[ProductResult]
    unknown_products: List[ProductResult]
    total_products: int
    checked_at: str
    message: Optional[str] = None