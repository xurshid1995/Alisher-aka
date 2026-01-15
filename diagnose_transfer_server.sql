-- Transfer muammolarini tekshirish

-- 1. So'nggi 50 ta transferni ko'rish (dokon 1 ga)
SELECT 
    t.id as transfer_id,
    t.from_warehouse_id,
    t.to_store_id,
    t.created_at,
    ti.product_id,
    p.name as product_name,
    ti.quantity as transferred_qty,
    ti.cost_price
FROM transfers t
JOIN transfer_items ti ON t.id = ti.transfer_id
JOIN products p ON ti.product_id = p.id
WHERE t.to_store_id = 1
ORDER BY t.created_at DESC
LIMIT 50;

-- 2. Har bir mahsulot uchun transfer qilingan va hozirgi stock
SELECT 
    p.id,
    p.name,
    COALESCE(SUM(ti.quantity), 0) as total_transferred,
    COALESCE(ss.quantity, 0) as current_stock,
    COALESCE(SUM(ti.quantity), 0) - COALESCE(ss.quantity, 0) as difference
FROM products p
LEFT JOIN transfer_items ti ON p.id = ti.product_id
LEFT JOIN transfers t ON ti.transfer_id = t.id AND t.to_store_id = 1
LEFT JOIN store_stocks ss ON p.id = ss.product_id AND ss.store_id = 1
WHERE p.id IN (
    SELECT DISTINCT product_id 
    FROM transfer_items ti2 
    JOIN transfers t2 ON ti2.transfer_id = t2.id 
    WHERE t2.to_store_id = 1
)
GROUP BY p.id, p.name, ss.quantity
HAVING COALESCE(SUM(ti.quantity), 0) != COALESCE(ss.quantity, 0)
ORDER BY difference DESC
LIMIT 30;

-- 3. Takroriy transferlarni tekshirish (bir xil mahsulot bir necha marta transfer qilingan)
SELECT 
    ti.product_id,
    p.name,
    COUNT(DISTINCT t.id) as transfer_count,
    SUM(ti.quantity) as total_quantity,
    ARRAY_AGG(t.id ORDER BY t.created_at) as transfer_ids,
    ARRAY_AGG(ti.quantity ORDER BY t.created_at) as quantities
FROM transfers t
JOIN transfer_items ti ON t.id = ti.transfer_id
JOIN products p ON ti.product_id = p.id
WHERE t.to_store_id = 1
GROUP BY ti.product_id, p.name
HAVING COUNT(DISTINCT t.id) > 1
ORDER BY transfer_count DESC
LIMIT 20;

-- 4. Stock changes jadvalida transfer yozuvlarini tekshirish
SELECT 
    sc.id,
    sc.product_id,
    p.name,
    sc.store_id,
    sc.quantity_change,
    sc.change_type,
    sc.created_at,
    sc.reference_id
FROM stock_changes sc
JOIN products p ON sc.product_id = p.id
WHERE sc.store_id = 1 
  AND sc.change_type = 'transfer_in'
ORDER BY sc.created_at DESC
LIMIT 50;

-- 5. Transfer qilingan lekin stock_changes da yo'q mahsulotlar
SELECT 
    t.id as transfer_id,
    ti.product_id,
    p.name,
    ti.quantity,
    t.created_at
FROM transfers t
JOIN transfer_items ti ON t.id = ti.transfer_id
JOIN products p ON ti.product_id = p.id
LEFT JOIN stock_changes sc ON 
    sc.reference_id = t.id 
    AND sc.change_type = 'transfer_in'
    AND sc.product_id = ti.product_id
WHERE t.to_store_id = 1 
  AND sc.id IS NULL
ORDER BY t.created_at DESC
LIMIT 30;
