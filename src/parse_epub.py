from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re


def parse_epub(filepath: str) -> list[dict]:
    book = epub.read_epub(f"sample_books/{filepath}")

    # Step 1: concatenate all document text in file order, with markers
    # we can split on later. We keep paragraph-level granularity by
    # joining each text node with a newline so heading-like lines stay
    # on their own line.
    full_text_parts = []

    for item in book.get_items():
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        # get_text with "\n" separator here is intentional --
        # we WANT line breaks to detect heading-like lines below
        text = soup.get_text(separator="\n")
        full_text_parts.append(text)

    full_text = "\n".join(full_text_parts)

    # Step 2: clean up whitespace, but preserve line breaks (not collapsing
    # everything to one line, unlike our earlier single-line fix)
    lines = [line.strip() for line in full_text.split("\n")]
    lines = [line for line in lines if line]  # drop empty lines

    # Step 3: detect chapter-heading-like lines.
    # Heuristics: short line, AND matches one of:
    #   - "Chapter <number/word>"
    #   - a lone Roman numeral (I, II, III, IV...)
    #   - a lone Arabic number
    heading_pattern = re.compile(
        r'^(chapter\s+\w+|[IVXLCDM]+|\d+)$',
        re.IGNORECASE
    )

    chapters = []
    current_title = "Introduction"
    current_lines = []
    order = 0

    def flush_chapter():
        nonlocal order
        text = " ".join(current_lines)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) >= 50:
            chapters.append({
                "title": current_title,
                "text": text,
                "order": order,
            })
            order += 1

    for line in lines:
        if heading_pattern.match(line) and len(line) < 30:
            flush_chapter()
            current_title = line
            current_lines = []
        else:
            current_lines.append(line)

    flush_chapter()  # don't forget the last chapter

    return chapters