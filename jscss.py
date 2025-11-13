def minify_files(html_file, css_file, js_file, output_file):
    """Embed and minify files"""
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
    
    # Read files and embed with minification
    with open(html_file, 'r') as f:
        html = f.read()
    
    with open(css_file, 'r') as f:
        css = minify_css(f.read())
    
    with open(js_file, 'r') as f:
        js = minify_js(f.read())
    
    # Replace references (similar to previous examples)
    html = html.replace(f'<link rel="stylesheet" href="{css_file}">', f'<style>{css}</style>')
    html = html.replace(f'<script src="{js_file}"></script>', f'<script>{js}</script>')
    
    with open(output_file, 'w') as f:
        f.write(html)
        
        
        
        
