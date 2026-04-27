-- Eski savdolardagi noto'g'ri _amount maydonlarini tuzatish
-- Muammo: create_sale funksiyasi _amount da UZS o'rniga USD saqlagan edi
-- Belgi: cash_amount ~= cash_usd (ya'ni UZS * kurs emas, to'g'ridan-to'g'ri USD)

-- 1. Avval tekshirish - nechta savdo ta'sirlangan
SELECT 
    COUNT(*) AS affected_count,
    MIN(id) AS min_id,
    MAX(id) AS max_id
FROM sales
WHERE currency_rate > 100
  AND (
    (cash_usd > 0 AND cash_amount > 0 AND cash_amount < cash_usd * 100)
    OR (click_usd > 0 AND click_amount > 0 AND click_amount < click_usd * 100)
    OR (terminal_usd > 0 AND terminal_amount > 0 AND terminal_amount < terminal_usd * 100)
    OR (debt_usd > 0 AND debt_amount > 0 AND debt_amount < debt_usd * 100)
  );

-- 2. Ta'sirlangan savdolarni ko'rish (tuzatishdan oldin)
SELECT 
    id,
    cash_usd,
    cash_amount AS cash_amount_old,
    ROUND(cash_usd * currency_rate) AS cash_amount_correct,
    click_usd,
    click_amount AS click_amount_old,
    ROUND(click_usd * currency_rate) AS click_amount_correct,
    terminal_usd,
    terminal_amount AS terminal_amount_old,
    ROUND(terminal_usd * currency_rate) AS terminal_amount_correct,
    debt_usd,
    debt_amount AS debt_amount_old,
    ROUND(debt_usd * currency_rate) AS debt_amount_correct,
    currency_rate,
    created_at::date AS date
FROM sales
WHERE currency_rate > 100
  AND (
    (cash_usd > 0 AND cash_amount > 0 AND cash_amount < cash_usd * 100)
    OR (click_usd > 0 AND click_amount > 0 AND click_amount < click_usd * 100)
    OR (terminal_usd > 0 AND terminal_amount > 0 AND terminal_amount < terminal_usd * 100)
    OR (debt_usd > 0 AND debt_amount > 0 AND debt_amount < debt_usd * 100)
  )
ORDER BY id DESC;

-- 3. Tuzatish (tekshirgandan keyin ushbu qatorni ishga tushiring)
UPDATE sales
SET
    cash_amount = CASE 
        WHEN cash_usd > 0 AND cash_amount > 0 AND cash_amount < cash_usd * 100 
        THEN ROUND(cash_usd * currency_rate) 
        ELSE cash_amount 
    END,
    click_amount = CASE 
        WHEN click_usd > 0 AND click_amount > 0 AND click_amount < click_usd * 100 
        THEN ROUND(click_usd * currency_rate) 
        ELSE click_amount 
    END,
    terminal_amount = CASE 
        WHEN terminal_usd > 0 AND terminal_amount > 0 AND terminal_amount < terminal_usd * 100 
        THEN ROUND(terminal_usd * currency_rate) 
        ELSE terminal_amount 
    END,
    debt_amount = CASE 
        WHEN debt_usd > 0 AND debt_amount > 0 AND debt_amount < debt_usd * 100 
        THEN ROUND(debt_usd * currency_rate) 
        ELSE debt_amount 
    END
WHERE currency_rate > 100
  AND (
    (cash_usd > 0 AND cash_amount > 0 AND cash_amount < cash_usd * 100)
    OR (click_usd > 0 AND click_amount > 0 AND click_amount < click_usd * 100)
    OR (terminal_usd > 0 AND terminal_amount > 0 AND terminal_amount < terminal_usd * 100)
    OR (debt_usd > 0 AND debt_amount > 0 AND debt_amount < debt_usd * 100)
  );

-- 4. Tekshirish - tuzatilgan qatorlar soni
SELECT 
    COUNT(*) AS still_wrong
FROM sales
WHERE currency_rate > 100
  AND (
    (cash_usd > 0 AND cash_amount > 0 AND cash_amount < cash_usd * 100)
    OR (click_usd > 0 AND click_amount > 0 AND click_amount < click_usd * 100)
    OR (terminal_usd > 0 AND terminal_amount > 0 AND terminal_amount < terminal_usd * 100)
    OR (debt_usd > 0 AND debt_amount > 0 AND debt_amount < debt_usd * 100)
  );
