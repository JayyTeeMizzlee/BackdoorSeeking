import sys

# Fix for Twisted/Scrapy reactor mismatch on Python 3.13+
if sys.platform != "win32":
    import asyncio
    from twisted.internet import asyncioreactor
    try:
        asyncioreactor.install()
    except Exception:
        pass  

import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from twisted.internet import reactor, defer

class BasicSpider(scrapy.Spider):
    name = "backdoor_web_scanner"

    def __init__(self, start_url, results, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.results = results

    def parse(self, response):
        self.results["urls"].add(response.url)

        for link in response.css('a::attr(href)').getall():
            full_url = urljoin(response.url, link)
            if full_url not in self.results["urls"]:
                self.results["urls"].add(full_url)
                yield scrapy.Request(full_url, callback=self.parse)

        if any(k in response.url.lower() for k in ['admin', 'login', 'upload', 'cmd', 'shell']):
            self.results["suspicious"].append(response.url)

def run_scrapy_scan(url):
    results = {
        "urls": set(),
        "suspicious": []
    }


    process = CrawlerProcess(settings={
        "LOG_ENABLED": False,
        "DEPTH_LIMIT": 5, # Added for better demonstration | depth is no longer unlimited
        "CLOSESPIDER_PAGECOUNT": 30 # Added for better demonstration | stops after 30 pages
    })

    @defer.inlineCallbacks
    def crawl():
        yield process.crawl(BasicSpider, start_url=url, results=results)
        reactor.stop()

    crawl()
    reactor.run()

    return {
        "urls": list(results["urls"]),
        "suspicious": results["suspicious"]
    }

def run_playwright_scan(url):
    dynamic_urls = set()
    suspicious_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, timeout=10000)
            page.wait_for_timeout(1000)  # Wait for JS to render

            # Anchor tags
            anchors = page.query_selector_all("a")
            for a in anchors:
                href = a.get_attribute("href")
                if href and href.startswith("/"):
                    full_url = urljoin(url, href)
                    dynamic_urls.add(full_url)

                    # Check for suspicious keywords
                    if any(k in href.lower() for k in ['admin', 'login', 'upload', 'cmd', 'shell']):
                        suspicious_paths.append(full_url)

        except Exception as e:
            print(f"[!] Playwright error: {e}")
        finally:
            browser.close()

    return {
        "dynamic_urls": list(dynamic_urls),
        "suspicious": suspicious_paths
    }
