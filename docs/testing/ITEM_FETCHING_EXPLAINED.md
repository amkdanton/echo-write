# 📥 How Items are Fetched and Stored in EchoWrite

## 🔄 Complete Fetching Flow

### Overview
```
User Creates Source → Scheduler/Manual Trigger → Fetch Feed → Parse Content → 
Check Duplicates → Store Items → Update Timestamp → Ready for Analysis
```

---

## 📊 Step-by-Step Process

### **Step 1: User Creates a Content Source**

User adds an RSS feed, YouTube channel, or Twitter account:

```python
# API Call
POST /api/v1/ingestion/sources
{
  "type": "rss",
  "handle": "https://feeds.feedburner.com/TechCrunch/",
  "name": "TechCrunch",
  "fetch_frequency": 3600  # seconds (1 hour)
}
```

**Stored in `sources` table:**
```sql
sources
├── id: "a516e5e6-..."
├── user_id: "69a39d10-..."
├── type: "rss"
├── handle: "https://feeds.feedburner.com/TechCrunch/"
├── name: "TechCrunch"
├── fetch_frequency: 3600  -- How often to fetch (seconds)
├── last_fetched_at: NULL  -- Last fetch timestamp
└── is_active: true
```

---

### **Step 2: Trigger Content Ingestion**

Two ways to trigger:
1. **Manual:** User clicks "Fetch Content" button
2. **Scheduled:** Background job runs every hour

```python
# API Call
POST /api/v1/ingestion/process
{
  "source_ids": ["a516e5e6-...", "80ed8153-..."],
  "force_refresh": false  # Respect fetch_frequency
}
```

---

### **Step 3: Check If Fetch is Needed**

**Current Logic (HARDCODED - Line 70):**
```python
# ❌ PROBLEM: Hardcoded 1 hour
if datetime.now() - last_fetched_dt < timedelta(hours=1):
    return {"message": "Skipped - recently updated"}
```

**What We'll Change To:**
```python
# ✅ SOLUTION: Use source's fetch_frequency
fetch_frequency_seconds = source.get("fetch_frequency", 3600)
time_since_fetch = datetime.now() - last_fetched_dt

if time_since_fetch < timedelta(seconds=fetch_frequency_seconds):
    return {"message": "Skipped - recently updated"}
```

**Example Decision Matrix:**

| Source | Fetch Frequency | Last Fetched | Time Since | Action |
|--------|----------------|--------------|------------|--------|
| TechCrunch | 1 hour (3600s) | 30 min ago | 1800s | ⏭️ **Skip** |
| The Verge | 2 hours (7200s) | 1 hour ago | 3600s | ⏭️ **Skip** |
| HN Front Page | 15 min (900s) | 20 min ago | 1200s | ✅ **Fetch** |
| Personal Blog | 24 hours (86400s) | 12 hours ago | 43200s | ⏭️ **Skip** |

---

### **Step 4: Fetch RSS Feed**

For RSS sources, we make an HTTP request:

```python
# GET request to RSS feed URL
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(source["handle"])
    # Example: GET https://feeds.feedburner.com/TechCrunch/
```

**RSS Feed XML Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>TechCrunch</title>
    <item>
      <title>Starcloud: Nvidia's New Platform</title>
      <link>https://blogs.nvidia.com/blog/starcloud/</link>
      <description>Nvidia has been making waves...</description>
      <pubDate>Tue, 22 Oct 2025 11:23:33 GMT</pubDate>
    </item>
    <item>
      <title>HarmonyOS 6 Full Overview</title>
      <link>https://www.youtube.com/watch?v=...</link>
      <description>New design, AI features...</description>
      <pubDate>Tue, 22 Oct 2025 11:23:12 GMT</pubDate>
    </item>
    <!-- ... more items ... -->
  </channel>
</rss>
```

---

### **Step 5: Parse Feed with Feedparser**

```python
feed = feedparser.parse(response.text)

