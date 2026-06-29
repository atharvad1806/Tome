

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap
    
    return chunks

def chunk_chapters(chapters: list[dict], chunk_size: int = 800, overlap: int = 150):
    all_chunks = []
    for chapter in chapters:
        chunks = chunk_text(chapter["text"], chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "chapter_title": chapter["title"],
                "chapter_order": chapter["order"],
                "chunk_index": i,
            })
    return all_chunks