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
  TrashIcon,
  Squares2X2Icon,
  ListBulletIcon,
  EnvelopeIcon
} from '@heroicons/react/24/outline'
import { apiService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import ConfirmDialog from '../components/ConfirmDialog'
import NewsletterRenderer from '../components/NewsletterRenderer'

interface Draft {
  id: string
  title: string
  body_md: string
  status: 'draft' | 'sent' | 'published'
  created_at: string
  sent_at?: string
  feedback?: {
    reaction: '👍' | '👎'
    created_at: string
  } | null
  generation_metadata?: {
    email_subject?: string
  }
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

  // Fetch drafts with feedback
  const { data: drafts, isLoading, error } = useQuery({
    queryKey: ['drafts'],
    queryFn: async () => {
      try {
        const apiDrafts = await apiService.getDrafts()
        
        // Fetch feedback for each draft
        const draftsWithFeedback = await Promise.all(
          apiDrafts.map(async (draft: any) => {
            try {
              const feedback = await apiService.getDraftFeedback(draft.id)
              // Get the most recent feedback
              const latestFeedback = feedback.length > 0 ? feedback[0] : null
              
              return {
                id: draft.id,
                title: draft.title || 'Untitled Newsletter',
                body_md: draft.body_md || '',
                status: draft.status || 'draft',
                created_at: draft.created_at,
                updated_at: draft.updated_at,
                sent_at: draft.sent_at,
                feedback: latestFeedback ? {
                  reaction: latestFeedback.reaction,
                  created_at: latestFeedback.created_at
                } : null
              }
            } catch (error) {
              console.error(`Failed to fetch feedback for draft ${draft.id}:`, error)
              return {
                id: draft.id,
                title: draft.title || 'Untitled Newsletter',
                body_md: draft.body_md || '',
                status: draft.status || 'draft',
                created_at: draft.created_at,
                updated_at: draft.updated_at,
                sent_at: draft.sent_at,
                feedback: null
              }
            }
          })
        )
        
        return draftsWithFeedback as Draft[]
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
        return { success: true, draftId, reaction }
      } catch (error) {
        console.error('Failed to submit feedback:', error)
        throw error
      }
    },
    onSuccess: (data) => {
      // Update the specific draft's feedback state optimistically
      queryClient.setQueryData(['drafts'], (oldDrafts: Draft[] | undefined) => {
        if (!oldDrafts) return oldDrafts
        return oldDrafts.map(draft => 
          draft.id === data.draftId 
            ? { ...draft, feedback: { reaction: data.reaction, created_at: new Date().toISOString() } }
            : draft
        )
      })
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
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleFeedback(draft.id, true)}
                          className={`p-2 rounded-xl transition-all duration-300 transform hover:scale-110 ${
                            draft.feedback?.reaction === '👍'
                              ? 'bg-green-500 text-white shadow-lg'
                              : 'bg-green-100 text-green-600 hover:bg-green-500 hover:text-white'
                          }`}
                          title="Good newsletter"
                        >
                          <HandThumbUpIcon className="h-5 w-5" />
                        </button>
                        <button
                          onClick={() => handleFeedback(draft.id, false)}
                          className={`p-2 rounded-xl transition-all duration-300 transform hover:scale-110 ${
                            draft.feedback?.reaction === '👎'
                              ? 'bg-red-500 text-white shadow-lg'
                              : 'bg-red-100 text-red-600 hover:bg-red-500 hover:text-white'
                          }`}
                          title="Needs improvement"
                        >
                          <HandThumbDownIcon className="h-5 w-5" />
                        </button>
                        <span className="text-xs text-gray-500 font-medium">
                          {draft.feedback ? draft.feedback.reaction : 'N/A'}
                        </span>
                      </div>
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

// Standardized newsletter preview modal
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
  // Calculate reading time
  const wordCount = draft.body_md.split(/\s+/).length
  const readingTime = Math.ceil(wordCount / 200)

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-slate-800 p-4 flex items-center justify-between border-b border-slate-200">
          <div className="flex items-center gap-3">
            <SparklesIcon className="h-6 w-6 text-slate-400" />
            <h3 className="text-lg font-medium text-slate-700">Newsletter Preview</h3>
          </div>
          <div className="flex items-center gap-2">
            {draft.status === 'draft' && (
              <button
                onClick={() => onSend(draft.id)}
                disabled={isSending}
                className="flex items-center gap-2 bg-slate-700 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-slate-600 transition-colors"
              >
                <PaperAirplaneIcon className="h-4 w-4" />
                {isSending ? 'Sending...' : 'Send Now'}
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-md transition-colors"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
        
        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 bg-white">
          {/* Email Subject Preview */}
          {draft.generation_metadata?.email_subject && (
            <div className="mb-4 p-3 bg-slate-50 rounded-md border border-slate-200">
              <div className="flex items-center gap-2 mb-1">
                <EnvelopeIcon className="h-4 w-4 text-slate-500" />
                <span className="text-xs font-medium text-slate-600 uppercase tracking-wide">Email Subject</span>
              </div>
              <p className="text-slate-800 text-sm font-medium">{draft.generation_metadata.email_subject}</p>
            </div>
          )}
          
          {/* Newsletter Header */}
          <div className="text-center mb-8 pb-6 border-b-2 border-slate-200 bg-gradient-to-r from-slate-50 to-blue-50 rounded-lg p-6">
            <h1 className="text-2xl font-bold mb-4 text-slate-800">
              {draft.title}
            </h1>
            <div className="flex items-center justify-center gap-6 text-slate-600 text-sm">
              <span className="flex items-center gap-2 bg-white px-3 py-1 rounded-full shadow-sm">
                <ClockIcon className="h-4 w-4 text-blue-500" />
                {new Date(draft.created_at).toLocaleDateString('en-US', { 
                  weekday: 'short', 
                  year: 'numeric', 
                  month: 'short', 
                  day: 'numeric' 
                })}
              </span>
              <span className="flex items-center gap-2 bg-white px-3 py-1 rounded-full shadow-sm">
                <span className="text-blue-500">☕</span>
                {readingTime} min read
              </span>
            </div>
          </div>

          {/* Newsletter Content using unified component */}
          <NewsletterRenderer 
            content={draft.body_md} 
            variant="draft"
            className="bg-transparent shadow-none border-none p-0"
          />

        </div>
      </div>
    </div>
  )
}
