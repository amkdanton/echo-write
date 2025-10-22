import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  ArrowPathIcon,
  DocumentTextIcon,
  RssIcon,
  FireIcon,
  EyeIcon,
  SparklesIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import { apiService } from '../services/api'
import toast from 'react-hot-toast'
import NewsletterGenerationLoader from '../components/NewsletterGenerationLoader'

export default function Dashboard() {
  const [isGenerating, setIsGenerating] = useState(false)

  // Fetch dashboard data
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      // Fetch sources and drafts to calculate stats
      const [sources, drafts] = await Promise.all([
        apiService.getSources(),
        apiService.getDrafts()
      ])
      
      return {
        totalSources: sources.length,
        activeSources: sources.filter((s: any) => s.is_active).length,
        totalItems: 0, // Will be calculated from items table
        draftsGenerated: drafts.length,
        lastGeneration: drafts.length > 0 ? drafts[0].created_at : null
      }
    }
  })

  const { data: recentDrafts } = useQuery({
    queryKey: ['recent-drafts'],
    queryFn: async () => {
      return await apiService.getDrafts()
    }
  })

  const handleGenerateNow = async () => {
    setIsGenerating(true)
    try {
      const sources = await apiService.getSources()
      
      if (sources.length === 0) {
        toast.error('Please add sources first')
        setIsGenerating(false)
        return
      }
      
      // The loader will handle the visual progress
      // Step 1: Process feeds to get fresh content
      const sourceIds = sources.map((s: any) => s.id)
      await apiService.processFeeds(sourceIds, true)
      
      // Step 2: Generate newsletter
      const result = await apiService.generateNewsletter([], undefined)
      
      if (result.success) {
        console.log('Newsletter generated:', result)
        // Loader will show completion and then redirect
      } else {
        toast.error(result.message || 'Generation failed')
        setIsGenerating(false)
      }
    } catch (error: any) {
      console.error('Generation failed:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate newsletter')
      setIsGenerating(false)
    }
  }

  const handleGenerationComplete = () => {
    toast.success('Newsletter generated successfully! 🎉')
    setTimeout(() => {
      window.location.reload()
    }, 500)
  }

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-20 bg-gradient-to-r from-blue-100 to-purple-100 rounded-2xl"></div>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl"></div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with gradient */}
      <div className="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-8 shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative md:flex md:items-center md:justify-between">
          <div className="min-w-0 flex-1">
            <h2 className="text-3xl font-bold text-white sm:text-4xl flex items-center gap-3">
              <SparklesIcon className="h-10 w-10 animate-pulse" />
              Dashboard
            </h2>
            <p className="mt-2 text-blue-100 text-lg">
              Welcome back! Here's what's happening with your newsletters. 📰
            </p>
          </div>
          <div className="mt-4 flex md:ml-4 md:mt-0">
            <button
              onClick={handleGenerateNow}
              disabled={isGenerating}
              className={`group relative overflow-hidden bg-white text-blue-600 px-6 py-4 rounded-xl font-bold flex items-center gap-2 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-2xl ${
                isGenerating ? 'animate-pulse' : ''
              }`}
            >
              <ArrowPathIcon className={`h-6 w-6 ${isGenerating ? 'animate-spin' : 'group-hover:rotate-180 transition-transform duration-500'}`} />
              <span>{isGenerating ? 'Generating Magic...' : 'Generate Now'}</span>
              {isGenerating && (
                <span className="absolute -top-1 -right-1 flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-600"></span>
                </span>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards with gradients and animations */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          icon={<RssIcon className="h-8 w-8" />}
          label="Active Sources"
          value={stats?.activeSources || 0}
          total={stats?.totalSources || 0}
          gradient="from-blue-500 to-cyan-500"
          delay="0"
        />
        <StatsCard
          icon={<DocumentTextIcon className="h-8 w-8" />}
          label="Content Items"
          value={stats?.totalItems || 0}
          gradient="from-green-500 to-emerald-500"
          delay="100"
        />
        <StatsCard
          icon={<FireIcon className="h-8 w-8" />}
          label="Drafts Generated"
          value={stats?.draftsGenerated || 0}
          gradient="from-orange-500 to-red-500"
          delay="200"
        />
        <StatsCard
          icon={<ClockIcon className="h-8 w-8" />}
          label="Last Generated"
          value={stats?.lastGeneration ? new Date(stats.lastGeneration).toLocaleDateString() : 'Never'}
          gradient="from-purple-500 to-pink-500"
          delay="300"
          isDate
        />
      </div>

      {/* Recent Drafts with enhanced design */}
      <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg border-2 border-gray-200 overflow-hidden">
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b-2 border-blue-100">
          <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 flex items-center gap-2">
            <ChartBarIcon className="h-7 w-7 text-blue-600" />
            Recent Drafts
          </h3>
        </div>
        <div className="p-6">
          {recentDrafts && recentDrafts.length > 0 ? (
            <div className="space-y-4">
              {recentDrafts.slice(0, 5).map((draft: any, index: number) => (
                <div 
                  key={draft.id} 
                  className="group bg-gradient-to-br from-white to-blue-50/30 rounded-xl p-5 border-2 border-gray-200 hover:border-blue-400 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <DocumentTextIcon className="h-6 w-6 text-blue-600" />
                        <h4 className="font-bold text-gray-900 text-lg group-hover:text-blue-600 transition-colors">
                          {draft.title}
                        </h4>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <ClockIcon className="h-4 w-4" />
                          {new Date(draft.created_at).toLocaleDateString()}
                        </span>
                        {draft.sent_at && (
                          <span className="flex items-center gap-1 text-green-600">
                            <EyeIcon className="h-4 w-4" />
                            Sent {new Date(draft.sent_at).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`px-4 py-2 text-sm font-bold rounded-full shadow-md ${
                        draft.status === 'sent' 
                          ? 'bg-gradient-to-r from-green-400 to-emerald-500 text-white animate-pulse' 
                          : draft.status === 'published'
                          ? 'bg-gradient-to-r from-blue-400 to-cyan-500 text-white'
                          : 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white'
                      }`}>
                        {draft.status === 'sent' ? '✓ Sent' : draft.status === 'published' ? '📡 Published' : '📝 Draft'}
                      </span>
                      <button className="p-3 bg-blue-100 text-blue-600 hover:bg-gradient-to-br hover:from-blue-500 hover:to-purple-600 hover:text-white rounded-xl transition-all duration-300 transform hover:scale-110">
                        <EyeIcon className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <div className="inline-block p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-full mb-4">
                <DocumentTextIcon className="h-16 w-16 text-blue-400 animate-bounce" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">No drafts yet</h3>
              <p className="text-gray-600 mb-6">
                Click "Generate Now" to create your first AI-powered newsletter! 🚀
              </p>
              <button
                onClick={handleGenerateNow}
                disabled={isGenerating}
                className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-bold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                <SparklesIcon className="h-6 w-6" />
                Generate Your First Newsletter
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Newsletter Generation Loader */}
      <NewsletterGenerationLoader 
        isOpen={isGenerating} 
        onComplete={handleGenerationComplete}
      />
    </div>
  )
}

interface StatsCardProps {
  icon: React.ReactNode
  label: string
  value: string | number
  total?: number
  gradient: string
  delay: string
  isDate?: boolean
}

function StatsCard({ icon, label, value, total, gradient, delay, isDate }: StatsCardProps) {
  return (
    <div 
      className="group relative overflow-hidden bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 shadow-lg border-2 border-gray-200 hover:border-blue-300 hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-300"
        style={{ backgroundImage: `linear-gradient(to bottom right, var(--tw-gradient-stops))` }}
      ></div>
      <div className="relative">
        <div className={`inline-flex p-4 bg-gradient-to-br ${gradient} rounded-xl shadow-lg text-white mb-4 group-hover:scale-110 transition-transform duration-300`}>
          {icon}
        </div>
        <div>
          <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-2">{label}</p>
          <div className="flex items-baseline gap-2">
            <p className={`${isDate ? 'text-2xl' : 'text-4xl'} font-black text-transparent bg-clip-text bg-gradient-to-r ${gradient}`}>
              {value}
            </p>
            {total !== undefined && (
              <span className="text-lg text-gray-500">/ {total}</span>
            )}
          </div>
        </div>
      </div>
      <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-gradient-to-br opacity-10 group-hover:opacity-20 transition-opacity duration-300"
        style={{ backgroundImage: `linear-gradient(to bottom right, var(--tw-gradient-stops))` }}
      ></div>
    </div>
  )
}
