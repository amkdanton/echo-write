import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  PlusIcon, 
  TrashIcon,
  PlayIcon,
  ExclamationTriangleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  DocumentTextIcon,
  CalendarIcon,
  LinkIcon,
  PencilIcon,
  RssIcon
} from '@heroicons/react/24/outline'
import { apiService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import toast from 'react-hot-toast'
import { TOPICS, PreloadedSource } from '../data/preloadedSources'
import ConfirmDialog from '../components/ConfirmDialog'
import BrowseSourcesModal from '../components/BrowseSourcesModal'

interface Source {
  id: string
  type: 'rss' | 'youtube' | 'twitter'
  handle: string
  name?: string
  topic?: string
  is_active: boolean
  fetch_frequency: number
  last_fetched_at?: string
  created_at: string
}

interface Item {
  id: string
  title: string
  url: string
  summary?: string
  published_at: string
  trend_score?: number
  image_url?: string
  image_alt?: string
}

export default function Sources() {
  const { } = useAuth()
  const [showAddForm, setShowAddForm] = useState(false)
  const [showBrowseModal, setShowBrowseModal] = useState(false)
  const [editingSource, setEditingSource] = useState<Source | null>(null)
  const [deleteConfirm, setDeleteConfirm] = useState<{ isOpen: boolean; sourceId: string | null }>({ 
    isOpen: false, 
    sourceId: null 
  })
  const [expandedSources, setExpandedSources] = useState<Set<string>>(new Set())
  const [newSource, setNewSource] = useState({
    type: 'rss' as const,
    handle: '',
    name: '',
    topic: '',
    fetch_frequency: 3600 // Default: 1 hour
  })
  const [customFrequency, setCustomFrequency] = useState<string>('')
  const [useCustomFrequency, setUseCustomFrequency] = useState(false)

  const queryClient = useQueryClient()

  // Helper function to format fetch frequency
  const formatFrequency = (seconds: number): string => {
    if (seconds < 3600) {
      const minutes = seconds / 60
      return `${minutes} min`
    } else if (seconds < 86400) {
      const hours = seconds / 3600
      return `${hours} hour${hours > 1 ? 's' : ''}`
    } else {
      const days = seconds / 86400
      return `${days} day${days > 1 ? 's' : ''}`
    }
  }

  // Helper function to format last fetched time
  const formatLastFetched = (timestamp?: string): string => {
    if (!timestamp) return 'Never'
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins} min ago`
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hour${Math.floor(diffMins / 60) > 1 ? 's' : ''} ago`
    return `${Math.floor(diffMins / 1440)} day${Math.floor(diffMins / 1440) > 1 ? 's' : ''} ago`
  }

  // Toggle source expansion
  const toggleSourceExpansion = (sourceId: string) => {
    const newExpanded = new Set(expandedSources)
    if (newExpanded.has(sourceId)) {
      newExpanded.delete(sourceId)
    } else {
      newExpanded.add(sourceId)
    }
    setExpandedSources(newExpanded)
  }

  // Fetch sources
  const { data: sources, isLoading } = useQuery({
    queryKey: ['sources'],
    queryFn: async () => {
      return await apiService.getSources()
    }
  })

  // Add source mutation
  const addSourceMutation = useMutation({
    mutationFn: async (sourceData: typeof newSource) => {
      return await apiService.createSource(sourceData)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] })
      setShowAddForm(false)
      setNewSource({ type: 'rss', handle: '', name: '', topic: '', fetch_frequency: 3600 })
      setCustomFrequency('')
      setUseCustomFrequency(false)
      toast.success('Source added successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to add source')
    }
  })

  // Update source mutation
  const updateSourceMutation = useMutation({
    mutationFn: async ({ sourceId, updates }: { sourceId: string, updates: any }) => {
      return await apiService.updateSource(sourceId, updates)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] })
      setEditingSource(null)
      setCustomFrequency('')
      setUseCustomFrequency(false)
      toast.success('Source updated successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update source')
    }
  })

  // Delete source mutation
  const deleteSourceMutation = useMutation({
    mutationFn: async (sourceId: string) => {
      return await apiService.deleteSource(sourceId)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sources'] })
      toast.success('Source deleted successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to delete source')
    }
  })

  // Test source mutation with loading state
  const [testingSourceId, setTestingSourceId] = useState<string | null>(null)
  
  const testSourceMutation = useMutation({
    mutationFn: async (sourceId: string) => {
      setTestingSourceId(sourceId)
      return await apiService.testSource(sourceId)
    },
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ['sources'] })
      queryClient.invalidateQueries({ queryKey: ['source-items'] })
      setTestingSourceId(null)
      toast.success(`Source test successful! Found ${result.new_items || 0} new items.`)
    },
    onError: (error: any) => {
      setTestingSourceId(null)
      toast.error(error.response?.data?.detail || 'Failed to test source')
    }
  })

  // Component to display source items
  const SourceItems = ({ sourceId }: { sourceId: string }) => {
    const { data: items, isLoading: itemsLoading } = useQuery({
      queryKey: ['source-items', sourceId],
      queryFn: () => apiService.getSourceItems(sourceId, 5),
      enabled: expandedSources.has(sourceId)
    })

    if (itemsLoading) {
      return (
        <div className="p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg animate-pulse">
          <div className="h-4 bg-gradient-to-r from-blue-200 to-purple-200 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-gradient-to-r from-blue-200 to-purple-200 rounded w-1/2"></div>
        </div>
      )
    }

    if (!items || items.length === 0) {
      return (
        <div className="p-6 bg-gradient-to-br from-gray-50 to-blue-50 rounded-lg text-center border-2 border-dashed border-gray-300">
          <div className="animate-bounce">
            <DocumentTextIcon className="h-12 w-12 mx-auto mb-3 text-blue-400" />
          </div>
          <p className="text-sm font-medium text-gray-600">No items fetched yet</p>
          <p className="text-xs text-gray-500 mt-1">Click the ▶ play button to fetch content</p>
        </div>
      )
    }

    return (
      <div className="mt-3 space-y-3">
        {items.map((item: Item, index: number) => (
          <div 
            key={item.id} 
            className="group p-4 bg-gradient-to-br from-white to-blue-50/30 border-2 border-gray-200 rounded-xl hover:border-blue-400 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5"
            style={{ animationDelay: `${index * 50}ms` }}
          >
            <div className="flex items-start gap-3">
              {/* Show image if available, otherwise show icon */}
              {item.image_url ? (
                <div className="flex-shrink-0">
                  <img 
                    src={item.image_url} 
                    alt={item.image_alt || item.title}
                    className="w-20 h-20 object-cover rounded-lg group-hover:scale-105 transition-transform duration-300 shadow-md"
                    onError={(e) => {
                      // Fallback to icon if image fails to load
                      const target = e.currentTarget as HTMLImageElement;
                      target.style.display = 'none';
                      const fallback = target.nextElementSibling as HTMLElement;
                      if (fallback) fallback.classList.remove('hidden');
                    }}
                  />
                  {/* Fallback icon (hidden by default) */}
                  <div className="hidden p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                    <DocumentTextIcon className="h-16 w-16 text-white" />
                  </div>
                </div>
              ) : (
                <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg group-hover:scale-110 transition-transform duration-300">
                  <DocumentTextIcon className="h-5 w-5 text-white flex-shrink-0" />
                </div>
              )}
              <div className="flex-1 min-w-0">
                <a 
                  href={item.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="font-semibold text-gray-900 hover:text-blue-600 line-clamp-2 block transition-colors duration-200"
                >
                  {item.title}
                </a>
                {item.summary && (
                  <p className="text-sm text-gray-600 mt-2 line-clamp-2 leading-relaxed">
                    {item.summary}
                  </p>
                )}
                <div className="flex items-center gap-3 mt-3 text-xs">
                  <div className="flex items-center gap-1.5 px-2 py-1 bg-gray-100 rounded-full text-gray-600">
                    <CalendarIcon className="h-3.5 w-3.5" />
                    {new Date(item.published_at).toLocaleDateString()}
                  </div>
                  {item.trend_score !== undefined && item.trend_score > 0 && (
                    <div className="flex items-center gap-1.5 px-2.5 py-1 bg-gradient-to-r from-orange-100 to-red-100 text-orange-700 rounded-full font-medium animate-pulse">
                      🔥 {(item.trend_score * 100).toFixed(0)}%
                    </div>
                  )}
                  <a 
                    href={item.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 px-2.5 py-1 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-full font-medium transition-colors duration-200"
                  >
                    <LinkIcon className="h-3.5 w-3.5" />
                    Visit
                  </a>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const finalFrequency = useCustomFrequency && customFrequency 
      ? parseInt(customFrequency) 
      : newSource.fetch_frequency
    addSourceMutation.mutate({ ...newSource, fetch_frequency: finalFrequency })
  }

  const handleEdit = (source: Source) => {
    setEditingSource(source)
    setCustomFrequency('')
    setUseCustomFrequency(false)
  }

  const handleUpdateSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!editingSource) return

    const updates: any = {
      name: editingSource.name,
      is_active: editingSource.is_active,
      fetch_frequency: useCustomFrequency && customFrequency
        ? parseInt(customFrequency)
        : editingSource.fetch_frequency
    }

    updateSourceMutation.mutate({ sourceId: editingSource.id, updates })
  }

  const handleDelete = (sourceId: string) => {
    setDeleteConfirm({ isOpen: true, sourceId })
  }

  const confirmDelete = () => {
    if (deleteConfirm.sourceId) {
      deleteSourceMutation.mutate(deleteConfirm.sourceId)
    }
    setDeleteConfirm({ isOpen: false, sourceId: null })
  }

  const handleAddPreloadedSource = (source: PreloadedSource, topic: string) => {
    const sourceData = {
      type: source.type as 'rss' | 'youtube' | 'twitter',
      handle: source.handle,
      name: source.name,
      topic: topic,
      fetch_frequency: 3600
    }
    addSourceMutation.mutate(sourceData as any)
    setShowBrowseModal(false)
  }

  const handleTest = (sourceId: string) => {
    testSourceMutation.mutate(sourceId)
  }

  if (isLoading) {
    return <div className="animate-pulse">Loading sources...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="md:flex md:items-center md:justify-between bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 p-6 rounded-2xl border-2 border-blue-100">
        <div className="min-w-0 flex-1">
          <h2 className="text-3xl font-extrabold leading-7 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 sm:text-4xl sm:tracking-tight">
            📡 Content Sources
          </h2>
          <p className="mt-2 text-sm text-gray-600 font-medium">
            Manage your RSS feeds, YouTube channels, and Twitter accounts with style! ✨
          </p>
        </div>
        <div className="mt-4 flex gap-3 md:ml-4 md:mt-0">
          <button
            onClick={() => setShowBrowseModal(true)}
            className="group relative px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center gap-2"
          >
            <RssIcon className="h-5 w-5" />
            Browse Sources
            <span className="absolute inset-0 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></span>
          </button>
          <button
            onClick={() => setShowAddForm(true)}
            className="group relative px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center gap-2"
          >
            <PlusIcon className="h-5 w-5 group-hover:rotate-90 transition-transform duration-300" />
            Add Custom
            <span className="absolute inset-0 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></span>
          </button>
        </div>
      </div>

      {/* Add Source Form */}
      {showAddForm && (
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Source</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Source Type
              </label>
              <select
                value={newSource.type}
                onChange={(e) => setNewSource({ ...newSource, type: e.target.value as any })}
                className="input-field"
              >
                <option value="rss">RSS Feed</option>
                <option value="youtube">YouTube Channel</option>
                <option value="twitter">Twitter Account</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {newSource.type === 'rss' ? 'RSS URL' : 
                 newSource.type === 'youtube' ? 'Channel ID or Username' : 
                 'Twitter Handle'}
              </label>
              <input
                type="text"
                value={newSource.handle}
                onChange={(e) => setNewSource({ ...newSource, handle: e.target.value })}
                placeholder={
                  newSource.type === 'rss' ? 'https://example.com/feed.xml' :
                  newSource.type === 'youtube' ? '@channelname or channel_id' :
                  '@username'
                }
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Display Name (optional)
              </label>
              <input
                type="text"
                value={newSource.name}
                onChange={(e) => setNewSource({ ...newSource, name: e.target.value })}
                placeholder="My Favorite Blog"
                className="input-field"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Topic/Category (optional)
              </label>
              <select
                value={newSource.topic}
                onChange={(e) => setNewSource({ ...newSource, topic: e.target.value })}
                className="input-field"
              >
                <option value="">-- Select a topic --</option>
                {TOPICS.map((topic) => (
                  <option key={topic.value} value={topic.value}>
                    {topic.icon} {topic.label}
                  </option>
                ))}
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Helps categorize your sources and get personalized recommendations
              </p>
            </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fetch Frequency
                  </label>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={useCustomFrequency}
                        onChange={(e) => setUseCustomFrequency(e.target.checked)}
                        className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                      />
                      <label className="text-sm text-gray-600">
                        Custom frequency (in seconds)
                      </label>
                    </div>
                    
                    {useCustomFrequency ? (
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
                        <span className="text-sm text-gray-500 whitespace-nowrap">
                          seconds
                        </span>
                      </div>
                    ) : (
                      <select
                        value={newSource.fetch_frequency}
                        onChange={(e) => setNewSource({ ...newSource, fetch_frequency: parseInt(e.target.value) })}
                        className="input-field"
                      >
                        <option value="300">Every 5 minutes (fast)</option>
                        <option value="900">Every 15 minutes</option>
                        <option value="1800">Every 30 minutes</option>
                        <option value="3600">Every 1 hour (default)</option>
                        <option value="7200">Every 2 hours</option>
                        <option value="10800">Every 3 hours</option>
                        <option value="21600">Every 6 hours</option>
                        <option value="43200">Every 12 hours</option>
                        <option value="86400">Once a day</option>
                        <option value="172800">Every 2 days</option>
                        <option value="604800">Once a week</option>
                      </select>
                    )}
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    {useCustomFrequency 
                      ? 'Enter fetch frequency in seconds (min 300 = 5 min, max 604800 = 7 days)'
                      : 'How often to check this source for new content'}
                  </p>
                </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={addSourceMutation.isPending}
                className="btn-primary"
              >
                {addSourceMutation.isPending ? 'Adding...' : 'Add Source'}
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Edit Source Modal */}
      {editingSource && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-gradient-to-r from-amber-500 to-orange-600 p-6 rounded-t-2xl">
              <h3 className="text-2xl font-bold text-white flex items-center gap-2">
                <PencilIcon className="h-7 w-7" />
                Edit Source
              </h3>
            </div>
            
            <form onSubmit={handleUpdateSubmit} className="p-6 space-y-5">
              <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg">
                <p className="text-sm text-blue-800">
                  <strong>Type:</strong> {editingSource.type.toUpperCase()} • 
                  <strong className="ml-2">Handle:</strong> {editingSource.handle}
                </p>
                <p className="text-xs text-blue-600 mt-1">
                  (Type and handle cannot be changed. Create a new source if needed.)
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Display Name
                </label>
                <input
                  type="text"
                  value={editingSource.name || ''}
                  onChange={(e) => setEditingSource({ ...editingSource, name: e.target.value })}
                  placeholder="Optional display name"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Topic/Category
                </label>
                <select
                  value={editingSource.topic || ''}
                  onChange={(e) => setEditingSource({ ...editingSource, topic: e.target.value })}
                  className="input-field"
                >
                  <option value="">-- Select a topic --</option>
                  {TOPICS.map((topic) => (
                    <option key={topic.value} value={topic.value}>
                      {topic.icon} {topic.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                <input
                  type="checkbox"
                  checked={editingSource.is_active}
                  onChange={(e) => setEditingSource({ ...editingSource, is_active: e.target.checked })}
                  className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                />
                <label className="text-sm font-medium text-gray-700">
                  Source is active (will be fetched automatically)
                </label>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fetch Frequency
                </label>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={useCustomFrequency}
                      onChange={(e) => setUseCustomFrequency(e.target.checked)}
                      className="h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <label className="text-sm text-gray-600">
                      Custom frequency (in seconds)
                    </label>
                  </div>
                  
                  {useCustomFrequency ? (
                    <div className="flex items-center gap-2">
                      <input
                        type="number"
                        min="300"
                        max="604800"
                        value={customFrequency || editingSource.fetch_frequency}
                        onChange={(e) => setCustomFrequency(e.target.value)}
                        placeholder="e.g., 7200 for 2 hours"
                        className="input-field flex-1"
                        required
                      />
                      <span className="text-sm text-gray-500 whitespace-nowrap">
                        seconds
                      </span>
                    </div>
                  ) : (
                    <select
                      value={editingSource.fetch_frequency}
                      onChange={(e) => setEditingSource({ ...editingSource, fetch_frequency: parseInt(e.target.value) })}
                      className="input-field"
                    >
                      <option value="300">Every 5 minutes (fast)</option>
                      <option value="900">Every 15 minutes</option>
                      <option value="1800">Every 30 minutes</option>
                      <option value="3600">Every 1 hour (default)</option>
                      <option value="7200">Every 2 hours</option>
                      <option value="10800">Every 3 hours</option>
                      <option value="21600">Every 6 hours</option>
                      <option value="43200">Every 12 hours</option>
                      <option value="86400">Once a day</option>
                      <option value="172800">Every 2 days</option>
                      <option value="604800">Once a week</option>
                    </select>
                  )}
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  {useCustomFrequency 
                    ? 'Enter fetch frequency in seconds (min 300 = 5 min, max 604800 = 7 days)'
                    : 'How often to check this source for new content'}
                </p>
                <div className="mt-2 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <p className="text-xs text-amber-800">
                    💡 <strong>How it works:</strong> The system will automatically fetch new items from this source 
                    after the specified time has passed since the last fetch. For example, if set to "Every 2 hours" (7200 seconds), 
                    it will check for new content 2 hours after the last successful fetch.
                  </p>
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={updateSourceMutation.isPending}
                  className="flex-1 group relative overflow-hidden bg-gradient-to-r from-amber-500 to-orange-600 text-white py-3 px-6 rounded-xl font-medium hover:from-amber-600 hover:to-orange-700 transition-all duration-300 transform hover:scale-105 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span className="relative z-10">
                    {updateSourceMutation.isPending ? 'Updating...' : 'Update Source'}
                  </span>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEditingSource(null)
                    setCustomFrequency('')
                    setUseCustomFrequency(false)
                  }}
                  className="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-medium hover:bg-gray-200 transition-all duration-300 transform hover:scale-105"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Sources List */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Your Sources</h3>
        <div className="space-y-4">
          {sources?.map((source: Source) => {
            const isExpanded = expandedSources.has(source.id)
            const isTesting = testingSourceId === source.id
            return (
              <div 
                key={source.id} 
                className="bg-gradient-to-br from-white to-gray-50 rounded-xl overflow-hidden border-2 border-gray-200 hover:border-blue-300 shadow-sm hover:shadow-md transition-all duration-300"
              >
                <div className="flex items-center justify-between p-5">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <span className={`px-3 py-1 text-xs font-bold rounded-full shadow-sm ${
                        source.type === 'rss' 
                          ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white' 
                          : source.type === 'youtube' 
                          ? 'bg-gradient-to-r from-red-500 to-red-600 text-white' 
                          : 'bg-gradient-to-r from-sky-500 to-sky-600 text-white'
                      }`}>
                        {source.type.toUpperCase()}
                      </span>
                      <h4 className="font-bold text-gray-900 text-lg">
                        {source.name || source.handle}
                      </h4>
                      {source.is_active ? (
                        <span className="px-3 py-1 text-xs font-bold rounded-full bg-gradient-to-r from-green-400 to-emerald-500 text-white shadow-sm animate-pulse">
                          ● Active
                        </span>
                      ) : (
                        <span className="px-3 py-1 text-xs font-medium rounded-full bg-gray-200 text-gray-600">
                          Inactive
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mt-2 font-medium">{source.handle}</p>
                    <div className="flex items-center gap-3 mt-3 flex-wrap">
                      <span className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 rounded-full text-xs font-medium">
                        📅 {new Date(source.created_at).toLocaleDateString()}
                      </span>
                      <span className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 rounded-full text-xs font-medium">
                        ⏰ Every {formatFrequency(source.fetch_frequency)}
                      </span>
                      <span className="flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-green-100 to-teal-100 text-green-700 rounded-full text-xs font-medium">
                        📥 {formatLastFetched(source.last_fetched_at)}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => toggleSourceExpansion(source.id)}
                      className={`group relative p-3 rounded-xl transition-all duration-300 transform hover:scale-110 ${
                        isExpanded 
                          ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-lg' 
                          : 'bg-gray-100 text-gray-600 hover:bg-gradient-to-br hover:from-blue-500 hover:to-purple-600 hover:text-white'
                      }`}
                      title={isExpanded ? "Hide items" : "Show items"}
                    >
                      {isExpanded ? (
                        <ChevronUpIcon className="h-5 w-5" />
                      ) : (
                        <ChevronDownIcon className="h-5 w-5" />
                      )}
                    </button>
                    <button
                      onClick={() => handleEdit(source)}
                      className="group p-3 bg-gray-100 text-gray-600 hover:bg-gradient-to-br hover:from-amber-500 hover:to-orange-600 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110 hover:shadow-lg"
                      title="Edit source"
                    >
                      <PencilIcon className="h-5 w-5 group-hover:rotate-12 transition-transform duration-300" />
                    </button>
                    <button
                      onClick={() => handleTest(source.id)}
                      disabled={isTesting}
                      className={`group relative p-3 rounded-xl transition-all duration-300 transform hover:scale-110 ${
                        isTesting
                          ? 'bg-gradient-to-br from-green-400 to-emerald-500 text-white animate-spin'
                          : 'bg-gray-100 text-gray-600 hover:bg-gradient-to-br hover:from-green-500 hover:to-emerald-600 hover:text-white hover:shadow-lg'
                      }`}
                      title={isTesting ? "Fetching..." : "Test & fetch content"}
                    >
                      <PlayIcon className={`h-5 w-5 ${isTesting ? 'animate-pulse' : ''}`} />
                      {isTesting && (
                        <span className="absolute -top-1 -right-1 flex h-3 w-3">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                        </span>
                      )}
                    </button>
                    <button
                      onClick={() => handleDelete(source.id)}
                      className="group p-3 bg-gray-100 text-gray-600 hover:bg-gradient-to-br hover:from-red-500 hover:to-pink-600 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110 hover:shadow-lg"
                      title="Delete source"
                    >
                      <TrashIcon className="h-5 w-5 group-hover:animate-bounce" />
                    </button>
                  </div>
                </div>

                {/* Expandable Items Section */}
                {isExpanded && (
                  <div className="px-5 pb-5 bg-gradient-to-b from-white to-blue-50/20 border-t-2 border-blue-100">
                    <div className="flex items-center justify-between mb-3 pt-4">
                      <h5 className="text-sm font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                        📰 Recent Items (Last 5)
                      </h5>
                    </div>
                    <SourceItems sourceId={source.id} />
                  </div>
                )}
              </div>
            )
          })}

          {sources?.length === 0 && (
            <div className="text-center py-12 bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl border-2 border-dashed border-blue-300">
              <div className="animate-bounce">
                <ExclamationTriangleIcon className="mx-auto h-16 w-16 text-blue-400" />
              </div>
              <h3 className="mt-4 text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                No sources yet! 🎯
              </h3>
              <p className="mt-2 text-sm text-gray-600 font-medium">
                Get started by adding your first content source above.
              </p>
              <button
                onClick={() => setShowAddForm(true)}
                className="mt-4 px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-300"
              >
                + Add Your First Source
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Confirmation Dialog */}
      <ConfirmDialog
        isOpen={deleteConfirm.isOpen}
        title="Delete Source"
        message="Are you sure you want to delete this source? This action cannot be undone and will remove all fetched items from this source."
        confirmText="Delete"
        cancelText="Cancel"
        type="danger"
        onConfirm={confirmDelete}
        onCancel={() => setDeleteConfirm({ isOpen: false, sourceId: null })}
      />

      {/* Browse Sources Modal */}
      <BrowseSourcesModal
        isOpen={showBrowseModal}
        onClose={() => setShowBrowseModal(false)}
        onAddSource={handleAddPreloadedSource}
      />
    </div>
  )
}
