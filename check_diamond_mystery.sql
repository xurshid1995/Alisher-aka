-- Diamond mahsulotlarini tekshirish

-- 1. Diamond mahsulotlar qachon yaratilgan
SELECT 
    id,
    name,
    cost_price,
    sell_price,
    created_at
FROM products
WHERE name LIKE 'Diamond%'
ORDER BY id
LIMIT 100;

-- 2. Warehouse dan RAVON ga transferlar (agar bor bo'lsa)
SELECT 
    t.id,
    t.product_id,
    p.name,
    t.quantity,
    t.from_location_type,
    t.from_location_id,
    w.name as from_warehouse,
    t.created_at,
    t.user_name
FROM transfers t
JOIN products p ON t.product_id = p.id
LEFT JOIN warehouses w ON t.from_location_id = w.id AND t.from_location_type = 'warehouse'
WHERE t.to_location_type = 'store' AND t.to_location_id = 7
  AND p.name LIKE 'Diamond%'
ORDER BY t.created_at DESC;

-- 3. Warehouse stocklarni tekshirish - Diamond mahsulotlar uchun
SELECT 
    ws.warehouse_id,
    w.name as warehouse_name,
    ws.product_id,
    p.name as product_name,
    ws.quantity
FROM warehouse_stocks ws
JOIN products p ON ws.product_id = p.id
JOIN warehouses w ON ws.warehouse_id = w.id
WHERE p.name LIKE 'Diamond%'
  AND ws.quantity > 0
ORDER BY ws.warehouse_id, p.id;

-- 4. Barcha transferlarni ko'rish (hamma storelar)
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
ORDER BY t.created_at DESC
LIMIT 100;

-- 5. Store stocks jadvalidagi barcha yozuvlar
SELECT COUNT(*) as total_store_stock_rows FROM store_stocks;

-- 6. Store stocks - barcha store'lar uchun
SELECT 
    ss.store_id,
    s.name as store_name,
    COUNT(ss.product_id) as products_count,
    SUM(ss.quantity) as total_quantity
FROM store_stocks ss
JOIN stores s ON ss.store_id = s.id
GROUP BY ss.store_id, s.name;
