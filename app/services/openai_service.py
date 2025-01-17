import json
from typing import Dict, List
from config import OPENAI_API_KEY, LLM_MODEL
from openai import AsyncOpenAI

# Initialize the client once
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_title_and_summary(chunk: str, url: str) -> Dict[str, str]:
    """Extract title and summary using GPT-4."""
    system_prompt = (
        "You are an AI that extracts titles and summaries from documentation chunks.\n"
        "Return a JSON object with 'title' and 'summary' keys.\n"
        "For the title: If this seems like the start of a document, extract its title. "
        "If it's a middle chunk, derive a descriptive title.\n"
        "For the summary: Create a concise summary of the main points in this chunk.\n"
        "Keep both title and summary concise but informative."
    )
    
    try:
        response = await openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"URL: {url}\n\nContent:\n{chunk[:1000]}..."}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error getting title and summary: {e}")
        return {"title": "Error processing title", "summary": "Error processing summary"}

async def get_embedding(text: str) -> List[float]:
    """Get embedding vector from OpenAI."""
    try:
        response = await openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        # Adjust the vector size as needed for your embedding model
        return [0] * 1536  # Zero vector on error
