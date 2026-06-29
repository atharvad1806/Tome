from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re

def parse_epub(filepath: str) -> list[dict]:
    book = epub.read_epub(filepath)

    chapters = []
    order = 0

    for item in book.get_items():
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        soup = BeautifulSoup(item.get_content(), "html.parser")

        for tag in soup(['script', 'style']):
            tag.decompose()

        text = soup.get_text(separator="\n")
        text = re.sub(r'\n\s*\n+', '\n', text).strip()
        
        if len(text) < 50:
            continue

        title_tag = soup.find(["h1", "h2", "h3"])
        title = title_tag.get_text().strip() if title_tag else f"Section {order + 1}"

        chapters.append({
            "title": title,
            "text": text,
            "order": order,
        })

        order += 1

    return chapters

