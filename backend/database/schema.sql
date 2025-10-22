-- EchoWrite Database Schema
-- This file contains the complete database schema for Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS TABLE
-- ============================================
-- Note: Supabase Auth handles user authentication
-- We'll reference auth.users(id) for user relations

-- ============================================
-- USER PROFILES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL UNIQUE,
  full_name TEXT,
  timezone TEXT DEFAULT 'UTC',
  voice_traits JSONB DEFAULT '[]'::jsonb,
  preferences JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- SOURCES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('rss', 'youtube', 'twitter', 'web')),
  handle TEXT NOT NULL, -- URL for RSS, channel ID for YouTube, handle for Twitter
  name TEXT,
  is_active BOOLEAN DEFAULT true,
  fetch_frequency INTEGER DEFAULT 3600, -- in seconds
  last_fetched_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sources_user_id ON sources(user_id);
CREATE INDEX idx_sources_type ON sources(type);
CREATE INDEX idx_sources_is_active ON sources(is_active);

-- ============================================
-- ITEMS TABLE (fetched content)
-- ============================================
CREATE TABLE IF NOT EXISTS items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  summary TEXT,
  url TEXT NOT NULL,
  content TEXT,
  author TEXT,
  published_at TIMESTAMPTZ,
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  trend_score DECIMAL(5,4) DEFAULT 0.0,
  keywords JSONB DEFAULT '[]'::jsonb,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_items_source_id ON items(source_id);
CREATE INDEX idx_items_user_id ON items(user_id);
CREATE INDEX idx_items_published_at ON items(published_at DESC);
CREATE INDEX idx_items_trend_score ON items(trend_score DESC);
CREATE INDEX idx_items_url ON items(url); -- for deduplication
CREATE UNIQUE INDEX idx_items_unique_url_user ON items(url, user_id);

-- ============================================
-- STYLE SAMPLES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS style_samples (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  title TEXT,
  content TEXT NOT NULL,
  source_type TEXT CHECK (source_type IN ('newsletter', 'blog', 'post', 'other')),
  extracted_traits JSONB DEFAULT '[]'::jsonb,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_style_samples_user_id ON style_samples(user_id);
CREATE INDEX idx_style_samples_is_active ON style_samples(is_active);

-- ============================================
-- DRAFTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS drafts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  title TEXT,
  body_md TEXT NOT NULL,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'published', 'archived')),
  generation_metadata JSONB DEFAULT '{}'::jsonb, -- stores LLM params, item IDs used, etc.
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_drafts_user_id ON drafts(user_id);
CREATE INDEX idx_drafts_status ON drafts(status);
CREATE INDEX idx_drafts_created_at ON drafts(created_at DESC);

-- ============================================
-- DRAFT ITEMS (junction table)
-- ============================================
CREATE TABLE IF NOT EXISTS draft_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  draft_id UUID NOT NULL REFERENCES drafts(id) ON DELETE CASCADE,
  item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  position INTEGER, -- order in the newsletter
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_draft_items_draft_id ON draft_items(draft_id);
CREATE INDEX idx_draft_items_item_id ON draft_items(item_id);
CREATE UNIQUE INDEX idx_draft_items_unique ON draft_items(draft_id, item_id);

