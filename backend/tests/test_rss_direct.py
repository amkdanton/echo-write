#!/usr/bin/env python3
"""
Test RSS feed parsing directly
"""

import feedparser
import httpx
import asyncio

async def test_rss_feed(url, name):
    print(f"\n🔍 Testing: {name}")
    print(f"   URL: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            print(f"   HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                
                if feed.bozo:
                    print(f"   ⚠️  Parser warning: {feed.bozo_exception}")
                
                print(f"   ✅ Found {len(feed.entries)} entries")
                
                if feed.entries:
                    print(f"   📰 Sample entries:")
                    for i, entry in enumerate(feed.entries[:3], 1):
                        print(f"      {i}. {entry.get('title', 'No title')[:60]}...")
                        print(f"         Link: {entry.get('link', 'No link')}")
                        print(f"         Published: {entry.get('published', 'No date')}")
                else:
                    print(f"   ❌ No entries found in feed!")
            else:
                print(f"   ❌ HTTP error: {response.status_code}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

async def main():
    print("="*70)
    print("Testing RSS Feeds Directly")
    print("="*70)
    
    feeds = [
        ("https://feeds.feedburner.com/TechCrunch/", "TechCrunch"),
        ("https://www.theverge.com/rss/index.xml", "The Verge"),
        ("https://hnrss.org/frontpage", "Hacker News"),
    ]
    
    for url, name in feeds:
        await test_rss_feed(url, name)
    
    print("\n" + "="*70)

if __name__ == "__main__":
    asyncio.run(main())


