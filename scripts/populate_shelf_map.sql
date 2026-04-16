-- =============================================
--  POPOLAZIONE SHELF_MAP per la POC
--  2 shelf di esempio (biscotti/snack + free-from)
-- =============================================

INSERT INTO shelf_map (shelf_id, store_id, name, zone, products, last_verified_at, confidence)
VALUES

-- =============================================
-- Shelf 1: Corsia Biscotti & Snack (Ripiano 2)
-- =============================================
(
    'store_001-A12-R2',
    'store_001',
    'Biscotti e snack - Ripiano 2',
    'Corsia 12 - Biscotti',
    '[
        {"ean": "8000500310427", "position": 1, "shelf_row": 2},
        {"ean": "8001234567890", "position": 2, "shelf_row": 2},
        {"ean": "8012345678901", "position": 3, "shelf_row": 2},
        {"ean": "8009876543210", "position": 4, "shelf_row": 2},
        {"ean": "8001112223334", "position": 5, "shelf_row": 2},
        {"ean": "8004445556667", "position": 6, "shelf_row": 2},
        {"ean": "8007778889990", "position": 7, "shelf_row": 2},
        {"ean": "8002223334445", "position": 8, "shelf_row": 2},
        {"ean": "8005556667778", "position": 9, "shelf_row": 2},
        {"ean": "8008889990001", "position": 10, "shelf_row": 2},
        {"ean": "8003334445556", "position": 11, "shelf_row": 2},
        {"ean": "8006667778889", "position": 12, "shelf_row": 2},
        {"ean": "8009990001112", "position": 13, "shelf_row": 2},
        {"ean": "8001122334455", "position": 14, "shelf_row": 2},
        {"ean": "8005566778899", "position": 15, "shelf_row": 2}
    ]'::jsonb,
    NOW(),
    0.95
),

-- =============================================
-- Shelf 2: Corsia Free-From / Senza Glutine (Ripiano 1)
-- =============================================
(
    'store_001-A12-R1',
    'store_001',
    'Prodotti Free-From - Ripiano 1',
    'Corsia 12 - Senza Glutine',
    '[
        {"ean": "8000500310427", "position": 1, "shelf_row": 1},
        {"ean": "8011112223334", "position": 2, "shelf_row": 1},
        {"ean": "8004445556667", "position": 3, "shelf_row": 1},
        {"ean": "8007778889990", "position": 4, "shelf_row": 1},
        {"ean": "8002223334445", "position": 5, "shelf_row": 1},
        {"ean": "8005556667778", "position": 6, "shelf_row": 1},
        {"ean": "8008889990001", "position": 7, "shelf_row": 1},
        {"ean": "8003334445556", "position": 8, "shelf_row": 1},
        {"ean": "8006667778889", "position": 9, "shelf_row": 1},
        {"ean": "8009990001112", "position": 10, "shelf_row": 1},
        {"ean": "8001122334455", "position": 11, "shelf_row": 1},
        {"ean": "8005566778899", "position": 12, "shelf_row": 1},
        {"ean": "8001234567890", "position": 13, "shelf_row": 1},
        {"ean": "8012345678901", "position": 14, "shelf_row": 1},
        {"ean": "8009876543210", "position": 15, "shelf_row": 1}
    ]'::jsonb,
    NOW(),
    0.98
);

-- =============================================
-- Verifica inserimento
-- =============================================
SELECT 
    shelf_id,
    name,
    jsonb_array_length(products) as num_products,
    last_verified_at,
    confidence
FROM shelf_map
ORDER BY shelf_id;