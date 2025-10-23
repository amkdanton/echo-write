import { CreditCardIcon, SparklesIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface CreditDisplayProps {
  credits: number
  totalGenerations: number
  isLoading?: boolean
  showWarning?: boolean
}

export default function CreditDisplay({ 
  credits, 
  totalGenerations, 
  isLoading = false,
  showWarning = true 
}: CreditDisplayProps) {
  const isLowCredits = credits <= 2
  const isOutOfCredits = credits === 0

  if (isLoading) {
    return (
      <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>
    )
  }

  return (
    <div className={`rounded-2xl p-6 transition-all duration-300 ${
      isOutOfCredits 
        ? 'bg-gradient-to-br from-red-100 to-pink-100 border-2 border-red-200' 
        : isLowCredits 
        ? 'bg-gradient-to-br from-yellow-100 to-orange-100 border-2 border-yellow-200'
        : 'bg-gradient-to-br from-purple-100 to-pink-100 border border-purple-200'
    }`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-3 rounded-xl ${
            isOutOfCredits ? 'bg-red-200' : isLowCredits ? 'bg-yellow-200' : 'bg-purple-200'
          }`}>
            <CreditCardIcon className={`h-6 w-6 ${
              isOutOfCredits ? 'text-red-600' : isLowCredits ? 'text-yellow-600' : 'text-purple-600'
            }`} />
          </div>
          <div>
            <h3 className={`font-bold text-lg ${
              isOutOfCredits ? 'text-red-800' : isLowCredits ? 'text-yellow-800' : 'text-purple-800'
            }`}>
              Generation Credits
            </h3>
            <p className={`text-sm ${
              isOutOfCredits ? 'text-red-600' : isLowCredits ? 'text-yellow-600' : 'text-purple-600'
            }`}>
              {totalGenerations} newsletters generated
            </p>
          </div>
        </div>
        
        {showWarning && isOutOfCredits && (
          <div className="flex items-center gap-2 bg-red-200 text-red-800 px-3 py-2 rounded-xl">
            <ExclamationTriangleIcon className="h-5 w-5" />
            <span className="text-sm font-semibold">No Credits</span>
          </div>
        )}
        
        {showWarning && isLowCredits && !isOutOfCredits && (
          <div className="flex items-center gap-2 bg-yellow-200 text-yellow-800 px-3 py-2 rounded-xl">
            <ExclamationTriangleIcon className="h-5 w-5" />
            <span className="text-sm font-semibold">Low Credits</span>
          </div>
        )}
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <SparklesIcon className={`h-5 w-5 ${
            isOutOfCredits ? 'text-red-600' : isLowCredits ? 'text-yellow-600' : 'text-purple-600'
          }`} />
          <span className={`text-2xl font-black ${
            isOutOfCredits ? 'text-red-700' : isLowCredits ? 'text-yellow-700' : 'text-purple-700'
          }`}>
            {credits}
          </span>
          <span className={`text-sm ${
            isOutOfCredits ? 'text-red-600' : isLowCredits ? 'text-yellow-600' : 'text-purple-600'
          }`}>
            credits remaining
          </span>
        </div>
        
        {isOutOfCredits && (
          <div className="text-right">
            <p className="text-sm text-red-600 font-medium">Contact support for more credits</p>
          </div>
        )}
        
        {isLowCredits && !isOutOfCredits && (
          <div className="text-right">
            <p className="text-sm text-yellow-600 font-medium">Consider upgrading for more credits</p>
          </div>
        )}
      </div>

      {/* Progress bar */}
      <div className="mt-4">
        <div className={`h-2 rounded-full overflow-hidden ${
          isOutOfCredits ? 'bg-red-200' : isLowCredits ? 'bg-yellow-200' : 'bg-purple-200'
        }`}>
          <div 
            className={`h-full transition-all duration-500 ${
              isOutOfCredits ? 'bg-red-500' : isLowCredits ? 'bg-yellow-500' : 'bg-purple-500'
            }`}
            style={{ width: `${Math.min(100, (credits / 10) * 100)}%` }}
          ></div>
        </div>
        <p className={`text-xs mt-1 ${
          isOutOfCredits ? 'text-red-600' : isLowCredits ? 'text-yellow-600' : 'text-purple-600'
        }`}>
          {credits} of 10 credits used
        </p>
      </div>
    </div>
  )
}
