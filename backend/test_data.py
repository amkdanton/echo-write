"""
Test Data Generator for EchoWrite
Contains sample sources for RSS, YouTube, and Twitter source types
"""

from datetime import datetime
from typing import List, Dict, Any

# Sample Test Sources
TEST_SOURCES = {
    "rss": [
        {
            "type": "rss",
            "handle": "https://techcrunch.com/feed/",
            "name": "TechCrunch",
            "is_active": True,
            "fetch_frequency": 3600,  # 1 hour
            "metadata": {
                "description": "Latest tech news and startup coverage",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.theverge.com/rss/index.xml",
            "name": "The Verge",
            "is_active": True,
            "fetch_frequency": 7200,  # 2 hours
            "metadata": {
                "description": "Technology news, reviews, and features",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://feeds.arstechnica.com/arstechnica/index",
            "name": "Ars Technica",
            "is_active": True,
            "fetch_frequency": 3600,
            "metadata": {
                "description": "Technology news and information",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.wired.com/feed/rss",
            "name": "WIRED",
            "is_active": True,
            "fetch_frequency": 10800,  # 3 hours
            "metadata": {
                "description": "Technology, science, and culture",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://hbr.org/feed",
            "name": "Harvard Business Review",
            "is_active": True,
            "fetch_frequency": 14400,  # 4 hours
            "metadata": {
                "description": "Management and business insights",
                "category": "business"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.forbes.com/innovation/feed/",
            "name": "Forbes Innovation",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Innovation and entrepreneurship news",
                "category": "business"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.producthunt.com/feed",
            "name": "Product Hunt",
            "is_active": True,
            "fetch_frequency": 3600,
            "metadata": {
                "description": "Latest product launches and tech trends",
                "category": "products"
            }
        },
        {
            "type": "rss",
            "handle": "https://news.ycombinator.com/rss",
            "name": "Hacker News",
            "is_active": True,
            "fetch_frequency": 1800,  # 30 minutes
            "metadata": {
                "description": "Tech and startup news from Y Combinator",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.engadget.com/rss.xml",
            "name": "Engadget",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Electronics and gadget news",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.cnet.com/rss/news/",
            "name": "CNET",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Technology product news and reviews",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://www.technologyreview.com/feed/",
            "name": "MIT Technology Review",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "Emerging technology analysis",
                "category": "technology"
            }
        },
        {
            "type": "rss",
            "handle": "https://venturebeat.com/feed/",
            "name": "VentureBeat",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Tech news and AI coverage",
                "category": "technology"
            }
        },
    ],
    "youtube": [
        {
            "type": "youtube",
            "handle": "UC2D2CMWXMOVWx7giW1n3LIg",
            "name": "Fireship",
            "is_active": True,
            "fetch_frequency": 86400,  # 1 day
            "metadata": {
                "description": "High-intensity coding tutorials",
                "category": "programming",
                "subscribers": "2M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCsBjURrPoezykLs9EqgamOA",
            "name": "Fireship (Alt Channel)",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Programming and tech content",
                "category": "programming"
            }
        },
        {
            "type": "youtube",
            "handle": "UCW5YeuERMmlnqo4oq8vwUpg",
            "name": "The Net Ninja",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Web development tutorials",
                "category": "programming",
                "subscribers": "1M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCCezIgC97PvUuR4_gbFUs5g",
            "name": "Corey Schafer",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Python and programming tutorials",
                "category": "programming",
                "subscribers": "1M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCsBjURrPoezykLs9EqgamOA",
            "name": "Traversy Media",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Web development and programming tutorials",
                "category": "programming",
                "subscribers": "2M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCVyRiMvfUNMA1UPlDPzG5Ow",
            "name": "lex Fridman",
            "is_active": True,
            "fetch_frequency": 172800,  # 2 days
            "metadata": {
                "description": "AI and technology podcast interviews",
                "category": "technology",
                "subscribers": "3M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCsooa4yRKGN_zEE8iknghZA",
            "name": "TechLead",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Tech career and engineering insights",
                "category": "technology"
            }
        },
        {
            "type": "youtube",
            "handle": "UC8butISFwT-Wl7EV0hUK0BQ",
            "name": "freeCodeCamp.org",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Free coding tutorials and courses",
                "category": "programming",
                "subscribers": "8M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCnxhETjJtTPs37hOZ7vQ88g",
            "name": "Computerphile",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Computer science and programming topics",
                "category": "computer-science"
            }
        },
        {
            "type": "youtube",
            "handle": "UCsBjURrPoezykLs9EqgamOA",
            "name": "Theo - t3.gg",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Full-stack web development and tech commentary",
                "category": "programming"
            }
        },
        {
            "type": "youtube",
            "handle": "UCsBjURrPoezykLs9EqgamOA",
            "name": "Web Dev Simplified",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Simplified web development tutorials",
                "category": "programming",
                "subscribers": "1M+"
            }
        },
        {
            "type": "youtube",
            "handle": "UCRLOenFsEsY8hG6SJBt9mzA",
            "name": "Coding Tech",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "Tech conference talks and tutorials",
                "category": "technology"
            }
        },
        {
            "type": "youtube",
            "handle": "UCsBjURrPoezykLs9EqgamOA",
            "name": "Kevin Powell",
            "is_active": True,
            "fetch_frequency": 86400,
            "metadata": {
                "description": "CSS and front-end web development",
                "category": "programming"
            }
        },
    ],
    "twitter": [
        {
            "type": "twitter",
            "handle": "@elonmusk",
            "name": "Elon Musk",
            "is_active": True,
            "fetch_frequency": 3600,
            "metadata": {
                "description": "Tesla, SpaceX, and technology updates",
                "category": "technology",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@paulg",
            "name": "Paul Graham",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Y Combinator co-founder, startup insights",
                "category": "startups",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@naval",
            "name": "Naval Ravikant",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "AngelList founder, philosophy and startups",
                "category": "startups",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@sama",
            "name": "Sam Altman",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "OpenAI CEO, AI and technology",
                "category": "AI",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@karenxcheng",
            "name": "Karen X. Cheng",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "AI and creative technology content creator",
                "category": "AI"
            }
        },
        {
            "type": "twitter",
            "handle": "@levelsio",
            "name": "Pieter Levels",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Indie hacker, digital nomad, maker",
                "category": "startups",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@patticus",
            "name": "Patrick Collison",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "Stripe CEO, technology and progress",
                "category": "technology",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@benedictevans",
            "name": "Benedict Evans",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "Tech analyst and investor",
                "category": "technology",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@balajis",
            "name": "Balaji Srinivasan",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "Tech investor and thought leader",
                "category": "technology",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@karpathy",
            "name": "Andrej Karpathy",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "AI researcher, former Tesla and OpenAI",
                "category": "AI",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@goodside",
            "name": "Riley Goodside",
            "is_active": True,
            "fetch_frequency": 7200,
            "metadata": {
                "description": "AI prompt engineering and LLMs",
                "category": "AI"
            }
        },
        {
            "type": "twitter",
            "handle": "@ylecun",
            "name": "Yann LeCun",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "Meta Chief AI Scientist",
                "category": "AI",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@dhh",
            "name": "DHH",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "Ruby on Rails creator, Basecamp founder",
                "category": "programming",
                "verified": True
            }
        },
        {
            "type": "twitter",
            "handle": "@dan_abramov",
            "name": "Dan Abramov",
            "is_active": True,
            "fetch_frequency": 14400,
            "metadata": {
                "description": "React core team member",
                "category": "programming",
                "verified": True
            }
        },
    ]
}

