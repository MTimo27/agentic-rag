from typing import List

def chunk_text(text: str, chunk_size: int = 5000) -> List[str]:
    """
    Split text into chunks, respecting code blocks and paragraphs.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end >= text_length:
            chunks.append(text[start:].strip())
            break

        chunk = text[start:end]
        code_block = chunk.rfind('```')
        if code_block != -1 and code_block > int(chunk_size * 0.3):
            end = start + code_block

        elif '\n\n' in chunk:
            last_break = chunk.rfind('\n\n')
            if last_break > int(chunk_size * 0.3):
                end = start + last_break

        elif '. ' in chunk:
            last_period = chunk.rfind('. ')
            if last_period > int(chunk_size * 0.3):
                end = start + last_period + 1

        segment = text[start:end].strip()
        if segment:
            chunks.append(segment)

        start = max(start + 1, end)

    return chunks