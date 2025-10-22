# 📝 Edit Source Feature with Custom Frequency

## Overview

Added a comprehensive **Edit Source** feature that allows users to modify existing content sources, including the ability to set custom fetch frequencies in seconds.

---

## ✨ New Features

### 1. **Edit Source Button** 🎨

- **Location**: Each source card now has an **Edit** button (pencil icon)
- **Styling**: Amber to orange gradient on hover with rotation animation
- **Functionality**: Opens a modal to edit source details

### 2. **Custom Fetch Frequency** ⏱️

- **Dropdown Options**: Choose from preset frequencies (5 min to 7 days)
- **Custom Input**: Toggle to enter any custom frequency in seconds
- **Range**: Min 300 seconds (5 min), Max 604800 seconds (7 days)
- **Available in**: Both "Add Source" and "Edit Source" forms

### 3. **Edit Modal Fields**

- **Display Name**: Update the friendly name for the source
- **Active Status**: Toggle whether source is actively fetched
- **Fetch Frequency**: Update how often to check for new content
- **Type & Handle**: Read-only (cannot be changed after creation)

---

## 🎯 How Fetch Frequency Works

> **Your Understanding is 100% Correct!** ✅

The `fetch_frequency` determines:

- ⏰ **How often** the system automatically checks the source for new items
- 🔄 **After X seconds** since the last successful fetch
- 📊 **Updates the database** with any new items found

### Example Scenarios:

| Frequency        | Seconds | Behavior                               |
| ---------------- | ------- | -------------------------------------- |
| Every 5 minutes  | 300     | Checks every 5 minutes for new content |
| Every 2 hours    | 7200    | Checks every 2 hours for new content   |
| Custom: 10 hours | 36000   | Checks every 10 hours for new content  |
| Once a day       | 86400   | Checks once per day for new content    |

### Visual Flow:

```
Last Fetch: 2:00 PM
Frequency: 2 hours (7200 seconds)
Next Fetch: 4:00 PM (after 7200 seconds have passed)
↓
System fetches new items
↓
Updates database
↓
Resets timer for next fetch
```

---

## 🖼️ UI Components

### **Edit Button**

```typescript
<button
  onClick={() => handleEdit(source)}
  className="group p-3 bg-gray-100 text-gray-600 hover:bg-gradient-to-br hover:from-amber-500 hover:to-orange-600 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110 hover:shadow-lg"
  title="Edit source"
>
  <PencilIcon className="h-5 w-5 group-hover:rotate-12 transition-transform duration-300" />
</button>
```

### **Custom Frequency Toggle**

```typescript
<div className="flex items-center gap-2">
  <input
    type="checkbox"
    checked={useCustomFrequency}
    onChange={(e) => setUseCustomFrequency(e.target.checked)}
    className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
  />
  <label className="text-sm text-gray-600">Custom frequency (in seconds)</label>
</div>
```

### **Custom Frequency Input**

```typescript
{
  useCustomFrequency ? (
    <div className="flex items-center gap-2">
      <input
        type="number"
        min="300"
        max="604800"
        value={customFrequency}
        onChange={(e) => setCustomFrequency(e.target.value)}
        placeholder="e.g., 7200 for 2 hours"
        className="input-field flex-1"
        required
      />
      <span className="text-sm text-gray-500 whitespace-nowrap">seconds</span>
    </div>
  ) : (
    <select
      value={editingSource.fetch_frequency}
      onChange={(e) =>
        setEditingSource({
          ...editingSource,
          fetch_frequency: parseInt(e.target.value),
        })
      }
      className="input-field"
    >
      <option value="300">Every 5 minutes (fast)</option>
      <option value="3600">Every 1 hour (default)</option>
      <option value="7200">Every 2 hours</option>
      {/* ... more options */}
    </select>
  );
}
```

---

## 🔧 Technical Implementation

### **Frontend Changes** (`Sources.tsx`)

1. **State Management**:

   ```typescript
   const [editingSource, setEditingSource] = useState<Source | null>(null);
   const [customFrequency, setCustomFrequency] = useState<string>("");
   const [useCustomFrequency, setUseCustomFrequency] = useState(false);
   ```

2. **Update Mutation**:

   ```typescript
   const updateSourceMutation = useMutation({
     mutationFn: async ({
       sourceId,
       updates,
     }: {
       sourceId: string;
       updates: any;
     }) => {
       return await apiService.updateSource(sourceId, updates);
     },
     onSuccess: () => {
       queryClient.invalidateQueries({ queryKey: ["sources"] });
       setEditingSource(null);
       setCustomFrequency("");
       setUseCustomFrequency(false);
       toast.success("Source updated successfully!");
     },
   });
   ```

3. **Handlers**:

   ```typescript
   const handleEdit = (source: Source) => {
     setEditingSource(source);
     setCustomFrequency("");
     setUseCustomFrequency(false);
   };

   const handleUpdateSubmit = (e: React.FormEvent) => {
     e.preventDefault();
     if (!editingSource) return;

     const updates: any = {
       name: editingSource.name,
       is_active: editingSource.is_active,
       fetch_frequency:
         useCustomFrequency && customFrequency
           ? parseInt(customFrequency)
           : editingSource.fetch_frequency,
     };

     updateSourceMutation.mutate({ sourceId: editingSource.id, updates });
   };
   ```

### **Backend (Already Exists)**

The backend endpoints were already implemented in the previous update:

- ✅ `PUT /ingestion/sources/{source_id}` - Update source
- ✅ `SourceUpdate` schema with validation
- ✅ `update_source()` service method