-- ============================================
-- FEEDBACK TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS feedback (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  draft_id UUID NOT NULL REFERENCES drafts(id) ON DELETE CASCADE,
  reaction TEXT CHECK (reaction IN ('👍', '👎', 'positive', 'negative')),
  notes TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feedback_user_id ON feedback(user_id);
CREATE INDEX idx_feedback_draft_id ON feedback(draft_id);
CREATE INDEX idx_feedback_reaction ON feedback(reaction);

-- ============================================
-- DELIVERY LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS delivery_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  draft_id UUID NOT NULL REFERENCES drafts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  recipient_email TEXT NOT NULL,
  delivery_status TEXT DEFAULT 'pending' CHECK (delivery_status IN ('pending', 'sent', 'failed', 'bounced')),
  provider_response JSONB DEFAULT '{}'::jsonb,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_delivery_logs_draft_id ON delivery_logs(draft_id);
CREATE INDEX idx_delivery_logs_user_id ON delivery_logs(user_id);
CREATE INDEX idx_delivery_logs_status ON delivery_logs(delivery_status);

-- ============================================
-- SCHEDULED JOBS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS scheduled_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  job_type TEXT NOT NULL CHECK (job_type IN ('ingestion', 'generation', 'delivery')),
  schedule_time TIME NOT NULL DEFAULT '08:00:00',
  timezone TEXT DEFAULT 'UTC',
  is_active BOOLEAN DEFAULT true,
  last_run_at TIMESTAMPTZ,
  next_run_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_scheduled_jobs_user_id ON scheduled_jobs(user_id);
CREATE INDEX idx_scheduled_jobs_is_active ON scheduled_jobs(is_active);
CREATE INDEX idx_scheduled_jobs_next_run ON scheduled_jobs(next_run_at);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sources_updated_at BEFORE UPDATE ON sources
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_style_samples_updated_at BEFORE UPDATE ON style_samples
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drafts_updated_at BEFORE UPDATE ON drafts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scheduled_jobs_updated_at BEFORE UPDATE ON scheduled_jobs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
ALTER TABLE style_samples ENABLE ROW LEVEL SECURITY;
ALTER TABLE drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE draft_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE delivery_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_jobs ENABLE ROW LEVEL SECURITY;

-- Policies for user_profiles
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Policies for sources
CREATE POLICY "Users can view own sources" ON sources
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own sources" ON sources
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sources" ON sources
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sources" ON sources
  FOR DELETE USING (auth.uid() = user_id);

-- Policies for items
CREATE POLICY "Users can view own items" ON items
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own items" ON items
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own items" ON items
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own items" ON items
  FOR DELETE USING (auth.uid() = user_id);

-- Policies for style_samples
CREATE POLICY "Users can view own style samples" ON style_samples
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own style samples" ON style_samples
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own style samples" ON style_samples
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own style samples" ON style_samples
  FOR DELETE USING (auth.uid() = user_id);

-- Policies for drafts
CREATE POLICY "Users can view own drafts" ON drafts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own drafts" ON drafts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own drafts" ON drafts
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own drafts" ON drafts
  FOR DELETE USING (auth.uid() = user_id);

-- Policies for draft_items
CREATE POLICY "Users can view own draft items" ON draft_items
  FOR SELECT USING (EXISTS (
    SELECT 1 FROM drafts WHERE drafts.id = draft_items.draft_id AND drafts.user_id = auth.uid()
  ));

CREATE POLICY "Users can create own draft items" ON draft_items
  FOR INSERT WITH CHECK (EXISTS (
    SELECT 1 FROM drafts WHERE drafts.id = draft_items.draft_id AND drafts.user_id = auth.uid()
  ));

CREATE POLICY "Users can delete own draft items" ON draft_items
  FOR DELETE USING (EXISTS (
    SELECT 1 FROM drafts WHERE drafts.id = draft_items.draft_id AND drafts.user_id = auth.uid()
  ));

-- Policies for feedback
CREATE POLICY "Users can view own feedback" ON feedback
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own feedback" ON feedback
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for delivery_logs
CREATE POLICY "Users can view own delivery logs" ON delivery_logs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own delivery logs" ON delivery_logs
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for scheduled_jobs
CREATE POLICY "Users can view own scheduled jobs" ON scheduled_jobs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own scheduled jobs" ON scheduled_jobs
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own scheduled jobs" ON scheduled_jobs
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own scheduled jobs" ON scheduled_jobs
  FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- SEED DATA (for testing)
-- ============================================

-- Note: Actual user creation is handled by Supabase Auth
-- This is just for reference/testing with a known user ID

-- Example: After creating a user through Supabase Auth, run:
-- INSERT INTO user_profiles (id, email, full_name, timezone) 
-- VALUES ('your-user-uuid', 'test@example.com', 'Test User', 'America/New_York');

