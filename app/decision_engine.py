from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(
    parser_result: Dict[str, Any],
    user_blacklist: List[str],
    strict_mode: bool = False
) -> DecisionResponse:
    
    if not user_blacklist:
        return DecisionResponse(
            status="SAFE",
            reasons=[],
            details=[],
            message="Nessun filtro applicato"
        )

    # Normalizza blacklist
    blacklist = [b.lower().strip() for b in user_blacklist]

    contains = parser_result.get("contains_matches", [])
    warnings = parser_result.get("warning_matches", [])

    matched = []
    details = []

    def is_match(item):
        if not item:
            return False
        cat = str(item.get("category", "")).lower()
        tok = str(item.get("token", "")).lower()
        
        for forbidden in blacklist:
            if (forbidden in cat or 
                forbidden in tok or 
                cat in forbidden or 
                tok in forbidden or
                forbidden.replace(" ", "") in cat.replace(" ", "") or
                forbidden.replace(" ", "") in tok.replace(" ", "")):
                return True
        return False

    # Controllo ingredienti principali
    for item in contains:
        if is_match(item):
            matched.append(item.get("category") or item.get("token"))
            details.append({"token": item.get("token"), "category": item.get("category"), "type": "contains"})

    if matched:
        return DecisionResponse(
            status="UNSAFE",
            reasons=list(set(matched)),
            details=details,
            message=f"Contiene {', '.join(set(matched))}"
        )

    # Controllo tracce
    for item in warnings:
        if is_match(item):
            matched.append(item.get("category") or item.get("token"))
            details.append({"token": item.get("token"), "category": item.get("category"), "type": "warning"})

    if matched:
        status = "UNSAFE" if strict_mode else "WARNING"
        return DecisionResponse(
            status=status,
            reasons=list(set(matched)),
            details=details,
            message=f"Può contenere tracce di {', '.join(set(matched))}"
        )

    return DecisionResponse(
        status="SAFE",
        reasons=[],
        details=[],
        message="Nessun ingrediente vietato trovato"
    )