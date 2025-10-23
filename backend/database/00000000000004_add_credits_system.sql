-- Add credit system to track LLM API usage
-- Migration: Add user credits and generation tracking

-- Add credits field to user_profiles
ALTER TABLE user_profiles 
ADD COLUMN IF NOT EXISTS credits INTEGER DEFAULT 10,
ADD COLUMN IF NOT EXISTS total_generations INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_generation_at TIMESTAMPTZ;

-- Create index for credit queries
CREATE INDEX IF NOT EXISTS idx_user_profiles_credits ON user_profiles(credits);

-- Add credit usage tracking to drafts
ALTER TABLE drafts 
ADD COLUMN IF NOT EXISTS credits_used INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS generation_cost DECIMAL(10,4) DEFAULT 0.0;

-- Create credit transactions table for audit trail
CREATE TABLE IF NOT EXISTS credit_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
  transaction_type TEXT NOT NULL CHECK (transaction_type IN ('generation', 'refill', 'bonus', 'deduction')),
  amount INTEGER NOT NULL, -- positive for credits added, negative for credits used
  description TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_credit_transactions_user_id ON credit_transactions(user_id);
CREATE INDEX idx_credit_transactions_type ON credit_transactions(transaction_type);
CREATE INDEX idx_credit_transactions_created_at ON credit_transactions(created_at DESC);

-- Enable RLS for credit_transactions
ALTER TABLE credit_transactions ENABLE ROW LEVEL SECURITY;

-- Create RLS policy for credit_transactions
CREATE POLICY "Users can view their own credit transactions" ON credit_transactions
  FOR SELECT USING (auth.uid() = user_id);

-- Add trigger to automatically create credit transaction when draft is created
CREATE OR REPLACE FUNCTION track_generation_credits()
RETURNS TRIGGER AS $$
BEGIN
  -- Deduct credit for generation
  UPDATE user_profiles 
  SET 
    credits = GREATEST(0, credits - NEW.credits_used),
    total_generations = total_generations + 1,
    last_generation_at = NOW()
  WHERE id = NEW.user_id;
  
  -- Create credit transaction record
  INSERT INTO credit_transactions (user_id, transaction_type, amount, description, metadata)
  VALUES (
    NEW.user_id, 
    'generation', 
    -NEW.credits_used, 
    'Newsletter generation',
    jsonb_build_object('draft_id', NEW.id, 'title', NEW.title)
  );
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for draft creation
DROP TRIGGER IF EXISTS trigger_track_generation_credits ON drafts;
CREATE TRIGGER trigger_track_generation_credits
  AFTER INSERT ON drafts
  FOR EACH ROW
  EXECUTE FUNCTION track_generation_credits();

-- Add function to check if user has enough credits
CREATE OR REPLACE FUNCTION user_has_credits(user_uuid UUID, required_credits INTEGER DEFAULT 1)
RETURNS BOOLEAN AS $$
DECLARE
  current_credits INTEGER;
BEGIN
  SELECT credits INTO current_credits 
  FROM user_profiles 
  WHERE id = user_uuid;
  
  RETURN COALESCE(current_credits, 0) >= required_credits;
END;
$$ LANGUAGE plpgsql;

-- Add function to add credits to user
CREATE OR REPLACE FUNCTION add_user_credits(user_uuid UUID, credit_amount INTEGER, description TEXT DEFAULT 'Credit refill')
RETURNS VOID AS $$
BEGIN
  -- Update user credits
  UPDATE user_profiles 
  SET credits = credits + credit_amount
  WHERE id = user_uuid;
  
  -- Create transaction record
  INSERT INTO credit_transactions (user_id, transaction_type, amount, description)
  VALUES (user_uuid, 'refill', credit_amount, description);
END;
$$ LANGUAGE plpgsql;