# Sample items for each source type (for testing ingestion)
SAMPLE_ITEMS = {
    "rss": [
        {
            "title": "The Future of AI: What's Next in 2025",
            "url": "https://techcrunch.com/2025/01/15/future-of-ai-2025",
            "summary": "Exploring the upcoming trends in artificial intelligence and machine learning for 2025",
            "published_at": "2025-01-15T10:00:00Z",
            "content": "Full article content here...",
            "author": "John Doe"
        },
        {
            "title": "Startup Funding Reaches New Heights",
            "url": "https://techcrunch.com/2025/01/14/startup-funding-records",
            "summary": "Venture capital funding hits record levels in Q1 2025",
            "published_at": "2025-01-14T15:30:00Z",
            "content": "Full article content here...",
            "author": "Jane Smith"
        },
        {
            "title": "The Rise of Edge Computing",
            "url": "https://www.theverge.com/2025/01/13/edge-computing-rise",
            "summary": "How edge computing is transforming cloud infrastructure",
            "published_at": "2025-01-13T09:00:00Z",
            "content": "Full article content here...",
            "author": "Tech Journalist"
        },
    ],
    "youtube": [
        {
            "title": "Building a Real-Time App with WebSockets",
            "url": "https://youtube.com/watch?v=example1",
            "summary": "Learn how to build real-time applications using WebSocket technology",
            "published_at": "2025-01-15T12:00:00Z",
            "content": "Video transcript here...",
            "author": "Fireship"
        },
        {
            "title": "Python in 100 Seconds",
            "url": "https://youtube.com/watch?v=example2",
            "summary": "Quick overview of Python programming language",
            "published_at": "2025-01-14T14:00:00Z",
            "content": "Video transcript here...",
            "author": "Fireship"
        },
    ],
    "twitter": [
        {
            "title": "Tweet about AI progress",
            "url": "https://twitter.com/sama/status/1234567890",
            "summary": "GPT-5 training is going better than expected",
            "published_at": "2025-01-15T08:30:00Z",
            "content": "GPT-5 training is going better than expected",
            "author": "Sam Altman"
        },
        {
            "title": "Tweet about startup advice",
            "url": "https://twitter.com/paulg/status/9876543210",
            "summary": "The best startups solve problems the founders have themselves",
            "published_at": "2025-01-14T11:00:00Z",
            "content": "The best startups solve problems the founders have themselves",
            "author": "Paul Graham"
        },
    ]
}


