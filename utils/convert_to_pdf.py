#!/usr/bin/env python3
"""
Script to convert the research proposal markdown to a professionally formatted PDF.
Uses markdown2, weasyprint, and custom CSS for academic formatting.
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def install_requirements():
    """Install required packages if not already installed."""
    packages = [
        'markdown2',
        'weasyprint',
        'pygments'  # for code syntax highlighting
    ]
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def create_css_styles():
    """Create CSS styles for professional academic formatting."""
    css_content = """
    @page {
    size: A4;
    margin: 1in;
    @bottom-center {
        content: "Page " counter(page);
        font-size: 9pt;
        color: #666;
    }
}

/* === TITLE PAGE === */
.title-page {
    page-break-after: always;
    text-align: center;
    padding: 2in 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.title-page h1 {
    font-size: 24pt;
    font-weight: bold;
    color: #2c3e50;
    margin: 0 0 40pt 0;
    border: none;
    padding: 0;
    line-height: 1.3;
}

.title-page .subtitle {
    font-size: 16pt;
    color: #34495e;
    font-style: italic;
    margin: 20pt 0 60pt 0;
}

.title-page .author-info {
    font-size: 14pt;
    color: #555;
    margin: 20pt 0;
    line-height: 1.4;
}

.title-page .author-name {
    font-size: 16pt;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10pt;
}

.title-page .author-title {
    font-size: 12pt;
    color: #666;
    margin: 5pt 0;
}

.title-page .grant-info {
    font-size: 14pt;
    color: #2c3e50;
    font-weight: bold;
    margin-top: 40pt;
    padding-top: 20pt;
}

/* === BODY === */
body {
    font-family: "Times New Roman", Georgia, serif;
    font-size: 12pt;
    color: #222;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

/* === HEADINGS === */
h1, h2, h3, h4 {
    font-family: "Times New Roman", Georgia, serif;
    color: #1a1a1a;
    page-break-after: avoid;
    page-break-inside: avoid;
}

h1 {
    font-size: 20pt;
    font-weight: bold;
    text-align: center;
    color: #2c3e50;
    margin: 0 0 24pt 0;
    border-bottom: 2pt solid #2c3e50;
    padding-bottom: 8pt;
}

h2 {
    font-size: 15pt;
    font-weight: bold;
    margin: 24pt 0 12pt 0;
    color: #34495e;
    border-bottom: 1pt solid #bdc3c7;
    padding-bottom: 4pt;
}

h3 {
    font-size: 13pt;
    font-weight: bold;
    margin: 18pt 0 10pt 0;
    color: #2c3e50;
}

h4 {
    font-size: 12pt;
    font-weight: bold;
    margin: 14pt 0 8pt 0;
    color: #2c3e50;
}

/* === PARAGRAPHS & TEXT === */
p {
    margin: 0 0 10pt 0;
    text-align: justify;
    orphans: 2;
    widows: 2;
}

strong { color: #2c3e50; font-weight: bold; }
em { font-style: italic; color: #555; }

blockquote {
    margin: 15pt 20pt;
    padding: 10pt 14pt;
    background-color: #f8f9fa;
    border-left: 4pt solid #3498db;
    font-style: italic;
    color: #333;
}

/* === LISTS === */
ul, ol {
    margin: 10pt 0 10pt 30pt;
    padding: 0;
}
li {
    margin: 4pt 0;
}

/* === TABLES === */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20pt 0;
    font-size: 11pt;
    page-break-inside: avoid;
    border: none;
}

th, td {
    border: none;
    border-bottom: 1pt solid #ccc;
    padding: 12pt 10pt;
    text-align: left;
    vertical-align: top;
}

th {
    background-color: transparent;
    color: #000;
    font-weight: bold;
    border-bottom: 1pt solid #000;
}

tr:nth-child(even) {
    background-color: transparent;
}

/* === SPECIAL SECTIONS === */
.abstract {
    background: #f8f9fa;
    border-left: 4pt solid #2980b9;
    padding: 14pt;
    margin: 18pt 0;
}
.abstract h2 {
    border: none;
    margin-top: 0;
    padding-bottom: 0;
    color: #2c3e50;
}

/* Force References section to start on new page */
#references-section {
    page-break-before: always;
    break-before: page;
}

.references {
    display: block;
    clear: both;
    margin-top: 0;
    padding-top: 0;
    font-size: 11pt;
}
.references h2 {
    page-break-before: always;
    break-before: page;
    border-bottom: 1pt solid #bdc3c7;
}
.references ol {
    padding-left: 20pt;
    counter-reset: ref;
}
.references li {
    list-style: none;
    counter-increment: ref;
    margin: 6pt 0;
}
.references li::before {
    content: "[" counter(ref) "] ";
    font-weight: bold;
    color: #2c3e50;
}

/* === CODE / PRE === */
code {
    font-family: "Courier New", monospace;
    background: #f3f4f5;
    padding: 2pt 4pt;
    border-radius: 3pt;
    font-size: 10pt;
}
pre {
    background: #f8f9fa;
    border: 1pt solid #ccc;
    padding: 10pt;
    font-family: "Courier New", monospace;
    font-size: 10pt;
    overflow-x: auto;
}

/* === LINKS === */
a {
    color: #2c3e50;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.references a {
    color: #2980b9;
    text-decoration: none;
}

/* === HR & SPACING === */
hr {
    border: none;
    border-top: 1pt solid #ccc;
    margin: 24pt 0;
}

/* === PAGE BREAK CONTROL === */
.page-break { page-break-before: always; }
.no-break { page-break-inside: avoid; }

/* === FRONT INFO === */
.author-info {
    text-align: center;
    font-size: 11pt;
    color: #777;
    margin-bottom: 20pt;
}

/* === TOC === */
.toc {
    background: #fdfdfd;
    border: 1pt solid #ddd;
    padding: 12pt;
    margin: 18pt 0;
}
.toc h2 {
    border: none;
    margin-bottom: 6pt;
    color: #2c3e50;
}
.toc ul {
    list-style: none;
    margin: 0;
    padding: 0;
}
.toc li {
    font-size: 11pt;
    margin: 3pt 0;
}
    """
    
    return css_content

def convert_markdown_to_html(markdown_file):
    """Convert markdown to HTML with proper formatting."""
    try:
        import markdown2
    except ImportError:
        print("Error: markdown2 not installed. Please run: pip install markdown2")
        return None
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Extract title page information from the first few lines
    lines = markdown_content.split('\n')
    title = lines[0].replace('# ', '') if lines[0].startswith('# ') else "Research Proposal"
    
    # Extract author information (assuming it's in the first 10 lines)
    author_info = []
    grant_info = ""
    for i, line in enumerate(lines[:10]):
        if line.startswith('**') and '**' in line[2:]:
            author_info.append(line.strip('*'))
        elif 'Phase-2 URI Student Seed Grant Proposal' in line:
            grant_info = line.strip('*')
    
    # Find where the abstract starts to skip the title page content
    abstract_start = 0
    for i, line in enumerate(lines):
        if line.strip().lower() == '## abstract':
            abstract_start = i
            break
    
    # Remove the title page content (title, author info, grant info) from markdown
    if abstract_start > 0:
        # Keep everything from the abstract onwards
        markdown_content = '\n'.join(lines[abstract_start:])
    
    # Configure markdown2 with extensions
    extras = [
        'fenced-code-blocks',
        'tables',
        'header-ids',
        'toc',
        'footnotes',
        'smarty-pants'
    ]
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_content, extras=extras)
    
    # Wrap the References section with the references class and add ID to trigger page break
    html_content = html_content.replace('<h2>References</h2>', '<div class="references" id="references-section"><h2>References</h2>')
    
    # Close the references div at the end of the document
    html_content = html_content + '</div>'
    
    # Process references to embed URLs in titles and add anchors
    def process_references(html):
        # Split at references section
        ref_section = html.split('<div class="references">')
        if len(ref_section) > 1:
            refs = ref_section[1]
            
            # Pattern to match reference format: Author. (Year). *Title*. URL
            ref_pattern = r'<li>(.*?)\.\s*\((\d{4})\)\.\s*\*(.*?)\*\.\s*(https?://[^\s<>"]+)'
            
            def replace_ref(match):
                author = match.group(1)
                year = match.group(2)
                title = match.group(3)
                url = match.group(4)
                return f'<li id="ref-{len(re.findall(r"<li>", refs[:match.start()])) + 1}">{author}. ({year}). <a href="{url}">{title}</a>.</li>'
            
            refs = re.sub(ref_pattern, replace_ref, refs)
            html = ref_section[0] + '<div class="references">' + refs
        
        # Link in-text citations [1], [2], etc.
        citation_pattern = r'\[(\d+)\]'
        html = re.sub(citation_pattern, r'<a href="#ref-\1">[\1]</a>', html)
        
        return html
    
    # Apply the reference processing
    html_content = process_references(html_content)
    
    # Create title page HTML
    title_page_html = f"""
    <div class="title-page">
        <h1>{title}</h1>
        <div class="subtitle">URI Phase II Proposal</div>
        <div class="author-info">
            <div class="author-name">Pablo Leyva</div>
            <div class="author-title">Undergraduate Researcher – Applied Statistics and Data Analytics, NJIT</div>
            <div class="author-title">Prev AI/ML intern at Apple</div>
            <div class="author-title">Advisor, Dr. Ding</div>
        </div>
        <div class="grant-info">{grant_info}</div>
    </div>
    """
    
    # Create the full HTML document
    css_styles = create_css_styles()
    
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
        {css_styles}
        </style>
    </head>
    <body>
        {title_page_html}
        {html_content}
    </body>
    </html>
    """
    
    return full_html

def convert_html_to_pdf(html_content, output_file):
    """Convert HTML to PDF using WeasyPrint."""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        print("Error: WeasyPrint not installed. Please run: pip install weasyprint")
        return False
    
    try:
        # Create HTML object
        html_doc = HTML(string=html_content)
        
        # Generate PDF
        html_doc.write_pdf(output_file)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

def main():
    """Main function to convert markdown to PDF."""
    # Get the current directory
    current_dir = Path(__file__).parent
    markdown_file = current_dir / "proposal.md"
    output_file = current_dir / "proposal.pdf"
    
    # Check if markdown file exists
    if not markdown_file.exists():
        print(f"Error: {markdown_file} not found!")
        return False
    
    print("Installing required packages...")
    install_requirements()
    
    print("Converting markdown to HTML...")
    html_content = convert_markdown_to_html(markdown_file)
    if not html_content:
        return False
    
    print("Converting HTML to PDF...")
    success = convert_html_to_pdf(html_content, output_file)
    
    if success:
        print(f"✅ PDF successfully generated: {output_file}")
        print(f"📄 File size: {output_file.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("❌ Failed to generate PDF")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