---

## 🎨 Modal Design

### **Header**

- **Gradient**: Amber to orange (`from-amber-500 to-orange-600`)
- **Icon**: Pencil icon (`PencilIcon`)
- **Sticky**: Header stays at top when scrolling

### **Info Box**

- **Background**: Light blue (`bg-blue-50`)
- **Border**: Left border (`border-l-4 border-blue-500`)
- **Content**: Shows type and handle (read-only)

### **Explanation Box**

- **Background**: Light amber (`bg-amber-50`)
- **Border**: Amber border (`border-amber-200`)
- **Icon**: 💡 lightbulb
- **Content**: Explains how fetch frequency works

### **Buttons**

- **Update**: Amber to orange gradient with hover effects
- **Cancel**: Gray background with hover scale

---

## 📱 User Flow

### **Editing a Source**

1. **Click Edit Button**:

   - Pencil icon button on source card
   - Opens modal with current values pre-filled

2. **Modify Fields**:

   - Change display name
   - Toggle active status
   - Update fetch frequency (preset or custom)

3. **Choose Frequency**:

   - **Option A**: Select from dropdown (e.g., "Every 2 hours")
   - **Option B**: Check "Custom frequency" and enter seconds (e.g., 36000 for 10 hours)

4. **Submit**:
   - Click "Update Source"
   - Toast notification confirms success
   - Modal closes automatically
   - Source card updates with new values

---

## 🧪 Testing Examples

### **Test 1: Edit with Preset Frequency**

```
1. Click edit button on an RSS source
2. Change name to "My Tech Blog"
3. Select "Every 6 hours" from dropdown
4. Click "Update Source"
✅ Expected: Source updates, shows "Every 6 hours" badge
```

### **Test 2: Edit with Custom Frequency**

```
1. Click edit button on a YouTube source
2. Check "Custom frequency (in seconds)"
3. Enter 36000 (10 hours)
4. Click "Update Source"
✅ Expected: Source updates, shows "10.0 hours" badge
```

### **Test 3: Deactivate Source**

```
1. Click edit button on any source
2. Uncheck "Source is active"
3. Click "Update Source"
✅ Expected: Source badge shows "Inactive"
```

### **Test 4: Cancel Edit**

```
1. Click edit button
2. Make changes
3. Click "Cancel"
✅ Expected: Modal closes, no changes saved
```

---

## 🚀 Quick Reference

### **Preset Frequencies**

| Label            | Seconds  | Use Case                         |
| ---------------- | -------- | -------------------------------- |
| Every 5 minutes  | 300      | Breaking news, high-volume feeds |
| Every 15 minutes | 900      | Active blogs, social media       |
| Every 30 minutes | 1800     | Regular news sites               |
| **Every 1 hour** | **3600** | **Default - Balanced**           |
| Every 2 hours    | 7200     | Low-frequency blogs              |
| Every 6 hours    | 21600    | Weekly newsletters               |
| Once a day       | 86400    | Archive sites                    |
| Once a week      | 604800   | Rarely updated sources           |

### **Custom Examples**

| Duration   | Seconds | Input    |
| ---------- | ------- | -------- |
| 10 minutes | 600     | `600`    |
| 45 minutes | 2700    | `2700`   |
| 4 hours    | 14400   | `14400`  |
| 10 hours   | 36000   | `36000`  |
| 3 days     | 259200  | `259200` |

### **Validation**

- ❌ Less than 300 seconds: Error
- ❌ More than 604800 seconds: Error
- ✅ Between 300-604800 seconds: Valid

---

## 💡 Pro Tips

1. **High-Frequency Sources**: Use 5-15 minutes for breaking news or social media
2. **Standard Blogs**: Stick with 1-2 hours (default)
3. **Newsletters**: Use 6-12 hours or once a day
4. **Archive Sites**: Use once a week
5. **Custom Timing**: Perfect for sources that update at specific intervals

---

## 🎯 Benefits

✅ **Flexibility**: Set any frequency from 5 minutes to 7 days
✅ **Precision**: Custom input for exact requirements (e.g., 10 hours)
✅ **Control**: Edit anytime without recreating sources
✅ **Efficiency**: Avoid unnecessary fetches for slow-updating sources
✅ **User-Friendly**: Preset options + custom input for power users

---

## 🎨 Animations

### **Edit Button**

- **Idle**: Gray background
- **Hover**: Amber to orange gradient, scale 1.1x, shadow
- **Icon**: Rotates 12° on hover

### **Modal**

- **Backdrop**: Black/50 with blur
- **Entry**: Smooth fade-in
- **Header**: Sticky with gradient
- **Buttons**: Scale and gradient animations

---

## 📝 Summary

| Feature                   | Status             |
| ------------------------- | ------------------ |
| Edit Button               | ✅ Added           |
| Edit Modal                | ✅ Implemented     |
| Custom Frequency Input    | ✅ Working         |
| Preset Frequency Dropdown | ✅ Enhanced        |
| Form Validation           | ✅ Active          |
| Success Notifications     | ✅ Integrated      |
| Animations                | ✅ Polished        |
| Backend API               | ✅ Already existed |

---

## 🔗 Related Files

- **Frontend**: `frontend/src/pages/Sources.tsx`
- **Backend API**: `backend/app/api/v1/ingestion.py`
- **Backend Service**: `backend/app/core/ingestion/service.py`
- **Schemas**: `backend/app/models/schemas.py`
- **API Client**: `frontend/src/services/api.ts`

---

**Ready to test!** 🚀 Click the edit button (pencil icon) on any source to try it out!
