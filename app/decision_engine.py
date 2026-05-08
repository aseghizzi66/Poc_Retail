from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(parser_result: Dict[str, Any], user_blacklist: List[str], strict_mode: bool = False):
    if not user_blacklist:
        return DecisionResponse(status="SAFE", reasons=[], details=[], message="OK")

    blacklist = [b.lower() for b in user_blacklist]

    # Controlla tutti gli ingredienti
    for item in parser_result.get("contains_matches", []) + parser_result.get("warning_matches", []):
        category = str(item.get("category", "")).lower()
        token = str(item.get("token", "")).lower()

        for forbidden in blacklist:
            if forbidden in category or forbidden in token:
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
        message="Nessun ingrediente vietato"
    )