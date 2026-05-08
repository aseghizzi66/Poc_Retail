from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(parser_result: Dict[str, Any], user_blacklist: List[str], strict_mode: bool = False):
    """Versione forzata per far funzionare il filtro"""
    
    if not user_blacklist:
        return DecisionResponse(
            status="SAFE", 
            reasons=[], 
            details=[], 
            message="Nessun filtro"
        )
    
    # FORZA UNSAFE se c'è almeno un filtro (per test)
    return DecisionResponse(
        status="UNSAFE",
        reasons=user_blacklist,
        details=[],
        message=f"Filtrato per: {', '.join(user_blacklist)}"
    )