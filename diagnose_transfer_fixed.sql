-- Transfer muammolarini tekshirish (to'g'rilangan)

-- 1. So'nggi 50 ta transferni ko'rish (dokon 1 ga)
SELECT 
    t.id,
    t.product_id,
    p.name as product_name,
    t.from_location_type,
    t.from_location_id,
    t.to_location_type,
    t.to_location_id,
    t.quantity,
    t.user_name,
    t.created_at
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE t.to_location_type = 'store' AND t.to_location_id = 1
ORDER BY t.created_at DESC
LIMIT 50;

-- 2. Har bir mahsulot uchun transfer qilingan va hozirgi stock
SELECT 
    p.id,
    p.name,
    COALESCE(SUM(t.quantity), 0) as total_transferred,
    COALESCE(ss.quantity, 0) as current_stock,
    COALESCE(SUM(t.quantity), 0) - COALESCE(ss.quantity, 0) as difference
FROM products p
LEFT JOIN transfers t ON p.id = t.product_id 
    AND t.to_location_type = 'store' 
    AND t.to_location_id = 1
LEFT JOIN store_stocks ss ON p.id = ss.product_id AND ss.store_id = 1
WHERE p.id IN (
    SELECT DISTINCT product_id 
    FROM transfers t2 
    WHERE t2.to_location_type = 'store' 
      AND t2.to_location_id = 1
)
GROUP BY p.id, p.name, ss.quantity
HAVING COALESCE(SUM(t.quantity), 0) != COALESCE(ss.quantity, 0)
ORDER BY difference DESC
LIMIT 30;

-- 3. Takroriy transferlarni tekshirish (bir xil mahsulot bir necha marta transfer qilingan)
SELECT 
    t.product_id,
    p.name,
    COUNT(*) as transfer_count,
    SUM(t.quantity) as total_quantity,
    ARRAY_AGG(t.id ORDER BY t.created_at) as transfer_ids,
    ARRAY_AGG(t.quantity ORDER BY t.created_at) as quantities,
    ARRAY_AGG(t.created_at ORDER BY t.created_at) as dates
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE t.to_location_type = 'store' AND t.to_location_id = 1
GROUP BY t.product_id, p.name
HAVING COUNT(*) > 1
ORDER BY transfer_count DESC
LIMIT 20;

-- 4. Stock changes jadvalida transfer yozuvlarini tekshirish
SELECT 
    sc.id,
    sc.product_id,
    p.name,
    sc.location_type,
    sc.location_id,
    sc.new_quantity,
    sc.old_quantity,
    sc.change_type,
    sc.created_at,
    sc.reference_id
FROM stock_changes sc
JOIN products p ON sc.product_id = p.id
WHERE sc.location_type = 'store' 
  AND sc.location_id = 1
  AND sc.change_type = 'transfer'
ORDER BY sc.created_at DESC
LIMIT 50;

-- 5. Transfer qilingan lekin stock_changes da yo'q mahsulotlar
SELECT 
    t.id as transfer_id,
    t.product_id,
    p.name,
    t.quantity,
    t.created_at,
    t.user_name
FROM transfers t
JOIN products p ON t.product_id = p.id
LEFT JOIN stock_changes sc ON 
    sc.reference_id = t.id 
    AND sc.change_type = 'transfer'
    AND sc.product_id = t.product_id
    AND sc.location_type = 'store'
    AND sc.location_id = 1
WHERE t.to_location_type = 'store' 
  AND t.to_location_id = 1
  AND sc.id IS NULL
ORDER BY t.created_at DESC
LIMIT 30;

-- 6. Har bir mahsulot uchun - transfer vs stock_changes vs hozirgi stock
SELECT 
    p.id,
    p.name,
    COALESCE(SUM(t.quantity), 0) as total_transfers,
    COALESCE(SUM(CASE WHEN sc.change_type = 'transfer' THEN sc.new_quantity - COALESCE(sc.old_quantity, 0) END), 0) as stock_changes_total,
    COALESCE(ss.quantity, 0) as current_stock_db,
    COALESCE(SUM(t.quantity), 0) - COALESCE(ss.quantity, 0) as transfer_vs_stock_diff
FROM products p
LEFT JOIN transfers t ON p.id = t.product_id 
    AND t.to_location_type = 'store' 
    AND t.to_location_id = 1
LEFT JOIN stock_changes sc ON p.id = sc.product_id
    AND sc.location_type = 'store'
    AND sc.location_id = 1
LEFT JOIN store_stocks ss ON p.id = ss.product_id AND ss.store_id = 1
WHERE p.id IN (
    SELECT DISTINCT product_id 
    FROM transfers t2 
    WHERE t2.to_location_type = 'store' 
      AND t2.to_location_id = 1
)
GROUP BY p.id, p.name, ss.quantity
ORDER BY transfer_vs_stock_diff DESC
LIMIT 30;
