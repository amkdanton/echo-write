-- Migration: Add image support to items table
-- This allows storing images for newsletter items from RSS/YouTube/Twitter

-- Add image columns to items table
ALTER TABLE items 
ADD COLUMN IF NOT EXISTS image_url TEXT,
ADD COLUMN IF NOT EXISTS image_alt TEXT;

-- Add index for better performance when querying items with images
CREATE INDEX IF NOT EXISTS idx_items_image_url ON items(image_url) WHERE image_url IS NOT NULL;

-- Add comment
COMMENT ON COLUMN items.image_url IS 'URL of the featured image for this item (from RSS enclosure, YouTube thumbnail, or Twitter image)';
COMMENT ON COLUMN items.image_alt IS 'Alt text / caption for the image';

