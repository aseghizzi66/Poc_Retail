import re
from typing import Dict, List

WARNING_PATTERNS = [
    "può contenere", "puo contenere", "può contenere tracce di",
    "tracce di", "may contain", "may contain traces of"
]

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"ingredienti[: ]*", "", text)
    text = re.sub(r"e[\s\-]*(\d{3})", r"e\1", text)
    text = re.sub(r"[%\.\;\:\(\)\[\]]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def tokenize(text: str) -> List[str]:
    parts = re.split(r"\s*,\s*|\s*/\s*", text)
    return [p.strip() for p in parts if p.strip()]

def normalize_token(token: str, dictionary: Dict) -> List[dict]:
    """Matching molto aggressivo"""
    matches = []
    token_lower = " " + token.lower() + " "

    for category, data in dictionary.items():
        for term in data["terms"]:
            term_lower = " " + term.lower() + " "
            if term_lower in token_lower or token_lower in term_lower:
                confidence = 1.0 if data["severity"] == "certain" else 0.7
                matches.append({
                    "token": token,
                    "category": category,
                    "severity": data["severity"],
                    "confidence": confidence
                })
                break
    return matches

def parse_ingredients(raw_text: str, dictionary: Dict) -> Dict:
    if not raw_text:
        return {"status": "UNKNOWN", "contains_matches": [], "warning_matches": [], 
                "unknown_tokens": ["ingredienti mancanti"], "ingredients_missing": True}

    cleaned = clean_text(raw_text)
    contains_text, warning_text = None, None

    for pattern in WARNING_PATTERNS:
        if pattern in cleaned:
            idx = cleaned.find(pattern)
            contains_text = cleaned[:idx].strip()
            warning_text = cleaned[idx:].strip()
            break

    if contains_text is None:
        contains_text = cleaned
        warning_text = ""

    contains_tokens = tokenize(contains_text)
    warning_tokens = tokenize(warning_text)

    contains_matches = []
    warning_matches = []
    unknown_tokens = []

    for token in contains_tokens:
        matches = normalize_token(token, dictionary)
        if matches:
            contains_matches.extend(matches)
        else:
            unknown_tokens.append(token)

    for token in warning_tokens:
        matches = normalize_token(token, dictionary)
        if matches:
            warning_matches.extend(matches)
        else:
            unknown_tokens.append(token)

    return {
        "status": "PROCESSED",
        "contains_matches": contains_matches,
        "warning_matches": warning_matches,
        "unknown_tokens": unknown_tokens,
        "ingredients_missing": False,
        "raw_text": raw_text
    }
