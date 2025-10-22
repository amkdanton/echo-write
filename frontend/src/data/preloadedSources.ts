// Preloaded sources organized by topic
// These are curated, high-quality sources that users can add with one click

export interface PreloadedSource {
  type: 'rss' | 'youtube' | 'twitter'
  handle: string
  name: string
  description: string
}

export interface TopicSources {
  topic: string
  icon: string
  sources: PreloadedSource[]
}

export const PRELOADED_SOURCES: TopicSources[] = [
  {
    topic: 'Technology',
    icon: '💻',
    sources: [
      {
        type: 'rss',
        handle: 'https://techcrunch.com/feed/',
        name: 'TechCrunch',
        description: 'Latest technology news and startup updates'
      },
      {
        type: 'rss',
        handle: 'https://www.theverge.com/rss/index.xml',
        name: 'The Verge',
        description: 'Tech, science, art, and culture'
      },
      {
        type: 'rss',
        handle: 'https://www.wired.com/feed/rss',
        name: 'Wired',
        description: 'Technology, business, and design'
      },
      {
        type: 'rss',
        handle: 'https://arstechnica.com/feed/',
        name: 'Ars Technica',
        description: 'In-depth tech news and analysis'
      },
      {
        type: 'youtube',
        handle: '@mkbhd',
        name: 'MKBHD',
        description: 'Tech reviews and analysis'
      },
      {
        type: 'youtube',
        handle: '@LinusTechTips',
        name: 'Linus Tech Tips',
        description: 'Tech reviews and tutorials'
      }
    ]
  },
  {
    topic: 'AI & Machine Learning',
    icon: '🤖',
    sources: [
      {
        type: 'rss',
        handle: 'https://openai.com/blog/rss/',
        name: 'OpenAI Blog',
        description: 'Latest from OpenAI'
      },
      {
        type: 'rss',
        handle: 'https://ai.googleblog.com/feeds/posts/default',
        name: 'Google AI Blog',
        description: 'Google AI research and updates'
      },
      {
        type: 'youtube',
        handle: '@TwoMinutePapers',
        name: 'Two Minute Papers',
        description: 'AI and ML research explained'
      },
      {
        type: 'rss',
        handle: 'https://www.anthropic.com/index/rss.xml',
        name: 'Anthropic',
        description: 'AI safety and research'
      }
    ]
  },
  {
    topic: 'Business & Startups',
    icon: '💼',
    sources: [
      {
        type: 'rss',
        handle: 'https://www.businessinsider.com/rss',
        name: 'Business Insider',
        description: 'Business news and analysis'
      },
      {
        type: 'rss',
        handle: 'https://www.inc.com/rss',
        name: 'Inc.',
        description: 'Startup and entrepreneur news'
      },
      {
        type: 'rss',
        handle: 'https://marker.medium.com/feed',
        name: 'Marker (Medium)',
        description: 'Business and tech stories'
      },
      {
        type: 'youtube',
        handle: '@ycombinator',
        name: 'Y Combinator',
        description: 'Startup advice and talks'
      }
    ]
  },
  {
    topic: 'Finance & Crypto',
    icon: '💰',
    sources: [
      {
        type: 'rss',
        handle: 'https://www.coindesk.com/arc/outboundfeeds/rss/',
        name: 'CoinDesk',
        description: 'Cryptocurrency news'
      },
      {
        type: 'rss',
        handle: 'https://cointelegraph.com/rss',
        name: 'Cointelegraph',
        description: 'Blockchain and crypto news'
      },
      {
        type: 'rss',
        handle: 'https://www.wsj.com/xml/rss/3_7085.xml',
        name: 'Wall Street Journal - Markets',
        description: 'Financial markets news'
      },
      {
        type: 'rss',
        handle: 'https://www.bloomberg.com/feed/podcast/etf-iq.xml',
        name: 'Bloomberg',
        description: 'Finance and markets'
      }
    ]
  },
  {
    topic: 'Science',
    icon: '🔬',
    sources: [
      {
        type: 'rss',
        handle: 'https://www.nature.com/nature.rss',
        name: 'Nature',
        description: 'Leading science journal'
      },
      {
        type: 'rss',
        handle: 'https://www.science.org/rss/news_current.xml',
        name: 'Science Magazine',
        description: 'Scientific research and news'
      },
      {
        type: 'rss',
        handle: 'https://www.scientificamerican.com/feed/',
        name: 'Scientific American',
        description: 'Science news and analysis'
      },
      {
        type: 'youtube',
        handle: '@veritasium',
        name: 'Veritasium',
        description: 'Science and engineering'
      }
    ]
  },
  {
    topic: 'Health & Fitness',
    icon: '💪',
    sources: [
      {
        type: 'rss',
        handle: 'https://www.health.harvard.edu/blog/feed',
        name: 'Harvard Health',
        description: 'Health advice from Harvard'
      },
      {
        type: 'rss',
        handle: 'https://www.mayoclinic.org/rss/all-health-topics',
        name: 'Mayo Clinic',
        description: 'Health information and advice'
      },
      {
        type: 'youtube',
        handle: '@JeffNippard',
        name: 'Jeff Nippard',
        description: 'Science-based fitness'
      },
      {
        type: 'rss',
        handle: 'https://www.healthline.com/rss',
        name: 'Healthline',
        description: 'Health and wellness news'
      }
    ]
  },
  {
    topic: 'Design & Creativity',
    icon: '🎨',
    sources: [
      {
        type: 'rss',
        handle: 'https://www.smashingmagazine.com/feed/',
        name: 'Smashing Magazine',
        description: 'Web design and development'
      },
      {
        type: 'rss',
        handle: 'https://www.creativebloq.com/feed',
        name: 'Creative Bloq',
        description: 'Design and creative news'
      },
      {
        type: 'rss',
        handle: 'https://www.designboom.com/feed/',
        name: 'Designboom',
        description: 'Architecture and design'
      },
      {
        type: 'youtube',
        handle: '@TheFutur',
        name: 'The Futur',
        description: 'Design business and creativity'
      }
    ]
  },
  {
    topic: 'Gaming',
    icon: '🎮',
    sources: [
      {
        type: 'rss',
        handle: 'https://www.ign.com/feed.xml',
        name: 'IGN',
        description: 'Gaming news and reviews'
      },
      {
        type: 'rss',
        handle: 'https://www.polygon.com/rss/index.xml',
        name: 'Polygon',
        description: 'Gaming culture and news'
      },
      {
        type: 'youtube',
        handle: '@gameranx',
        name: 'Gameranx',
        description: 'Gaming news and features'
      },
      {
        type: 'rss',
        handle: 'https://www.pcgamer.com/rss/',
        name: 'PC Gamer',
        description: 'PC gaming news'
      }
    ]
  },
  {
    topic: 'News & Politics',
    icon: '📰',
    sources: [
      {
        type: 'rss',
        handle: 'https://feeds.bbci.co.uk/news/rss.xml',
        name: 'BBC News',
        description: 'World news'
      },
      {
        type: 'rss',
        handle: 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        name: 'New York Times',
        description: 'News and opinion'
      },
      {
        type: 'rss',
        handle: 'https://www.theguardian.com/world/rss',
        name: 'The Guardian',
        description: 'International news'
      },
      {
        type: 'rss',
        handle: 'https://www.economist.com/the-world-this-week/rss.xml',
        name: 'The Economist',
        description: 'Global affairs and business'
      }
    ]
  },
  {
    topic: 'Marketing & Growth',
    icon: '📈',
    sources: [
      {
        type: 'rss',
        handle: 'https://blog.hubspot.com/marketing/rss.xml',
        name: 'HubSpot Marketing Blog',
        description: 'Marketing tips and strategies'
      },
      {
        type: 'rss',
        handle: 'https://moz.com/blog/feed',
        name: 'Moz Blog',
        description: 'SEO and marketing'
      },
      {
        type: 'rss',
        handle: 'https://neilpatel.com/feed/',
        name: 'Neil Patel',
        description: 'Digital marketing advice'
      },
      {
        type: 'rss',
        handle: 'https://growthhackers.com/feed',
        name: 'Growth Hackers',
        description: 'Growth marketing tactics'
      }
    ]
  }
]

export const TOPICS = PRELOADED_SOURCES.map(t => ({ 
  value: t.topic.toLowerCase().replace(/\s+/g, '-'), 
  label: t.topic,
  icon: t.icon 
}))

