# Retail POC - Totem Shelf Check

**Soluzione per totem interattivo in corsia supermercato**

## Dopo il deploy su Railway

Esegui questi comandi una volta sola:

```bash
psql $DATABASE_URL -f scripts/populate_dictionary.sql
psql $DATABASE_URL -f scripts/populate_products.sql
psql $DATABASE_URL -f scripts/populate_shelf_map.sql
python scripts/refresh_all.py --force