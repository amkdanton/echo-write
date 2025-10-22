# 📝 Changes Summary - Configurable Fetch Frequency

## 🎯 What Was Added

Added **configurable fetch frequency** feature that allows users to control how often each content source is checked for new items (from 5 minutes to 7 days).

---

## 📂 Files Modified

### **Backend (4 files)**

1. **`backend/app/models/schemas.py`**

   - Added `fetch_frequency` field to `SourceBase` (default: 3600s)
   - Added validation (min: 300s, max: 604800s)
   - Created new `SourceUpdate` model
   - Added `last_fetched_at` to `Source` model

2. **`backend/app/core/ingestion/service.py`**

   - **Line 69-80:** Updated fetch logic to use source's `fetch_frequency` instead of hardcoded 1 hour
   - Added logging for skipped fetches
   - **Line 239-249:** Added `update_source()` method to update source settings

3. **`backend/app/api/v1/ingestion.py`**

   - Imported `SourceUpdate` model
   - **Line 113-126:** Added `PUT /api/v1/ingestion/sources/{source_id}` endpoint

4. **`backend/database/schema.sql`** (Already had field)
   - `fetch_frequency INTEGER DEFAULT 3600` already exists in sources table ✅

### **Frontend (1 file)**

5. **`frontend/src/pages/Sources.tsx`**
   - **Line 19-20:** Added `fetch_frequency` and `last_fetched_at` to Source interface
   - **Line 31:** Added `fetch_frequency: 3600` to newSource state
   - **Line 37-62:** Added helper functions: `formatFrequency()` and `formatLastFetched()`
   - **Line 182-206:** Added fetch frequency dropdown in Add Source form (11 preset options)
   - **Line 285-297:** Updated source list display to show frequency and last fetched time

---

## 🆕 New Features

### **1. UI: Fetch Frequency Selector**

Dropdown in "Add Source" form with 11 options:

- Every 5 minutes (fast)
- Every 15 minutes
- Every 30 minutes
- **Every 1 hour (default)**
- Every 2 hours
- Every 3 hours
- Every 6 hours
- Every 12 hours
- Once a day
- Every 2 days
- Once a week

### **2. UI: Source Information Display**

Each source now shows:

- 🕐 **Fetch frequency**: "Fetch every 1 hour"
- 📥 **Last fetched**: "30 min ago" / "Never"

### **3. API: Update Source Endpoint**

```bash
PUT /api/v1/ingestion/sources/{source_id}
```

Can update: `name`, `is_active`, `fetch_frequency`

### **4. Backend: Smart Fetch Logic**

- Checks if enough time has passed since last fetch
- Skips if too soon (logs message)
- Fetches if frequency duration has passed

---

## 🔄 How It Works Now

### **Before (Hardcoded)**

```python
# ❌ Always 1 hour for all sources
if datetime.now() - last_fetched < timedelta(hours=1):
    skip()
```

### **After (Configurable)**

```python
# ✅ Uses source's fetch_frequency setting
fetch_frequency_seconds = source.get("fetch_frequency", 3600)
time_since_fetch = (datetime.utcnow() - last_fetched).total_seconds()

if time_since_fetch < fetch_frequency_seconds:
    skip()  # Too soon
else:
    fetch()  # Enough time passed
```

---

## 📊 Database Schema (No Changes Needed)

The `sources` table already had the field:

```sql
CREATE TABLE sources (
  ...
  fetch_frequency INTEGER DEFAULT 3600,  -- Already exists! ✅
  last_fetched_at TIMESTAMPTZ,
  ...
);
```

---

## 🧪 Testing

### **To Test from UI:**

1. **Open browser**: http://localhost:3000/sources

2. **Add a new source:**

   - Click "Add Source"
   - Fill in RSS URL
   - Select fetch frequency (try "Every 15 minutes")
   - Click "Add Source"

3. **Verify display:**

   - Should show: "🕐 Fetch every 15 min"
   - Should show: "📥 Last fetched: Never"

4. **Test fetching:**
   - Click the ▶ (play) button to test source
   - Wait a few seconds
   - Try again - should skip (too soon)
   - Check backend logs for skip message

### **Backend Logs to Look For:**

```
INFO: Skipping source TechCrunch: fetched 30s ago, frequency is 900s
```

---

## 🎯 Benefits

1. **Performance**: Reduces unnecessary API calls
2. **Cost**: Saves bandwidth and external API usage
3. **Flexibility**: Each source can have different frequency
4. **Control**: User decides based on content type

---

## ✅ Checklist

- [x] Backend: Read fetch_frequency from database
- [x] Backend: Use fetch_frequency in ingestion logic
- [x] Backend: Add update_source() method
- [x] Backend: Add PUT endpoint
- [x] Frontend: Add fetch_frequency to interface
- [x] Frontend: Add dropdown in form
- [x] Frontend: Display frequency and last fetched
- [x] Frontend: Format helper functions
- [x] Documentation: Created ITEM_FETCHING_EXPLAINED.md
- [x] Documentation: Created FETCH_FREQUENCY_FEATURE.md
- [x] Documentation: Created test script
- [x] Validation: Min 5 min, Max 7 days
- [ ] User Testing: Test from UI
- [ ] User Testing: Verify fetch logic works

---

## 🚀 Ready to Test!

**Next Steps:**

1. Open http://localhost:3000/sources
2. Create a source with custom frequency
3. Test the fetch behavior
4. Verify it skips when too soon
5. Check backend logs

---

## 📋 API Endpoints Summary

| Method  | Endpoint                             | Purpose                              |
| ------- | ------------------------------------ | ------------------------------------ |
| POST    | `/api/v1/ingestion/sources`          | Create source (with fetch_frequency) |
| GET     | `/api/v1/ingestion/sources`          | List all sources                     |
| **PUT** | **`/api/v1/ingestion/sources/{id}`** | **Update source settings ⭐ NEW**    |
| DELETE  | `/api/v1/ingestion/sources/{id}`     | Delete source                        |
| POST    | `/api/v1/ingestion/process`          | Fetch content (respects frequency)   |
| POST    | `/api/v1/ingestion/test/{id}`        | Test source                          |

---

## 🎉 Implementation Complete!

All code changes are done. Ready for UI testing! 🚀
