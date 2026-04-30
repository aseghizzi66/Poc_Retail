from typing import Dict, List, Any
from app.schemas import DecisionResponse

def decide_status(
    parser_result: Dict[str, Any],
    user_blacklist: List[str],
    strict_mode: bool = False
) -> DecisionResponse:
    
    # 1. Normalizziamo la blacklist dell'utente in minuscolo per il confronto
    user_blacklist = [b.lower() for b in user_blacklist]

    contains = parser_result.get("contains_matches", [])
    warnings = parser_result.get("warning_matches", [])
    unknown_tokens = parser_result.get("unknown_tokens", [])
    ingredients_missing = parser_result.get("ingredients_missing", False)

    # 2. Estraiamo le categorie normalizzandole in minuscolo
    # Usiamo un dizionario per mantenere il riferimento tra categoria minuscola e oggetto originale
    contains_map = {m["category"].lower(): m for m in contains}
    warning_map = {m["category"].lower(): m for m in warnings}
    
    contains_categories = set(contains_map.keys())
    warning_categories = set(warning_map.keys())

    matched_reasons = []
    details = []

    # 3. Controllo ingredienti presenti (CONTAINS)
    matches = contains_categories & set(user_blacklist)
    if matches:
        for cat in matches:
            orig_match = contains_map[cat]
            matched_reasons.append(cat)
            details.append({
                "token": orig_match.get("token"), 
                "category": cat, 
                "type": "contains"
            })
            
        return DecisionResponse(
            status="UNSAFE",
            reasons=list(set(matched_reasons)),
            details=details,
            message=f"Contiene {', '.join(set(matched_reasons))}"
        )

    # 4. Controllo tracce (WARNINGS)
    warning_matches = warning_categories & set(user_blacklist)
    if warning_matches:
        for cat in warning_matches:
            orig_match = warning_map[cat]
            matched_reasons.append(cat)
            details.append({
                "token": orig_match.get("token"), 
                "category": cat, 
                "type": "warning"
            })
            
        status = "UNSAFE" if strict_mode else "WARNING"
        return DecisionResponse(
            status=status,
            reasons=list(set(matched_reasons)),
            details=details,
            message=f"Può contenere tracce di {', '.join(set(matched_reasons))}"
        )

    # 5. Gestione dati mancanti
    if ingredients_missing or unknown_tokens:
        return DecisionResponse(
            status="UNKNOWN",
            reasons=[],
            details=[{"token": t} for t in unknown_tokens[:5]],
            message="Dati ingredienti incompleti"
        )

    # 6. Risultato sicuro
    return DecisionResponse(
        status="SAFE",
        reasons=[],
        details=[],
        message="Nessun ingrediente vietato trovato"
    )