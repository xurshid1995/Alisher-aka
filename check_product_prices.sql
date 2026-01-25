-- Products jadvalidan tan narx va sotish narxlarini tekshirish
SELECT 
    id,
    name,
    cost_price,
    sell_price,
    last_batch_cost,
    -- Agar cost_price USD bo'lsa, UZS da qancha
    cost_price * 12500 as if_usd_then_uzs,
    -- Agar cost_price UZS bo'lsa, USD da qancha
    cost_price / 12500 as if_uzs_then_usd
FROM products
WHERE name ILIKE '%diamond%' OR name ILIKE '%kobalt%' OR name ILIKE '%lacetti%'
ORDER BY id DESC
LIMIT 5;
