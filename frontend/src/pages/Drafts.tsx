import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'
import { 
  EyeIcon, 
  PaperAirplaneIcon,
  HandThumbUpIcon,
  HandThumbDownIcon,
  DocumentTextIcon,
  XMarkIcon,
  SparklesIcon,
  ClockIcon,
  FireIcon,
  LightBulbIcon,
  ChartBarIcon,
  TrashIcon,
  Squares2X2Icon,
  ListBulletIcon
} from '@heroicons/react/24/outline'
import { apiService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import ConfirmDialog from '../components/ConfirmDialog'

interface Draft {
  id: string
  title: string
  body_md: string
  status: 'draft' | 'sent' | 'published'
  created_at: string
  sent_at?: string
}

export default function Drafts() {
  const [selectedDraft, setSelectedDraft] = useState<Draft | null>(null)
  const [showPreview, setShowPreview] = useState(false)
  const [viewMode, setViewMode] = useState<'cards' | 'list'>('cards')
  const [deleteConfirm, setDeleteConfirm] = useState<{ isOpen: boolean; draftId: string | null }>({ 
    isOpen: false, 
    draftId: null 
  })
  const [sendEmailDialog, setSendEmailDialog] = useState<{ isOpen: boolean; draftId: string | null; email: string }>({ 
    isOpen: false, 
    draftId: null,
    email: ''
  })

  const queryClient = useQueryClient()
  
  // Get user email from auth context
  const { user } = useAuth()

  // Fetch drafts
  const { data: drafts, isLoading, error } = useQuery({
    queryKey: ['drafts'],
    queryFn: async () => {
      try {
        const apiDrafts = await apiService.getDrafts()
        return apiDrafts.map((draft: any) => ({
          id: draft.id,
          title: draft.title || 'Untitled Newsletter',
          body_md: draft.body_md || '',
          status: draft.status || 'draft',
          created_at: draft.created_at,
          updated_at: draft.updated_at,
          sent_at: draft.sent_at
        })) as Draft[]
      } catch (error) {
        console.error('Failed to fetch drafts:', error)
        return []
      }
    }
  })

  // Send draft mutation
  const sendDraftMutation = useMutation({
    mutationFn: async ({ draftId, email }: { draftId: string; email: string }) => {
      try {
        await apiService.sendNewsletter(draftId, email)
        return { success: true }
      } catch (error) {
        console.error('Failed to send newsletter:', error)
        throw error
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drafts'] })
      setShowPreview(false)
      setSendEmailDialog({ isOpen: false, draftId: null, email: '' })
      toast.success('Newsletter sent successfully! 🎉 Check your inbox!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to send newsletter')
    }
  })

  const handleSendNewsletter = (draftId: string) => {
    setSendEmailDialog({ 
      isOpen: true, 
      draftId, 
      email: user?.email || '' 
    })
  }

  // Feedback mutation
  const feedbackMutation = useMutation({
    mutationFn: async ({ draftId, reaction }: { draftId: string, reaction: '👍' | '👎' }) => {
      try {
        await apiService.submitFeedback(draftId, reaction, '')
        return { success: true }
      } catch (error) {
        console.error('Failed to submit feedback:', error)
        throw error
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drafts'] })
      toast.success('Feedback submitted! 💬')
    },
    onError: () => {
      toast.error('Failed to submit feedback')
    }
  })

  // Delete draft mutation
  const deleteDraftMutation = useMutation({
    mutationFn: async (draftId: string) => {
      try {
        await apiService.deleteDraft(draftId)
        return { success: true }
      } catch (error) {
        console.error('Failed to delete draft:', error)
        throw error
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['drafts'] })
      toast.success('Draft deleted! 🗑️')
    },
    onError: () => {
      toast.error('Failed to delete draft')
    }
  })

  const handleSend = (draftId: string) => {
    handleSendNewsletter(draftId)
  }

  const confirmSend = () => {
    if (sendEmailDialog.draftId && sendEmailDialog.email) {
      sendDraftMutation.mutate({ 
        draftId: sendEmailDialog.draftId, 
        email: sendEmailDialog.email 
      })
    }
  }

  const handleFeedback = (draftId: string, isPositive: boolean) => {
    feedbackMutation.mutate({ draftId, reaction: isPositive ? '👍' : '👎' })
  }

  const handleDelete = (draftId: string) => {
    setDeleteConfirm({ isOpen: true, draftId })
  }

  const confirmDelete = () => {
    if (deleteConfirm.draftId) {
      deleteDraftMutation.mutate(deleteConfirm.draftId)
    }
    setDeleteConfirm({ isOpen: false, draftId: null })
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-20 bg-gradient-to-r from-purple-100 to-pink-100 rounded-2xl mb-6"></div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-48 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-16">
        <div className="inline-block p-6 bg-gradient-to-br from-red-50 to-pink-50 rounded-full mb-4">
          <DocumentTextIcon className="h-16 w-16 text-red-400" />
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">Error loading drafts</h3>
        <p className="text-gray-600">
          Failed to load drafts. Please try again later.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with gradient */}
      <div className="relative overflow-hidden bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 rounded-2xl p-8 shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative">
          <h2 className="text-3xl font-bold text-white sm:text-4xl flex items-center gap-3">
            <DocumentTextIcon className="h-10 w-10" />
            Newsletter Drafts
          </h2>
          <p className="mt-2 text-purple-100 text-lg">
            Review, edit, and send your AI-generated newsletters. ✨
          </p>
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-600">View:</span>
          <div className="inline-flex rounded-xl border-2 border-gray-200 bg-white p-1 shadow-sm">
            <button
              onClick={() => setViewMode('cards')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                viewMode === 'cards'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Squares2X2Icon className="h-5 w-5" />
              Cards
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                viewMode === 'list'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <ListBulletIcon className="h-5 w-5" />
              List
            </button>
          </div>
        </div>
        <div className="text-sm text-gray-500">
          {drafts?.length || 0} draft{drafts?.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Drafts Grid or List */}
      {drafts && drafts.length > 0 ? (
        viewMode === 'cards' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {drafts.map((draft, index) => (
            <div 
              key={draft.id} 
              className="group bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg border-2 border-gray-200 hover:border-purple-300 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {/* Status Banner */}
              <div className={`h-2 ${
                draft.status === 'sent' 
                  ? 'bg-gradient-to-r from-green-400 to-emerald-500' 
                  : draft.status === 'published'
                  ? 'bg-gradient-to-r from-blue-400 to-cyan-500'
                  : 'bg-gradient-to-r from-yellow-400 to-orange-500'
              }`}></div>

              <div className="p-6">
                {/* Title */}
                <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-purple-600 transition-colors">
                  {draft.title}
                </h3>

                {/* Meta Info */}
                <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                  <span className="flex items-center gap-1">
                    <ClockIcon className="h-4 w-4" />
                    {new Date(draft.created_at).toLocaleDateString()}
                  </span>
                  {draft.sent_at && (
                    <span className="flex items-center gap-1 text-green-600">
                      <PaperAirplaneIcon className="h-4 w-4" />
                      Sent
                    </span>
                  )}
                </div>

                {/* Status Badge */}
                <div className="mb-4">
                  <span className={`inline-flex items-center gap-2 px-4 py-2 text-sm font-bold rounded-full shadow-md ${
                    draft.status === 'sent' 
                      ? 'bg-gradient-to-r from-green-400 to-emerald-500 text-white' 
                      : draft.status === 'published'
                      ? 'bg-gradient-to-r from-blue-400 to-cyan-500 text-white'
                      : 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white'
                  }`}>
                    {draft.status === 'sent' ? '✓ Sent' : draft.status === 'published' ? '📡 Published' : '📝 Draft'}
                  </span>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2 pt-4 border-t border-gray-200">
                  <button
                    onClick={() => {
                      setSelectedDraft(draft)
                      setShowPreview(true)
                    }}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105"
                  >
                    <EyeIcon className="h-4 w-4" />
                    Preview
                  </button>
                  
                  {draft.status === 'draft' && (
                    <button
                      onClick={() => handleSend(draft.id)}
                      disabled={sendDraftMutation.isPending}
                      className="p-2 bg-green-100 text-green-600 hover:bg-gradient-to-br hover:from-green-500 hover:to-emerald-600 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110"
                      title="Send newsletter"
                    >
                      <PaperAirplaneIcon className="h-5 w-5" />
                    </button>
                  )}

                  {draft.status === 'sent' && (
                    <>
                      <button
                        onClick={() => handleFeedback(draft.id, true)}
                        className="p-2 bg-green-100 text-green-600 hover:bg-green-500 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110"
                        title="Good newsletter"
                      >
                        <HandThumbUpIcon className="h-5 w-5" />
                      </button>
                      <button
                        onClick={() => handleFeedback(draft.id, false)}
                        className="p-2 bg-red-100 text-red-600 hover:bg-red-500 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110"
                        title="Needs improvement"
                      >
                        <HandThumbDownIcon className="h-5 w-5" />
                      </button>
                    </>
                  )}

                  {/* Delete Button */}
                  <button
                    onClick={() => handleDelete(draft.id)}
                    disabled={deleteDraftMutation.isPending}
                    className="p-2 bg-red-100 text-red-600 hover:bg-gradient-to-br hover:from-red-500 hover:to-pink-600 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110"
                    title="Delete draft"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
        ) : (
          /* LIST VIEW */
          <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gradient-to-r from-purple-50 to-pink-50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Title</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {drafts.map((draft) => (
                  <tr key={draft.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <DocumentTextIcon className="h-5 w-5 text-purple-500 flex-shrink-0" />
                        <div>
                          <div className="font-semibold text-gray-900">{draft.title}</div>
                          {draft.sent_at && (
                            <div className="text-xs text-gray-500">Sent {new Date(draft.sent_at).toLocaleDateString()}</div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(draft.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-3 py-1 text-xs font-bold rounded-full ${
                        draft.status === 'sent' 
                          ? 'bg-green-100 text-green-800' 
                          : draft.status === 'published'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {draft.status === 'sent' ? '✓ Sent' : draft.status === 'published' ? '📡 Published' : '📝 Draft'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => { setSelectedDraft(draft); setShowPreview(true); }}
                          className="p-2 bg-blue-100 text-blue-600 hover:bg-blue-200 rounded-lg transition-colors"
                          title="Preview"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </button>
                        {draft.status === 'draft' && (
                          <button
                            onClick={() => handleSend(draft.id)}
                            className="p-2 bg-green-100 text-green-600 hover:bg-green-200 rounded-lg transition-colors"
                            title="Send"
                          >
                            <PaperAirplaneIcon className="h-4 w-4" />
                          </button>
                        )}
                        <button
                          onClick={() => handleDelete(draft.id)}
                          className="p-2 bg-red-100 text-red-600 hover:bg-red-200 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <TrashIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      ) : (
        <div className="text-center py-16">
          <div className="inline-block p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-full mb-4 animate-bounce">
            <DocumentTextIcon className="h-16 w-16 text-purple-400" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No drafts yet</h3>
          <p className="text-gray-600 mb-6 text-lg">
            Your AI-generated newsletters will appear here. 🚀
          </p>
          <button className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-xl font-bold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg">
            <SparklesIcon className="h-6 w-6" />
            Generate First Newsletter
          </button>
        </div>
      )}

      {/* Enhanced Preview Modal */}
      {showPreview && selectedDraft && (
        <NewsletterPreviewModal 
          draft={selectedDraft} 
          onClose={() => setShowPreview(false)}
          onSend={handleSend}
          isSending={sendDraftMutation.isPending}
        />
      )}

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={deleteConfirm.isOpen}
        title="Delete Draft"
        message="Are you sure you want to delete this draft? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
        type="danger"
        onConfirm={confirmDelete}
        onCancel={() => setDeleteConfirm({ isOpen: false, draftId: null })}
      />

      {/* Email Input Dialog */}
      {sendEmailDialog.isOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">📧 Send Newsletter</h3>
            <p className="text-gray-600 mb-6">Enter the email address where you'd like to receive this newsletter.</p>
            
            <input
              type="email"
              placeholder="your@email.com"
              value={sendEmailDialog.email}
              onChange={(e) => setSendEmailDialog({ ...sendEmailDialog, email: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all mb-4"
              autoFocus
            />
            
            <div className="flex gap-3">
              <button
                onClick={() => setSendEmailDialog({ isOpen: false, draftId: null, email: '' })}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-xl hover:bg-gray-300 transition-colors font-medium"
              >
                Cancel
              </button>
              <button
                onClick={confirmSend}
                disabled={!sendEmailDialog.email || sendDraftMutation.isPending}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all font-bold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {sendDraftMutation.isPending ? 'Sending...' : 'Send Now 🚀'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// Magazine-style preview modal
function NewsletterPreviewModal({ 
  draft, 
  onClose, 
  onSend, 
  isSending 
}: { 
  draft: Draft
  onClose: () => void
  onSend: (id: string) => void
  isSending: boolean
}) {
  // Parse special sections from markdown
  const parseNewsletterSections = (markdown: string) => {
    const sections = {
      executiveSummary: '',
      didYouKnow: '',
      byTheNumbers: [] as string[],
      mainContent: markdown
    }

    // Extract Executive Summary
    const execMatch = markdown.match(/##?\s*📝\s*Executive Summary[\s\S]*?\n([\s\S]*?)(?=\n##|$)/i)
    if (execMatch) {
      sections.executiveSummary = execMatch[1].trim()
      sections.mainContent = sections.mainContent.replace(execMatch[0], '')
    }

    // Extract Did You Know
    const didYouKnowMatch = markdown.match(/##?\s*💡\s*Did You Know\?[\s\S]*?\n([\s\S]*?)(?=\n##|$)/i)
    if (didYouKnowMatch) {
      sections.didYouKnow = didYouKnowMatch[1].trim()
      sections.mainContent = sections.mainContent.replace(didYouKnowMatch[0], '')
    }

    // Extract By The Numbers
    const numbersMatch = markdown.match(/##?\s*📊\s*By The Numbers[\s\S]*?\n([\s\S]*?)(?=\n##|$)/i)
    if (numbersMatch) {
      const numbersContent = numbersMatch[1].trim()
      sections.byTheNumbers = numbersContent
        .split('\n')
        .filter(line => line.trim().match(/^[-•*]\s/))
        .map(line => line.replace(/^[-•*]\s+/, '').trim())
      sections.mainContent = sections.mainContent.replace(numbersMatch[0], '')
    }

    return sections
  }

  const formatMarkdown = (markdown: string) => {
    return markdown
      // Handle images
      .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="w-full rounded-xl shadow-lg my-6 object-cover max-h-96" />')
      // Handle links
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-purple-600 hover:text-purple-800 font-semibold underline decoration-2 decoration-purple-300 hover:decoration-purple-500 transition-all">$1</a>')
      // Headers
      .replace(/^# (.*$)/gim, '<h1 class="text-4xl font-black mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">$1</h1>')
      .replace(/^## (.*$)/gim, '<h2 class="text-3xl font-bold mb-4 mt-8 text-gray-900 flex items-center gap-2"><span class="text-purple-600">▸</span> $1</h2>')
      .replace(/^### (.*$)/gim, '<h3 class="text-2xl font-semibold mb-3 text-gray-800">$1</h3>')
      // Lists
      .replace(/^[-•*] (.*$)/gim, '<li class="mb-2 text-gray-700 leading-relaxed">$1</li>')
      .replace(/^\d+\. (.*$)/gim, '<li class="mb-2 text-gray-700 leading-relaxed">$1</li>')
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-gray-900">$1</strong>')
      // Paragraphs
      .replace(/\n\n/g, '</p><p class="mb-4 text-gray-700 leading-relaxed">')
      .replace(/^(?!<[h|l|i])/gm, '<p class="mb-4 text-gray-700 leading-relaxed">')
  }

  const sections = parseNewsletterSections(draft.body_md)
  
  // Calculate reading time
  const wordCount = draft.body_md.split(/\s+/).length
  const readingTime = Math.ceil(wordCount / 200)

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <SparklesIcon className="h-8 w-8 text-white" />
            <h3 className="text-2xl font-bold text-white">Newsletter Preview</h3>
          </div>
          <div className="flex items-center gap-2">
            {draft.status === 'draft' && (
              <button
                onClick={() => onSend(draft.id)}
                disabled={isSending}
                className="flex items-center gap-2 bg-white text-purple-600 px-6 py-2 rounded-xl font-bold hover:bg-purple-50 transition-all duration-300 transform hover:scale-105"
              >
                <PaperAirplaneIcon className="h-5 w-5" />
                {isSending ? 'Sending...' : 'Send Now'}
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 text-white hover:bg-white/20 rounded-lg transition-colors"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>
        </div>
        
        {/* Content */}
        <div className="flex-1 overflow-y-auto p-8 bg-gradient-to-b from-white to-gray-50">
          {/* Newsletter Header */}
          <div className="text-center mb-8 pb-8 border-b-2 border-purple-200">
            <h1 className="text-4xl md:text-5xl font-black mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              {draft.title}
            </h1>
            <div className="flex items-center justify-center gap-6 text-gray-600">
              <span className="flex items-center gap-2">
                <ClockIcon className="h-5 w-5" />
                {new Date(draft.created_at).toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </span>
              <span className="flex items-center gap-2">
                ☕ {readingTime} min read
              </span>
            </div>
          </div>

          {/* Executive Summary Box - Only show if present */}
          {sections.executiveSummary && (
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 border-l-4 border-blue-500 rounded-xl p-6 mb-8 shadow-md hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center gap-2 mb-3">
                <FireIcon className="h-6 w-6 text-blue-600" />
                <h3 className="text-xl font-bold text-gray-900">📝 Executive Summary</h3>
              </div>
              <div 
                className="text-gray-700 leading-relaxed"
                dangerouslySetInnerHTML={{ __html: formatMarkdown(sections.executiveSummary) }}
              />
            </div>
          )}

          {/* Main Content */}
          <div className="prose prose-lg max-w-none mb-8">
            <div 
              dangerouslySetInnerHTML={{ 
                __html: formatMarkdown(sections.mainContent) 
              }}
              className="newsletter-content"
            />
          </div>

          {/* Trivia Section - Only show if present */}
          {sections.didYouKnow && (
            <div className="bg-gradient-to-br from-yellow-50 to-orange-50 border-l-4 border-yellow-500 rounded-xl p-6 mb-8 shadow-md hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center gap-2 mb-3">
                <LightBulbIcon className="h-6 w-6 text-yellow-600" />
                <h3 className="text-xl font-bold text-gray-900">💡 Did You Know?</h3>
              </div>
              <div 
                className="text-gray-700 leading-relaxed"
                dangerouslySetInnerHTML={{ __html: formatMarkdown(sections.didYouKnow) }}
              />
            </div>
          )}

          {/* By The Numbers - Only show if present */}
          {sections.byTheNumbers.length > 0 && (
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-l-4 border-green-500 rounded-xl p-6 mb-8 shadow-md hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center gap-2 mb-4">
                <ChartBarIcon className="h-6 w-6 text-green-600" />
                <h3 className="text-xl font-bold text-gray-900">📊 By The Numbers</h3>
              </div>
              <div className="space-y-3">
                {sections.byTheNumbers.map((stat, index) => (
                  <div 
                    key={index} 
                    className="flex items-start gap-3 p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
                  >
                    <span className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600">
                      {index + 1}
                    </span>
                    <p className="text-gray-700 leading-relaxed flex-1">{stat}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="text-center mt-8 pt-8 border-t border-gray-200">
            <p className="text-gray-600">
              Crafted with ✨ by EchoWrite
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
