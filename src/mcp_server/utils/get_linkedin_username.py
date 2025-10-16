import re

def get_username(url):
    match = re.search(r"linkedin\.com/in/([^/]+)/?", url)
    if match:
        return match.group(1)
    return None