# Iterate through entries (limit to 20 most recent)
for entry in feed.entries[:20]:
    title = entry.get("title")
    url = entry.get("link")
    summary = entry.get("summary") or entry.get("description")
    published_at = entry.get("published")
```

**Extracted Data:**
```python
{
  "title": "Starcloud: Nvidia's New Platform",
  "url": "https://blogs.nvidia.com/blog/starcloud/",
  "summary": "Nvidia has been making waves with its new...",
  "published_at": "2025-10-22T11:23:33Z"
}
```

---

### **Step 6: Check for Duplicates**

Before inserting, we check if the item already exists:

```python
# Query database by URL
existing = supabase.table("items").select("id").eq("url", item_url).execute()

if existing.data:
    continue  # Skip this item, already in database
```

**Why check by URL?**
- URLs are unique identifiers for content
- Prevents duplicate articles in database
- Even if same article is in multiple feeds, only stored once

**Unique Index in Database:**
```sql
CREATE UNIQUE INDEX idx_items_unique_url_user 
ON items(url, user_id);
```

---

### **Step 7: Store Item in Database**

If item is new, insert into `items` table:

```python
item_data = {
    "title": "Starcloud: Nvidia's New Platform",
    "url": "https://blogs.nvidia.com/blog/starcloud/",
    "summary": "Nvidia has been making waves...",
    "published_at": "2025-10-22T11:23:33Z",
    "source_id": "a516e5e6-...",  # Links to source
    "user_id": "69a39d10-...",     # Links to user
    "trend_score": 0.0,             # Calculated later
    "fetched_at": "2025-10-22T12:20:30Z"
}

supabase.table("items").insert(item_data).execute()
```

**Database Record:**
```sql
items
├── id: "f3c8a1b2-..." (auto-generated UUID)
├── source_id: "a516e5e6-..." (foreign key → sources)
├── user_id: "69a39d10-..." (foreign key → user_profiles)
├── title: "Starcloud: Nvidia's New Platform"
├── url: "https://blogs.nvidia.com/blog/starcloud/"
├── summary: "Nvidia has been making waves with its new Starcloud..."
├── content: NULL (full content - optional)
├── author: NULL (if available in feed)
├── published_at: "2025-10-22T11:23:33Z"
├── fetched_at: "2025-10-22T12:20:30Z"
├── trend_score: 0.0 (calculated in trend analysis step)
├── keywords: [] (extracted later)
├── metadata: {} (additional data)
└── created_at: "2025-10-22T12:20:30Z"
```

---

### **Step 8: Update Source Timestamp**

After processing all entries, update the source:

```python
supabase.table("sources").update({
    "last_fetched_at": datetime.utcnow().isoformat()
}).eq("id", source_id).execute()
```

**Updated Source:**
```sql
sources
├── id: "a516e5e6-..."
├── last_fetched_at: "2025-10-22T12:20:30Z" ← UPDATED
└── ...
```

This timestamp prevents fetching the same source too frequently.

---

## 🔢 Source Type Examples

### **1. RSS Feed (Blog/News Site)**

```python
{
  "type": "rss",
  "handle": "https://feeds.feedburner.com/TechCrunch/",
  "fetch_frequency": 3600  # Check every 1 hour
}
```

**Process:**
1. HTTP GET to RSS URL
2. Parse XML with feedparser
3. Extract 20 most recent entries
4. Store new items only

---

### **2. YouTube Channel**

```python
{
  "type": "youtube",
  "handle": "@mkbhd",  # Channel handle
  "fetch_frequency": 7200  # Check every 2 hours
}
```

**Process:**
1. Convert handle to RSS feed URL:
   ```
   https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ
   ```
2. Parse YouTube RSS feed (same as RSS)
3. Extract video title, link, description
4. Store new videos

---

### **3. Twitter/X (Future)**

```python
{
  "type": "twitter",
  "handle": "@elonmusk",
  "fetch_frequency": 900  # Check every 15 minutes
}
```

**Process:**
1. Call Twitter API v2
2. Get recent tweets
3. Extract tweet text, links, media
4. Store new tweets

---

## 📊 Database Relationships

```
user_profiles (1) ──────┐
                        │
                        │ user_id
                        ▼
