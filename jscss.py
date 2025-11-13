import re

def replace_special_chars(text):
    return re.sub(r'[^a-zA-Z0-9]', '_', text)