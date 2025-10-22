# ⏰ Configurable Fetch Frequency Feature

## 📋 Overview

We've added **configurable fetch frequency** to EchoWrite, allowing users to control how often each content source is checked for new items. This prevents unnecessary API calls and allows customization based on content update patterns.

---

## 🎯 What Changed?

### **Backend Changes**

1. ✅ **Database Schema** - `sources` table already has `fetch_frequency` field (defaults to 3600 seconds = 1 hour)

2. ✅ **Pydantic Models** (`backend/app/models/schemas.py`)

   - Added `fetch_frequency` to `SourceBase` with validation (min: 300s, max: 604800s)
   - Added `SourceUpdate` model for updating source settings
   - Added `last_fetched_at` to `Source` model

3. ✅ **Ingestion Service** (`backend/app/core/ingestion/service.py`)

   - Updated fetch logic to use source's `fetch_frequency` instead of hardcoded 1 hour
   - Added logging for skipped fetches
   - Added `update_source()` method

4. ✅ **API Endpoints** (`backend/app/api/v1/ingestion.py`)
   - Added `PUT /api/v1/ingestion/sources/{source_id}` to update sources
   - Supports updating: `name`, `is_active`, `fetch_frequency`

### **Frontend Changes**

1. ✅ **Source Interface** (`frontend/src/pages/Sources.tsx`)

   - Added `fetch_frequency` and `last_fetched_at` fields

2. ✅ **Add Source Form**

   - Added dropdown with preset frequency options:
     - Every 5 minutes (300s)
     - Every 15 minutes (900s)
     - Every 30 minutes (1800s)
     - Every 1 hour - default (3600s)
     - Every 2 hours (7200s)
     - Every 3 hours (10800s)
     - Every 6 hours (21600s)
     - Every 12 hours (43200s)
     - Once a day (86400s)
     - Every 2 days (172800s)
     - Once a week (604800s)

3. ✅ **Source List Display**
   - Shows fetch frequency: "🕐 Fetch every X hours/minutes/days"
   - Shows last fetched time: "📥 Last fetched: X min/hours/days ago"

---

## 🎨 UI Screenshots (What You'll See)

### **Add Source Form**

```
┌─────────────────────────────────────────────────┐
│  Add New Source                                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  Source Type                                     │
│  [RSS Feed ▼]                                    │
│                                                  │
│  RSS URL                                         │
│  [https://example.com/feed.xml              ]   │
│                                                  │
│  Display Name (optional)                         │
│  [My Favorite Blog                          ]   │
│                                                  │
│  Fetch Frequency                                 │
│  [Every 1 hour (default) ▼]                     │
│   ├─ Every 5 minutes (fast)                     │
│   ├─ Every 15 minutes                           │
│   ├─ Every 30 minutes                           │
│   ├─ Every 1 hour (default)     ← Selected      │
│   ├─ Every 2 hours                              │
│   ├─ Every 3 hours                              │
│   └─ ...                                        │
│                                                  │
│  How often to check this source for new content │
│                                                  │
│  [Add Source]  [Cancel]                         │
└─────────────────────────────────────────────────┘
```

### **Source List Item**

```
┌─────────────────────────────────────────────────────────────┐
│  [RSS] TechCrunch                         [Active]          │
│                                                              │
│  https://feeds.feedburner.com/TechCrunch/                   │
│                                                              │
│  Added 10/22/2025 • 🕐 Fetch every 1 hour • 📥 Last        │
│  fetched: 30 min ago                                        │
│                                                      [▶] [🗑]│
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 How It Works

### **Flow Diagram**

```
User Creates Source with Frequency
        ↓
Stored in DB (fetch_frequency: 3600)
        ↓
System Triggers Ingestion
        ↓
Check: Has enough time passed?
    ├─ YES → Fetch content
    │         Update last_fetched_at
    │         Store new items
    └─ NO  → Skip (log message)
           "Skipped - fetched 30s ago (frequency: 3600s)"
