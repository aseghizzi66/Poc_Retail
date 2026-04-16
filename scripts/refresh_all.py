#!/usr/bin/env python3
"""
refresh_all.py
========================================
Aggiorna parsing + product_ingredients per TUTTI i prodotti presenti nel DB
Versione completa e robusta per la POC
========================================
"""

import sys
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

# ====================== CONFIGURAZIONE ======================
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/retail_poc"   # ← MODIFICA CON I TUOI DATI

# Opzionale: Redis (se lo usi)
REDIS_URL = "redis://localhost:6379/0"   # commenta se non lo usi

# ====================== IMPORT ======================
from app.parser import parse_ingredients
from app.decision_engine import decide_status
from app.models import Product, ProductIngredient

# ====================== FUNZIONE UNIFICATA ======================
def parse_and_save_product(db, ean: str, force_reparse: bool = False):
    """Versione semplificata della funzione che ti ho dato prima"""
    product = db.query(Product).filter(Product.ean == ean).first()
    if not product or not product.ingredients_raw:
        return {"status": "SKIP", "ean": ean, "reason": "no ingredients"}

    # Se non forziamo e il parsing esiste già → skip
    if not force_reparse:
        existing = db.query(ProductIngredient).filter(
            ProductIngredient.product_ean == ean
        ).first()
        if existing:
            return {"status": "CACHED", "ean": ean}

    # Parsing
    parse_result = parse_ingredients(product.ingredients_raw, {})   # dictionary caricato globalmente

    # Cancella vecchi record
    db.query(ProductIngredient).filter(
        ProductIngredient.product_ean == ean
    ).delete()

    # Salva contains
    for m in parse_result.get("contains_matches", []):
        db.add(ProductIngredient(
            product_ean=ean,
            token_original=m["token"],
            ingredient_norm=m["token"],
            category=m["category"],
            severity=m["severity"],
            confidence=m.get("confidence", 1.0),
            is_warning=False
        ))

    # Salva warning
    for m in parse_result.get("warning_matches", []):
        db.add(ProductIngredient(
            product_ean=ean,
            token_original=m["token"],
            ingredient_norm=m["token"],
            category=m["category"],
            severity=m["severity"],
            confidence=m.get("confidence", 0.8),
            is_warning=True
        ))

    db.commit()
    return {
        "status": "SUCCESS",
        "ean": ean,
        "name": product.name,
        "contains": len(parse_result.get("contains_matches", [])),
        "warning": len(parse_result.get("warning_matches", []))
    }


# ====================== MAIN ======================
def refresh_all(force_reparse: bool = False):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()

    print("🔄 Refresh parsing di tutti i prodotti...\n")

    # Recupera tutti gli EAN
    eans = [row[0] for row in db.query(Product.ean).order_by(Product.ean).all()]
    total = len(eans)

    if total == 0:
        print("❌ Nessun prodotto trovato nel database!")
        db.close()
        sys.exit(1)

    success = 0
    cached = 0
    skipped = 0
    errors = 0

    start_time = time.time()

    for ean in tqdm(eans, desc="Aggiornamento prodotti"):
        try:
            result = parse_and_save_product(db, ean, force_reparse=force_reparse)
            
            if result["status"] == "SUCCESS":
                success += 1
            elif result["status"] == "CACHED":
                cached += 1
            else:
                skipped += 1

        except Exception as e:
            errors += 1
            print(f"\n✗ Errore su {ean}: {e}")

    db.close()
    elapsed = time.time() - start_time

    print("\n" + "="*60)
    print("🎉 REFRESH COMPLETATO!")
    print("="*60)
    print(f"Prodotti totali          : {total}")
    print(f"Aggiornati con successo  : {success}")
    print(f"Già in cache             : {cached}")
    print(f"Skipped                  : {skipped}")
    print(f"Errori                   : {errors}")
    print(f"Tempo impiegato          : {elapsed:.1f} secondi")
    print(f"Media per prodotto       : {elapsed/total:.2f} sec")
    print("="*60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Forza il re-parsing anche se i dati esistono già")
    args = parser.parse_args()

    refresh_all(force_reparse=args.force)