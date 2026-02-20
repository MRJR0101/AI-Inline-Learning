# patterns/python/web_scraping.py
# Copy-paste ready inline learning warnings for web scraping mistakes
# Add these at the exact lines where scraping decisions happen

# -------------------------------------------------------------------
# REQUEST TIMEOUT
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the hanging script on dead servers?
# MISTAKE: requests.get(url) with no timeout - hung 25 minutes on dead server
# LESSON: Some servers never respond - script waits forever
# RULE: ALWAYS set timeout=10 for all requests.get() calls in this project
#
# PATTERN:
# response = requests.get(url, timeout=10, headers=HEADERS)


# -------------------------------------------------------------------
# USER AGENT
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the 40% block rate from missing User-Agent?
# MISTAKE: Used default Python requests User-Agent - blocked by most sites
# LESSON: Sites actively filter requests by User-Agent to block scrapers
# RULE: Always define HEADERS with realistic browser User-Agent at module level
#
# PATTERN:
# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# }
# response = requests.get(url, timeout=10, headers=HEADERS)


# -------------------------------------------------------------------
# RATE LIMITING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember the IP ban from UltimateScraper in November 2024?
# MISTAKE: Scraped 500 pages in 2 minutes - IP banned for 48 hours
# LESSON: Sites monitor request frequency and block aggressive crawlers
# RULE: Always sleep 1-2 seconds between requests. Never remove the delay.
# CONTEXT: Being banned is far more expensive than being 35% slower
#
# PATTERN:
# import time
# for url in url_list:
#     result = scrape_links(url)
#     time.sleep(1.5)  # rate limit - do not remove


# -------------------------------------------------------------------
# HTTP ERROR HANDLING
# -------------------------------------------------------------------

# HEY CLAUDE: Remember processing 404 pages as valid content?
# MISTAKE: Did not call raise_for_status() - silently processed error pages
# LESSON: requests does not raise exceptions on 4xx/5xx status codes by default
# RULE: Always call response.raise_for_status() immediately after requests.get()
#
# PATTERN:
# response = requests.get(url, timeout=10, headers=HEADERS)
# response.raise_for_status()


# -------------------------------------------------------------------
# NONE VALUES IN LINK LISTS
# -------------------------------------------------------------------

# HEY CLAUDE: Remember None values crashing downstream processing?
# MISTAKE: soup.find_all('a') includes tags without href - returns None
# LESSON: Not all <a> tags have href attributes (JS handlers, anchors, etc.)
# RULE: Always filter None: [a.get('href') for a if a.get('href')]
#
# PATTERN:
# links = [
#     a.get('href')
#     for a in soup.find_all('a')
#     if a.get('href') and not a.get('href').startswith('#')
# ]


# -------------------------------------------------------------------
# ROBOTS.TXT COMPLIANCE
# -------------------------------------------------------------------

# HEY CLAUDE: Remember scraping paths disallowed by robots.txt?
# MISTAKE: Scraped /admin/ and /private/ paths that were disallowed
# LESSON: Violating robots.txt gets IPs banned and is ethically wrong
# RULE: Check robots.txt before scraping any new domain in this project
#
# PATTERN:
# from urllib.robotparser import RobotFileParser
# rp = RobotFileParser()
# rp.set_url('https://example.com/robots.txt')
# rp.read()
# if rp.can_fetch('*', url):
#     response = requests.get(url, timeout=10, headers=HEADERS)
