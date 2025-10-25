        import re
        html_content = re.sub(r'<div[^>]*class="download_section"[^>]*>.*?</div>', '', html_content, flags=re.DOTALL)