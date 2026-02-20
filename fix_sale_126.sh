#!/bin/bash

export PGPASSWORD='bwjtaUueHturzUv2TuNf'

echo "=== Fixing Sale 126 ==="
psql -h localhost -U alisher_aka_user -d alisher_aka_db << 'EOF'

BEGIN;

-- 1. Add missing Teyes Q8 sale_item
INSERT INTO sale_items (
    sale_id, 
    product_id, 
    quantity, 
    unit_price, 
    total_price,
    cost_price,
    profit,
    source_type,
    source_id,
    created_at
) VALUES (
    126,                    -- sale_id
    144,                    -- product_id (Teyes Q8)
    5.00,                   -- quantity
    37.00,                  -- unit_price
    185.00,                 -- total_price (5 × 37)
    0.00,                   -- cost_price (unknown)
    185.00,                 -- profit (assuming cost is 0 for now)
    'store',                -- source_type
    2,                      -- source_id (Sergeli store)
    '2026-02-08 16:01:35'   -- created_at (same as sale)
);

-- 2. Update sale total_amount (56 + 185 = 241)
UPDATE sales 
SET total_amount = 241.00,
    total_profit = total_profit + 185.00,
    updated_at = NOW()
WHERE id = 126;

-- 3. Reduce Teyes Q8 stock (100 - 5 = 95)
UPDATE store_stocks 
SET quantity = quantity - 5.00
WHERE product_id = 144 
  AND store_id = 2;

-- 4. Log this manual fix in operations_history
INSERT INTO operations_history (
    user_id,
    username,
    operation_type,
    table_name,
    record_id,
    description,
    old_data,
    new_data,
    created_at
)
SELECT 
    u.id,
    u.username,
    'manual_fix',
    'sale_items',
    126,
    'Sale 126 tuzatildi: Teyes Q8 x5 qo''shildi (auto-save failure tufayli)',
    '{"total_amount": 56, "items_count": 1, "stock_teyes_q8": 100}',
    '{"total_amount": 241, "items_count": 2, "stock_teyes_q8": 95}',
    NOW()
FROM users u
WHERE u.username = 'admin'
LIMIT 1;

COMMIT;

-- Verify the fix
SELECT 
    s.id,
    s.total_amount,
    s.cash_usd,
    COUNT(si.id) as items_count,
    SUM(si.total_price) as items_total
FROM sales s
LEFT JOIN sale_items si ON s.id = si.sale_id
WHERE s.id = 126
GROUP BY s.id, s.total_amount, s.cash_usd;

SELECT 'Sale Items:' as info;
SELECT 
    si.id,
    p.name,
    si.quantity,
    si.unit_price,
    si.total_price
FROM sale_items si
JOIN products p ON si.product_id = p.id
WHERE si.sale_id = 126;

SELECT 'Teyes Q8 Stock:' as info;
SELECT quantity 
FROM store_stocks 
WHERE product_id = 144 AND store_id = 2;

EOF
