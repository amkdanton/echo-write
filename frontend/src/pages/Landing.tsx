import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-hot-toast'
import { 
  SparklesIcon, 
  RocketLaunchIcon,
  ClockIcon,
  BoltIcon,
  UserGroupIcon,
  UserIcon,
  ArrowRightIcon,
  ChartBarIcon,
  CpuChipIcon,
  GlobeAltIcon,
  NewspaperIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { useAuth } from '../contexts/AuthContext'

// Custom hook for scroll animations
function useScrollAnimation() {
  const [isVisible, setIsVisible] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    if (ref.current) {
      observer.observe(ref.current)
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current)
      }
    }
  }, [])

  return [ref, isVisible] as const
}

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
    <div className="min-h-screen bg-white text-gray-900 overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-white/90 backdrop-blur-xl border-b border-gray-200/50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <SparklesIcon className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">EchoWrite</span>
            </div>
            <div className="flex items-center gap-6">
              <button
                onClick={() => setShowAuth(true)}
                className="text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium"
              >
                Sign In
              </button>
              <button
                onClick={() => setShowAuth(true)}
                className="bg-gray-900 text-white px-6 py-2 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-6xl lg:text-8xl font-bold mb-8 leading-tight animate-fade-in">
              Crafting clarity
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 animate-pulse-slow">
                from the chatter
              </span>
            </h1>
            <p className="text-xl lg:text-2xl text-gray-600 max-w-3xl mx-auto mb-12 leading-relaxed animate-fade-in-delay">
              AI-powered content curation and newsletter automation. 
              Save hours researching and writing — while staying true to your voice.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up">
              <button
                onClick={() => setShowAuth(true)}
                className="bg-gray-900 text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-gray-800 transition-all transform hover:scale-105 flex items-center justify-center gap-3"
              >
                Start Building
                <ArrowRightIcon className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Process Flow Visualization */}
          <div className="relative animate-slide-up">
            <ProcessFlow />
          </div>
        </div>
      </section>

      {/* App Screenshots Section */}
      <section className="py-20 px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-gray-900 animate-fade-in">
              See EchoWrite in Action
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto animate-fade-in-delay">
              From content discovery to newsletter delivery in one seamless workflow
            </p>
          </div>
          <div className="animate-slide-up">
            <AppScreenshots />
          </div>
        </div>
      </section>

      {/* Generate Now Workflow Section */}
      <section className="py-20 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-gray-900 animate-fade-in">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto animate-fade-in-delay">
              Watch the magic happen in real-time with our step-by-step generation process
            </p>
          </div>
          <div className="animate-slide-up">
            <GenerateWorkflowSection />
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-gray-900 animate-fade-in">
              Everything You Need
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto animate-fade-in-delay">
              Powerful features designed for modern content creators
            </p>
          </div>
          <div className="animate-slide-up">
            <FeaturesGrid />
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-20 px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-gray-900 animate-fade-in">
              Built for creators and teams
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto animate-fade-in-delay">
              Whether you're a solo creator or managing multiple brands
            </p>
          </div>
          <div className="animate-slide-up">
            <UseCasesSection />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6 lg:px-8 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="max-w-6xl mx-auto">
          <div className="animate-slide-up">
            <StatsSection />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl lg:text-5xl font-bold mb-8 text-gray-900 animate-fade-in">
            Ready to Transform Your Content?
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto animate-fade-in-delay">
            Join thousands of creators who've revolutionized their newsletter workflow
          </p>
          <div className="animate-slide-up">
            <button
              onClick={() => setShowAuth(true)}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-12 py-4 rounded-full text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 animate-pulse-slow"
            >
              Get Started Today
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-12 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-3 mb-4 md:mb-0">
              <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <SparklesIcon className="h-4 w-4 text-white" />
              </div>
              <span className="text-lg font-bold text-gray-900">EchoWrite</span>
            </div>
            <div className="text-gray-500 text-sm">
              © 2025 EchoWrite. All rights reserved.
            </div>
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      {showAuth && <AuthModal onClose={() => setShowAuth(false)} />}
    </div>
  )
}

