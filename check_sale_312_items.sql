-- Sale #312 ning itemlarini batafsil ko'rish
SELECT 
    si.id,
    p.name as product_name,
    p.cost_price as product_cost_uzs,
    si.quantity,
    si.unit_price as unit_price_saved,
    si.cost_price as cost_price_saved,
    si.total_price,
    si.profit as profit_saved,
    s.currency_rate,
    -- Hisoblangan qiymatlar
    (si.unit_price - si.cost_price) * si.quantity as calculated_profit,
    -- Agar cost_price USD bo'lsa
    si.cost_price * s.currency_rate as cost_in_uzs_if_usd,
    -- Agar cost_price UZS bo'lsa
    si.cost_price / s.currency_rate as cost_in_usd_if_uzs
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN sales s ON si.sale_id = s.id
WHERE si.sale_id = 312;
