import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parse_epub import parse_epub
from chunker import chunk_chapters


def test_parse_epub(debug=True):
    chapters = parse_epub("sample_books/test.epub")
    if debug:
        print(f"Parsed {len(chapters)} chapters/sections")
    for c in chapters[:3]:
        print(f"\n--- {c['title']} (order {c['order']}) ---")
        if debug:
            print(c["text"][:300])


def test_chunker(debug=True):
    chapters = parse_epub("sample_books/test.epub")
    chunks = chunk_chapters(chapters)
    if debug:
        print(f"Created {len(chunks)} chunks from {len(chapters)} chapters")
        print("\nSample chunk:")
        print(chunks[0])


def run_all_tests():
    debug = False
    test_parse_epub(debug)
    test_chunker(debug)


if __name__ == "__main__":
    run_all_tests()

