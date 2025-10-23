"""
Email templates for newsletters
"""

from datetime import datetime
import re
import os

def get_newsletter_html_template(newsletter_title: str, newsletter_body_html: str, unsubscribe_url: str = "#", draft_id: str = None) -> str:
    """
    Generate beautiful HTML email template for newsletter
    
    Args:
        newsletter_title: Title of the newsletter
        newsletter_body_html: HTML content of the newsletter
        unsubscribe_url: URL for unsubscribe link
    
    Returns:
        Complete HTML email template
    """
    # Get the base URL from environment or use localhost for development
    base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{newsletter_title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .email-wrapper {{
            padding: 20px;
            min-height: 100vh;
        }}
        
        .email-container {{
            max-width: 680px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            overflow: hidden;
            position: relative;
        }}
        
        .email-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }}
        
        .email-header {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 50px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .email-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(180deg); }}
        }}
        
        .email-header h1 {{
            margin: 0;
            color: #ffffff;
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .email-header .subtitle {{
            margin: 15px 0 0;
            color: #cbd5e1;
            font-size: 16px;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }}
        
        .email-header .date-info {{
            margin: 20px 0 0;
            display: flex;
            justify-content: center;
            gap: 20px;
            position: relative;
            z-index: 1;
        }}
        
        .date-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #94a3b8;
            font-size: 14px;
            font-weight: 500;
        }}
        
        .date-item .icon {{
            width: 16px;
            height: 16px;
            opacity: 0.8;
        }}
        }}
        
        .email-body {{
            padding: 50px 40px;
            color: #374151;
            background: #ffffff;
        }}
        
        .email-body h1 {{
            color: #1e293b;
            font-size: 28px;
            font-weight: 800;
            margin: 0 0 20px;
            letter-spacing: -0.5px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .email-body h2 {{
            color: #1e293b;
            font-size: 24px;
            font-weight: 700;
            margin: 40px 0 20px;
            position: relative;
            padding-left: 20px;
        }}
        
        .email-body h2::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }}
        
        .email-body h3 {{
            color: #475569;
            font-size: 20px;
            font-weight: 600;
            margin: 30px 0 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .email-body h3::before {{
            content: '';
            width: 8px;
            height: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            flex-shrink: 0;
        }}
        
        .email-body p {{
            margin: 0 0 20px;
            color: #475569;
            line-height: 1.8;
            font-size: 16px;
        }}
        
        .special-section p {{
            margin: 0 0 20px;
            color: #374151;
            line-height: 1.8;
            font-size: 16px;
            position: relative;
        }}
        
        .special-section p:first-of-type {{
            margin-top: 10px;
        }}
        
        .special-section strong {{
            color: #1e293b;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .special-section ul {{
            margin: 20px 0;
            padding-left: 0;
            list-style: none;
        }}
        
        .special-section li {{
            margin: 12px 0;
            padding: 12px 20px;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            border-left: 4px solid;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .special-section.executive li {{
            border-left-color: #0ea5e9;
        }}
        
        .special-section.trivia li {{
            border-left-color: #f59e0b;
        }}
        
        .special-section.stats li {{
            border-left-color: #10b981;
        }}
        
        .special-section.trends li {{
            border-left-color: #8b5cf6;
        }}
        
        .special-section li:hover {{
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .special-section li::before {{
            content: '▶';
            position: absolute;
            left: 8px;
            top: 12px;
            color: #667eea;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .email-body a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .email-body a::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}
        
        .email-body a:hover::after {{
            width: 100%;
        }}
        
        .email-body img {{
            max-width: 100%;
            height: auto;
            border-radius: 16px;
            margin: 25px 0;
            display: block;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .email-body img:hover {{
            transform: translateY(-2px);
        }}
        
        .hero-image {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 20px;
            margin: 20px 0 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }}
        
        .hero-image:hover {{
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }}
        
        .article-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 12px;
            margin: 15px 0 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }}
        
        .article-image:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .email-body ul, .email-body ol {{
            margin: 0 0 25px;
            padding-left: 0;
            list-style: none;
        }}
        
        .email-body li {{
            margin: 12px 0;
            color: #475569;
            padding-left: 25px;
            position: relative;
            font-size: 16px;
            line-height: 1.7;
        }}
        
        .email-body ul li::before {{
            content: '▶';
            position: absolute;
            left: 0;
            color: #667eea;
            font-size: 12px;
            top: 6px;
        }}
        
        .email-body ol {{
            counter-reset: item;
        }}
        
        .email-body ol li {{
            counter-increment: item;
        }}
        
        .email-body ol li::before {{
            content: counter(item);
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: 600;
            font-size: 14px;
            top: 2px;
        }}
        
        .email-body strong {{
            color: #1e293b;
            font-weight: 700;
        }}
        .special-section {{
            margin: 40px 0;
            border-radius: 24px;
            padding: 40px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 2px solid transparent;
            background-clip: padding-box;
            transition: all 0.3s ease;
        }}
        
        .special-section:hover {{
            transform: translateY(-5px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
        }}
        
        .special-section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            border-radius: 24px 24px 0 0;
        }}
        
        .special-section::after {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            border-radius: 24px;
            z-index: -1;
            opacity: 0.1;
        }}
        
        .special-section.executive {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
            border: 2px solid #0ea5e9;
            box-shadow: 0 20px 40px rgba(14, 165, 233, 0.2);
        }}
        
        .special-section.executive:hover {{
            box-shadow: 0 30px 60px rgba(14, 165, 233, 0.3);
        }}
        
        .special-section.trivia {{
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #fde68a 100%);
            border: 2px solid #f59e0b;
            box-shadow: 0 20px 40px rgba(245, 158, 11, 0.2);
        }}
        
        .special-section.trivia:hover {{
            box-shadow: 0 30px 60px rgba(245, 158, 11, 0.3);
        }}
        
        .special-section.stats {{
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
            border: 2px solid #10b981;
            box-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
        }}
        
        .special-section.stats:hover {{
            box-shadow: 0 30px 60px rgba(16, 185, 129, 0.3);
        }}
        
        .special-section.trends {{
            background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 50%, #e9d5ff 100%);
            border: 2px solid #8b5cf6;
            box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2);
        }}
        
        .special-section.trends:hover {{
            box-shadow: 0 30px 60px rgba(139, 92, 246, 0.3);
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 800;
            color: #1e293b;
            margin: 0 0 25px;
            display: flex;
            align-items: center;
            gap: 15px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
        }}
        
        .section-title::before {{
            content: '';
            width: 8px;
            height: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        .email-body table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .email-body th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
        }}
        
        .email-body td {{
            padding: 15px 20px;
            border-bottom: 1px solid #f1f5f9;
            color: #475569;
            font-size: 14px;
            line-height: 1.6;
        }}
        
        .email-body tr:hover {{
            background: #f8fafc;
        }}
        
        .email-body tr:last-child td {{
            border-bottom: none;
        }}
        
        .email-footer {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .email-footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        }}
        
        .email-footer p {{
            margin: 8px 0;
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.6;
        }}
        
        .email-footer a {{
            color: #60a5fa;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        
        .email-footer a:hover {{
            color: #93c5fd;
        }}
        
        .branding {{
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #475569;
            position: relative;
        }}
        
        .branding::before {{
            content: '✨';
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            padding: 0 15px;
            font-size: 16px;
        }}
        
        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .social-link {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50%;
            transition: transform 0.3s ease;
        }}
        
        .social-link:hover {{
            transform: translateY(-2px);
        }}
        
        .unsubscribe {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #475569;
        }}
        
        .unsubscribe a {{
            color: #94a3b8;
            font-size: 12px;
            text-decoration: none;
        }}
        
        .unsubscribe a:hover {{
            color: #cbd5e1;
        }}
        
        /* Mobile Responsive */
        @media (max-width: 600px) {{
            .email-wrapper {{
                padding: 10px;
            }}
            
            .email-container {{
                border-radius: 16px;
            }}
            
            .email-header {{
                padding: 30px 20px;
            }}
            
            .email-header h1 {{
                font-size: 24px;
            }}
            
            .email-body {{
                padding: 30px 20px;
            }}
            
            .email-body h2 {{
                font-size: 20px;
            }}
            
            .email-footer {{
                padding: 30px 20px;
            }}
            
            .date-info {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
        }}
        .branding p {{
            margin: 5px 0;
            font-size: 12px;
            color: #9ca3af;
        }}
        .feedback-section {{
            margin: 40px 0;
            padding: 30px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 20px;
            text-align: center;
            border: 2px solid #e2e8f0;
            position: relative;
            overflow: hidden;
        }}
        
        .feedback-section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }}
        
        .feedback-section h3 {{
            margin: 0 0 10px;
            color: #1e293b;
            font-size: 20px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
        
        .feedback-section p {{
            margin: 0 0 25px;
            color: #64748b;
            font-size: 15px;
            line-height: 1.6;
        }}
        
        .feedback-buttons {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .feedback-button {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 16px 32px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 16px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            min-width: 160px;
            justify-content: center;
        }}
        
        .feedback-button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }}
        
        .feedback-button:hover::before {{
            left: 100%;
        }}
        
        .feedback-button.positive {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }}
        
        .feedback-button.positive:hover {{
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(16, 185, 129, 0.4);
        }}
        
        .feedback-button.negative {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
        }}
        
        .feedback-button.negative:hover {{
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(239, 68, 68, 0.4);
        }}
        
        .feedback-emoji {{
            font-size: 20px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        }}
        @media only screen and (max-width: 600px) {{
            .feedback-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            .feedback-button {{
                width: 100%;
                max-width: 200px;
            }}
        }}
        @media only screen and (max-width: 600px) {{
            .email-header {{
                padding: 30px 20px;
            }}
            .email-body {{
                padding: 30px 20px;
            }}
            .email-header h1 {{
                font-size: 24px;
            }}
            .email-body h2 {{
                font-size: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="email-container">
            <div class="email-header">
                <h1>{newsletter_title}</h1>
                <p class="subtitle">Your curated weekly pulse of innovation, hand-picked and written by AI — reviewed by humans.</p>
                <div class="date-info">
                    <div class="date-item">
                        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        </svg>
                        {datetime.now().strftime('%a, %b %d, %Y')}
                    </div>
                    <div class="date-item">
                        <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        </svg>
                        3 min read
                    </div>
                </div>
            </div>
            
            <div class="email-body">
                {newsletter_body_html}
            </div>
            
            <div class="email-footer">
                <p><strong>EchoWrite</strong> - AI-Powered Newsletter Generation</p>
                <p>This newsletter was generated using AI and curated content from your selected sources.</p>
                
                    <div class="social-links">
                        <a href="{base_url}" class="social-link" title="Visit EchoWrite">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                            </svg>
                        </a>
                    </div>
                
                <div class="branding">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>Draft ID: {draft_id or 'N/A'}</p>
                </div>
                
                <div class="unsubscribe">
                    <a href="{unsubscribe_url}">Unsubscribe</a> | 
                    <a href="{base_url}">Visit App</a>
                </div>
                
                {get_feedback_section(draft_id) if draft_id else ""}
            </div>
        </div>
    </div>
</body>
</html>
"""


def markdown_to_email_html(markdown_text: str) -> str:
    """
    Convert markdown to email-friendly HTML with beautiful styling
    
    Args:
        markdown_text: Markdown content
    
    Returns:
        HTML formatted for email with beautiful styling
    """
    
    # Check if content is already HTML (contains HTML tags)
    if markdown_text.find('<h1') != -1 or markdown_text.find('<h2') != -1 or markdown_text.find('<p') != -1 or markdown_text.find('<div') != -1:
        # Clean up any raw HTML attributes that are being rendered as text
        cleaned = markdown_text
        # Remove standalone HTML attributes that are being rendered as text
        cleaned = re.sub(r'class="[^"]*"', '', cleaned)
        cleaned = re.sub(r'style="[^"]*"', '', cleaned)
        cleaned = re.sub(r'onerror="[^"]*"', '', cleaned)
        cleaned = re.sub(r'/>', '>', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned
    
    html = markdown_text
    
    # Headers with beautiful styling
    html = re.sub(r'^# (.*$)', r'<h1 class="text-4xl font-bold mb-8 text-slate-800 text-center bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent border-b-4 border-gradient-to-r from-blue-500 to-purple-500 pb-4">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2 class="text-3xl font-bold text-slate-800 mb-6 mt-12 flex items-center gap-4 relative"><div class="w-4 h-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full shadow-lg"></div>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3 class="text-2xl font-bold text-slate-800 mb-4 mt-8 flex items-center gap-3"><div class="w-3 h-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></div>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold with gradient styling
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-slate-800 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">\1</strong>', html)
    
    # Links with beautiful styling
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-blue-600 hover:text-blue-800 font-semibold underline decoration-2 underline-offset-2 hover:decoration-blue-800 transition-all duration-200">\1</a>', html)
    
    # Images with enhanced styling and fallback
    def process_image(match):
        alt_text = match.group(1)
        src = match.group(2)
        
        # Fallback images for different types
        fallback_images = {
            'hero': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=400&fit=crop&crop=center',
            'article': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop&crop=center',
            'default': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop&crop=center'
        }
        
        # Check if image URL is valid, otherwise use fallback
        def is_valid_url(url):
            try:
                from urllib.parse import urlparse
                result = urlparse(url)
                return all([result.scheme, result.netloc]) and url.startswith('http') and 'undefined' not in url and 'null' not in url
            except:
                return False
        
        image_url = src if is_valid_url(src) else fallback_images.get('hero' if 'hero' in alt_text.lower() else 'article' if 'article' in alt_text.lower() else 'default', fallback_images['default'])
        
        if 'hero' in alt_text.lower():
            return f'''<div class="relative w-full my-8 group">
                <img src="{image_url}" alt="{alt_text}" class="w-full rounded-3xl shadow-2xl object-cover h-80 border-2 border-slate-200 hover:shadow-3xl transition-all duration-500 hover:scale-[1.02] hover:border-blue-300" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>'''
        elif 'article' in alt_text.lower():
            return f'''<div class="relative w-full my-6 group">
                <img src="{image_url}" alt="{alt_text}" class="w-full rounded-2xl shadow-xl object-cover h-64 border-2 border-slate-200 hover:shadow-2xl transition-all duration-300 hover:scale-[1.01] hover:border-purple-300" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>'''
        else:
            return f'<img src="{image_url}" alt="{alt_text}" class="w-full rounded-xl shadow-lg object-cover my-6 border border-slate-200 hover:shadow-xl transition-all duration-300" />'
    
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', process_image, html)
    
    # Enhanced table conversion
    lines = html.split('\n')
    in_table = False
    table_html = []
    processed_lines = []
    
    for line in lines:
        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
                table_html = ['<div class="overflow-x-auto my-8 rounded-2xl shadow-xl"><table class="w-full bg-white">']
            
            # Check if it's a separator line
            if re.match(r'^\|[\s\-\|]+\|$', line.strip()):
                continue
            
            # Process table row
            cells = [cell.strip() for cell in line.strip().split('|')[1:-1]]
            if cells:
                # Check if first row looks like headers (contains emojis or specific keywords)
                if any('🔖' in cell or '💬' in cell or '📈' in cell for cell in cells):
                    table_html.append('<thead><tr>')
                    for cell in cells:
                        table_html.append(f'<th class="px-6 py-4 text-left text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600">{cell}</th>')
                    table_html.append('</tr></thead><tbody>')
                else:
                    table_html.append('<tr class="hover:bg-slate-50 transition-colors">')
                    for cell in cells:
                        table_html.append(f'<td class="px-6 py-4 text-sm text-slate-700 border-b border-slate-200">{cell}</td>')
                    table_html.append('</tr>')
        else:
            if in_table:
                in_table = False
                table_html.append('</tbody></table></div>')
                processed_lines.append('\n'.join(table_html))
                table_html = []
            processed_lines.append(line)
    
    # Close any remaining table
    if in_table:
        table_html.append('</tbody></table></div>')
        processed_lines.append('\n'.join(table_html))
    
    html = '\n'.join(processed_lines)
    
    # Lists with beautiful styling
    html = re.sub(r'^[-•*] (.*$)', r'<li class="mb-4 text-slate-600 leading-relaxed flex items-start gap-4 p-3 rounded-lg hover:bg-slate-50 transition-colors"><span class="text-blue-500 font-bold text-sm mt-1 min-w-[24px] flex-shrink-0">▶</span><span class="flex-1">\1</span></li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li class="[^"]*">.*?</li>)', r'<ul class="space-y-2">\1</ul>', html, flags=re.DOTALL)
    
    # Numbered lists
    html = re.sub(r'^\d+\. (.*$)', r'<li class="mb-4 text-slate-600 leading-relaxed flex items-start gap-4 p-3 rounded-lg hover:bg-slate-50 transition-colors"><span class="text-blue-500 font-bold text-sm mt-1 min-w-[24px] flex-shrink-0">$1.</span><span class="flex-1">$2</span></li>', html, flags=re.MULTILINE)
    
    # Paragraphs
    lines = html.split('\n\n')
    paragraphs = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<'):
            paragraphs.append(f'<p class="mb-6 text-slate-600 leading-relaxed text-lg">\1</p>')
        else:
            paragraphs.append(line)
    
    html = '\n'.join(paragraphs)
    
    # Wrap special sections with beautiful styling
    section_patterns = [
        (r'<h2[^>]*>🔍 Executive Summary</h2>(.*?)(?=<h[12]|$)', 'executive', '🔍 Executive Summary'),
        (r'<h2[^>]*>🧠 Big Picture</h2>(.*?)(?=<h[12]|$)', 'stats', '🧠 Big Picture'),
        (r'<h2[^>]*>🚀 Top Picks of the Week</h2>(.*?)(?=<h[12]|$)', 'trends', '🚀 Top Picks of the Week'),
        (r'<h2[^>]*>🌐 Trends to Watch</h2>(.*?)(?=<h[12]|$)', 'trends', '🌐 Trends to Watch'),
        (r'<h2[^>]*>💡 Quick Bytes</h2>(.*?)(?=<h[12]|$)', 'stats', '💡 Quick Bytes'),
        (r'<h2[^>]*>📊 Data Pulse</h2>(.*?)(?=<h[12]|$)', 'stats', '📊 Data Pulse'),
        (r'<h2[^>]*>🧭 Featured Tool</h2>(.*?)(?=<h[12]|$)', 'trivia', '🧭 Featured Tool'),
        (r'<h2[^>]*>🧩 Did You Know\?</h2>(.*?)(?=<h[12]|$)', 'trivia', '🧩 Did You Know?'),
        (r'<h2[^>]*>💬 From the Editor</h2>(.*?)(?=<h[12]|$)', 'executive', '💬 From the Editor'),
        (r'<h2[^>]*>📅 Coming Next Week</h2>(.*?)(?=<h[12]|$)', 'trends', '📅 Coming Next Week'),
        (r'<h2[^>]*>📨 Wrap-Up</h2>(.*?)(?=<h[12]|$)', 'executive', '📨 Wrap-Up'),
    ]
    
    for pattern, section_type, title in section_patterns:
        gradient_classes = {
            'executive': 'from-blue-50 via-sky-50 to-blue-100',
            'stats': 'from-green-50 via-emerald-50 to-green-100',
            'trends': 'from-purple-50 via-violet-50 to-purple-100',
            'trivia': 'from-amber-50 via-orange-50 to-amber-100'
        }
        
        border_classes = {
            'executive': 'border-blue-500',
            'stats': 'border-green-500',
            'trends': 'border-purple-500',
            'trivia': 'border-amber-500'
        }
        
        icon_classes = {
            'executive': 'from-blue-500 to-sky-500',
            'stats': 'from-green-500 to-emerald-500',
            'trends': 'from-purple-500 to-violet-500',
            'trivia': 'from-amber-500 to-orange-500'
        }
        
        dot_classes = {
            'executive': 'bg-blue-500',
            'stats': 'bg-green-500',
            'trends': 'bg-purple-500',
            'trivia': 'bg-amber-500'
        }
        
        html = re.sub(
            pattern,
            f'''<div class="mt-12 p-12 bg-gradient-to-br {gradient_classes[section_type]} border-2 {border_classes[section_type]} rounded-3xl shadow-2xl relative overflow-hidden hover:shadow-3xl transition-all duration-500 hover:-translate-y-3 group backdrop-blur-sm">
                <div class="absolute top-0 left-0 right-0 h-3 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-t-3xl"></div>
                <div class="absolute -top-2 -left-2 -right-2 -bottom-2 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl opacity-5 -z-10"></div>
                <div class="absolute inset-0 bg-white/20 backdrop-blur-sm rounded-3xl"></div>
                <div class="relative z-10">
                    <div class="flex items-center gap-6 mb-8">
                        <div class="p-5 bg-gradient-to-r {icon_classes[section_type]} rounded-2xl shadow-xl group-hover:scale-110 transition-transform duration-300">
                            <svg class="h-10 w-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <h3 class="text-3xl font-bold text-slate-800 flex items-center gap-4 relative">
                            <div class="w-4 h-4 {dot_classes[section_type]} rounded-full shadow-lg"></div>
                            {title}
                        </h3>
                    </div>
                    \\1
                </div>
            </div>''',
            html,
            flags=re.DOTALL
        )
    
    return html


def get_feedback_section(draft_id: str) -> str:
    """
    Generate feedback collection section for email
    
    Args:
        draft_id: ID of the draft for feedback tracking
    
    Returns:
        HTML for feedback section
    """
    if not draft_id:
        return ""
    
    # Get the base URL from environment or use localhost for development
    base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    return f"""
    <div class="feedback-section">
        <h3>💬 How was this newsletter?</h3>
        <p>Your feedback helps us improve future newsletters!</p>
        <div class="feedback-buttons">
            <a href="{api_url}/api/v1/feedback/public?draft_id={draft_id}&reaction=👍&source=email" 
               class="feedback-button positive">
                <span class="feedback-emoji">👍</span>
                Great newsletter!
            </a>
            <a href="{api_url}/api/v1/feedback/public?draft_id={draft_id}&reaction=👎&source=email" 
               class="feedback-button negative">
                <span class="feedback-emoji">👎</span>
                Needs improvement
            </a>
        </div>
    </div>
    """

