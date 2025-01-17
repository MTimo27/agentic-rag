import asyncio
from crawler import get_pydantic_ai_docs_urls, crawl_parallel

async def main():
    urls = get_pydantic_ai_docs_urls()
    if not urls:
        print("No URLs found to crawl")
        return
    print(f"Found {len(urls)} URLs to crawl")
    await crawl_parallel(urls)

if __name__ == "__main__":
    asyncio.run(main())
