-- Migration: Add last_batch tracking columns to products table
-- Date: 2025-12-23
-- Description: Oxirgi partiya ma'lumotlarini saqlash uchun ustunlar qo'shish

-- Ustunlarni qo'shish
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS last_batch_cost DECIMAL(10, 2),
ADD COLUMN IF NOT EXISTS last_batch_date TIMESTAMP;

-- Mavjud mahsulotlar uchun last_batch_cost ni cost_price dan olish
UPDATE products 
SET last_batch_cost = cost_price,
    last_batch_date = created_at
WHERE last_batch_cost IS NULL;

-- Comment qo'shish
COMMENT ON COLUMN products.last_batch_cost IS 'Oxirgi partiya tan narxi';
COMMENT ON COLUMN products.last_batch_date IS 'Oxirgi partiya sanasi';
