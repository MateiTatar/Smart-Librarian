import os
from modules.db_utils import get_chroma_client
from modules.embeddings import get_embedding
from modules.tools import get_summary_by_title
import openai

# Pentru interfață CLI

def search_books(query: str):
    client = get_chroma_client()
    collection = client.get_or_create_collection('book_summaries')
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    if results['ids'] and results['metadatas']:
        title = results['metadatas'][0][0]['title']
        return title
    return None

def chat():
    print("Bine ai venit la Smart Librarian! Scrie ce tip de carte cauți.")
    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ["exit", "quit", "iesire"]:
            print("La revedere!")
            break
        # (Opțional) Filtru limbaj nepotrivit
        # ...
        title = search_books(user_input)
        if title:
            print(f"\nRecomandare: {title}")
            summary = get_summary_by_title(title)
            print(f"Rezumat detaliat: {summary}")
        else:
            print("Nu am găsit o recomandare potrivită. Încearcă să reformulezi întrebarea.")

if __name__ == "__main__":
    chat()
