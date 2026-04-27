-- customers jadvaliga last_debt_payment_uzs ustunini qo'shish
-- Maqsad: qarz to'lovida aniq UZS qiymatini saqlash (USD*rate float xatosidan qochish)
ALTER TABLE customers
    ADD COLUMN IF NOT EXISTS last_debt_payment_uzs NUMERIC(15, 2) DEFAULT 0;
