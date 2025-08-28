# -*- coding: utf-8 -*-
from smart_librarian.utils import load_env
from smart_librarian.rag import Retriever
from smart_librarian.tools import get_summary_by_title
from smart_librarian.filters import is_clean_text


def main():
    cfg = load_env()
    retriever = Retriever(top_k=cfg.get('TOP_K', 3))
    print("Bine ai venit la Smart Librarian CLI. Scrie 'exit' pentru a închide.")
    while True:
        q = input("Tu: ")
        if not q:
            continue
        if q.lower() in ("exit", "quit", "iesire"):
            print("La revedere!")
            break
        if not is_clean_text(q):
            print("Mesajul conține limbaj nepotrivit. Vă rugăm să reformulați.")
            continue
        titles = retriever.retrieve(q)
        if titles:
            title = titles[0]
            print(f"\nRecomandare: {title}\n")
            summary = get_summary_by_title(title)
            if summary:
                print("Rezumat detaliat:\n", summary)
            else:
                print("Rezumat detaliat indisponibil pentru acest titlu.")
        else:
            print("Nu am găsit o carte potrivită. Încearcă să reformulezi.")


if __name__ == '__main__':
    main()