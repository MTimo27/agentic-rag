import asyncio
from datetime import datetime, timezone
from urllib.parse import urlparse
from typing import Dict, Any

from models import ProcessedChunk
from utils import chunk_text
from services.openai_service import get_title_and_summary, get_embedding
from services.supabase_service import insert_data

async def process_chunk(chunk: str, chunk_number: int, url: str) -> ProcessedChunk:
    """Process a single chunk of text."""
    extracted: Dict[str, str] = await get_title_and_summary(chunk, url)
    embedding = await get_embedding(chunk)
    
    metadata: Dict[str, Any] = {
        "source": "pydantic_ai_docs",
        "chunk_size": len(chunk),
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "url_path": urlparse(url).path
    }
    
    return ProcessedChunk(
        url=url,
        chunk_number=chunk_number,
        title=extracted.get('title', ''),
        summary=extracted.get('summary', ''),
        content=chunk,
        metadata=metadata,
        embedding=embedding
    )

async def process_and_store_document(url: str, markdown: str):
    """Process a document by chunking and storing its data in parallel."""
    chunks = chunk_text(markdown)
    tasks = [
        process_chunk(chunk, idx, url)
        for idx, chunk in enumerate(chunks)
    ]
    processed_chunks = await asyncio.gather(*tasks)
    
    # Store processed chunks in parallel
    insert_tasks = [
        asyncio.to_thread(insert_data, "site_pages", {
            "url": chunk.url,
            "chunk_number": chunk.chunk_number,
            "title": chunk.title,
            "summary": chunk.summary,
            "content": chunk.content,
            "metadata": chunk.metadata,
            "embedding": chunk.embedding
        })
        for chunk in processed_chunks
    ]
    await asyncio.gather(*insert_tasks)
