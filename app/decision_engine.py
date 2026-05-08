from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(
    parser_result: Dict[str, Any],
    user_blacklist: List[str],
    strict_mode: bool = False
) -> DecisionResponse:
    
    if not user_blacklist:
        return DecisionResponse(status="SAFE", reasons=[], details=[], message="Nessun filtro")

    blacklist = [b.lower().strip() for b in user_blacklist]

    contains = parser_result.get("contains_matches", [])
    warnings = parser_result.get("warning_matches", [])

    matched = []

    for item in contains + warnings:
        category = str(item.get("category", "")).lower()
        token = str(item.get("token", "")).lower()

        for forbidden in blacklist:
            if (forbidden in category or 
                forbidden in token or 
                category in forbidden or 
                token in forbidden):
                matched.append(forbidden)
                break

    if matched:
        status = "UNSAFE" if any(m in ["latte", "glutine"] for m in matched) else "WARNING"
        return DecisionResponse(
            status=status,
            reasons=list(set(matched)),
            details=[],
            message=f"Trovato: {', '.join(set(matched))}"
        )

    return DecisionResponse(
        status="SAFE",
        reasons=[],
        details=[],
        message="Nessun match trovato"
    )