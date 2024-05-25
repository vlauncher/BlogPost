import requests, os
import re

def fetch_github_raw_text(url):
    cleaned_url = re.sub(r'^https?://github\.com/', 'https://raw.githubusercontent.com/', url)
    cleaned_url = re.sub(r'/blob/', '/', cleaned_url)
    
    response = requests.get(cleaned_url)
    if response.status_code == 200:
        return response.text
    return None
 