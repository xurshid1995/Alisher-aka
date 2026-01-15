-- TRANSFER MUAMMOSINI TAHLIL QILISH
-- Bu skript transferlar va stok o'zgarishlari o'rtasidagi farqlarni topadi

-- 1. So'nggi 40 kunlik transferlarni ko'rish
SELECT 
    t.id,
    t.created_at AT TIME ZONE 'Asia/Tashkent' as transfer_time,
    p.name as product_name,
    p.barcode,
    t.from_location_type || '_' || t.from_location_id as from_location,
    t.to_location_type || '_' || t.to_location_id as to_location,
    t.quantity,
    t.user_name
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE t.created_at >= NOW() - INTERVAL '40 days'
ORDER BY t.created_at DESC
LIMIT 100;

-- 2. Har bir mahsulot uchun transferlarning umumiy miqdorini ko'rish
SELECT 
    p.name as product_name,
    p.barcode,
    COUNT(t.id) as transfer_count,
    SUM(CASE WHEN t.to_location_type = 'store' THEN t.quantity ELSE 0 END) as to_store_total,
    SUM(CASE WHEN t.from_location_type = 'store' THEN t.quantity ELSE 0 END) as from_store_total,
    SUM(CASE WHEN t.to_location_type = 'warehouse' THEN t.quantity ELSE 0 END) as to_warehouse_total,
    SUM(CASE WHEN t.from_location_type = 'warehouse' THEN t.quantity ELSE 0 END) as from_warehouse_total
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE t.created_at >= NOW() - INTERVAL '40 days'
GROUP BY p.id, p.name, p.barcode
ORDER BY transfer_count DESC
LIMIT 50;

-- 3. Muayyan do'kon uchun transferlarni ko'rish (dokon1 = store_id 1)
SELECT 
    t.created_at AT TIME ZONE 'Asia/Tashkent' as transfer_time,
    p.name as product_name,
    p.barcode,
    CASE 
        WHEN t.from_location_type = 'store' AND t.from_location_id = 1 THEN 'CHIQIM'
        WHEN t.to_location_type = 'store' AND t.to_location_id = 1 THEN 'KIRIM'
    END as direction,
    t.quantity,
    t.from_location_type || '_' || t.from_location_id as from_location,
    t.to_location_type || '_' || t.to_location_id as to_location
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE (t.from_location_id = 1 AND t.from_location_type = 'store')
   OR (t.to_location_id = 1 AND t.to_location_type = 'store')
ORDER BY t.created_at DESC
LIMIT 100;

-- 4. Hozirgi stok miqdorlari va transferlarning umumiy balansini solishtirish
-- Har bir mahsulot va do'kon uchun
WITH transfer_balance AS (
    SELECT 
        t.product_id,
        CASE 
            WHEN t.to_location_type = 'store' THEN t.to_location_id
            WHEN t.from_location_type = 'store' THEN t.from_location_id
        END as store_id,
        SUM(CASE 
            WHEN t.to_location_type = 'store' THEN t.quantity 
            ELSE -t.quantity 
        END) as transfer_net_quantity
    FROM transfers t
    WHERE t.to_location_type = 'store' OR t.from_location_type = 'store'
    GROUP BY t.product_id, 
        CASE 
            WHEN t.to_location_type = 'store' THEN t.to_location_id
            WHEN t.from_location_type = 'store' THEN t.from_location_id
        END
)
SELECT 
    p.name as product_name,
    p.barcode,
    s.name as store_name,
    COALESCE(ss.quantity, 0) as current_stock,
    COALESCE(tb.transfer_net_quantity, 0) as transfer_net,
    COALESCE(ss.quantity, 0) - COALESCE(tb.transfer_net_quantity, 0) as difference
FROM products p
CROSS JOIN stores s
LEFT JOIN store_stocks ss ON ss.product_id = p.id AND ss.store_id = s.id
LEFT JOIN transfer_balance tb ON tb.product_id = p.id AND tb.store_id = s.id
WHERE COALESCE(ss.quantity, 0) != 0 OR COALESCE(tb.transfer_net_quantity, 0) != 0
ORDER BY ABS(COALESCE(ss.quantity, 0) - COALESCE(tb.transfer_net_quantity, 0)) DESC
LIMIT 50;

-- 5. Oxirgi 7 kundagi eng ko'p transfer qilingan mahsulotlar
SELECT 
    p.name as product_name,
    p.barcode,
    COUNT(t.id) as transfer_count,
    SUM(t.quantity) as total_quantity,
    MIN(t.created_at) AT TIME ZONE 'Asia/Tashkent' as first_transfer,
    MAX(t.created_at) AT TIME ZONE 'Asia/Tashkent' as last_transfer
FROM transfers t
JOIN products p ON t.product_id = p.id
WHERE t.created_at >= NOW() - INTERVAL '7 days'
GROUP BY p.id, p.name, p.barcode
ORDER BY transfer_count DESC
LIMIT 20;

-- 6. Transferda ishtirok etgan do'konlar va ombor statistics
SELECT 
    'Store' as location_type,
    s.id as location_id,
    s.name as location_name,
    COUNT(DISTINCT CASE WHEN t.from_location_type = 'store' AND t.from_location_id = s.id THEN t.id END) as outgoing_transfers,
    COUNT(DISTINCT CASE WHEN t.to_location_type = 'store' AND t.to_location_id = s.id THEN t.id END) as incoming_transfers,
    SUM(CASE WHEN t.from_location_type = 'store' AND t.from_location_id = s.id THEN t.quantity ELSE 0 END) as outgoing_quantity,
    SUM(CASE WHEN t.to_location_type = 'store' AND t.to_location_id = s.id THEN t.quantity ELSE 0 END) as incoming_quantity
FROM stores s
LEFT JOIN transfers t ON (t.from_location_id = s.id AND t.from_location_type = 'store')
                      OR (t.to_location_id = s.id AND t.to_location_type = 'store')
WHERE t.created_at >= NOW() - INTERVAL '40 days' OR t.created_at IS NULL
GROUP BY s.id, s.name

UNION ALL

SELECT 
    'Warehouse' as location_type,
    w.id as location_id,
    w.name as location_name,
    COUNT(DISTINCT CASE WHEN t.from_location_type = 'warehouse' AND t.from_location_id = w.id THEN t.id END) as outgoing_transfers,
    COUNT(DISTINCT CASE WHEN t.to_location_type = 'warehouse' AND t.to_location_id = w.id THEN t.id END) as incoming_transfers,
    SUM(CASE WHEN t.from_location_type = 'warehouse' AND t.from_location_id = w.id THEN t.quantity ELSE 0 END) as outgoing_quantity,
    SUM(CASE WHEN t.to_location_type = 'warehouse' AND t.to_location_id = w.id THEN t.quantity ELSE 0 END) as incoming_quantity
FROM warehouses w
LEFT JOIN transfers t ON (t.from_location_id = w.id AND t.from_location_type = 'warehouse')
                      OR (t.to_location_id = w.id AND t.to_location_type = 'warehouse')
WHERE t.created_at >= NOW() - INTERVAL '40 days' OR t.created_at IS NULL
GROUP BY w.id, w.name
ORDER BY location_type, incoming_quantity DESC;
