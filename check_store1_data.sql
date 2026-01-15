-- Dokon 1 uchun barcha operatsiyalar
SELECT * FROM stock_changes WHERE store_id = 1 ORDER BY change_date DESC LIMIT 30;

-- Transfer action bilan
SELECT 
    sc.*,
    p.name as product_name
FROM stock_changes sc
JOIN products p ON sc.product_id = p.id
WHERE sc.store_id = 1 
  AND sc.action = 'transfer'
ORDER BY sc.change_date DESC
LIMIT 30;

-- Dokon 1 dagi hozirgi stocklar
SELECT 
    ss.product_id,
    p.name,
    ss.quantity,
    ss.store_id
FROM store_stocks ss
JOIN products p ON ss.product_id = p.id
WHERE ss.store_id = 1
ORDER BY ss.quantity DESC
LIMIT 30;

-- Barcha transferlarni ko'rish (dokon 1 ga)
SELECT 
    t.id,
    t.product_id,
    p.name,
    t.quantity,
    t.from_location_type,
    t.from_location_id,
    t.to_location_type,
    t.to_location_id,
    t.user_name,
    t.created_at
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE t.to_location_type = 'store' AND t.to_location_id = 1
ORDER BY t.created_at DESC
LIMIT 50;

-- Barcha storelarni ko'rish
SELECT * FROM stores;
