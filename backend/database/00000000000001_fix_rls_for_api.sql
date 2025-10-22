-- Fix RLS policies for API service account
-- This allows the service account to bypass RLS for API operations

-- Create a service role that bypasses RLS
-- The service account should use this role when making API calls

-- For now, let's create policies that allow service account access
-- We'll identify the service account by checking if auth.uid() is null (service account)

-- Sources table policies
DROP POLICY IF EXISTS "Users can view own sources" ON sources;
DROP POLICY IF EXISTS "Users can create own sources" ON sources;
DROP POLICY IF EXISTS "Users can update own sources" ON sources;
DROP POLICY IF EXISTS "Users can delete own sources" ON sources;

-- Create new policies that allow both user access and service account access
CREATE POLICY "Users can view own sources" ON sources
  FOR SELECT USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can create own sources" ON sources
  FOR INSERT WITH CHECK (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can update own sources" ON sources
  FOR UPDATE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can delete own sources" ON sources
  FOR DELETE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

-- Items table policies
DROP POLICY IF EXISTS "Users can view own items" ON items;
DROP POLICY IF EXISTS "Users can create own items" ON items;
DROP POLICY IF EXISTS "Users can update own items" ON items;
DROP POLICY IF EXISTS "Users can delete own items" ON items;

CREATE POLICY "Users can view own items" ON items
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM sources 
      WHERE sources.id = items.source_id 
      AND (sources.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can create own items" ON items
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM sources 
      WHERE sources.id = items.source_id 
      AND (sources.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can update own items" ON items
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM sources 
      WHERE sources.id = items.source_id 
      AND (sources.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can delete own items" ON items
  FOR DELETE USING (
    EXISTS (
      SELECT 1 FROM sources 
      WHERE sources.id = items.source_id 
      AND (sources.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

-- Drafts table policies
DROP POLICY IF EXISTS "Users can view own drafts" ON drafts;
DROP POLICY IF EXISTS "Users can create own drafts" ON drafts;
DROP POLICY IF EXISTS "Users can update own drafts" ON drafts;
DROP POLICY IF EXISTS "Users can delete own drafts" ON drafts;

CREATE POLICY "Users can view own drafts" ON drafts
  FOR SELECT USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can create own drafts" ON drafts
  FOR INSERT WITH CHECK (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can update own drafts" ON drafts
  FOR UPDATE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can delete own drafts" ON drafts
  FOR DELETE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

-- Draft items table policies
DROP POLICY IF EXISTS "Users can view own draft items" ON draft_items;
DROP POLICY IF EXISTS "Users can create own draft items" ON draft_items;
DROP POLICY IF EXISTS "Users can update own draft items" ON draft_items;
DROP POLICY IF EXISTS "Users can delete own draft items" ON draft_items;

CREATE POLICY "Users can view own draft items" ON draft_items
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = draft_items.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can create own draft items" ON draft_items
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = draft_items.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can update own draft items" ON draft_items
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = draft_items.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can delete own draft items" ON draft_items
  FOR DELETE USING (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = draft_items.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

-- Style samples table policies
DROP POLICY IF EXISTS "Users can view own style samples" ON style_samples;
DROP POLICY IF EXISTS "Users can create own style samples" ON style_samples;
DROP POLICY IF EXISTS "Users can update own style samples" ON style_samples;
DROP POLICY IF EXISTS "Users can delete own style samples" ON style_samples;

CREATE POLICY "Users can view own style samples" ON style_samples
  FOR SELECT USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can create own style samples" ON style_samples
  FOR INSERT WITH CHECK (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can update own style samples" ON style_samples
  FOR UPDATE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can delete own style samples" ON style_samples
  FOR DELETE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

-- Feedback table policies
DROP POLICY IF EXISTS "Users can view own feedback" ON feedback;
DROP POLICY IF EXISTS "Users can create own feedback" ON feedback;

CREATE POLICY "Users can view own feedback" ON feedback
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = feedback.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can create own feedback" ON feedback
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = feedback.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

-- Delivery logs table policies
DROP POLICY IF EXISTS "Users can view own delivery logs" ON delivery_logs;
DROP POLICY IF EXISTS "Users can create own delivery logs" ON delivery_logs;

CREATE POLICY "Users can view own delivery logs" ON delivery_logs
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = delivery_logs.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

CREATE POLICY "Users can create own delivery logs" ON delivery_logs
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM drafts 
      WHERE drafts.id = delivery_logs.draft_id 
      AND (drafts.user_id = auth.uid() OR auth.uid() IS NULL)
    ) OR auth.uid() IS NULL
  );

-- Scheduled jobs table policies
DROP POLICY IF EXISTS "Users can view own scheduled jobs" ON scheduled_jobs;
DROP POLICY IF EXISTS "Users can create own scheduled jobs" ON scheduled_jobs;
DROP POLICY IF EXISTS "Users can update own scheduled jobs" ON scheduled_jobs;
DROP POLICY IF EXISTS "Users can delete own scheduled jobs" ON scheduled_jobs;

CREATE POLICY "Users can view own scheduled jobs" ON scheduled_jobs
  FOR SELECT USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can create own scheduled jobs" ON scheduled_jobs
  FOR INSERT WITH CHECK (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can update own scheduled jobs" ON scheduled_jobs
  FOR UPDATE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );

CREATE POLICY "Users can delete own scheduled jobs" ON scheduled_jobs
  FOR DELETE USING (
    auth.uid() = user_id OR 
    auth.uid() IS NULL  -- Allow service account access
  );
