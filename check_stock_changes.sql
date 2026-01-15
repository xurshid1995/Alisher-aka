-- Stock changes strukturasini ko'rish
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'stock_changes'
ORDER BY ordinal_position;

-- Dokon 1 uchun stock changes
SELECT * FROM stock_changes WHERE store_id = 1 ORDER BY created_at DESC LIMIT 20;
