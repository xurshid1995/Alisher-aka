-- Performance Indexes - Xotira va tezlikni oshirish
-- 2026-01-31: Optimizatsiya uchun indexlar

-- Sales jadvalidagi tez-tez ishlatilgan ustunlar
CREATE INDEX IF NOT EXISTS idx_sales_location_date 
ON sales(location_id, location_type, sale_date DESC);

CREATE INDEX IF NOT EXISTS idx_sales_payment_status 
ON sales(payment_status);

CREATE INDEX IF NOT EXISTS idx_sales_customer_date 
ON sales(customer_id, sale_date DESC);

-- Sale items join'i uchun
CREATE INDEX IF NOT EXISTS idx_sale_items_sale_product 
ON sale_items(sale_id, product_id);

-- Operations history uchun
CREATE INDEX IF NOT EXISTS idx_operations_created 
ON operations_history(created_at DESC);

-- Warehouse stocks uchun
CREATE INDEX IF NOT EXISTS idx_warehouse_stocks_product 
ON warehouse_stocks(product_id, warehouse_id);

CREATE INDEX IF NOT EXISTS idx_warehouse_stocks_warehouse 
ON warehouse_stocks(warehouse_id);

-- Store stocks uchun
CREATE INDEX IF NOT EXISTS idx_store_stocks_product 
ON store_stocks(product_id, store_id);

CREATE INDEX IF NOT EXISTS idx_store_stocks_store 
ON store_stocks(store_id);

-- Customers uchun
CREATE INDEX IF NOT EXISTS idx_customers_name 
ON customers(name);

-- Products uchun
CREATE INDEX IF NOT EXISTS idx_products_barcode 
ON products(barcode) WHERE barcode IS NOT NULL;

-- Debt payments uchun
CREATE INDEX IF NOT EXISTS idx_debt_payments_customer 
ON debt_payments(customer_id, payment_date DESC);

CREATE INDEX IF NOT EXISTS idx_debt_payments_sale 
ON debt_payments(sale_id);

-- ANALYZE - statistikani yangilash
ANALYZE sales;
ANALYZE sale_items;
ANALYZE operations_history;
ANALYZE warehouse_stocks;
ANALYZE store_stocks;
ANALYZE products;
ANALYZE customers;
ANALYZE debt_payments;
