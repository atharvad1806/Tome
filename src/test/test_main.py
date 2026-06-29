import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parse_epub import *


def test_parse_epub():
    import sys
    chapters = parse_epub("sample_books/test.epub")
    print(f"Parsed {len(chapters)} chapters/sections")
    for c in chapters[:3]:
        print(f"\n--- {c['title']} (order {c['order']}) ---")
        print(c["text"][:300])


def run_all_tests():
    test_parse_epub()


if __name__ == "__main__":
    run_all_tests()

