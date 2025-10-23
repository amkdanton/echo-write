import React from 'react'

interface NewsletterRendererProps {
  content: string
  variant?: 'email' | 'preview' | 'draft'
  className?: string
}

const NewsletterRenderer: React.FC<NewsletterRendererProps> = ({ 
  content, 
  variant = 'preview',
  className = '' 
}) => {
  const formatMarkdown = (markdown: string) => {
    // Check if content is already HTML (contains HTML tags)
    if (markdown.includes('<h1') || markdown.includes('<h2') || markdown.includes('<p') || markdown.includes('<div')) {
      // Clean up any raw HTML attributes that are being rendered as text
      let cleaned = markdown
        // Remove standalone HTML attributes that are being rendered as text
        .replace(/class="[^"]*"/g, '')
        .replace(/style="[^"]*"/g, '')
        .replace(/onerror="[^"]*"/g, '')
        .replace(/\/>/g, '>')
        .replace(/\s+/g, ' ')
        .trim()
      
      return cleaned
    }
    
    let html = markdown
      // Handle images with enhanced styling and fallback
      .replace(/!\[(.*?)\]\((.*?)\)/g, (_, alt, src) => {
        // Fallback images for different types
        const fallbackImages = {
          hero: 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop&crop=center',
          article: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop&crop=center',
          default: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop&crop=center'
        }
        
        // Check if image URL is valid, otherwise use fallback
        const isValidUrl = (url: string) => {
          try {
            new URL(url)
            return url.startsWith('http') && !url.includes('undefined') && !url.includes('null')
          } catch {
            return false
          }
        }
        
        const imageUrl = isValidUrl(src) ? src : fallbackImages[alt.toLowerCase().includes('hero') ? 'hero' : alt.toLowerCase().includes('article') ? 'article' : 'default']
        
        if (alt.toLowerCase().includes('hero')) {
          return `<div class="relative w-full my-8 group">
            <img src="${imageUrl}" alt="${alt}" 
                 class="w-full rounded-3xl shadow-2xl object-cover h-80 border-2 border-slate-200 hover:shadow-3xl transition-all duration-500 hover:scale-[1.02] hover:border-blue-300" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>`
        } else if (alt.toLowerCase().includes('article')) {
          return `<div class="relative w-full my-6 group">
            <img src="${imageUrl}" alt="${alt}" 
                 class="w-full rounded-2xl shadow-xl object-cover h-64 border border-slate-200 hover:shadow-2xl transition-all duration-300 hover:scale-[1.01]" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>`
        } else {
          return `<div class="relative w-full my-6 group">
            <img src="${imageUrl}" alt="${alt}" 
                 class="w-full rounded-2xl shadow-xl object-cover max-h-96 border border-slate-200 hover:shadow-2xl transition-all duration-300 hover:scale-[1.02]" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>`
        }
      })
      // Handle links
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 font-semibold underline decoration-2 decoration-blue-200 hover:decoration-blue-400 transition-all duration-200 hover:bg-blue-50 px-1 py-0.5 rounded">$1</a>')
      // Headers
      .replace(/^# (.*$)/gim, '<h1 class="text-4xl font-bold mb-8 text-slate-800 text-center bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent border-b-4 border-gradient-to-r from-blue-500 to-purple-500 pb-4">$1</h1>')
      .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold mb-6 mt-12 text-slate-700 flex items-center gap-4 relative pl-8"><div class="absolute left-0 top-1/2 transform -translate-y-1/2 w-2 h-12 bg-gradient-to-b from-blue-500 via-purple-500 to-pink-500 rounded-full shadow-lg"></div>$1</h2>')
      .replace(/^### (.*$)/gim, '<h3 class="text-xl font-semibold mb-5 text-slate-700 flex items-center gap-3"><div class="w-3 h-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full shadow-md"></div>$1</h3>')
      // Lists
      .replace(/^[-•*] (.*$)/gim, '<li class="mb-4 text-slate-600 leading-relaxed flex items-start gap-4 p-3 rounded-lg hover:bg-slate-50 transition-colors"><span class="text-blue-500 mt-2 text-sm font-bold flex-shrink-0">▶</span><span class="flex-1">$1</span></li>')
      .replace(/^\d+\. (.*$)/gim, '<li class="mb-4 text-slate-600 leading-relaxed flex items-start gap-4 p-3 rounded-lg hover:bg-slate-50 transition-colors"><span class="text-blue-500 font-bold text-sm mt-1 min-w-[24px] flex-shrink-0">$1.</span><span class="flex-1">$2</span></li>')
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-slate-800 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">$1</strong>')
    
    // Enhanced table conversion
    const lines = html.split('\n')
    let inTable = false
    let tableHtml: string[] = []
    let processedLines: string[] = []
    
    for (const line of lines) {
      if (line.includes('|') && line.trim().startsWith('|') && line.trim().endsWith('|')) {
        if (!inTable) {
          inTable = true
          tableHtml = ['<div class="overflow-x-auto my-8 rounded-2xl shadow-xl"><table class="w-full bg-white">']
        }
        
        // Check if it's a separator line
        if (/^\|[\s\-\|]+\|$/.test(line.trim())) {
          continue
        }
        
        // Process table row
        const cells = line.trim().split('|').slice(1, -1).map(cell => cell.trim())
        if (cells.length > 0) {
          // Check if first row looks like headers (contains emojis or specific keywords)
          if (cells.some(cell => /🔖|💬|📈|Trend|What's|Impact/.test(cell))) {
            tableHtml.push('<thead class="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white"><tr>')
            for (const cell of cells) {
              tableHtml.push(`<th class="px-6 py-4 text-left font-bold text-lg">${cell}</th>`)
            }
            tableHtml.push('</tr></thead><tbody>')
          } else {
            tableHtml.push('<tr class="hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 transition-all duration-200 border-b border-slate-100">')
            for (const cell of cells) {
              tableHtml.push(`<td class="px-6 py-4 text-slate-600 font-medium">${cell}</td>`)
            }
            tableHtml.push('</tr>')
          }
        }
      } else {
        if (inTable) {
          inTable = false
          tableHtml.push('</tbody></table></div>')
          processedLines.push(tableHtml.join(''))
          tableHtml = []
        }
        processedLines.push(line)
      }
    }
    
    // Close any remaining table
    if (inTable) {
      tableHtml.push('</tbody></table></div>')
      processedLines.push(tableHtml.join(''))
    }
    
    html = processedLines.join('\n')
    
    // Wrap special sections with enhanced styling
    const sectionPatterns = [
      { pattern: /<h2[^>]*>🔍 Executive Summary<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'executive', title: '🔍 Executive Summary', color: 'blue' },
      { pattern: /<h2[^>]*>🧠 Big Picture<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'stats', title: '🧠 Big Picture', color: 'green' },
      { pattern: /<h2[^>]*>🚀 Top Picks of the Week<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'trends', title: '🚀 Top Picks of the Week', color: 'purple' },
      { pattern: /<h2[^>]*>🌐 Trends to Watch<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'trends', title: '🌐 Trends to Watch', color: 'purple' },
      { pattern: /<h2[^>]*>💡 Quick Bytes<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'stats', title: '💡 Quick Bytes', color: 'green' },
      { pattern: /<h2[^>]*>📊 Data Pulse<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'stats', title: '📊 Data Pulse', color: 'green' },
      { pattern: /<h2[^>]*>🧭 Featured Tool<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'trivia', title: '🧭 Featured Tool', color: 'amber' },
      { pattern: /<h2[^>]*>🧩 Did You Know\?<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'trivia', title: '🧩 Did You Know?', color: 'amber' },
      { pattern: /<h2[^>]*>💬 From the Editor<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'executive', title: '💬 From the Editor', color: 'blue' },
      { pattern: /<h2[^>]*>📅 Coming Next Week<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'trends', title: '📅 Coming Next Week', color: 'purple' },
      { pattern: /<h2[^>]*>📨 Wrap-Up<\/h2>(.*?)(?=<h[12]|$)/gs, type: 'executive', title: '📨 Wrap-Up', color: 'blue' },
    ]
    
    for (const { pattern, type, title } of sectionPatterns) {
      const gradientClasses: Record<string, string> = {
        executive: 'from-blue-50 via-sky-50 to-blue-100',
        stats: 'from-green-50 via-emerald-50 to-green-100',
        trends: 'from-purple-50 via-violet-50 to-purple-100',
        trivia: 'from-amber-50 via-orange-50 to-amber-100'
      }
      
      const borderClasses: Record<string, string> = {
        executive: 'border-blue-500',
        stats: 'border-green-500',
        trends: 'border-purple-500',
        trivia: 'border-amber-500'
      }
      
      const iconClasses: Record<string, string> = {
        executive: 'from-blue-500 to-sky-500',
        stats: 'from-green-500 to-emerald-500',
        trends: 'from-purple-500 to-violet-500',
        trivia: 'from-amber-500 to-orange-500'
      }
      
      const dotClasses: Record<string, string> = {
        executive: 'bg-blue-500',
        stats: 'bg-green-500',
        trends: 'bg-purple-500',
        trivia: 'bg-amber-500'
      }
      
      html = html.replace(pattern, 
        `<div class="mt-12 p-12 bg-gradient-to-br ${gradientClasses[type]} border-2 ${borderClasses[type]} rounded-3xl shadow-2xl relative overflow-hidden hover:shadow-3xl transition-all duration-500 hover:-translate-y-3 group backdrop-blur-sm">
          <div class="absolute top-0 left-0 right-0 h-3 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-t-3xl"></div>
          <div class="absolute -top-2 -left-2 -right-2 -bottom-2 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl opacity-5 -z-10"></div>
          <div class="absolute inset-0 bg-white/20 backdrop-blur-sm rounded-3xl"></div>
          <div class="relative z-10">
            <div class="flex items-center gap-6 mb-8">
              <div class="p-5 bg-gradient-to-r ${iconClasses[type]} rounded-2xl shadow-xl group-hover:scale-110 transition-transform duration-300">
                <svg class="h-10 w-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 class="text-3xl font-bold text-slate-800 flex items-center gap-4 relative">
                <div class="w-4 h-4 ${dotClasses[type]} rounded-full shadow-lg"></div>
                ${title}
              </h3>
            </div>
            <div class="text-slate-700 leading-relaxed text-lg relative z-10 space-y-4">$1</div>
          </div>
        </div>`
      )
    }
    
    // Paragraphs
    html = html
      .replace(/\n\n/g, '</p><p class="mb-6 text-slate-600 leading-relaxed text-lg">')
      .replace(/^(?!<[h|l|i|t|d])/gm, '<p class="mb-6 text-slate-600 leading-relaxed text-lg">')
    
    return html
  }

  const getVariantStyles = () => {
    switch (variant) {
      case 'email':
        return 'bg-white max-w-4xl mx-auto p-8 rounded-2xl shadow-xl'
      case 'preview':
        return 'bg-white max-w-5xl mx-auto p-8 rounded-3xl shadow-2xl border border-slate-200'
      case 'draft':
        return 'bg-white max-w-4xl mx-auto p-6 rounded-2xl shadow-lg border border-slate-200'
      default:
        return 'bg-white max-w-4xl mx-auto p-8 rounded-2xl shadow-xl'
    }
  }

  const getFeedbackSection = () => {
    return `
      <div class="mt-12 p-8 bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl border-2 border-slate-200 relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-purple-500"></div>
        <h3 class="text-2xl font-bold text-slate-800 mb-4 flex items-center justify-center gap-3">
          <span class="text-3xl">💬</span>
          How was this newsletter?
        </h3>
        <p class="text-slate-600 text-lg mb-8 text-center">
          Your feedback helps us improve future newsletters!
        </p>
        <div class="flex gap-6 justify-center flex-wrap">
          <button class="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-green-500 to-green-600 text-white font-bold rounded-full hover:from-green-600 hover:to-green-700 transform hover:-translate-y-2 transition-all duration-300 shadow-lg hover:shadow-xl">
            <span class="text-2xl">👍</span>
            Great newsletter!
          </button>
          <button class="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-red-500 to-red-600 text-white font-bold rounded-full hover:from-red-600 hover:to-red-700 transform hover:-translate-y-2 transition-all duration-300 shadow-lg hover:shadow-xl">
            <span class="text-2xl">👎</span>
            Needs improvement
          </button>
        </div>
      </div>
    `
  }

  const processedContent = formatMarkdown(content)
  const feedbackSection = getFeedbackSection()
  const finalHTML = processedContent + feedbackSection

  return (
    <div className={`newsletter-renderer ${getVariantStyles()} ${className}`}>
      <div 
        className="newsletter-content"
        dangerouslySetInnerHTML={{ 
          __html: finalHTML
        }}
      />
    </div>
  )
}

export default NewsletterRenderer