// Process Flow Component
function ProcessFlow() {
  const steps = [
    { icon: <GlobeAltIcon className="h-8 w-8" />, title: "Content Discovery", desc: "AI scans 1000+ sources" },
    { icon: <CpuChipIcon className="h-8 w-8" />, title: "Smart Analysis", desc: "Trends & insights extracted" },
    { icon: <NewspaperIcon className="h-8 w-8" />, title: "Newsletter Generation", desc: "Your voice, AI-powered" },
    { icon: <RocketLaunchIcon className="h-8 w-8" />, title: "Auto Delivery", desc: "Sent to your audience" }
  ]

  return (
    <div className="relative">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {steps.map((step, index) => (
          <div key={index} className="text-center group animate-fade-in" style={{ animationDelay: `${index * 0.2}s` }}>
            <div className="relative mb-6">
              <div className="w-20 h-20 mx-auto bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300 animate-float" style={{ animationDelay: `${index * 0.5}s` }}>
                <div className="text-blue-600 group-hover:text-purple-700 transition-colors">
                  {step.icon}
                </div>
              </div>
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-10 left-full w-full h-0.5 bg-gradient-to-r from-blue-300 to-purple-300 transform translate-x-4 animate-pulse-slow"></div>
              )}
            </div>
            <h3 className="text-lg font-semibold mb-2 text-gray-900">{step.title}</h3>
            <p className="text-sm text-gray-600">{step.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

// App Screenshots Component
function AppScreenshots() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Dashboard Analytics Card */}
      <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 animate-fade-in">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
        </div>
        <div className="space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center animate-pulse-slow">
            <div className="flex items-end gap-1">
              <div className="w-4 h-8 bg-blue-500 rounded-t"></div>
              <div className="w-4 h-12 bg-purple-500 rounded-t"></div>
              <div className="w-4 h-6 bg-pink-500 rounded-t"></div>
              <div className="w-4 h-10 bg-blue-600 rounded-t"></div>
            </div>
          </div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
        <p className="text-sm text-gray-600 mt-4 font-medium">Dashboard Analytics</p>
      </div>
      
      {/* Newsletter Preview Card */}
      <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 animate-fade-in" style={{ animationDelay: '0.2s' }}>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
        </div>
        <div className="space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-20 bg-gradient-to-br from-green-100 to-emerald-100 rounded-lg flex items-center justify-center animate-float">
            <div className="text-center">
              <NewspaperIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <div className="text-xs text-green-700 font-medium">Newsletter Preview</div>
            </div>
          </div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
        <p className="text-sm text-gray-600 mt-4 font-medium">Newsletter Preview</p>
      </div>
      
      {/* AI Generation Card */}
      <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 animate-fade-in" style={{ animationDelay: '0.4s' }}>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
        </div>
        <div className="space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg flex items-center justify-center animate-pulse-slow">
            <div className="text-center">
              <BoltIcon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <div className="text-xs text-purple-700 font-medium">AI Generation</div>
            </div>
          </div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
        <p className="text-sm text-gray-600 mt-4 font-medium">AI Generation</p>
      </div>
    </div>
  )
}

// Features Grid Component
function FeaturesGrid() {
  const features = [
    {
      icon: <SparklesIcon className="h-6 w-6" />,
      title: "Smart Curation",
      description: "AI-powered content discovery from 1000+ sources"
    },
    {
      icon: <BoltIcon className="h-6 w-6" />,
      title: "Trend Analysis",
      description: "Real-time trend detection and scoring"
    },
    {
      icon: <UserIcon className="h-6 w-6" />,
      title: "Voice Training",
      description: "Learn and replicate your unique writing style"
    },
    {
      icon: <ClockIcon className="h-6 w-6" />,
      title: "Daily Automation",
      description: "Automated newsletter generation every morning"
    },
    {
      icon: <ChartBarIcon className="h-6 w-6" />,
      title: "Analytics",
      description: "Comprehensive performance tracking"
    },
    {
      icon: <UserGroupIcon className="h-6 w-6" />,
      title: "Team Collaboration",
      description: "Multi-user support for agencies"
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {features.map((feature, index) => (
        <div key={index} className="group animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
          <div className="bg-white border border-gray-200 rounded-2xl p-8 hover:border-blue-300 transition-all duration-300 hover:shadow-lg hover:scale-105">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 animate-float" style={{ animationDelay: `${index * 0.3}s` }}>
              <div className="text-blue-600 group-hover:text-purple-700 transition-colors">
                {feature.icon}
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900">{feature.title}</h3>
            <p className="text-gray-600 leading-relaxed">{feature.description}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

// Stats Section Component
function StatsSection() {
  const stats = [
    { value: "95%", label: "Time Saved", sublabel: "per newsletter" },
    { value: "8:00 AM", label: "Daily Delivery", sublabel: "automated" },
    { value: "1000+", label: "Sources", sublabel: "monitored" },
    { value: "24/7", label: "AI Analysis", sublabel: "continuous" }
  ]

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
      {stats.map((stat, index) => (
        <div key={index} className="text-center group animate-fade-in" style={{ animationDelay: `${index * 0.2}s` }}>
          <div className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2 group-hover:scale-110 transition-transform duration-300 animate-pulse-slow" style={{ animationDelay: `${index * 0.5}s` }}>
            {stat.value}
          </div>
          <div className="text-lg font-semibold text-gray-900 mb-1">{stat.label}</div>
          <div className="text-sm text-gray-600">{stat.sublabel}</div>
        </div>
      ))}
    </div>
  )
}

// Use Cases Section Component
function UseCasesSection() {
  const [ref1, isVisible1] = useScrollAnimation()
  const [ref2, isVisible2] = useScrollAnimation()

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div ref={ref1} className={`bg-white rounded-2xl p-8 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 animate-on-scroll ${isVisible1 ? 'visible' : ''}`}>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl flex items-center justify-center animate-float">
            <UserIcon className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900">Independent Creators</h3>
        </div>
        <p className="text-gray-600 mb-6 leading-relaxed">
          Maintain consistency and save time. Focus on creating while EchoWrite handles research and drafting.
        </p>
        <ul className="space-y-3">
          {[
            "Reduce newsletter creation from 3 hours to 20 minutes",
            "Never miss a trending topic in your niche",
            "Maintain your authentic voice at scale"
          ].map((benefit, index) => (
            <li key={index} className="flex items-start gap-3 animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg className="h-4 w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700">{benefit}</span>
            </li>
          ))}
        </ul>
      </div>
      
      <div ref={ref2} className={`bg-white rounded-2xl p-8 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 animate-on-scroll ${isVisible2 ? 'visible' : ''}`}>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl flex items-center justify-center animate-float" style={{ animationDelay: '0.5s' }}>
            <UserGroupIcon className="h-8 w-8 text-purple-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900">Agencies & Teams</h3>
        </div>
        <p className="text-gray-600 mb-6 leading-relaxed">
          Scale your content operations. Manage multiple brand voices and deliver consistent quality.
        </p>
        <ul className="space-y-3">
          {[
            "Manage newsletters for multiple clients",
            "Maintain distinct voice profiles per brand",
            "Streamline team workflow and approvals"
          ].map((benefit, index) => (
            <li key={index} className="flex items-start gap-3 animate-fade-in" style={{ animationDelay: `${index * 0.1 + 0.3}s` }}>
              <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg className="h-4 w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700">{benefit}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

// Generate Workflow Section Component
function GenerateWorkflowSection() {
  const steps = [
    {
      step: "1",
      title: "Content Discovery",
      description: "AI scans 1000+ sources in real-time",
      icon: <GlobeAltIcon className="h-8 w-8" />,
      color: "from-blue-500 to-blue-600",
      bgColor: "from-blue-50 to-blue-100"
    },
    {
      step: "2", 
      title: "Trend Analysis",
      description: "Identifies trending topics and insights",
      icon: <ChartBarIcon className="h-8 w-8" />,
      color: "from-purple-500 to-purple-600",
      bgColor: "from-purple-50 to-purple-100"
    },
    {
      step: "3",
      title: "AI Generation",
      description: "Creates newsletter in your unique voice",
      icon: <BoltIcon className="h-8 w-8" />,
      color: "from-green-500 to-green-600", 
      bgColor: "from-green-50 to-green-100"
    },
    {
      step: "4",
      title: "Review & Send",
      description: "Preview, edit, and deliver to your audience",
      icon: <RocketLaunchIcon className="h-8 w-8" />,
      color: "from-orange-500 to-orange-600",
      bgColor: "from-orange-50 to-orange-100"
    }
  ]

  return (
    <div className="space-y-12">
      {/* Step-by-step workflow */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {steps.map((step, index) => (
          <div key={index} className="text-center group animate-fade-in" style={{ animationDelay: `${index * 0.2}s` }}>
            <div className="relative mb-6">
              <div className={`w-20 h-20 mx-auto bg-gradient-to-br ${step.bgColor} rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300 animate-float`} style={{ animationDelay: `${index * 0.5}s` }}>
                <div className={`text-${step.color.split('-')[1]}-600`}>
                  {step.icon}
                </div>
              </div>
              <div className={`absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r ${step.color} rounded-full flex items-center justify-center text-white font-bold text-sm animate-pulse-slow`}>
                {step.step}
              </div>
            </div>
            <h3 className="text-lg font-semibold mb-2 text-gray-900">{step.title}</h3>
            <p className="text-sm text-gray-600">{step.description}</p>
          </div>
        ))}
      </div>

      {/* Modern infographic showing the process */}
      <div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-3xl p-8 animate-slide-up">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h3 className="text-3xl font-bold text-gray-900 mb-6">Real-time Generation Process</h3>
            <div className="space-y-6">
              <div className="flex items-start gap-4 animate-fade-in">
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <SparklesIcon className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Smart Content Curation</h4>
                  <p className="text-gray-600">Our AI analyzes trending topics, filters relevant content, and identifies key insights from 1000+ sources in real-time.</p>
                </div>
              </div>
              <div className="flex items-start gap-4 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <CpuChipIcon className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">AI-Powered Writing</h4>
                  <p className="text-gray-600">Advanced language models generate content that matches your unique voice and writing style, ensuring authenticity.</p>
                </div>
              </div>
              <div className="flex items-start gap-4 animate-fade-in" style={{ animationDelay: '0.4s' }}>
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <NewspaperIcon className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Professional Formatting</h4>
                  <p className="text-gray-600">Automatically structures content with engaging headlines, bullet points, and professional formatting for maximum impact.</p>
                </div>
              </div>
            </div>
          </div>
          <div className="relative">
            <div className="bg-white rounded-2xl p-6 shadow-xl border border-gray-200 animate-float">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
              <div className="space-y-4">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                <div className="h-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <BoltIcon className="h-8 w-8 text-blue-600 mx-auto mb-2 animate-pulse-slow" />
                    <div className="text-xs text-blue-700 font-medium">Generating Newsletter...</div>
                  </div>
                </div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>
              <p className="text-sm text-gray-600 mt-4 font-medium text-center">Live Generation Preview</p>
            </div>
          </div>
        </div>
      </div>
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
    <div className="fixed inset-0 bg-black/50 backdrop-blur-xl z-50 flex items-center justify-center p-4">
      <div className="bg-white border border-gray-200 rounded-3xl max-w-md w-full p-8 relative shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-6 right-6 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon className="h-6 w-6" />
        </button>

        <div className="flex items-center gap-3 mb-8">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <SparklesIcon className="h-5 w-5 text-white" />
          </div>
          <span className="text-2xl font-bold text-gray-900">EchoWrite</span>
        </div>

        <div className="flex gap-1 mb-8 bg-gray-100 p-1 rounded-xl">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-3 rounded-lg font-medium transition-all ${
              isLogin ? 'bg-white text-gray-900 shadow-lg' : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-3 rounded-lg font-medium transition-all ${
              !isLogin ? 'bg-white text-gray-900 shadow-lg' : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {!isLogin && !userType && (
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700 mb-4">
                I am a...
              </label>
              <button
                type="button"
                onClick={() => setUserType('creator')}
                className="w-full bg-gray-50 hover:bg-gray-100 border border-gray-200 hover:border-blue-300 rounded-xl p-6 text-left transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <UserIcon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <div className="text-gray-900 font-semibold text-lg">Independent Creator</div>
                    <div className="text-sm text-gray-600">Building my own newsletter</div>
                  </div>
                </div>
              </button>
              <button
                type="button"
                onClick={() => setUserType('agency')}
                className="w-full bg-gray-50 hover:bg-gray-100 border border-gray-200 hover:border-purple-300 rounded-xl p-6 text-left transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                    <UserGroupIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div>
                    <div className="text-gray-900 font-semibold text-lg">Agency / Team</div>
                    <div className="text-sm text-gray-600">Managing multiple newsletters</div>
                  </div>
                </div>
              </button>
            </div>
          )}

          {(isLogin || userType) && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Password
                </label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                  placeholder="••••••••"
                />
              </div>

              {!isLogin && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                      placeholder="John Doe"
                    />
                  </div>

                  {userType === 'agency' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-3">
                        Agency Name
                      </label>
                      <input
                        type="text"
                        value={agencyName}
                        onChange={(e) => setAgencyName(e.target.value)}
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
                        placeholder="Your Agency"
                      />
                    </div>
                  )}
                </>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed text-white py-4 rounded-xl font-semibold transition-all transform hover:scale-105 disabled:scale-100"
              >
                {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Create Account')}
              </button>

              {isLogin && (
                <div className="text-center">
                  <a href="#" className="text-sm text-blue-600 hover:text-blue-700 transition-colors">
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
            className="mt-6 text-sm text-gray-600 hover:text-gray-900 flex items-center gap-2 transition-colors"
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

