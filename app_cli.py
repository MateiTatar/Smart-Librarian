# -*- coding: utf-8 -*-
import argparse
from smart_librarian.utils import load_env
from smart_librarian.tools import get_summary_by_title
from smart_librarian.filters import is_clean_text
from data.book_summaries_dict import book_summaries_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true', help='Use offline TF-IDF retriever (no OpenAI key needed)')
    args = parser.parse_args()
    cfg = load_env()
    top_k = int(cfg.get('TOP_K', 3))
    if args.offline:
        from smart_librarian.offline import OfflineRAG
        retriever = OfflineRAG(summaries=book_summaries_dict, top_k=top_k)
        print("Pornit în modul OFFLINE (TF-IDF). Scrie 'exit' pentru a închide.")
    else:
        from smart_librarian.rag import build_retriever
        retriever = build_retriever(use_offline=False, top_k=top_k)
        print("Pornit în modul ONLINE (Chroma + OpenAI). Scrie 'exit' pentru a închide.")

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
        results = retriever.retrieve(q)
        # offline retriever returns (title, score) tuples; online returns list of titles
        if results:
            if isinstance(results[0], tuple):
                title = results[0][0]
            else:
                title = results[0]
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