```

### **Decision Logic**

```python
# Get source configuration
fetch_frequency_seconds = source.get("fetch_frequency", 3600)  # Default 1 hour
last_fetched_at = source.get("last_fetched_at")

# Calculate time since last fetch
time_since_fetch = (datetime.utcnow() - last_fetched_dt).total_seconds()

# Decision
if time_since_fetch < fetch_frequency_seconds:
    # SKIP - Too soon
    return {"message": f"Skipped - fetched {time_since_fetch}s ago"}
else:
    # FETCH - Enough time has passed
    fetch_and_store_items()
    update_last_fetched_at()
```

---

## 🧪 Testing Guide

### **Test Scenario 1: Create Source with Custom Frequency**

1. Navigate to **Sources** page
2. Click **"Add Source"**
3. Fill in details:
   - Type: RSS Feed
   - URL: `https://feeds.feedburner.com/TechCrunch/`
   - Name: `TechCrunch Fast`
   - **Frequency: Every 15 minutes**
4. Click **"Add Source"**

**Expected:**

- Source created with `fetch_frequency: 900` (15 minutes)
- Displays: "🕐 Fetch every 15 min"

---

### **Test Scenario 2: Fetch Respects Frequency**

1. Create source with **1 hour** frequency
2. Trigger ingestion (manually or via test button)
3. Wait 10 seconds
4. Try to fetch again

**Expected:**

- First fetch: ✅ **Fetches content** (never fetched before)
- Second fetch: ⏭️ **Skips** (only 10s passed, need 3600s)
- Backend log: `"Skipping source TechCrunch: fetched 10s ago, frequency is 3600s"`

---

### **Test Scenario 3: Different Sources, Different Frequencies**

Create 3 sources:

1. **Fast News** - Every 15 min (900s)
2. **Normal Blog** - Every 1 hour (3600s)
3. **Weekly Newsletter** - Once a week (604800s)

Trigger fetch at T=0, T+15min, T+1hour:

| Time    | Fast News | Normal Blog | Weekly NL |
| ------- | --------- | ----------- | --------- |
| T=0     | ✅ Fetch  | ✅ Fetch    | ✅ Fetch  |
| T+15min | ✅ Fetch  | ⏭️ Skip     | ⏭️ Skip   |
| T+1hour | ✅ Fetch  | ✅ Fetch    | ⏭️ Skip   |

---

## 📊 API Examples

### **Create Source with Frequency**

```bash
POST /api/v1/ingestion/sources
Authorization: Bearer <token>

{
  "type": "rss",
  "handle": "https://feeds.feedburner.com/TechCrunch/",
  "name": "TechCrunch",
  "fetch_frequency": 900  # 15 minutes
}
```

**Response:**

```json
{
  "id": "a516e5e6-...",
  "type": "rss",
  "handle": "https://feeds.feedburner.com/TechCrunch/",
  "name": "TechCrunch",
  "fetch_frequency": 900,
  "last_fetched_at": null,
  "is_active": true,
  "created_at": "2025-10-22T12:00:00Z"
}
```

---

### **Update Source Frequency**

```bash
PUT /api/v1/ingestion/sources/{source_id}
Authorization: Bearer <token>

{
  "fetch_frequency": 7200  # Change to 2 hours
}
```

**Response:**

```json
{
  "id": "a516e5e6-...",
  "name": "TechCrunch",
  "fetch_frequency": 7200,
  "last_fetched_at": "2025-10-22T12:30:00Z",
  "updated_at": "2025-10-22T13:00:00Z"
}
```

---

### **Process Feed (Respects Frequency)**

```bash
POST /api/v1/ingestion/process
Authorization: Bearer <token>

{
  "source_ids": ["a516e5e6-..."],
  "force_refresh": false  # Respect fetch_frequency
}
```

**Response (if too soon):**

```json
{
  "processed_sources": 1,
  "new_items": 0,
  "errors": [],
  "message": "Skipped - fetched 300s ago (frequency: 3600s)"
}
```

