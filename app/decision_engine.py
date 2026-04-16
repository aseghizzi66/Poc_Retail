from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(
    parser_result: Dict[str, Any],
    user_blacklist: List[str],
    strict_mode: bool = False
) -> DecisionResponse:
    contains = parser_result.get("contains_matches", [])
    warnings = parser_result.get("warning_matches", [])
    unknown_tokens = parser_result.get("unknown_tokens", [])
    ingredients_missing = parser_result.get("ingredients_missing", False)

    contains_categories = {m["category"] for m in contains}
    warning_categories = {m["category"] for m in warnings}

    matched_reasons = []
    details = []

    if contains_categories & set(user_blacklist):
        for m in contains:
            if m["category"] in user_blacklist:
                matched_reasons.append(m["category"])
                details.append({"token": m["token"], "category": m["category"], "type": "contains"})
        return DecisionResponse(
            status="UNSAFE",
            reasons=list(set(matched_reasons)),
            details=details,
            message=f"Contiene {', '.join(set(matched_reasons))}"
        )

    if warning_categories & set(user_blacklist):
        for m in warnings:
            if m["category"] in user_blacklist:
                matched_reasons.append(m["category"])
                details.append({"token": m["token"], "category": m["category"], "type": "warning"})
        status = "UNSAFE" if strict_mode else "WARNING"
        return DecisionResponse(
            status=status,
            reasons=list(set(matched_reasons)),
            details=details,
            message=f"Può contenere tracce di {', '.join(set(matched_reasons))}"
        )

    if ingredients_missing or unknown_tokens:
        return DecisionResponse(
            status="UNKNOWN",
            reasons=[],
            details=[{"token": t} for t in unknown_tokens[:5]],
            message="Dati ingredienti incompleti"
        )

    return DecisionResponse(
        status="SAFE",
        reasons=[],
        details=[],
        message="Nessun ingrediente vietato trovato"
    )