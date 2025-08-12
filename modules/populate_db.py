import os
from modules.db_utils import get_chroma_client
from modules.embeddings import get_embedding

BOOKS_FILE = os.path.join(os.path.dirname(__file__), '../book_summaries.txt')


def load_books():
    """Încarcă titlurile și rezumatele scurte din fișierul book_summaries.txt."""
    books = []
    with open(BOOKS_FILE, encoding='utf-8') as f:
        lines = f.readlines()
    title = None
    summary = []
    for line in lines:
        if line.startswith('## Title: '):
            if title and summary:
                books.append({'title': title, 'summary': ' '.join(summary).strip()})
            title = line.replace('## Title: ', '').strip()
            summary = []
        elif line.strip():
            summary.append(line.strip())
    if title and summary:
        books.append({'title': title, 'summary': ' '.join(summary).strip()})
    return books


def populate_chroma():
    """Populează ChromaDB cu embeddings pentru fiecare rezumat."""
    client = get_chroma_client()
    collection = client.get_or_create_collection('book_summaries')
    books = load_books()
    for book in books:
        embedding = get_embedding(book['summary'])
        collection.add(
            documents=[book['summary']],
            embeddings=[embedding],
            metadatas=[{'title': book['title']}],
            ids=[book['title']]
        )
    print('ChromaDB populat cu rezumate de cărți.')

if __name__ == "__main__":
    populate_chroma()
