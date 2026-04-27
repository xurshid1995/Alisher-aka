-- debt_payments jadvalidagi USD kolonnalarini DECIMAL(12,4) dan DECIMAL(15,10) ga o'zgartirish
ALTER TABLE debt_payments
    ALTER COLUMN cash_usd TYPE DECIMAL(15,10),
    ALTER COLUMN click_usd TYPE DECIMAL(15,10),
    ALTER COLUMN terminal_usd TYPE DECIMAL(15,10),
    ALTER COLUMN total_usd TYPE DECIMAL(15,10);
