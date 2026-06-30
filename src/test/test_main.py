import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv

from parse_epub import parse_epub
from chunker import chunk_chapters
from vector_store import VectorStore

TEST_BOOK = "Animal_Farm_by_George_Orwell.epub"


def test_parse_epub(debug=True):
    print("="*50)
    print("\nPARSE_EPUB() TEST\n")
    print("="*50)
    chapters = parse_epub(TEST_BOOK)
    if debug:
        print(f"Parsed {len(chapters)} chapters/sections")
    for c in chapters[:3]:
        print(f"\n--- {c['title']} (order {c['order']}) ---")
        if debug:
            print(c["text"][:300])


def test_chunker(debug=True):
    print("="*50)
    print("\nCHUNK_CHAPTERS() TEST\n")
    print("="*50)
    chapters = parse_epub(TEST_BOOK)
    chunks = chunk_chapters(chapters)
    if debug:
        print(f"Created {len(chunks)} chunks from {len(chapters)} chapters")
        print("\nSample chunk:")
        print(chunks[0])

def test_vector_store(debug=True):
    print("="*50)
    print("\nVECTOR STORE TEST\n")
    print("="*50)
    load_dotenv()
    chapters = parse_epub(TEST_BOOK)
    chunks = chunk_chapters(chapters)
    store = VectorStore()
    if os.path.exists(f"book_data/{TEST_BOOK}_embeddings.npy"):
        print("Loading cached embeddings")
        store.load(TEST_BOOK)
    else:
        store.build(chunks)
        store.save(TEST_BOOK)
    results = store.search("Who is Napoleon?")
    for r in results:
        print(f"[score={r['score']:.3f}] {r['chapter_title']}: {r['text'][:500]}")


def run_all_tests():
    debug = True
    # debug = False
    # test_parse_epub(debug)
    # test_chunker(debug=False)
    test_vector_store(debug)


if __name__ == "__main__":
    run_all_tests()

