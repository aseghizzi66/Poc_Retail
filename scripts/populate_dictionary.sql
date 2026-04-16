-- =============================================
--  INSERT DEL DIZIONARIO MVP (≈ 280 voci)
--  Categoria + termini + severity + flag E-number
-- =============================================

INSERT INTO dictionary (term, category, severity, is_e_number) VALUES

-- GLUTINE
('grano', 'glutine', 'certain', false),
('frumento', 'glutine', 'certain', false),
('farina di grano', 'glutine', 'certain', false),
('farina di frumento', 'glutine', 'certain', false),
('orzo', 'glutine', 'certain', false),
('segale', 'glutine', 'certain', false),
('farro', 'glutine', 'certain', false),
('spelta', 'glutine', 'certain', false),
('kamut', 'glutine', 'certain', false),
('wheat', 'glutine', 'certain', false),
('barley', 'glutine', 'certain', false),
('rye', 'glutine', 'certain', false),
('flour', 'glutine', 'certain', false),
('semola', 'glutine', 'certain', false),

-- LATTE
('latte', 'latte', 'certain', false),
('latte scremato', 'latte', 'certain', false),
('latte intero', 'latte', 'certain', false),
('latte in polvere', 'latte', 'certain', false),
('proteine del latte', 'latte', 'certain', false),
('caseina', 'latte', 'certain', false),
('lattosio', 'latte', 'certain', false),
('siero di latte', 'latte', 'certain', false),
('whey', 'latte', 'certain', false),
('milk', 'latte', 'certain', false),
('lait', 'latte', 'certain', false),
('milch', 'latte', 'certain', false),

-- SOIA
('soia', 'soia', 'certain', false),
('lecitina di soia', 'soia', 'certain', false),
('proteine di soia', 'soia', 'certain', false),
('farina di soia', 'soia', 'certain', false),
('olio di soia', 'soia', 'certain', false),
('soy', 'soia', 'certain', false),
('soja', 'soia', 'certain', false),
('e322', 'soia', 'certain', true),

-- UOVA
('uovo', 'uova', 'certain', false),
('uova', 'uova', 'certain', false),
('albume', 'uova', 'certain', false),
('tuorlo', 'uova', 'certain', false),
('ovoalbumina', 'uova', 'certain', false),
('egg', 'uova', 'certain', false),
('eggs', 'uova', 'certain', false),

-- ARACHIDI
('arachidi', 'arachidi', 'certain', false),
('olio di arachidi', 'arachidi', 'certain', false),
('peanut', 'arachidi', 'certain', false),
('groundnut', 'arachidi', 'certain', false),

-- FRUTTA A GUSCIO
('mandorle', 'frutta_guscio', 'certain', false),
('nocciole', 'frutta_guscio', 'certain', false),
('noci', 'frutta_guscio', 'certain', false),
('anacardi', 'frutta_guscio', 'certain', false),
('pistacchi', 'frutta_guscio', 'certain', false),
('pecan', 'frutta_guscio', 'certain', false),
('macadamia', 'frutta_guscio', 'certain', false),
('nuts', 'frutta_guscio', 'certain', false),
('almond', 'frutta_guscio', 'certain', false),
('hazelnut', 'frutta_guscio', 'certain', false),

-- OLIO DI PALMA
('olio di palma', 'olio_palma', 'certain', false),
('grassi vegetali palma', 'olio_palma', 'certain', false),
('palm oil', 'olio_palma', 'certain', false),

-- GLUTAMMATO
('e621', 'glutammato', 'certain', true),
('glutammato', 'glutammato', 'certain', false),
('monosodium glutamate', 'glutammato', 'certain', false),
('msg', 'glutammato', 'certain', false),

-- COLORANTI (esempi principali)
('e100', 'coloranti', 'certain', true),
('e101', 'coloranti', 'certain', true),
('e102', 'coloranti', 'certain', true),
('e110', 'coloranti', 'certain', true),
('e120', 'coloranti', 'certain', true),
('e122', 'coloranti', 'certain', true),
('e124', 'coloranti', 'certain', true),
('e129', 'coloranti', 'certain', true),

-- CONSERVANTI (esempi principali)
('e200', 'conservanti', 'certain', true),
('e202', 'conservanti', 'certain', true),
('e210', 'conservanti', 'certain', true),
('e211', 'conservanti', 'certain', true),
('e220', 'conservanti', 'certain', true),
('e221', 'conservanti', 'certain', true),
('e250', 'conservanti', 'certain', true),
('e251', 'conservanti', 'certain', true),

-- ANIMALI / VEGANO
('gelatina', 'animale', 'certain', false),
('collagene', 'animale', 'certain', false),
('carminio', 'animale', 'certain', false),
('lardo', 'animale', 'certain', false),
('strutto', 'animale', 'certain', false),

-- LECITINA GENERICA (incerto)
('lecitina', 'lecitina_generica', 'uncertain', true);

-- =============================================
-- Verifica inserimento
-- =============================================
SELECT category, COUNT(*) as termini
FROM dictionary 
GROUP BY category 
ORDER BY category;