import { useState } from 'react'
import { XMarkIcon, PlusIcon, RssIcon } from '@heroicons/react/24/outline'
import { PRELOADED_SOURCES, PreloadedSource } from '../data/preloadedSources'

interface BrowseSourcesModalProps {
  isOpen: boolean
  onClose: () => void
  onAddSource: (source: PreloadedSource, topic: string) => void
}

export default function BrowseSourcesModal({ isOpen, onClose, onAddSource }: BrowseSourcesModalProps) {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null)

  if (!isOpen) return null

  const selectedCategory = selectedTopic 
    ? PRELOADED_SOURCES.find(cat => cat.topic === selectedTopic)
    : null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[85vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <RssIcon className="h-7 w-7" />
              Browse Curated Sources
            </h2>
            <p className="text-blue-100 mt-1">Add high-quality sources with one click</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/20 rounded-lg p-2 transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden flex">
          {/* Sidebar - Topics */}
          <div className="w-64 border-r border-gray-200 overflow-y-auto bg-gray-50">
            <div className="p-4">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
                Categories
              </h3>
              <div className="space-y-1">
                {PRELOADED_SOURCES.map((category) => (
                  <button
                    key={category.topic}
                    onClick={() => setSelectedTopic(category.topic)}
                    className={`w-full text-left px-4 py-3 rounded-xl font-medium transition-all duration-200 ${
                      selectedTopic === category.topic
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md'
                        : 'text-gray-700 hover:bg-white hover:shadow'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{category.icon}</span>
                      <div className="flex-1">
                        <div className="font-semibold">{category.topic}</div>
                        <div className={`text-xs ${
                          selectedTopic === category.topic ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          {category.sources.length} sources
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main content - Sources */}
          <div className="flex-1 overflow-y-auto p-6">
            {!selectedCategory ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <RssIcon className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    Select a Category
                  </h3>
                  <p className="text-gray-600">
                    Choose a topic from the left to see curated sources
                  </p>
                </div>
              </div>
            ) : (
              <div>
                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                    <span className="text-3xl">{selectedCategory.icon}</span>
                    {selectedCategory.topic}
                  </h3>
                  <p className="text-gray-600 mt-1">
                    {selectedCategory.sources.length} hand-picked sources for {selectedCategory.topic.toLowerCase()}
                  </p>
                </div>

                <div className="grid gap-4">
                  {selectedCategory.sources.map((source, idx) => (
                    <div
                      key={idx}
                      className="group bg-gradient-to-br from-white to-gray-50 border-2 border-gray-200 rounded-xl p-5 hover:border-blue-400 hover:shadow-lg transition-all duration-300"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <span className={`px-2.5 py-1 text-xs font-bold rounded-lg ${
                              source.type === 'rss' 
                                ? 'bg-orange-100 text-orange-700'
                                : source.type === 'youtube'
                                ? 'bg-red-100 text-red-700'
                                : 'bg-blue-100 text-blue-700'
                            }`}>
                              {source.type.toUpperCase()}
                            </span>
                            <h4 className="font-bold text-gray-900 text-lg">
                              {source.name}
                            </h4>
                          </div>
                          <p className="text-gray-600 text-sm mb-3 leading-relaxed">
                            {source.description}
                          </p>
                          <code className="text-xs bg-gray-100 text-gray-700 px-3 py-1.5 rounded-lg font-mono">
                            {source.handle}
                          </code>
                        </div>
                        <button
                          onClick={() => onAddSource(source, selectedCategory.topic.toLowerCase().replace(/\s+/g, '-'))}
                          className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105"
                        >
                          <PlusIcon className="h-5 w-5" />
                          Add
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

