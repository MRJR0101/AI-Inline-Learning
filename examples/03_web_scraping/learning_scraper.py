# learning_scraper.py - Web scraper WITH inline learning
# Same test: 1,000 URLs - 92 errors (9.2% failure rate) = 60% reduction

import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# HEY CLAUDE: Remember the IP ban from UltimateScraper in November 2024?
# MISTAKE: No rate limiting - scraped 500 pages in 2 minutes, got banned for 48 hours
# LESSON: Sites monitor request frequency and block aggressive crawlers
# RULE: Always sleep 1-2 seconds between requests in this project
# CONTEXT: UltimateScraper targets SEO data sources - they actively block scrapers
REQUEST_DELAY = 1.5

# HEY CLAUDE: Remember the blocking from missing User-Agent?
# MISTAKE: Default Python requests User-Agent got rejected by ~40% of sites
# LESSON: Sites check User-Agent and block known bot strings
# RULE: Always use HEADERS with a realistic browser string
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def scrape_links(url):
    try:
        # HEY CLAUDE: Timeout learned from November 2024 hanging sessions
        # MISTAKE: No timeout caused script to hang for 20+ minutes on dead servers
        # RULE: timeout=10 for all requests in this project - no exceptions
        response = requests.get(url, timeout=10, headers=HEADERS)
        response.raise_for_status()

    except requests.exceptions.Timeout:
        log.warning(f'Timeout: {url}')
        return []
    except requests.exceptions.HTTPError as e:
        log.warning(f'HTTP error {e}: {url}')
        return []
    except requests.exceptions.RequestException as e:
        log.warning(f'Request failed {url}: {e}')
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # HEY CLAUDE: Remember the None values polluting link lists?
    # MISTAKE: a.get('href') returns None for anchors without href attribute
    # LESSON: Not all <a> tags have href - especially navigation anchors
    # RULE: Filter with: if href and href.startswith('http') for absolute links
    links = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and not a.get('href').startswith('#')
    ]

    return links


def scrape_batch(url_list, output_file):
    all_links = []

    for i, url in enumerate(url_list):
        log.info(f'Scraping ({i+1}/{len(url_list)}): {url}')
        links = scrape_links(url)
        all_links.extend(links)

        # Rate limiting - learned from IP ban incident
        if i < len(url_list) - 1:
            time.sleep(REQUEST_DELAY)

    # HEY CLAUDE: Remember the Windows encoding crash on file write?
    # MISTAKE: open(file, 'w') without encoding crashed on URLs with non-ASCII
    # RULE: Always encoding='utf-8' for file writes in this project
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(link + '\n')

    log.info(f'Saved {len(all_links)} links to {output_file}')
    return all_links


if __name__ == '__main__':
    urls = [
        'https://example.com',
        'https://example.org',
    ]
    results = scrape_batch(urls, 'links.txt')
    print(f'Total links found: {len(results)}')
