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

    blacklist = [item.lower().strip() for item in user_blacklist]

    # Controlla tutti gli ingredienti (contains + warning)
    for group in ["contains_matches", "warning_matches"]:
        for item in parser_result.get(group, []):
            category = str(item.get("category", "")).lower()
            token = str(item.get("token", "")).lower()

            for forbidden in blacklist:
                if forbidden in category or forbidden in token or category in forbidden or token in forbidden:
                    return DecisionResponse(
                        status="UNSAFE",
                        reasons=[forbidden],
                        details=[],
                        message=f"Contiene {forbidden}"
                    )

    return DecisionResponse(
        status="SAFE",
        reasons=[],
        details=[],
        message="Nessun ingrediente vietato trovato"
    )