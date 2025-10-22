import { useEffect, useState } from 'react'
import {
  RssIcon,
  FireIcon,
  DocumentTextIcon,
  SparklesIcon,
  CheckCircleIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'

interface Step {
  id: string
  title: string
  description: string
  icon: React.ReactNode
  estimatedSeconds: number
}

const GENERATION_STEPS: Step[] = [
  {
    id: 'fetching',
    title: 'Fetching Content',
    description: 'Getting items from your sources...',
    icon: <RssIcon className="h-6 w-6" />,
    estimatedSeconds: 5
  },
  {
    id: 'analyzing',
    title: 'Analyzing Trends',
    description: 'Scoring and ranking content...',
    icon: <FireIcon className="h-6 w-6" />,
    estimatedSeconds: 8
  },
  {
    id: 'training',
    title: 'Loading Voice Profile',
    description: 'Applying your writing style...',
    icon: <DocumentTextIcon className="h-6 w-6" />,
    estimatedSeconds: 5
  },
  {
    id: 'generating',
    title: 'Generating Content',
    description: 'AI is writing your newsletter...',
    icon: <SparklesIcon className="h-6 w-6" />,
    estimatedSeconds: 12
  },
  {
    id: 'finalizing',
    title: 'Finalizing',
    description: 'Formatting and saving draft...',
    icon: <CheckCircleIcon className="h-6 w-6" />,
    estimatedSeconds: 3
  }
]

interface NewsletterGenerationLoaderProps {
  isOpen: boolean
  onComplete?: () => void
}

export default function NewsletterGenerationLoader({ 
  isOpen, 
  onComplete 
}: NewsletterGenerationLoaderProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0)
  const [progress, setProgress] = useState(0)
  const [isCompleted, setIsCompleted] = useState(false)

  useEffect(() => {
    if (!isOpen) {
      // Reset when closed
      setCurrentStepIndex(0)
      setProgress(0)
      setIsCompleted(false)
      return
    }

    // Simulate step progression
    const totalSteps = GENERATION_STEPS.length
    const currentStep = GENERATION_STEPS[currentStepIndex]
    
    if (currentStepIndex < totalSteps) {
      const stepDuration = currentStep.estimatedSeconds * 1000
      const progressInterval = 50 // Update every 50ms
      const progressIncrement = (100 / (stepDuration / progressInterval))

      const progressTimer = setInterval(() => {
        setProgress(prev => {
          const newProgress = prev + progressIncrement
          if (newProgress >= 100) {
            clearInterval(progressTimer)
            // Move to next step after a short delay
            setTimeout(() => {
              if (currentStepIndex < totalSteps - 1) {
                setCurrentStepIndex(currentStepIndex + 1)
                setProgress(0)
              } else {
                // All steps complete
                setIsCompleted(true)
                setTimeout(() => {
                  onComplete?.()
                }, 1500)
              }
            }, 300)
            return 100
          }
          return newProgress
        })
      }, progressInterval)

      return () => clearInterval(progressTimer)
    }
  }, [isOpen, currentStepIndex, onComplete])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-[100] flex items-center justify-center p-4 animate-fadeIn">
      <div className="bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl max-w-2xl w-full overflow-hidden border-4 border-purple-200">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 p-8 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-grid-white/10"></div>
          <div className="relative">
            <div className="inline-block p-4 bg-white/20 rounded-full mb-4 animate-pulse">
              <SparklesIcon className="h-12 w-12 text-white animate-spin" style={{ animationDuration: '3s' }} />
            </div>
            <h2 className="text-3xl font-black text-white mb-2">
              {isCompleted ? '🎉 Newsletter Generated!' : '✨ Generating Your Newsletter'}
            </h2>
            <p className="text-purple-100 text-lg">
              {isCompleted ? 'Your draft is ready for review!' : 'Please wait while we craft your personalized content...'}
            </p>
          </div>
        </div>

        {/* Steps */}
        <div className="p-8 space-y-4">
          {GENERATION_STEPS.map((step, index) => {
            const isCurrentStep = index === currentStepIndex && !isCompleted
            const isCompleteStep = index < currentStepIndex || isCompleted

            return (
              <div
                key={step.id}
                className={`relative flex items-start gap-4 p-5 rounded-2xl border-2 transition-all duration-500 ${
                  isCurrentStep
                    ? 'bg-gradient-to-r from-blue-50 to-purple-50 border-purple-400 shadow-lg scale-105'
                    : isCompleteStep
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-400'
                    : 'bg-gray-50 border-gray-200'
                }`}
                style={{
                  animationDelay: `${index * 100}ms`,
                  transform: isCurrentStep ? 'scale(1.02)' : 'scale(1)'
                }}
              >
                {/* Icon */}
                <div
                  className={`flex-shrink-0 p-3 rounded-xl transition-all duration-500 ${
                    isCurrentStep
                      ? 'bg-gradient-to-br from-purple-500 to-blue-600 text-white shadow-lg animate-pulse'
                      : isCompleteStep
                      ? 'bg-gradient-to-br from-green-500 to-emerald-600 text-white'
                      : 'bg-gray-200 text-gray-400'
                  }`}
                >
                  {isCompleteStep ? (
                    <CheckCircleIcon className="h-6 w-6" />
                  ) : isCurrentStep ? (
                    <div className="relative">
                      {step.icon}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <ArrowPathIcon className="h-4 w-4 animate-spin" />
                      </div>
                    </div>
                  ) : (
                    step.icon
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-2">
                    <h3
                      className={`font-bold text-lg ${
                        isCurrentStep
                          ? 'text-purple-900'
                          : isCompleteStep
                          ? 'text-green-900'
                          : 'text-gray-500'
                      }`}
                    >
                      {step.title}
                    </h3>
                    {isCompleteStep && (
                      <span className="flex items-center gap-1 text-sm font-medium text-green-600 animate-fadeIn">
                        <CheckCircleIcon className="h-4 w-4" />
                        Done
                      </span>
                    )}
                    {isCurrentStep && (
                      <span className="flex items-center gap-1 text-sm font-medium text-purple-600 animate-pulse">
                        <ArrowPathIcon className="h-4 w-4 animate-spin" />
                        In Progress
                      </span>
                    )}
                  </div>
                  <p
                    className={`text-sm ${
                      isCurrentStep || isCompleteStep ? 'text-gray-700' : 'text-gray-400'
                    }`}
                  >
                    {step.description}
                  </p>

                  {/* Progress Bar (only for current step) */}
                  {isCurrentStep && (
                    <div className="mt-3">
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-purple-500 to-blue-600 transition-all duration-300 ease-out"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 mt-1">
                        {Math.round(progress)}% complete
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Footer */}
        <div className="bg-gradient-to-r from-gray-50 to-blue-50 px-8 py-6 text-center border-t-2 border-gray-200">
          {isCompleted ? (
            <div className="animate-fadeIn">
              <div className="inline-flex items-center gap-2 text-green-600 font-bold text-lg mb-2">
                <CheckCircleIcon className="h-6 w-6" />
                Success! Your newsletter is ready
              </div>
              <p className="text-gray-600 text-sm">
                Redirecting to drafts...
              </p>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-center gap-2 text-gray-600 mb-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
              <p className="text-gray-600 text-sm">
                Estimated time: {GENERATION_STEPS.reduce((acc, step) => acc + step.estimatedSeconds, 0)} seconds
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

// Add CSS for fade in animation (add to your global CSS or use Tailwind config)
// @keyframes fadeIn {
//   from { opacity: 0; transform: scale(0.95); }
//   to { opacity: 1; transform: scale(1); }
// }
// .animate-fadeIn {
//   animation: fadeIn 0.3s ease-out forwards;
// }

