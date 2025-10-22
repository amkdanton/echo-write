# 📰 Show Fetched Items Per Source Feature

## 🎯 Overview

Added beautiful, expandable UI to show the **last 5 fetched items** for each content source. Keeps the interface clean with expand/collapse functionality - items only load when expanded.

---

## ✨ What's New

### **1. Expandable Source Cards**

- Click the chevron (▼/▲) button to expand/collapse
- Only fetched when expanded (performance optimization)
- Shows loading state while fetching
- Beautiful animations and transitions

### **2. Item Display**

Each item shows:

- 📄 **Title** (clickable link to original article)
- 📝 **Summary** (first 2 lines, truncated)
- 📅 **Published date**
- 🔥 **Trend score** (if calculated, shown as percentage badge)
- 🔗 **Visit link** (opens in new tab)

### **3. Empty States**

- "No items fetched yet" message with icon
- Prompts user to click play button to fetch content

---

## 🎨 UI Design

### **Collapsed State** (Default)

```
┌───────────────────────────────────────────────────────────────┐
│  [RSS] TechCrunch                [Active]              [▼][▶][🗑] │
│  https://feeds.feedburner.com/TechCrunch/                     │
│  Added 10/22/2025 • 🕐 Fetch every 1 hour • 📥 Last: 30min ago │
└───────────────────────────────────────────────────────────────┘
```

### **Expanded State** (Shows Items)

```
┌───────────────────────────────────────────────────────────────────┐
│  [RSS] TechCrunch                [Active]              [▲][▶][🗑]   │
│  https://feeds.feedburner.com/TechCrunch/                         │
│  Added 10/22/2025 • 🕐 Fetch every 1 hour • 📥 Last: 30min ago     │
├───────────────────────────────────────────────────────────────────┤
│  Recent Items (Last 5)                                            │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 📄  Starcloud: Nvidia's New Platform                        │ │
│  │     Nvidia has been making waves with its new Starcloud...  │ │
│  │     📅 Oct 22, 2025  🔥 85%  🔗 Visit                       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 📄  HarmonyOS 6 Full Overview                               │ │
│  │     New design, AI features and privacy upgrades...         │ │
│  │     📅 Oct 22, 2025  🔥 82%  🔗 Visit                       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  [... 3 more items ...]                                          │
└───────────────────────────────────────────────────────────────────┘
```

### **Empty State** (No Items)

```
┌───────────────────────────────────────────────────────────────────┐
│  [RSS] New Blog                   [Active]              [▲][▶][🗑]   │
│  https://example.com/feed.xml                                     │
│  Added 10/22/2025 • 🕐 Fetch every 1 hour • 📥 Last: Never         │
├───────────────────────────────────────────────────────────────────┤
│  Recent Items (Last 5)                                            │
│                                                                   │
│                     📄                                            │
│          No items fetched yet.                                    │
│    Click the play button to fetch content.                       │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Technical Implementation

### **Backend Changes**

#### **1. New API Endpoint**

```python
GET /api/v1/ingestion/sources/{source_id}/items?limit=10
```

Returns recent items for a specific source:

```json
[
  {
    "id": "item-uuid",
    "title": "Article Title",
    "url": "https://...",
    "summary": "Article summary...",
    "published_at": "2025-10-22T10:00:00Z",
    "trend_score": 0.85
  }
]
```

#### **2. Service Method**

```python
# backend/app/core/ingestion/service.py
async def get_source_items(user_id, source_id, limit=10):
    # Verify source ownership
    # Fetch items from database
    # Return sorted by published_at DESC
