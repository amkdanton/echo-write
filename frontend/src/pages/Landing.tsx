import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-hot-toast'
import { 
  SparklesIcon, 
  RocketLaunchIcon,
  ClockIcon,
  BoltIcon,
  UserGroupIcon,
  UserIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'

export default function Landing() {
  const navigate = useNavigate()
  const { user, loading } = useAuth()
  const [showAuth, setShowAuth] = useState(false)

  // Redirect to dashboard if already logged in
  useEffect(() => {
    console.log('🔵 [Landing] useEffect check', { loading, hasUser: !!user, user })
    if (!loading && user) {
      console.log('🟢 [Landing] User already logged in, redirecting to dashboard')
      navigate('/dashboard', { replace: true })
    } else if (!loading && !user) {
      console.log('🟡 [Landing] Not logged in, staying on landing page')
    } else {
      console.log('🔵 [Landing] Still loading...')
    }
  }, [user, loading, navigate])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <SparklesIcon className="h-8 w-8 text-blue-500" />
              <span className="text-2xl font-bold text-white">EchoWrite</span>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowAuth(true)}
                className="text-gray-300 hover:text-white transition-colors"
              >
                Sign In
              </button>
              <button
                onClick={() => setShowAuth(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Crafting clarity
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">
              from the chatter
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-3xl mx-auto">
            AI-powered content curation and newsletter automation. 
            Save hours researching and writing — while staying true to your voice.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => setShowAuth(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105 flex items-center justify-center gap-2"
            >
              <RocketLaunchIcon className="h-6 w-6" />
              Start Free Trial
            </button>
            <button className="border border-gray-600 hover:border-gray-500 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors">
              Watch Demo
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-500 mb-2">2-3 hours</div>
            <div className="text-gray-400">saved per newsletter</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-500 mb-2">8:00 AM</div>
            <div className="text-gray-400">daily automated drafts</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-green-500 mb-2">100%</div>
            <div className="text-gray-400">in your authentic voice</div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-16">
          Everything you need to scale your newsletter
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <FeatureCard
            icon={<SparklesIcon className="h-8 w-8" />}
            title="Smart Content Curation"
            description="Automatically aggregates insights from RSS feeds, YouTube channels, and more."
          />
          <FeatureCard
            icon={<BoltIcon className="h-8 w-8" />}
            title="Trend Detection"
            description="AI-powered analysis identifies what's trending in your niche right now."
          />
          <FeatureCard
            icon={<UserIcon className="h-8 w-8" />}
            title="Voice Training"
            description="Learns your unique writing style to generate newsletters that sound like you."
          />
          <FeatureCard
            icon={<RocketLaunchIcon className="h-8 w-8" />}
            title="AI Generation"
            description="GPT-4 powered newsletter creation with your voice and trending topics."
          />
          <FeatureCard
            icon={<ClockIcon className="h-8 w-8" />}
            title="Daily Automation"
            description="Wake up to a ready-to-send newsletter draft every morning at 8 AM."
          />
          <FeatureCard
            icon={<UserGroupIcon className="h-8 w-8" />}
            title="Multi-Brand Support"
            description="Perfect for agencies managing multiple client newsletters."
          />
        </div>
      </div>

      {/* Use Cases */}
      <div className="bg-gray-800/50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-16">
            Built for creators and teams
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <UseCaseCard
              icon={<UserIcon className="h-12 w-12" />}
              title="Independent Creators"
              description="Maintain consistency and save time. Focus on creating while EchoWrite handles research and drafting."
              benefits={[
                'Reduce newsletter creation from 3 hours to 20 minutes',
                'Never miss a trending topic in your niche',
                'Maintain your authentic voice at scale'
              ]}
            />
            <UseCaseCard
              icon={<UserGroupIcon className="h-12 w-12" />}
              title="Agencies & Teams"
              description="Scale your content operations. Manage multiple brand voices and deliver consistent quality."
              benefits={[
                'Manage newsletters for multiple clients',
                'Maintain distinct voice profiles per brand',
                'Streamline team workflow and approvals'
              ]}
            />
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
          Ready to transform your newsletter workflow?
        </h2>
        <p className="text-xl text-gray-300 mb-8">
          Join creators who've saved hundreds of hours with AI-powered curation.
        </p>
        <button
          onClick={() => setShowAuth(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-10 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105"
        >
          Start Your Free Trial
        </button>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <SparklesIcon className="h-6 w-6 text-blue-500" />
              <span className="text-xl font-bold text-white">EchoWrite</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 EchoWrite. Crafting clarity from the chatter.
            </div>
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      {showAuth && <AuthModal onClose={() => setShowAuth(false)} />}
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6 hover:border-blue-500/50 transition-colors">
      <div className="text-blue-500 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}

function UseCaseCard({ 
  icon, 
  title, 
  description, 
  benefits 
}: { 
  icon: React.ReactNode
  title: string
  description: string
  benefits: string[]
}) {
  return (
    <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-8">
      <div className="text-blue-500 mb-4">{icon}</div>
      <h3 className="text-2xl font-bold text-white mb-3">{title}</h3>
      <p className="text-gray-400 mb-6">{description}</p>
      <ul className="space-y-3">
        {benefits.map((benefit, index) => (
          <li key={index} className="flex items-start gap-3">
            <svg className="h-6 w-6 text-green-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-gray-300">{benefit}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function AuthModal({ onClose }: { onClose: () => void }) {
  const [isLogin, setIsLogin] = useState(true)
  const [userType, setUserType] = useState<'creator' | 'agency' | null>(null)
  const [loading, setLoading] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [agencyName, setAgencyName] = useState('')
  const { signUp, signIn } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    console.log('🔵 [Landing] handleSubmit START', { isLogin, email })
    e.preventDefault()
    setLoading(true)
    console.log('🔵 [Landing] Loading set to true')

    try {
      if (isLogin) {
        console.log('🔵 [Landing] Login mode - calling signIn...')
        await signIn({ email, password })
        console.log('🟢 [Landing] signIn completed successfully')
        // Don't close modal or reset loading - navigation will happen and unmount this component
      } else {
        console.log('🔵 [Landing] Signup mode')
        if (!userType) {
          console.log('🔴 [Landing] No user type selected')
          alert('Please select a user type')
          setLoading(false)
          return
        }
        console.log('🔵 [Landing] Calling signUp...', { userType })
        await signUp({
          email,
          password,
          fullName,
          userType,
          agencyName: userType === 'agency' ? agencyName : undefined,
        })
        console.log('🟢 [Landing] signUp completed successfully')
        // Don't close modal or reset loading - navigation will happen and unmount this component
      }
    } catch (error: any) {
      console.error('🔴 [Landing] Auth error:', error)
      setLoading(false)
      toast.error(error.message || 'Authentication failed')
    }
    console.log('🟢 [Landing] handleSubmit COMPLETE')
  }

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl max-w-md w-full p-8 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
        >
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div className="flex items-center gap-2 mb-8">
          <SparklesIcon className="h-8 w-8 text-blue-500" />
          <span className="text-2xl font-bold text-white">EchoWrite</span>
        </div>

        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
              isLogin ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
              !isLogin ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400'
            }`}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && !userType && (
            <div className="space-y-3">
              <label className="block text-sm font-medium text-gray-300 mb-3">
                I am a...
              </label>
              <button
                type="button"
                onClick={() => setUserType('creator')}
                className="w-full bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-blue-500 rounded-lg p-4 text-left transition-all"
              >
                <div className="flex items-center gap-3">
                  <UserIcon className="h-6 w-6 text-blue-500" />
                  <div>
                    <div className="text-white font-medium">Independent Creator</div>
                    <div className="text-sm text-gray-400">Building my own newsletter</div>
                  </div>
                </div>
              </button>
              <button
                type="button"
                onClick={() => setUserType('agency')}
                className="w-full bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-blue-500 rounded-lg p-4 text-left transition-all"
              >
                <div className="flex items-center gap-3">
                  <UserGroupIcon className="h-6 w-6 text-purple-500" />
                  <div>
                    <div className="text-white font-medium">Agency / Team</div>
                    <div className="text-sm text-gray-400">Managing multiple newsletters</div>
                  </div>
                </div>
              </button>
            </div>
          )}

          {(isLogin || userType) && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                  placeholder="••••••••"
                />
              </div>

              {!isLogin && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                      placeholder="John Doe"
                    />
                  </div>

                  {userType === 'agency' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">
                        Agency Name
                      </label>
                      <input
                        type="text"
                        value={agencyName}
                        onChange={(e) => setAgencyName(e.target.value)}
                        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        placeholder="Your Agency"
                      />
                    </div>
                  )}
                </>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white py-3 rounded-lg font-medium transition-colors"
              >
                {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Create Account')}
              </button>

              {isLogin && (
                <div className="text-center">
                  <a href="#" className="text-sm text-blue-500 hover:text-blue-400">
                    Forgot password?
                  </a>
                </div>
              )}
            </>
          )}
        </form>

        {!isLogin && userType && (
          <button
            onClick={() => setUserType(null)}
            className="mt-4 text-sm text-gray-400 hover:text-white flex items-center gap-2"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to user type selection
          </button>
        )}
      </div>
    </div>
  )
}

