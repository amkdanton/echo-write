# EchoWrite Database Setup

## 🗄️ Database Schema Overview

EchoWrite uses **Supabase (PostgreSQL)** as its database with the following tables:

### Core Tables

1. **user_profiles** - User settings and preferences
2. **sources** - RSS feeds, YouTube channels, etc.
3. **items** - Fetched content from sources
4. **style_samples** - Writing samples for voice training
5. **drafts** - Generated newsletters
6. **draft_items** - Items included in each draft
7. **feedback** - User reactions to drafts
8. **delivery_logs** - Email delivery tracking
9. **scheduled_jobs** - Automated task scheduling

## 🚀 Setup Instructions

### Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in:
   - **Project Name**: `echowrite` (or your choice)
   - **Database Password**: (save this!)
   - **Region**: Choose closest to you
4. Wait for project creation (~2 minutes)

### Step 2: Get Your Credentials

1. In your Supabase project dashboard, go to **Settings > API**
2. Copy these values:

   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbG...` (long JWT token)
   - **service_role key**: `eyJhbG...` (for admin operations)

3. Update your `backend/.env`:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbG...  # anon key for client operations
   SUPABASE_SERVICE_KEY=eyJhbG...  # service_role for admin (optional)
   ```

### Step 3: Run the Schema

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy the entire contents of `schema.sql`
4. Paste and click **Run**
5. Verify: Go to **Table Editor** - you should see all 9 tables

### Step 4: Enable Authentication

1. Go to **Authentication > Providers**
2. Enable **Email** provider (already on by default)
3. (Optional) Enable **Google**, **GitHub**, etc.

### Step 5: Test Connection

Run this test script:

```bash
cd backend
source venv/bin/activate
python -c "
from app.core.database import get_supabase
client = get_supabase()
print('✅ Supabase connected successfully!')
print(f'URL: {client.supabase_url}')
"
```

## 📊 Database Schema Details

### Entity Relationships

```
user_profiles (1) ───< sources (many)
                 │
                 ├───< items (many)
                 │
                 ├───< style_samples (many)
                 │
                 ├───< drafts (many)
                 │
                 └───< scheduled_jobs (many)

sources (1) ───< items (many)
drafts (1) ───< draft_items (many) ───> items (many)
drafts (1) ───< feedback (many)
drafts (1) ───< delivery_logs (many)
```

### Key Features

- **UUID Primary Keys**: Using `uuid_generate_v4()` for unique IDs
- **Row Level Security (RLS)**: Users can only access their own data
- **Automatic Timestamps**: `created_at` and `updated_at` tracked automatically
- **Cascade Deletes**: Deleting a user removes all their data
- **Indexes**: Optimized for common queries (user_id, created_at, trend_score)
- **JSON Storage**: Flexible metadata fields for extensions

## 🔒 Row Level Security (RLS)

All tables have RLS enabled. Users can only:

- **View** their own data
- **Create** data associated with their user_id
- **Update/Delete** their own data

This is enforced at the database level, providing security even if the API has bugs.

## 📝 Common Queries

### Get all sources for a user

```sql
SELECT * FROM sources
WHERE user_id = 'user-uuid-here'
AND is_active = true;
```

### Get top trending items

```sql
SELECT * FROM items
WHERE user_id = 'user-uuid-here'
AND published_at > NOW() - INTERVAL '48 hours'
ORDER BY trend_score DESC
LIMIT 10;
```

### Get recent drafts

```sql
SELECT * FROM drafts
WHERE user_id = 'user-uuid-here'
ORDER BY created_at DESC
LIMIT 20;
```

### Get draft with items

```sql
SELECT
  d.*,
  json_agg(i.*) as items
FROM drafts d
LEFT JOIN draft_items di ON di.draft_id = d.id
LEFT JOIN items i ON i.id = di.item_id
WHERE d.user_id = 'user-uuid-here'
GROUP BY d.id
ORDER BY d.created_at DESC;
```

## 🧪 Testing Data

For development, you can add test data:

```sql
-- Get your user ID from Supabase Auth
-- Then insert a profile:
INSERT INTO user_profiles (id, email, full_name, timezone)
VALUES ('your-auth-user-id', 'test@example.com', 'Test User', 'UTC');

-- Add a test RSS source:
INSERT INTO sources (user_id, type, handle, name)
VALUES ('your-auth-user-id', 'rss', 'https://news.ycombinator.com/rss', 'Hacker News');

-- Test item:
INSERT INTO items (source_id, user_id, title, url, summary, published_at)
VALUES (
  'source-uuid',
  'your-auth-user-id',
  'Test Article',
  'https://example.com/article',
  'This is a test article summary',
  NOW()
);
```

## 🔄 Migrations

For future schema changes:

1. Create a new `.sql` file in `backend/database/migrations/`
2. Name it: `YYYYMMDD_description.sql`
3. Run it in Supabase SQL Editor
4. Document the change

## 🆘 Troubleshooting

### Can't connect to Supabase

- Check your `.env` file has correct `SUPABASE_URL` and `SUPABASE_KEY`
- Verify the project is active in Supabase dashboard
- Check network/firewall settings

### RLS blocking queries

- Make sure you're using the authenticated user's context
- For admin operations, use `service_role` key (bypasses RLS)
- Check the RLS policies in Supabase dashboard

### Tables not created

- Run the schema.sql again
- Check SQL Editor for error messages
- Ensure UUID extension is enabled: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`

## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
