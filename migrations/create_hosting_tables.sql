-- ============================================
-- HOSTING TO'LOV TIZIMI TABLOLARI
-- ============================================
-- Yaratilgan: 2026-03-02
-- Ishlatish: psql -U postgres -d sayt_db -f migrations/create_hosting_tables.sql

-- 1. Hosting mijozlar
CREATE TABLE IF NOT EXISTS hosting_clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    telegram_chat_id BIGINT,
    telegram_username VARCHAR(100),
    
    -- DigitalOcean ma'lumotlari
    droplet_id BIGINT,
    droplet_name VARCHAR(200),
    server_ip VARCHAR(50),
    
    -- To'lov ma'lumotlari
    monthly_price_uzs DECIMAL(15, 2) NOT NULL DEFAULT 0,
    payment_day INTEGER DEFAULT 1,
    
    -- Holat
    is_active BOOLEAN DEFAULT TRUE,
    server_status VARCHAR(20) DEFAULT 'active',
    
    -- Vaqtlar
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    notes TEXT
);

-- 2. To'lov buyurtmalari
CREATE TABLE IF NOT EXISTS hosting_payment_orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES hosting_clients(id) ON DELETE CASCADE,
    order_code VARCHAR(20) UNIQUE NOT NULL,
    
    -- To'lov ma'lumotlari
    amount_uzs DECIMAL(15, 2) NOT NULL,
    months INTEGER DEFAULT 1,
    
    -- Status
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    
    -- Card Xabar matching
    card_xabar_amount DECIMAL(15, 2),
    card_xabar_time TIMESTAMP,
    card_xabar_message TEXT,
    
    -- Vaqtlar
    created_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP,
    matched_at TIMESTAMP,
    approved_at TIMESTAMP,
    expires_at TIMESTAMP,
    
    admin_notes TEXT
);

-- 3. Tasdiqlangan to'lovlar
CREATE TABLE IF NOT EXISTS hosting_payments (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES hosting_clients(id) ON DELETE CASCADE,
    order_id INTEGER REFERENCES hosting_payment_orders(id) ON DELETE SET NULL,
    
    -- To'lov ma'lumotlari
    amount_uzs DECIMAL(15, 2) NOT NULL,
    months_paid INTEGER DEFAULT 1,
    payment_date TIMESTAMP DEFAULT NOW(),
    
    -- Davr
    period_start DATE,
    period_end DATE,
    
    -- Tasdiqlash
    confirmed_by VARCHAR(100) DEFAULT 'admin',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexlar
CREATE INDEX IF NOT EXISTS idx_hosting_clients_telegram ON hosting_clients(telegram_chat_id);
CREATE INDEX IF NOT EXISTS idx_hosting_clients_active ON hosting_clients(is_active);
CREATE INDEX IF NOT EXISTS idx_hosting_orders_status ON hosting_payment_orders(status);
CREATE INDEX IF NOT EXISTS idx_hosting_orders_client ON hosting_payment_orders(client_id);
CREATE INDEX IF NOT EXISTS idx_hosting_orders_code ON hosting_payment_orders(order_code);
CREATE INDEX IF NOT EXISTS idx_hosting_payments_client ON hosting_payments(client_id);
CREATE INDEX IF NOT EXISTS idx_hosting_payments_date ON hosting_payments(payment_date);

-- Status uchun CHECK constraint
ALTER TABLE hosting_payment_orders DROP CONSTRAINT IF EXISTS chk_order_status;
ALTER TABLE hosting_payment_orders ADD CONSTRAINT chk_order_status 
    CHECK (status IN ('pending', 'client_confirmed', 'payment_matched', 'approved', 'rejected', 'expired'));

COMMENT ON TABLE hosting_clients IS 'Hosting mijozlari - DigitalOcean serverlar';
COMMENT ON TABLE hosting_payment_orders IS 'To''lov buyurtmalari - 3 bosqichli tekshiruv';
COMMENT ON TABLE hosting_payments IS 'Tasdiqlangan to''lovlar tarixi';
