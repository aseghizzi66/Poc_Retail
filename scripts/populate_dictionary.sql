INSERT INTO dictionary (term, category, severity, is_e_number) VALUES
('grano', 'glutine', 'certain', false),
('frumento', 'glutine', 'certain', false),
('farina di frumento', 'glutine', 'certain', false),
('latte', 'latte', 'certain', false),
('latte scremato', 'latte', 'certain', false),
('caseina', 'latte', 'certain', false),
('soia', 'soia', 'certain', false),
('lecitina di soia', 'soia', 'certain', false),
('e322', 'soia', 'certain', true),
('uova', 'uova', 'certain', false),
('arachidi', 'arachidi', 'certain', false),
('olio di palma', 'olio_palma', 'certain', false),
('lecitina', 'lecitina_generica', 'uncertain', true);
SELECT 'Dictionary popolato' as result;
