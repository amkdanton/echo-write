"""
Email templates for newsletters
"""

def get_newsletter_html_template(newsletter_title: str, newsletter_body_html: str, unsubscribe_url: str = "#") -> str:
    """
    Generate beautiful HTML email template for newsletter
    
    Args:
        newsletter_title: Title of the newsletter
        newsletter_body_html: HTML content of the newsletter
        unsubscribe_url: URL for unsubscribe link
    
    Returns:
        Complete HTML email template
    """
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{newsletter_title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f3f4f6;
            line-height: 1.6;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
        }}
        .email-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            text-align: center;
        }}
        .email-header h1 {{
            margin: 0;
            color: #ffffff;
            font-size: 28px;
            font-weight: 700;
        }}
        .email-header p {{
            margin: 10px 0 0;
            color: #e0e7ff;
            font-size: 14px;
        }}
        .email-body {{
            padding: 40px 30px;
            color: #374151;
        }}
        .email-body h2 {{
            color: #1f2937;
            font-size: 24px;
            font-weight: 700;
            margin: 30px 0 15px;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }}
        .email-body h3 {{
            color: #374151;
            font-size: 20px;
            font-weight: 600;
            margin: 25px 0 12px;
        }}
        .email-body p {{
            margin: 0 0 15px;
            color: #4b5563;
            line-height: 1.7;
        }}
        .email-body a {{
            color: #667eea;
            text-decoration: underline;
            font-weight: 600;
        }}
        .email-body a:hover {{
            color: #764ba2;
        }}
        .email-body img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            margin: 20px 0;
            display: block;
        }}
        .email-body ul, .email-body ol {{
            margin: 0 0 20px;
            padding-left: 25px;
        }}
        .email-body li {{
            margin: 8px 0;
            color: #4b5563;
        }}
        .email-body strong {{
            color: #1f2937;
            font-weight: 600;
        }}
        .special-section {{
            border-left: 4px solid #667eea;
            background-color: #f9fafb;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
        }}
        .special-section.executive {{
            border-left-color: #3b82f6;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        }}
        .special-section.trivia {{
            border-left-color: #f59e0b;
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        }}
        .special-section.stats {{
            border-left-color: #10b981;
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #1f2937;
            margin: 0 0 12px;
        }}
        .email-footer {{
            background-color: #f9fafb;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }}
        .email-footer p {{
            margin: 5px 0;
            color: #6b7280;
            font-size: 13px;
        }}
        .email-footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        .email-footer a:hover {{
            text-decoration: underline;
        }}
        .branding {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
        .branding p {{
            margin: 5px 0;
            font-size: 12px;
            color: #9ca3af;
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
    <div class="email-container">
        <!-- Header -->
        <div class="email-header">
            <h1>✨ {newsletter_title}</h1>
            <p>Your curated newsletter digest</p>
        </div>
        
        <!-- Body -->
        <div class="email-body">
            {newsletter_body_html}
        </div>
        
        <!-- Footer -->
        <div class="email-footer">
            <p><strong>Thank you for reading! 🎉</strong></p>
            <p>Stay informed, stay ahead.</p>
            
            <div class="branding">
                <p>Crafted with ✨ by <strong>EchoWrite</strong></p>
                <p>
                    <a href="{unsubscribe_url}">Unsubscribe</a> | 
                    <a href="https://echowrite.ai">Visit our website</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""


def markdown_to_email_html(markdown_text: str) -> str:
    """
    Convert markdown to email-friendly HTML
    
    Args:
        markdown_text: Markdown content
    
    Returns:
        HTML formatted for email
    """
    import re
    
    html = markdown_text
    
    # Headers
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Images
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', html)
    
    # Lists (simplified)
    html = re.sub(r'^[-•*] (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    # Paragraphs
    lines = html.split('\n\n')
    paragraphs = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<'):
            paragraphs.append(f'<p>{line}</p>')
        else:
            paragraphs.append(line)
    
    html = '\n'.join(paragraphs)
    
    # Wrap special sections
    html = re.sub(
        r'<h2>📝 Executive Summary</h2>(.*?)(?=<h2>|$)',
        r'<div class="special-section executive"><p class="section-title">📝 Executive Summary</p>\1</div>',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'<h2>💡 Did You Know\?</h2>(.*?)(?=<h2>|$)',
        r'<div class="special-section trivia"><p class="section-title">💡 Did You Know?</p>\1</div>',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'<h2>📊 By The Numbers</h2>(.*?)(?=<h2>|$)',
        r'<div class="special-section stats"><p class="section-title">📊 By The Numbers</p>\1</div>',
        html,
        flags=re.DOTALL
    )
    
    return html

