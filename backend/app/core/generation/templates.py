"""
Standardized newsletter templates and email subject generation
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class NewsletterTemplate:
    """Standardized newsletter template with consistent sections"""
    
    @staticmethod
    def get_standard_sections() -> List[Dict[str, str]]:
        """Get the standard newsletter sections based on sample format"""
        return [
            {
                "id": "header",
                "title": "Newsletter Header",
                "description": "Title, subtitle, and branding",
                "required": True
            },
            {
                "id": "big_picture",
                "title": "🧠 Big Picture",
                "description": "High-level overview and theme",
                "required": True
            },
            {
                "id": "executive_summary",
                "title": "🔍 Executive Summary",
                "description": "Key developments and highlights",
                "required": True
            },
            {
                "id": "top_picks",
                "title": "🚀 Top Picks of the Week",
                "description": "Featured articles with analysis",
                "required": True
            },
            {
                "id": "trends_to_watch",
                "title": "🌐 Trends to Watch",
                "description": "Trending topics in table format",
                "required": True
            },
            {
                "id": "quick_bytes",
                "title": "💡 Quick Bytes",
                "description": "Quick news snippets",
                "required": True
            },
            {
                "id": "data_pulse",
                "title": "📊 Data Pulse",
                "description": "Statistics and metrics",
                "required": True
            },
            {
                "id": "featured_tool",
                "title": "🧭 Featured Tool",
                "description": "Tool or resource spotlight",
                "required": True
            },
            {
                "id": "did_you_know",
                "title": "🧩 Did You Know?",
                "description": "Fun trivia or interesting fact",
                "required": True
            },
            {
                "id": "from_editor",
                "title": "💬 From the Editor",
                "description": "Personal note from the editor",
                "required": True
            },
            {
                "id": "coming_next",
                "title": "📅 Coming Next Week",
                "description": "Preview of upcoming content",
                "required": True
            },
            {
                "id": "wrap_up",
                "title": "📨 Wrap-Up",
                "description": "Closing message and call-to-action",
                "required": True
            }
        ]
    
    @staticmethod
    def build_generation_prompt(
        trending_items: List[Any],
        voice_traits: List[str],
        trending_keywords: List[Dict[str, Any]],
        newsletter_title: Optional[str] = None
    ) -> str:
        """Build standardized generation prompt"""
        
        # Format trending keywords
        keywords_text = ", ".join([kw.get('keyword', '') for kw in trending_keywords[:5]])
        
        # Format trending items with enhanced image handling
        items_text = ""
        hero_images = []  # Collect potential hero images
        
        for i, item in enumerate(trending_items[:5], 1):
            title = getattr(item, 'title', 'Untitled')
            url = getattr(item, 'url', '#')
            summary = getattr(item, 'summary', '') or ''
            image_url = getattr(item, 'image_url', '') or ''
            
            items_text += f"{i}. **{title}**\n"
            items_text += f"   URL: {url}\n"
            if summary:
                items_text += f"   Summary: {summary[:200]}...\n"
            if image_url:
                items_text += f"   Image: {image_url}\n"
                # Collect high-quality images for potential hero use
                if i <= 3 and image_url:  # Use top 3 items' images as hero candidates
                    hero_images.append(image_url)
            items_text += "\n"
        
        # Build voice description
        voice_description = "Professional, engaging, and informative" if not voice_traits else ", ".join(voice_traits)
        
        # Build the comprehensive prompt based on sample format
        hero_image_1 = hero_images[0] if hero_images else 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop&crop=center'
        hero_image_2 = hero_images[1] if len(hero_images) > 1 else 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop&crop=center'
        hero_image_3 = hero_images[2] if len(hero_images) > 2 else 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop&crop=center'
        
        prompt = f"""You are a professional newsletter writer creating a comprehensive weekly newsletter. Follow the EXACT format and structure provided below.

**Newsletter Title:** {newsletter_title or "Weekly Tech Newsletter"}

**Writing Style/Voice:**
{voice_description}

**Trending Topics to Cover:**
{keywords_text}

**Top Content to Feature:**
{items_text}

**Instructions:**
Create a comprehensive newsletter in Markdown format following this EXACT structure:

# ⚡️ [NEWSLETTER TITLE] — [SUBTITLE] 🚀

*Your curated weekly pulse of innovation, hand-picked and written by AI — reviewed by humans.*

---

