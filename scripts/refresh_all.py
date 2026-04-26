#!/usr/bin/env python3
"""
refresh_all.py - Versione corretta per Railway
"""

import sys
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from app.models import Product, ProductIngredient
from app.parser import parse_ingredients

# === DATABASE URL DI RAILWAY (hardcoded per evitare problemi) ===
DATABASE_URL = "postgresql://postgres:bjnoaSvAtwHUytGpFayWMWTwDzTqqPpJ@shortline.proxy.rlwy.net:57052/railway"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def parse_and_save_product(db, ean: str):
    product = db.query(Product).filter(Product.ean == ean).first()
    if not product or not product.ingredients_raw:
        return {"status": "SKIP", "ean": ean}

    parse_result = parse_ingredients(product.ingredients_raw, {})

    db.query(ProductIngredient).filter(ProductIngredient.product_ean == ean).delete()

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
    return {"status": "SUCCESS", "ean": ean}

def refresh_all():
    db = Session()
    eans = [row[0] for row in db.query(Product.ean).all()]

    print(f"🔄 Refresh parsing di {len(eans)} prodotti...\n")

    success = 0
    for ean in tqdm(eans, desc="Aggiornamento"):
        try:
            result = parse_and_save_product(db, ean)
            if result["status"] == "SUCCESS":
                success += 1
        except Exception as e:
            print(f"✗ Errore su {ean}: {e}")

    db.close()

    print("\n🎉 REFRESH COMPLETATO!")
    print(f"Prodotti totali: {len(eans)}")
    print(f"Aggiornati con successo: {success}")

if __name__ == "__main__":
    refresh_all()
