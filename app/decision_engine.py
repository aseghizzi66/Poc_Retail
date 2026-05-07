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
            message="Nessun filtro applicato - tutti i prodotti sono sicuri"
        )

    user_blacklist = [b.lower().strip() for b in user_blacklist]

    contains = parser_result.get("contains_matches", [])
    warnings = parser_result.get("warning_matches", [])

    matched_reasons = []
    details = []

    def check_match(item):
        category = str(item.get("category", "")).lower()
        token = str(item.get("token", "")).lower()
        
        for forbidden in user_blacklist:
            if forbidden in category or forbidden in token or category in forbidden or token in forbidden:
                return forbidden
        return None

    # Controllo ingredienti presenti (contains)
    for m in contains:
        found = check_match(m)
        if found:
            matched_reasons.append(found)
            details.append({"token": m.get("token"), "category": m.get("category"), "type": "contains"})

    if matched_reasons:
        return DecisionResponse(
            status="UNSAFE",
            reasons=list(set(matched_reasons)),
            details=details,
            message=f"Contiene {', '.join(set(matched_reasons))}"
        )

    # Controllo tracce (warning)
    for w in warnings:
        found = check_match(w)
        if found:
            matched_reasons.append(found)
            details.append({"token": w.get("token"), "category": w.get("category"), "type": "warning"})

    if matched_reasons:
        status = "UNSAFE" if strict_mode else "WARNING"
        return DecisionResponse(
            status=status,
            reasons=list(set(matched_reasons)),
            details=details,
            message=f"Può contenere tracce di {', '.join(set(matched_reasons))}"
        )

    return DecisionResponse(
        status="SAFE",
        reasons=[],
        details=[],
        message="Nessun ingrediente vietato trovato"
    )