-- Transfers jadval strukturasini ko'rish
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'transfers'
ORDER BY ordinal_position;

-- Transfers jadvalidagi ma'lumotlarni ko'rish
SELECT * FROM transfers WHERE to_store_id = 1 ORDER BY created_at DESC LIMIT 10;
