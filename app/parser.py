import re
from typing import Dict, List, Tuple

WARNING_PATTERNS = [
    "può contenere", "puo contenere", "può contenere tracce di",
    "tracce di", "may contain", "may contain traces of",
    "prodotto in uno stabilimento che utilizza"
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

def split_warning_section(text: str) -> Tuple[str, str]:
    for pattern in WARNING_PATTERNS:
        idx = text.find(pattern)
        if idx != -1:
            return text[:idx].strip(), text[idx:].strip()
    return text, ""

def tokenize(text: str) -> List[str]:
    parts = re.split(r"\s*,\s*|\s*/\s*", text)
    return [p.strip() for p in parts if p.strip()]

def normalize_token(token: str, dictionary: Dict) -> List[dict]:
    matches = []
    token_lower = token.lower()
    for category, data in dictionary.items():
        for term in data["terms"]:
            if term in token_lower:
                confidence = 1.0 if data["severity"] == "certain" else 0.6
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
    contains_text, warning_text = split_warning_section(cleaned)

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