sources (1) ─────┐  user_id
  │              │
  │ source_id    │
  ▼              │
items (many) ◄───┘
  │
  │ item_id
  ▼
draft_items (many)
  │
  │ draft_id
  ▼
drafts (1)
```

**Example Data Flow:**
```
User: "69a39d10-..."
  └─> Source: "TechCrunch" (a516e5e6-...)
       └─> Item 1: "Starcloud" (f3c8a1b2-...)
       └─> Item 2: "HarmonyOS 6" (b7d4e9a1-...)
       └─> Item 3: "Uber EVs" (c2f8a3d5-...)
```

---

## ⚙️ Fetch Frequency Configuration

### **Current Issue:**
- ❌ Hardcoded 1-hour limit for all sources
- ❌ Cannot customize per source
- ❌ Not flexible for different content types

### **Solution:**
- ✅ Use `fetch_frequency` field from database
- ✅ Configurable per source
- ✅ Default to 1 hour (3600 seconds)

### **Examples:**

| Content Type | Suggested Frequency | Reason |
|--------------|---------------------|--------|
| Breaking News (CNN) | 15 min (900s) | Fast-moving content |
| Tech News (TC) | 1 hour (3600s) | Regular updates |
| Personal Blogs | 6 hours (21600s) | Infrequent posts |
| Weekly Newsletter | 24 hours (86400s) | Weekly content |
| Social Media | 5 min (300s) | Real-time updates |

---

## 🔄 Complete Example Flow

### Input: User has 3 sources

```
1. TechCrunch (RSS) - fetch_frequency: 3600s (1 hour)
2. The Verge (RSS) - fetch_frequency: 7200s (2 hours)  
3. Hacker News (RSS) - fetch_frequency: 900s (15 min)
```

### Scenario: Process All Sources at 12:00 PM

**12:00 PM - First Fetch:**
```
✅ TechCrunch → Fetched 15 items → last_fetched: 12:00
✅ The Verge → Fetched 12 items → last_fetched: 12:00
✅ Hacker News → Fetched 20 items → last_fetched: 12:00

Total: 47 items stored
```

**12:15 PM - Second Fetch (15 min later):**
```
⏭️ TechCrunch → SKIP (only 15 min, need 60 min)
⏭️ The Verge → SKIP (only 15 min, need 120 min)
✅ Hacker News → Fetched 3 new items (15 min passed ≥ 15 min frequency)

Total: 3 new items
```

**1:00 PM - Third Fetch (1 hour later):**
```
✅ TechCrunch → Fetched 5 new items (60 min passed ≥ 60 min frequency)
⏭️ The Verge → SKIP (only 60 min, need 120 min)
✅ Hacker News → Fetched 8 new items (60 min passed ≥ 15 min frequency)

Total: 13 new items
```

---

## 🎯 Benefits of Configurable Fetch Frequency

1. **⚡ Performance:**
   - Avoid unnecessary API calls
   - Reduce server load
   - Save bandwidth

2. **💰 Cost Optimization:**
   - Fewer API requests to external services
   - Lower database operations
   - Reduced OpenAI API costs (less content to analyze)

3. **🎯 Content Quality:**
   - High-frequency for breaking news
   - Low-frequency for slower content
   - Match natural update patterns

4. **🔋 Rate Limit Compliance:**
   - Respect API rate limits
   - Avoid being blocked by sources
   - Better citizenship

---

## 🚀 Next Steps

We'll update the code to:
1. ✅ Read `fetch_frequency` from source record
2. ✅ Use it instead of hardcoded 1 hour
3. ✅ Allow setting it when creating sources
4. ✅ Allow updating it per source
5. ✅ Add validation (min: 5 min, max: 7 days)

---

**Ready to implement!** 🎉

