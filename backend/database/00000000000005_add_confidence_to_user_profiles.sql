-- Add confidence field to user_profiles table
-- This field stores the confidence score for the user's voice profile

ALTER TABLE user_profiles 
ADD COLUMN confidence DECIMAL(3,2) DEFAULT 0.0 CHECK (confidence >= 0.0 AND confidence <= 1.0);

-- Add comment for clarity
COMMENT ON COLUMN user_profiles.confidence IS 'Confidence score for the user voice profile (0.0 to 1.0)';
