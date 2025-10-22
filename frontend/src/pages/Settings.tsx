import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  UserIcon,
  ClockIcon,
  DocumentTextIcon,
  LanguageIcon,
  SparklesIcon,
  CheckCircleIcon,
  PlusIcon,
  TrashIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

export default function Settings() {
  const [activeTab, setActiveTab] = useState('profile')
  const [styleSamples, setStyleSamples] = useState([
    { content: '', type: 'newsletter' }
  ])

  const queryClient = useQueryClient()

  // Fetch user profile
  const { data: profile, isLoading } = useQuery({
    queryKey: ['user-profile'],
    queryFn: async () => {
      // Mock data for now
      return {
        id: '1',
        email: 'user@example.com',
        name: 'John Doe',
        timezone: 'America/New_York',
        delivery_time: '08:00',
        language: 'en',
        voice_traits: ['friendly', 'analytical', 'concise']
      }
    }
  })

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: async () => {
      await new Promise(resolve => setTimeout(resolve, 1000))
      return { success: true }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-profile'] })
      toast.success('Profile updated successfully! ✓')
    }
  })

  // Train voice mutation
  const trainVoiceMutation = useMutation({
    mutationFn: async () => {
      await new Promise(resolve => setTimeout(resolve, 3000))
      return { 
        success: true, 
        voice_profile: { traits: ['friendly', 'analytical', 'concise'], confidence: 0.85 }
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user-profile'] })
      setStyleSamples([{ content: '', type: 'newsletter' }])
      toast.success('Voice trained successfully! 🎉')
    }
  })

  const handleAddSample = () => {
    setStyleSamples([...styleSamples, { content: '', type: 'newsletter' }])
  }

  const handleRemoveSample = (index: number) => {
    setStyleSamples(styleSamples.filter((_, i) => i !== index))
  }

  const handleSampleChange = (index: number, field: string, value: string) => {
    const updated = [...styleSamples]
    updated[index] = { ...updated[index], [field]: value }
    setStyleSamples(updated)
  }

  const handleTrainVoice = () => {
    const validSamples = styleSamples.filter(sample => sample.content.trim())
    if (validSamples.length < 3) {
      toast.error('Please provide at least 3 writing samples')
      return
    }
    trainVoiceMutation.mutate()
  }

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-20 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-2xl"></div>
        <div className="h-64 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl"></div>
      </div>
    )
  }

  const tabs = [
    { id: 'profile', name: 'Profile', icon: UserIcon, gradient: 'from-blue-500 to-cyan-500' },
    { id: 'schedule', name: 'Schedule', icon: ClockIcon, gradient: 'from-purple-500 to-pink-500' },
    { id: 'voice', name: 'Voice Training', icon: DocumentTextIcon, gradient: 'from-green-500 to-emerald-500' },
    { id: 'preferences', name: 'Preferences', icon: LanguageIcon, gradient: 'from-orange-500 to-red-500' },
  ]

  return (
    <div className="space-y-6">
      {/* Header with gradient */}
      <div className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-8 shadow-xl">
        <div className="absolute inset-0 bg-grid-white/10"></div>
        <div className="relative">
          <h2 className="text-3xl font-bold text-white sm:text-4xl flex items-center gap-3">
            <SparklesIcon className="h-10 w-10 animate-pulse" />
            Settings
          </h2>
          <p className="mt-2 text-indigo-100 text-lg">
            Configure your newsletter preferences and AI voice training. ⚙️
          </p>
        </div>
      </div>

      {/* Tabs with gradient */}
      <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg border-2 border-gray-200 overflow-hidden">
        <nav className="flex border-b-2 border-gray-200">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 py-4 px-6 font-bold text-sm flex items-center justify-center gap-2 transition-all duration-300 ${
                activeTab === tab.id
                  ? `bg-gradient-to-r ${tab.gradient} text-white shadow-lg`
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <tab.icon className="h-5 w-5" />
              {tab.name}
            </button>
          ))}
        </nav>

        {/* Tab Content */}
        <div className="p-8">
          {activeTab === 'profile' && (
            <div className="max-w-2xl mx-auto">
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-600 mb-2">
                  Profile Information
                </h3>
                <p className="text-gray-600">Update your personal details</p>
              </div>
              <form className="space-y-5" onSubmit={(e) => { e.preventDefault(); updateProfileMutation.mutate() }}>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    defaultValue={profile?.name || ''}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    defaultValue={profile?.email || ''}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300"
                  />
                </div>
                <button
                  type="submit"
                  disabled={updateProfileMutation.isPending}
                  className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-4 rounded-xl font-bold hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
                >
                  <CheckCircleIcon className="h-6 w-6" />
                  {updateProfileMutation.isPending ? 'Updating...' : 'Update Profile'}
                </button>
              </form>
            </div>
          )}

          {activeTab === 'schedule' && (
            <div className="max-w-2xl mx-auto">
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 mb-2">
                  Delivery Schedule
                </h3>
                <p className="text-gray-600">Set when your newsletters are generated and sent</p>
              </div>
              <form className="space-y-5">
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    🌍 Timezone
                  </label>
                  <select 
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300"
                    defaultValue={profile?.timezone || 'America/New_York'}
                  >
                    <option value="America/New_York">Eastern Time (ET)</option>
                    <option value="America/Chicago">Central Time (CT)</option>
                    <option value="America/Denver">Mountain Time (MT)</option>
                    <option value="America/Los_Angeles">Pacific Time (PT)</option>
                    <option value="Europe/London">London (GMT)</option>
                    <option value="Europe/Paris">Paris (CET)</option>
                    <option value="Asia/Tokyo">Tokyo (JST)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    ⏰ Delivery Time
                  </label>
                  <input
                    type="time"
                    defaultValue={profile?.delivery_time || '08:00'}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300"
                  />
                </div>
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 border-l-4 border-purple-500 p-4 rounded-xl">
                  <p className="text-sm text-purple-900 font-medium">
                    <strong>💡 Pro Tip:</strong> Newsletters will be automatically generated and sent at the specified time each day.
                  </p>
                </div>
                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-bold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
                >
                  <CheckCircleIcon className="h-6 w-6" />
                  Update Schedule
                </button>
              </form>
            </div>
          )}

          {activeTab === 'voice' && (
            <div className="max-w-3xl mx-auto space-y-6">
              {/* Current Voice Profile */}
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border-2 border-green-200">
                <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600 mb-4">
                  ✨ Current Voice Profile
                </h3>
                {profile?.voice_traits && profile.voice_traits.length > 0 ? (
                  <div>
                    <div className="flex flex-wrap gap-3 mb-4">
                      {profile.voice_traits.map((trait, index) => (
                        <span
                          key={index}
                          className="px-4 py-2 text-sm font-bold bg-gradient-to-r from-green-400 to-emerald-500 text-white rounded-full shadow-md animate-pulse"
                        >
                          {trait}
                        </span>
                      ))}
                    </div>
                    <p className="text-sm text-green-800 font-medium">
                      Confidence: <span className="font-bold">85%</span> • Last trained: <span className="font-bold">2 days ago</span>
                    </p>
                  </div>
                ) : (
                  <p className="text-green-800">No voice profile trained yet. Add writing samples below to get started! 🚀</p>
                )}
              </div>

              {/* Voice Training */}
              <div className="bg-white rounded-2xl p-6 border-2 border-gray-200 shadow-lg">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">🎯 Train Your Voice</h3>
                <p className="text-gray-600 mb-6">
                  Upload 3-10 writing samples (newsletters, blog posts, social media) to train the AI to match your unique style.
                </p>
                
                <div className="space-y-4">
                  {styleSamples.map((sample, index) => (
                    <div key={index} className="bg-gradient-to-br from-gray-50 to-blue-50 border-2 border-gray-200 rounded-xl p-5">
                      <div className="flex items-center justify-between mb-3">
                        <label className="text-sm font-bold text-gray-700">
                          📝 Sample {index + 1}
                        </label>
                        {styleSamples.length > 1 && (
                          <button
                            onClick={() => handleRemoveSample(index)}
                            className="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                            title="Remove sample"
                          >
                            <TrashIcon className="h-5 w-5" />
                          </button>
                        )}
                      </div>
                      <select
                        value={sample.type}
                        onChange={(e) => handleSampleChange(index, 'type', e.target.value)}
                        className="w-full px-4 py-2 border-2 border-gray-300 rounded-xl mb-3 focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all duration-300"
                      >
                        <option value="newsletter">Newsletter</option>
                        <option value="blog">Blog Post</option>
                        <option value="social">Social Media</option>
                      </select>
                      <textarea
                        value={sample.content}
                        onChange={(e) => handleSampleChange(index, 'content', e.target.value)}
                        placeholder="Paste your writing sample here... The more content, the better the AI can learn your style!"
                        rows={6}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all duration-300 resize-none"
                      />
                    </div>
                  ))}
                  
                  <button
                    onClick={handleAddSample}
                    className="w-full py-3 border-2 border-dashed border-gray-300 hover:border-green-500 rounded-xl text-gray-600 hover:text-green-600 font-medium transition-all duration-300 flex items-center justify-center gap-2"
                  >
                    <PlusIcon className="h-5 w-5" />
                    Add Another Sample
                  </button>
                  
                  <button
                    onClick={handleTrainVoice}
                    disabled={trainVoiceMutation.isPending}
                    className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-4 rounded-xl font-bold hover:from-green-700 hover:to-emerald-700 transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
                  >
                    <SparklesIcon className={`h-6 w-6 ${trainVoiceMutation.isPending ? 'animate-spin' : ''}`} />
                    {trainVoiceMutation.isPending ? 'Training Voice...' : 'Train My Voice'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'preferences' && (
            <div className="max-w-2xl mx-auto">
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-red-600 mb-2">
                  Newsletter Preferences
                </h3>
                <p className="text-gray-600">Customize how your newsletters are generated</p>
              </div>
              <form className="space-y-5">
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    🌐 Language
                  </label>
                  <select 
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-orange-500 focus:ring-4 focus:ring-orange-100 transition-all duration-300"
                    defaultValue={profile?.language || 'en'}
                  >
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="it">Italian</option>
                    <option value="pt">Portuguese</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-3">
                    🎯 Content Preferences
                  </label>
                  <div className="space-y-3">
                    {[
                      { label: 'Include trending topics', checked: true },
                      { label: 'Include analysis and insights', checked: true },
                      { label: 'Include social media highlights', checked: false },
                      { label: 'Add trivia and fun facts', checked: true },
                    ].map((pref, index) => (
                      <label key={index} className="flex items-center gap-3 p-4 bg-gradient-to-r from-white to-gray-50 rounded-xl border-2 border-gray-200 hover:border-orange-300 cursor-pointer transition-all duration-300">
                        <input type="checkbox" defaultChecked={pref.checked} className="h-5 w-5 text-orange-600 rounded focus:ring-orange-500" />
                        <span className="text-sm font-medium text-gray-700">{pref.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    📏 Newsletter Length
                  </label>
                  <select className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-orange-500 focus:ring-4 focus:ring-orange-100 transition-all duration-300">
                    <option value="short">Short (2-3 minutes read)</option>
                    <option value="medium" selected>Medium (5-7 minutes read)</option>
                    <option value="long">Long (10+ minutes read)</option>
                  </select>
                </div>
                
                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white py-4 rounded-xl font-bold hover:from-orange-700 hover:to-red-700 transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
                >
                  <CheckCircleIcon className="h-6 w-6" />
                  Save Preferences
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
