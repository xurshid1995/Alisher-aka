-- Mahsulot nomi ustunini 100 belgidan 255 belgiga oshirish
-- Sabab: Uzun nomli mahsulotlar uchun 100 belgi yetarli emas

ALTER TABLE products 
ALTER COLUMN name TYPE VARCHAR(255);

-- Barcode ustunini ham oshiramiz (agar mavjud bo'lsa)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'products' AND column_name = 'barcode'
    ) THEN
        ALTER TABLE products ALTER COLUMN barcode TYPE VARCHAR(255);
    END IF;
END $$;

-- Yangilanish sanasini qo'shamiz
COMMENT ON COLUMN products.name IS 'Mahsulot nomi - maksimal 255 belgi (2026-01-27 da oshirilgan)';
