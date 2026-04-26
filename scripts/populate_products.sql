INSERT INTO products (ean, name, brand, ingredients_raw, ingredients_normalized, data_quality) VALUES
('8000500310427', 'Biscotti Integrali Classici', 'Mulino Bianco', 'farina di frumento, zucchero, olio di palma, latte scremato in polvere, uova, lievito, sale', '["farina di frumento","zucchero","olio di palma","latte scremato in polvere","uova"]'::jsonb, 'manual'),
('8001234567890', 'Biscotti al Cioccolato', 'Barilla', 'farina di frumento, zucchero, burro, cioccolato 20%, uova, latte intero in polvere', '["farina di frumento","zucchero","burro","cioccolato","uova","latte intero in polvere"]'::jsonb, 'manual'),
('8012345678901', 'Crackers Salati', 'Ritz', 'farina di frumento, olio di palma, sale, lievito', '["farina di frumento","olio di palma","sale"]'::jsonb, 'manual'),
('8009876543211', 'Biscotti al Burro', 'Oreo', 'farina di frumento, zucchero, burro, cacao, lattosio', '["farina di frumento","zucchero","burro","cacao","lattosio"]'::jsonb, 'manual'),
('8004445556667', 'Snack di Mais', 'San Carlo', 'mais 95%, olio di girasole, sale', '["mais","olio di girasole","sale"]'::jsonb, 'manual'),
('8007778889990', 'Patatine Classiche', 'San Carlo', 'patate, olio di palma, sale', '["patate","olio di palma","sale"]'::jsonb, 'manual'),
('8002223334445', 'Snack di Riso', 'Pavesi', 'farina di riso, olio di palma, sale', '["farina di riso","olio di palma","sale"]'::jsonb, 'manual'),
('8005556667778', 'Biscotti Senza Glutine', 'Schar', 'farina di riso, zucchero, olio di girasole, uova, sale', '["farina di riso","zucchero","olio di girasole","uova"]'::jsonb, 'manual'),
('8008889990001', 'Crackers Senza Glutine', 'Schar', 'farina di mais, farina di riso, olio di oliva, sale', '["farina di mais","farina di riso","olio di oliva","sale"]'::jsonb, 'manual'),
('8003334445556', 'Biscotti Vegani Senza Lattosio', 'Pleniday', 'farina di avena, zucchero di canna, olio di cocco, cacao', '["farina di avena","zucchero di canna","olio di cocco","cacao"]'::jsonb, 'manual'),
('8006667778889', 'Snack di Mais Senza Glutine', 'Bio', 'mais, olio di girasole, sale', '["mais","olio di girasole","sale"]'::jsonb, 'manual'),
('8009990001112', 'Biscotti al Cacao Senza Glutine', 'Schar', 'farina di riso, zucchero, olio di girasole, cacao 15%', '["farina di riso","zucchero","olio di girasole","cacao"]'::jsonb, 'manual'),
('8001122334455', 'Crackers Senza Glutine e Senza Latte', 'Schar', 'farina di mais, olio di oliva, sale', '["farina di mais","olio di oliva","sale"]'::jsonb, 'manual'),
('8005566778899', 'Biscotti Senza Glutine e Senza Uova', 'Pleniday', 'farina di riso, zucchero, olio di cocco, lievito', '["farina di riso","zucchero","olio di cocco","lievito"]'::jsonb, 'manual');

SELECT COUNT(*) as total_products FROM products;
