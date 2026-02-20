# before.py - Code WITHOUT inline learning
# AI makes the same mistakes repeatedly with no persistent warnings

import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    # No timeout - hangs on slow or dead servers
    response = requests.get(url)

    # No status check - silently processes error pages as valid content
    soup = BeautifulSoup(response.content, 'html.parser')

    # No None check - crashes when href is missing
    links = [a.get('href') for a in soup.find_all('a')]

    return links


def save_results(links, filename):
    # No encoding specified - crashes on non-ASCII content on Windows
    with open(filename, 'w') as f:
        for link in links:
            # No None filter - writes "None" into the file silently
            f.write(link + '\n')


if __name__ == '__main__':
    results = fetch_page('https://example.com')
    save_results(results, 'output.txt')
    print('Done.')