## 🧠 Big Picture
**Write a compelling opening statement about the week's theme.**  
This week, [newsletter name] dives into [key themes from the content]. Plus, [additional context about what's happening].

> TL;DR: [One-sentence summary of the main themes and what readers will learn].

---

## 🔍 Executive Summary
- **[Key Development 1]** - [Brief description]
- **[Key Development 2]** - [Brief description]  
- **[Key Development 3]** - [Brief description]
- **[Key Development 4]** - [Brief description]
- **[Key Development 5]** - [Brief description]

---

## 🚀 Top Picks of the Week

### 🧩 [Article Title 1](URL)
![Hero Image]({hero_image_1})
[Brief description of why this matters].  
*Why it matters:* [2-3 sentences explaining the impact and relevance].

---

### 💰 [Article Title 2](URL)
![Article Image]({hero_image_2})
[Brief description of why this matters].  
*Why it matters:* [2-3 sentences explaining the impact and relevance].

---

### 🧮 [Article Title 3](URL)
![Article Image]({hero_image_3})
[Brief description of why this matters].  
*Why it matters:* [2-3 sentences explaining the impact and relevance].

---

## 🌐 Trends to Watch

| 🔖 Trend | 💬 What's Happening | 📈 Impact |
|----------|--------------------|-----------|
| [Trend 1] | [Description] | [Impact statement] |
| [Trend 2] | [Description] | [Impact statement] |
| [Trend 3] | [Description] | [Impact statement] |

---

## 💡 Quick Bytes
- **[Tool/Product 1]:** [Brief description]
- **[Tool/Product 2]:** [Brief description]
- **[Tool/Product 3]:** [Brief description]
- **[Tool/Product 4]:** [Brief description]

---

## 📊 Data Pulse
- [Statistic 1] of [demographic] [action/behavior]
- [Number] of [category] this [time period] are [characteristic]
- [Metric] expected to [prediction] by [year]

---

## 🧭 Featured Tool
**Name:** [Tool Name](URL)  
**What it does:** [Description of functionality].  
**Why it's cool:** [Unique selling point or interesting aspect].

---

## 🧩 Did You Know?
[Interesting fact or trivia related to the newsletter's topics].  
[Additional context or connection to current events].

---

## 💬 From the Editor
[Personal note about the newsletter's mission or the week's content].  
[Connection to readers and what makes this newsletter special].

---

## 📅 Coming Next Week
- "[Topic] special edition"
- Deep dive: "[Specific topic or trend]"
- New beta: "[Feature or content preview]"

---

## 📨 Wrap-Up
That's a wrap for this week's **[Newsletter Name]**.  
If you loved this issue, share it with one curious mind.  
Feedback? Reply to this email — we actually read them 💬

> *Written with ❤️ by EchoWrite AI — powered by your curiosity.*

---

### 🔗 Footer
*Thank you for reading! We hope you found this newsletter valuable.*

**Important Guidelines:**
- Use the EXACT section headers provided
- Include all sections in the specified order
- Make it engaging, informative, and professional
- Use proper Markdown formatting
- Include relevant links and data
- Write in the specified voice/tone
- Include all URLs from the items
- IMPORTANT: Use the provided hero images for Top Picks sections
- Place images prominently at the start of each Top Pick to make the newsletter visually engaging
- If source images are available, use them; otherwise use the provided fallback images
- For other sections, include relevant images from the source content when available
- Aim for 400-600 words total
- Use the EXACT section headers provided above
- Make images large and prominent (800x400px) for visual impact
- Be authentic and engaging
- Make the Executive Summary actionable and compelling
- Ensure trivia is relevant and interesting
- Use visual elements (images, emojis, formatting) to break up text
- Each section should flow naturally into the next

Generate the newsletter now:"""
        
        return prompt
    
    @staticmethod
    def generate_email_subject(
        newsletter_title: str,
        trending_topics: List[str],
        user_name: Optional[str] = None
    ) -> str:
        """Generate structured email subject line"""
        
        # Common subject templates
        templates = [
            f"{newsletter_title} - Weekly Insights",
            f"{newsletter_title} - This Week's Highlights", 
            f"{newsletter_title} - Trending Topics & Insights",
            f"{newsletter_title} - Your Weekly Digest",
            f"{newsletter_title} - Latest Trends & Updates"
        ]
        
        # Add trending topic if available
        if trending_topics:
            main_topic = trending_topics[0]
            templates.extend([
                f"{newsletter_title} - {main_topic} & More",
                f"{newsletter_title} - Spotlight on {main_topic}",
                f"{newsletter_title} - {main_topic} Takes Center Stage"
            ])
        
        # Add personal touch if user name available
        if user_name:
            templates.extend([
                f"{user_name}'s {newsletter_title} - Weekly Insights",
                f"{newsletter_title} - Curated for {user_name}",
                f"Your {newsletter_title} - Weekly Highlights"
            ])
        
        # Return the first template (can be randomized later)
        return templates[0]
    
    @staticmethod
    def parse_newsletter_sections(content: str) -> Dict[str, str]:
        """Parse newsletter content into standardized sections"""
        sections = {
            "executive_summary": "",
            "introduction": "",
            "top_picks": "",
            "trends_to_watch": "",
            "did_you_know": "",
            "by_the_numbers": "",
            "closing": "",
            "raw_content": content
        }
        
        # Define section patterns
        section_patterns = {
            "executive_summary": r"##\s*📝\s*Executive Summary\s*\n([\s\S]*?)(?=\n##|$)",
            "introduction": r"##\s*Introduction\s*\n([\s\S]*?)(?=\n##|$)",
            "top_picks": r"##\s*🔥\s*Top Picks\s*\n([\s\S]*?)(?=\n##|$)",
            "trends_to_watch": r"##\s*📈\s*Trends to Watch\s*\n([\s\S]*?)(?=\n##|$)",
            "did_you_know": r"##\s*💡\s*Did You Know\?\s*\n([\s\S]*?)(?=\n##|$)",
            "by_the_numbers": r"##\s*📊\s*By The Numbers\s*\n([\s\S]*?)(?=\n##|$)",
            "closing": r"##\s*Closing\s*\n([\s\S]*?)(?=\n##|$)"
        }
        
        # Extract sections
        for section_id, pattern in section_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                sections[section_id] = match.group(1).strip()
        
        return sections
    
    @staticmethod
    def validate_newsletter_structure(content: str) -> Dict[str, Any]:
        """Validate that newsletter has required sections"""
        sections = NewsletterTemplate.parse_newsletter_sections(content)
        required_sections = ["executive_summary", "introduction", "top_picks", "trends_to_watch", "closing"]
        
        validation_result = {
            "is_valid": True,
            "missing_sections": [],
            "section_count": len([s for s in sections.values() if s.strip()]),
            "word_count": len(content.split()),
            "has_images": bool(re.search(r'!\[.*?\]\(.*?\)', content)),
            "has_links": bool(re.search(r'\[.*?\]\(.*?\)', content))
        }
        
        for section in required_sections:
            if not sections.get(section, "").strip():
                validation_result["is_valid"] = False
                validation_result["missing_sections"].append(section)
        
        return validation_result
