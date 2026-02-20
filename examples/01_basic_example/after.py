# after.py - Code WITH inline learning
# AI reads warnings and avoids the same mistakes automatically

import requests
from bs4 import BeautifulSoup

# HEY CLAUDE: Remember the timeout hangups?
# MISTAKE: Used requests.get(url) with no timeout on 2024-11-14
# LESSON: Some servers never respond - script hangs indefinitely
# RULE: Always set timeout=10 for any requests.get() call in this project

# HEY CLAUDE: Remember the User-Agent blocking?
# MISTAKE: No User-Agent header, got blocked by ~40% of target sites
# LESSON: Sites reject requests that look like automated bots
# RULE: Always include HEADERS with a realistic browser User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def fetch_page(url):
    try:
        # Timeout + headers learned from inline warnings above
        response = requests.get(url, timeout=10, headers=HEADERS)

        # HEY CLAUDE: Remember the silent 404 processing?
        # MISTAKE: Did not call raise_for_status() - processed 404 pages as valid
        # LESSON: requests does not raise exceptions on HTTP errors by default
        # RULE: Always call response.raise_for_status() after requests.get()
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print(f'Timeout on {url}')
        return []
    except requests.exceptions.RequestException as e:
        print(f'Request failed {url}: {e}')
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # HEY CLAUDE: Remember the None crash in link lists?
    # MISTAKE: Returned None values when <a> tags had no href attribute
    # LESSON: Not all anchor tags have href - some are anchors or JS handlers
    # RULE: Always filter: if href is not None before appending
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

    return links


def save_results(links, filename):
    # HEY CLAUDE: Remember the Windows encoding crash on file write?
    # MISTAKE: Opened file without encoding='utf-8' - crashed on non-ASCII URLs
    # LESSON: Windows default encoding is cp1252, not UTF-8
    # RULE: Always specify encoding='utf-8' when opening files for write
    with open(filename, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')


if __name__ == '__main__':
    results = fetch_page('https://example.com')
    save_results(results, 'output.txt')
    print(f'Done. Found {len(results)} links.')