```

### **Frontend Changes**

#### **1. API Service** (`frontend/src/services/api.ts`)

```typescript
async getSourceItems(sourceId: string, limit = 10) {
  const response = await api.get(
    endpoints.getSourceItems(sourceId),
    { params: { limit } }
  )
  return response.data
}
```

#### **2. Sources Component** (`frontend/src/pages/Sources.tsx`)

**State Management:**

```typescript
const [expandedSources, setExpandedSources] = useState<Set<string>>(new Set());
```

**Toggle Function:**

```typescript
const toggleSourceExpansion = (sourceId: string) => {
  const newExpanded = new Set(expandedSources);
  if (newExpanded.has(sourceId)) {
    newExpanded.delete(sourceId);
  } else {
    newExpanded.add(sourceId);
  }
  setExpandedSources(newExpanded);
};
```

**SourceItems Component:**

- Uses React Query for data fetching
- Only enabled when source is expanded
- Shows loading skeleton
- Displays items in beautiful cards
- Handles empty state

---

## 🎨 Design Features

### **1. Performance Optimized**

- ✅ Lazy loading: Items only fetch when expanded
- ✅ Conditional queries: `enabled: expandedSources.has(sourceId)`
- ✅ Caching: React Query caches responses
- ✅ Limit: Only fetches 5 most recent items

### **2. Beautiful UI**

- ✅ Smooth expand/collapse animations
- ✅ Hover states on all interactive elements
- ✅ Color-coded badges (type, status, trend score)
- ✅ Clean card layout with proper spacing
- ✅ Truncated text with `line-clamp-2`

### **3. Uncluttered**

- ✅ Collapsed by default (saves space)
- ✅ Expand on demand
- ✅ Clear visual hierarchy
- ✅ Proper whitespace

### **4. Accessibility**

- ✅ Clear button titles (tooltips)
- ✅ Semantic HTML
- ✅ Keyboard navigable
- ✅ Color contrast compliance

---

## 🧪 Testing Guide

### **Test 1: View Items**

1. Go to http://localhost:3000/sources
2. Find a source with fetched items
3. Click the **chevron down (▼)** button
4. Should expand and show 5 most recent items

**Expected:**

- Smooth animation
- Items appear with title, summary, date
- Each item is clickable

---

### **Test 2: Empty State**

1. Create a new source (never fetched)
2. Click chevron to expand
3. Should show empty state message

**Expected:**

- Icon displayed
- "No items fetched yet" message
- Prompt to click play button

---

### **Test 3: Collapse**

1. Expand a source
2. Click **chevron up (▲)** button
3. Should collapse smoothly

**Expected:**

- Items hidden
- Chevron changes to down (▼)
- Smooth animation

---

### **Test 4: Multiple Sources**

1. Have multiple sources
2. Expand source #1
3. Expand source #2
4. Both should show their items independently

**Expected:**

- Can expand multiple sources at once
- Each shows its own items
- No interference

---

## 📊 Files Modified

### **Backend (2 files)**

1. **`backend/app/api/v1/ingestion.py`**

   - Line 156-169: Added `GET /ingestion/sources/{source_id}/items` endpoint

2. **`backend/app/core/ingestion/service.py`**
   - Line 266-279: Added `get_source_items()` method

### **Frontend (2 files)**

3. **`frontend/src/services/api.ts`**

   - Line 61: Added endpoint definition
   - Line 125-130: Added `getSourceItems()` service function

4. **`frontend/src/pages/Sources.tsx`**
   - Lines 8-12: Added new icons
   - Lines 29-36: Added Item interface
   - Line 41: Added `expandedSources` state
   - Lines 79-88: Added `toggleSourceExpansion()` function
   - Lines 141-213: Added `SourceItems` component
   - Lines 360-444: Updated source rendering with expand/collapse

---

## 🎯 Benefits

### **1. Better User Experience**

- See what content is being fetched
- Verify sources are working correctly
- Preview items before generating newsletter
- Quick access to original articles

### **2. Transparency**

- Users know exactly what's in their sources
- Can spot stale or broken sources
- See trend scores for items
- Understand what AI will use

### **3. Clean Interface**

- Not overwhelming (collapsed by default)
- Expand only what you need
- Beautiful, modern design
- Easy to navigate

### **4. Performance**

- Only loads when needed
- Caches results
- Fast transitions
- Minimal API calls

---

## 💡 Future Enhancements

Possible future improvements:

- [ ] Show item count badge on source card
- [ ] Filter items by date range
- [ ] Search within items
- [ ] Bulk actions (mark as read, etc.)
- [ ] Preview full content in modal
- [ ] Mark favorites
- [ ] Export items list

---

## ✅ Summary

**What's New:**

- ✅ Expandable source cards with chevron button
- ✅ Beautiful item display with title, summary, date
- ✅ Trend score badges for scored items
- ✅ Empty state handling
- ✅ Performance optimized (lazy loading)
- ✅ Clean, uncluttered design

**How It Works:**

1. User clicks chevron (▼) to expand source
2. API fetches last 5 items for that source
3. Items display in beautiful cards
4. User can click to visit original article
5. Click chevron (▲) to collapse

**Ready to Test!** 🚀

Visit http://localhost:3000/sources and expand a source to see it in action!

---

**Implementation Complete!** 🎉
