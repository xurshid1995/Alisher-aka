-- Sale items va transfer items jadvallariga product_name_snapshot ustuni qo'shish
-- Bu mahsulot o'chirilganda ham tarixda nomi saqlanishi uchun

-- 1. sale_items jadvaliga ustun qo'shish
ALTER TABLE sale_items 
ADD COLUMN IF NOT EXISTS product_name_snapshot VARCHAR(255);

-- 2. transfer_items jadvaliga ustun qo'shish
ALTER TABLE transfer_items 
ADD COLUMN IF NOT EXISTS product_name_snapshot VARCHAR(255);

-- 3. Mavjud ma'lumotlarni yangilash - sale_items
UPDATE sale_items si
SET product_name_snapshot = p.name
FROM products p
WHERE si.product_id = p.id 
  AND si.product_name_snapshot IS NULL;

-- 4. Mavjud ma'lumotlarni yangilash - transfer_items
UPDATE transfer_items ti
SET product_name_snapshot = p.name
FROM products p
WHERE ti.product_id = p.id 
  AND ti.product_name_snapshot IS NULL;

-- 5. Tekshirish - nechta qator yangilandi
SELECT 
    'sale_items' as jadval,
    COUNT(*) as jami,
    COUNT(product_name_snapshot) as snapshot_bor,
    COUNT(*) - COUNT(product_name_snapshot) as snapshot_yoq
FROM sale_items
UNION ALL
SELECT 
    'transfer_items' as jadval,
    COUNT(*) as jami,
    COUNT(product_name_snapshot) as snapshot_bor,
    COUNT(*) - COUNT(product_name_snapshot) as snapshot_yoq
FROM transfer_items;
