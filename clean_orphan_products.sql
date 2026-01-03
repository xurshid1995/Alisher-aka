-- Yetim mahsulotlarni topish va o'chirish
-- (hech qanday do'kon yoki omborda mavjud bo'lmagan mahsulotlar)

-- Avval nechta yetim mahsulot borligini ko'rish
SELECT COUNT(*) as yetim_mahsulotlar_soni
FROM product p
WHERE NOT EXISTS (
    SELECT 1 FROM store_stock ss WHERE ss.product_id = p.product_id
)
AND NOT EXISTS (
    SELECT 1 FROM warehouse_stock ws WHERE ws.product_id = p.product_id
);

-- Yetim mahsulotlarni ko'rish
SELECT p.product_id, p.name, p.barcode
FROM product p
WHERE NOT EXISTS (
    SELECT 1 FROM store_stock ss WHERE ss.product_id = p.product_id
)
AND NOT EXISTS (
    SELECT 1 FROM warehouse_stock ws WHERE ws.product_id = p.product_id
)
LIMIT 20;

-- Yetim mahsulotlarni o'chirish
DELETE FROM product p
WHERE NOT EXISTS (
    SELECT 1 FROM store_stock ss WHERE ss.product_id = p.product_id
)
AND NOT EXISTS (
    SELECT 1 FROM warehouse_stock ws WHERE ws.product_id = p.product_id
);
