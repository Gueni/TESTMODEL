def create_html_with_assets(html_content, css_content, js_content, output_file):
    """Embed CSS and JS content into HTML"""
    import re
    
    def minify_css(css):
        # Remove comments, whitespace, etc.
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        css = re.sub(r'\s+', ' ', css)
        css = re.sub(r';\s*', ';', css)
        css = re.sub(r':\s*', ':', css)
        css = re.sub(r'\s*\{\s*', '{', css)
        css = re.sub(r'\s*\}\s*', '}', css)
        return css.strip()
    
    def minify_js(js):
        # Basic JS minification
        js = re.sub(r'//.*', '', js)
        js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
        js = re.sub(r'\s+', ' ', js)
        return js.strip()
    
    # Minify the content
    minified_css = minify_css(css_content)
    minified_js = minify_js(js_content)
    
    # Replace or add style and script tags
    # Method 1: Replace existing style/script tags
    html_content = re.sub(r'<style>.*?</style>', f'<style>{minified_css}</style>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<script>.*?</script>', f'<script>{minified_js}</script>', html_content, flags=re.DOTALL)
    
    # Method 2: Or add them if they don't exist
    if '<style>' not in html_content:
        html_content = html_content.replace('</head>', f'<style>{minified_css}</style></head>')
    if '<script>' not in html_content:
        html_content = html_content.replace('</body>', f'<script>{minified_js}</script></body>')
    
    with open(output_file, 'w') as f:
        f.write(html_content)

# Usage example
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
    <style></style>
</head>
<body>
    <h1>Hello World</h1>
    <script></script>
</body>
</html>
"""

css_content = """
/* My CSS */
body { 
    background-color: #f0f0f0; 
    font-family: Arial, sans-serif;
}
h1 { color: blue; }
"""

js_content = """
// My JavaScript
function hello() {
    alert('Hello World!');
    console.log('Page loaded');
}
"""

create_html_with_assets(html_template, css_content, js_content, 'output.html')
        
