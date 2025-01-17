import asyncio
import requests
from xml.etree import ElementTree
from typing import List

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from processor import process_and_store_document

def get_pydantic_ai_docs_urls() -> List[str]:
    """Get URLs from the Pydantic AI docs sitemap."""

    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

async def crawl_parallel(urls: List[str], max_concurrent: int = 5):
    """Crawl multiple URLs in parallel with a concurrency limit."""
    
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_url(url: str):
        async with semaphore:
            result = await crawler.arun(url=url, config=crawl_config, session_id="session1")
            if result.success:
                print(f"Successfully crawled: {url}")
                await process_and_store_document(url, result.markdown_v2.raw_markdown)
            else:
                print(f"Failed crawling: {url} - Error: {result.error_message}")

    try:
        await asyncio.gather(*[process_url(url) for url in urls])
    finally:
        await crawler.close()
