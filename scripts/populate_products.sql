#!/usr/bin/env python3
"""
Script per popolare product_ingredients per tutta la POC
Esegue il parser su ogni prodotto presente in tabella products
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.parser import parse_ingredients          # il parser che ti ho fornito prima
from app.models import Dictionary                # se usi ORM, altrimenti usa query diretta

# ====================== CONFIGURAZIONE ======================
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/retail_poc"  # MODIFICA CON I TUOI DATI

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Carica il dizionario una sola volta
def load_dictionary(session):
    rows = session.execute(text("SELECT term, category, severity FROM dictionary")).fetchall()
    dictionary = {}
    for term, category, severity in rows:
        if category not in dictionary:
            dictionary[category] = {"terms": [], "severity": severity}
        dictionary[category]["terms"].append(term.lower())
    return dictionary

# ====================== POPOLAZIONE ======================
def populate_product_ingredients():
    session = Session()
    dictionary = load_dictionary(session)

    # Recupera tutti i prodotti
    products = session.execute(text("""
        SELECT ean, ingredients_raw 
        FROM products 
        ORDER BY ean
    """)).fetchall()

    print(f"✅ Trovati {len(products)} prodotti da parsare...\n")

    inserted = 0
    for ean, raw_text in products:
        if not raw_text:
            continue

        try:
            # Esegui il parser
            parse_result = parse_ingredients(raw_text, dictionary)

            # Cancella eventuali record precedenti
            session.execute(text(
                "DELETE FROM product_ingredients WHERE product_ean = :ean"
            ), {"ean": ean})

            # Inserisci contains_matches
            for m in parse_result.get("contains_matches", []):
                session.execute(text("""
                    INSERT INTO product_ingredients 
                    (product_ean, token_original, ingredient_norm, category, severity, confidence, is_warning)
                    VALUES (:ean, :token, :norm, :cat, :sev, :conf, FALSE)
                """), {
                    "ean": ean,
                    "token": m["token"],
                    "norm": m["token"],
                    "cat": m["category"],
                    "sev": m["severity"],
                    "conf": m["confidence"]
                })

            # Inserisci warning_matches
            for m in parse_result.get("warning_matches", []):
                session.execute(text("""
                    INSERT INTO product_ingredients 
                    (product_ean, token_original, ingredient_norm, category, severity, confidence, is_warning)
                    VALUES (:ean, :token, :norm, :cat, :sev, :conf, TRUE)
                """), {
                    "ean": ean,
                    "token": m["token"],
                    "norm": m["token"],
                    "cat": m["category"],
                    "sev": m["severity"],
                    "conf": m["confidence"]
                })

            inserted += 1
            print(f"✓ {ean} → {len(parse_result.get('contains_matches', [])) + len(parse_result.get('warning_matches', []))} ingredienti parsati")

        except Exception as e:
            print(f"✗ Errore su {ean}: {e}")

    session.commit()
    session.close()

    print(f"\n🎉 POPOLAZIONE COMPLETATA! {inserted} prodotti parsati e salvati in product_ingredients.")


if __name__ == "__main__":
    populate_product_ingredients()