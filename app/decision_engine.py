from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(parser_result: Dict[str, Any], user_blacklist: List[str], strict_mode: bool = False):
    """Versione ultra-semplice per debug"""
    
    if not user_blacklist:
        return DecisionResponse(status="SAFE", reasons=[], details=[], message="Nessun filtro")

    # Forza UNSAFE se ci sono filtri (per test)
    if user_blacklist:
        return DecisionResponse(
            status="UNSAFE", 
            reasons=user_blacklist,
            details=[],
            message=f"Filtrato per: {', '.join(user_blacklist)}"
        )

    return DecisionResponse(status="SAFE", reasons=[], details=[], message="OK")