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
            message="Nessun filtro attivo"
        )

    blacklist = [b.lower().strip() for b in user_blacklist]
    matched = []

    # Controlla sia gli ingredienti presenti che le tracce
    for group_name in ["contains_matches", "warning_matches"]:
        for item in parser_result.get(group_name, []):
            category = str(item.get("category", "")).lower()
            token = str(item.get("token", "")).lower()

            for forbidden in blacklist:
                # Matching intelligente
                if (forbidden in category or 
                    forbidden in token or 
                    category in forbidden or 
                    token in forbidden or
                    forbidden.replace(" ", "") in category.replace(" ", "") or
                    forbidden.replace(" ", "") in token.replace(" ", "")):
                    
                    matched.append(forbidden)
                    break

    if matched:
        status = "UNSAFE" if strict_mode else "WARNING"
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
        message="Nessun ingrediente vietato trovato"
    )