# naive_scraper.py - Web scraper WITHOUT inline learning
# Tested against 1,000 URLs - 230 errors (23% failure rate)

import requests
from bs4 import BeautifulSoup


def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        links.append(href)
    return links


def scrape_batch(url_list, output_file):
    all_links = []
    for url in url_list:
        print(f'Scraping: {url}')
        links = scrape_links(url)
        all_links.extend(links)

    with open(output_file, 'w') as f:
        for link in all_links:
            f.write(str(link) + '\n')

    return all_links


if __name__ == '__main__':
    urls = [
        'https://example.com',
        'https://example.org',
    ]
    results = scrape_batch(urls, 'links.txt')
    print(f'Total links: {len(results)}')
