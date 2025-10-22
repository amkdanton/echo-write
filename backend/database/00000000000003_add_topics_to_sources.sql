-- Migration: Add topic/category to sources
-- This allows users to categorize sources and get topic-based recommendations

-- Add topic column to sources table
ALTER TABLE sources 
ADD COLUMN IF NOT EXISTS topic VARCHAR(100);

-- Add index for better performance when filtering by topic
CREATE INDEX IF NOT EXISTS idx_sources_topic ON sources(topic) WHERE topic IS NOT NULL;

-- Add comment
COMMENT ON COLUMN sources.topic IS 'Topic/category of the source (e.g., technology, business, health, etc.)';

-- Common topics: technology, business, health, science, sports, entertainment, politics, finance, startup, ai, etc.

