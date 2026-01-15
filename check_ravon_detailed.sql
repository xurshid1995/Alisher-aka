-- RAVON dokon (id=7) uchun barcha ma'lumotlar

-- 1. RAVON ga transferlar
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
WHERE t.to_location_type = 'store' AND t.to_location_id = 7
ORDER BY t.created_at DESC
LIMIT 50;

-- 2. RAVON stock changes
SELECT 
    sc.id,
    sc.product_id,
    p.name,
    sc.action,
    sc.quantity,
    sc.user_id,
    sc.change_date,
    sc.notes
FROM stock_changes sc
JOIN products p ON sc.product_id = p.id
WHERE sc.store_id = 7
ORDER BY sc.change_date DESC
LIMIT 50;

-- 3. RAVON hozirgi stocklar
SELECT 
    ss.product_id,
    p.name,
    ss.quantity
FROM store_stocks ss
JOIN products p ON ss.product_id = p.id
WHERE ss.store_id = 7
ORDER BY ss.quantity DESC
LIMIT 50;

-- 4. Transfer qilingan, lekin stock_changes da yo'q
SELECT 
    t.id,
    t.product_id,
    p.name,
    t.quantity,
    t.created_at,
    t.user_name
FROM transfers t
JOIN products p ON t.product_id = p.id
LEFT JOIN stock_changes sc ON 
    sc.product_id = t.product_id
    AND sc.store_id = 7
    AND sc.action = 'transfer'
    AND ABS(sc.quantity - t.quantity) < 0.01
    AND sc.change_date >= t.created_at - INTERVAL '1 minute'
    AND sc.change_date <= t.created_at + INTERVAL '1 minute'
WHERE t.to_location_type = 'store' 
  AND t.to_location_id = 7
  AND sc.id IS NULL
ORDER BY t.created_at DESC;

-- 5. Har mahsulot bo'yicha: Transfer vs Hozirgi Stock
SELECT 
    p.id,
    p.name,
    COALESCE(SUM(t.quantity), 0) as total_transferred,
    COALESCE(ss.quantity, 0) as current_stock,
    COALESCE(SUM(t.quantity), 0) - COALESCE(ss.quantity, 0) as difference
FROM products p
LEFT JOIN transfers t ON p.id = t.product_id 
    AND t.to_location_type = 'store' 
    AND t.to_location_id = 7
LEFT JOIN store_stocks ss ON p.id = ss.product_id AND ss.store_id = 7
WHERE p.id IN (
    SELECT DISTINCT product_id 
    FROM transfers t2 
    WHERE t2.to_location_type = 'store' 
      AND t2.to_location_id = 7
)
GROUP BY p.id, p.name, ss.quantity
HAVING COALESCE(SUM(t.quantity), 0) != COALESCE(ss.quantity, 0)
ORDER BY difference DESC;

-- 6. RAVON ga sotilgan mahsulotlar
SELECT 
    s.id,
    si.product_id,
    p.name,
    si.quantity,
    si.price,
    s.sale_date,
    s.user_name
FROM sales s
JOIN sale_items si ON s.id = si.sale_id
JOIN products p ON si.product_id = p.id
WHERE s.store_id = 7
ORDER BY s.sale_date DESC
LIMIT 50;
