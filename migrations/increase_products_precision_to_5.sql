-- products jadvalidagi USD ustunlar precision ni 4 dan 5 ga oshirish
ALTER TABLE products
    ALTER COLUMN cost_price TYPE NUMERIC(10, 5),
    ALTER COLUMN sell_price TYPE NUMERIC(10, 5);
