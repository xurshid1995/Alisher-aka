-- sale_items jadvaliga unit_price_uzs va total_price_uzs ustunlari qo'shish
-- Maqsad: UZS narxlarni to'g'ridan-to'g'ri saqlash (USD*rate hisoblash xatoligini bartaraf etish)

ALTER TABLE sale_items
    ADD COLUMN IF NOT EXISTS unit_price_uzs NUMERIC(15, 2) DEFAULT 0,
    ADD COLUMN IF NOT EXISTS total_price_uzs NUMERIC(15, 2) DEFAULT 0;

-- Mavjud ma'lumotlarni savdo valyuta kursi yordamida to'ldirish
UPDATE sale_items si
SET
    unit_price_uzs = ROUND(si.unit_price * s.currency_rate),
    total_price_uzs = ROUND(si.total_price * s.currency_rate)
FROM sales s
WHERE si.sale_id = s.id
  AND s.currency_rate IS NOT NULL
  AND s.currency_rate > 0
  AND (si.unit_price_uzs = 0 OR si.unit_price_uzs IS NULL);
