-- Add stock_check_locations column to users table
-- This separates stock check locations from sales allowed_locations

ALTER TABLE users ADD COLUMN IF NOT EXISTS stock_check_locations JSONB DEFAULT '[]'::jsonb;

-- Migrate existing data: users who had stock_check permission
-- copy allowed_locations to stock_check_locations as a starting point
UPDATE users
SET stock_check_locations = allowed_locations
WHERE permissions::jsonb ? 'stock_check'
  AND (stock_check_locations IS NULL OR stock_check_locations = '[]'::jsonb);
