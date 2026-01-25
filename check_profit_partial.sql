-- Qarzli savdolarda foyda tekshirish
SELECT 
    s.id,
    s.total_amount,
    s.total_cost,
    s.total_profit,
    s.payment_status,
    s.currency_rate,
    (s.total_amount - s.total_cost) as calculated_profit,
    -- Har bir item'dan hisoblangan foyda
    (SELECT SUM(si.profit) FROM sale_items si WHERE si.sale_id = s.id) as items_profit_sum
FROM sales s
WHERE s.payment_status IN ('partial', 'debt')
ORDER BY s.id DESC
LIMIT 10;