**Response (if enough time passed):**

```json
{
  "processed_sources": 1,
  "new_items": 15,
  "errors": []
}
```

---

## 🎯 Benefits

### **1. Performance Optimization**

- ⚡ Reduces unnecessary HTTP requests
- 💾 Saves database operations
- 🔋 Lower server resource usage

### **2. Cost Savings**

- 💰 Fewer API calls to external services
- 📉 Reduced bandwidth usage
- 🎯 Only fetch when needed

### **3. Content-Specific Optimization**

- 📰 Fast frequency for breaking news (15 min)
- 📝 Medium frequency for blogs (1-6 hours)
- 📧 Slow frequency for newsletters (daily/weekly)

### **4. Rate Limit Compliance**

- ✅ Respect external API rate limits
- 🤝 Better citizenship
- 🛡️ Avoid being blocked

---

## 🔧 Frequency Guidelines

| Content Type          | Recommended Frequency | Reasoning           |
| --------------------- | --------------------- | ------------------- |
| **Breaking News**     | 15-30 minutes         | Fast-moving content |
| **Tech News**         | 1 hour                | Regular updates     |
| **Personal Blogs**    | 3-6 hours             | Infrequent posts    |
| **Daily Newsletter**  | 12-24 hours           | Once per day        |
| **Weekly Newsletter** | 7 days                | Weekly schedule     |
| **Social Media**      | 5-15 minutes          | Real-time updates   |

---

## ⚙️ Configuration

### **Validation Rules**

```python
fetch_frequency: int = Field(
    default=3600,           # 1 hour default
    ge=300,                 # Min: 5 minutes
    le=604800,              # Max: 7 days
    description="Seconds between fetches"
)
```

### **Common Values**

| Duration   | Seconds | Use Case                |
| ---------- | ------- | ----------------------- |
| 5 minutes  | 300     | Very fast (testing)     |
| 15 minutes | 900     | Breaking news           |
| 30 minutes | 1800    | Active blogs            |
| 1 hour     | 3600    | **Default** - tech news |
| 2 hours    | 7200    | Medium blogs            |
| 6 hours    | 21600   | Slow blogs              |
| 12 hours   | 43200   | Semi-daily              |
| 1 day      | 86400   | Daily newsletters       |
| 7 days     | 604800  | Weekly content          |

---

## 🐛 Troubleshooting

### **Problem: Source not fetching**

**Check:**

1. Is `is_active = true`?
2. Has enough time passed since `last_fetched_at`?
3. Check backend logs for skip messages

**Solution:**

- Wait for frequency duration to pass, OR
- Use `force_refresh: true` to bypass frequency check

---

### **Problem: Fetching too frequently**

**Check:**

- Current `fetch_frequency` setting
- Backend logs showing fetch attempts

**Solution:**

- Increase `fetch_frequency` via UI or API
- Update source: `PUT /api/v1/ingestion/sources/{id}`

---

## ✅ Summary

**What's New:**

- ✅ Configurable fetch frequency per source (5 min to 7 days)
- ✅ UI dropdown with 11 preset options
- ✅ Visual display of frequency and last fetch time
- ✅ Backend respects frequency settings
- ✅ API endpoint to update frequency
- ✅ Smart skipping with logging

**Benefits:**

- ⚡ Better performance
- 💰 Cost savings
- 🎯 Content-optimized fetching
- 🛡️ Rate limit compliance

**Ready to use!** 🚀

---

## 📝 Testing Checklist

- [ ] Create source with default frequency (1 hour)
- [ ] Create source with fast frequency (15 min)
- [ ] Create source with slow frequency (1 day)
- [ ] Verify frequency displays in source list
- [ ] Trigger fetch - should work first time
- [ ] Trigger fetch again immediately - should skip
- [ ] Wait for frequency duration - should work again
- [ ] Check "Last fetched" timestamp updates
- [ ] Update source frequency via UI (when implemented)
- [ ] Verify backend logs show skip messages

---

**Implementation Complete!** 🎉