def get_sources_by_type(source_type: str) -> List[Dict[str, Any]]:
    """Get all test sources for a specific type"""
    return TEST_SOURCES.get(source_type, [])


def get_all_sources() -> List[Dict[str, Any]]:
    """Get all test sources"""
    all_sources = []
    for sources in TEST_SOURCES.values():
        all_sources.extend(sources)
    return all_sources


def get_sample_items_by_type(source_type: str) -> List[Dict[str, Any]]:
    """Get sample items for a specific source type"""
    return SAMPLE_ITEMS.get(source_type, [])


def get_source_count_by_type() -> Dict[str, int]:
    """Get count of sources by type"""
    return {
        source_type: len(sources)
        for source_type, sources in TEST_SOURCES.items()
    }


def print_test_data_summary():
    """Print summary of test data"""
    print("=" * 60)
    print("TEST DATA SUMMARY")
    print("=" * 60)
    
    counts = get_source_count_by_type()
    total = sum(counts.values())
    
    print(f"\nTotal Sources: {total}")
    print("\nSources by Type:")
    for source_type, count in counts.items():
        print(f"  - {source_type.upper()}: {count} sources")
    
    print("\n" + "=" * 60)
    print("SOURCE DETAILS")
    print("=" * 60)
    
    for source_type, sources in TEST_SOURCES.items():
        print(f"\n{source_type.upper()} SOURCES:")
        print("-" * 60)
        for i, source in enumerate(sources, 1):
            print(f"{i}. {source['name']}")
            print(f"   Handle: {source['handle']}")
            print(f"   Frequency: {source['fetch_frequency']}s ({source['fetch_frequency'] // 60} min)")
            if 'description' in source.get('metadata', {}):
                print(f"   Description: {source['metadata']['description']}")
            print()


if __name__ == "__main__":
    print_test_data_summary()

