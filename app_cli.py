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
    # If user asked for offline, or if no API key is set, use offline fallback
    if args.offline:
        from smart_librarian.offline import OfflineRAG
        retriever = OfflineRAG(summaries=book_summaries_dict, top_k=top_k)
        print("Pornit în modul OFFLINE (TF-IDF). Scrie 'exit' pentru a închide.")
    else:
        # try to build online retriever; if that fails because API key is missing,
        # automatically fall back to offline mode with a clear message.
        try:
            from smart_librarian.rag import build_retriever
            retriever = build_retriever(use_offline=False, top_k=top_k)
            print("Pornit în modul ONLINE (Chroma + OpenAI). Scrie 'exit' pentru a închide.")
        except Exception as e:
            print("\n[WARN] Nu am putut porni modul ONLINE (cheie OpenAI lipsă sau invalidă).\n"
                  "Folosesc fallback OFFLINE (TF-IDF).\n")
            from smart_librarian.offline import OfflineRAG
            retriever = OfflineRAG(summaries=book_summaries_dict, top_k=top_k)

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
        # results may be list of (title, score) or list of titles
        chosen_title = None
        if results:
            if isinstance(results[0], tuple):
                # pick top by score
                results_sorted = sorted(results, key=lambda x: x[1], reverse=True)
                chosen_title = results_sorted[0][0]
                print("\nRecomandări (online):")
                for t, s in results_sorted:
                    print(f" - {t} (score={s:.3f})")
            else:
                chosen_title = results[0]

        # fallback: if no chosen_title from retriever, try substring match in Chroma metadata (online only)
        if not chosen_title and not args.offline:
            try:
                # lazy import chroma client
                from smart_librarian.rag import CHROMA_DB_DIR, COLLECTION_NAME
                import chromadb
                from chromadb.config import Settings
                client = chromadb.Client(Settings(persist_directory=CHROMA_DB_DIR, anonymized_telemetry=False))
                coll = client.get_or_create_collection(COLLECTION_NAME)
                # naive metadata search via stored metadatas
                # fetch all ids/metadata and do substring match
                all_meta = coll.get(include=['metadatas', 'ids'])
                matched = []
                for md_list, id_list in zip(all_meta.get('metadatas', []), all_meta.get('ids', [])):
                    for md, idv in zip(md_list, id_list):
                        title = md.get('title')
                        if title and q.lower() in title.lower():
                            matched.append((title, 1.0))
                if matched:
                    chosen_title = matched[0][0]
                    print('\nFallback metadate match:')
                    for t, s in matched:
                        print(f" - {t}")
            except Exception:
                # ignore fallback errors and continue to offline message
                chosen_title = None

        if chosen_title:
            print(f"\nRecomandare: {chosen_title}\n")
            summary = get_summary_by_title(chosen_title)
            if summary:
                print("Rezumat detaliat:\n", summary)
            else:
                print("Rezumat detaliat indisponibil pentru acest titlu.")
        else:
            # final fallback: local token-overlap ranking against book_summaries_dict
            try:
                from data.book_summaries_dict import book_summaries_dict as local_summaries
                q_tokens = set(q.lower().split())
                scores = []
                for t, s in local_summaries.items():
                    t_tokens = set(t.lower().split())
                    overlap = len(q_tokens & t_tokens)
                    if overlap > 0:
                        scores.append((t, float(overlap)))
                if scores:
                    scores.sort(key=lambda x: x[1], reverse=True)
                    chosen_title = scores[0][0]
                    print(f"\nFallback local: {chosen_title}\n")
                    summary = get_summary_by_title(chosen_title)
                    if summary:
                        print("Rezumat detaliat:\n", summary)
                    else:
                        print("Rezumat detaliat indisponibil pentru acest titlu.")
                else:
                    print("Nu am găsit o carte potrivită. Încearcă să reformulezi.")
            except Exception:
                print("Nu am găsit o carte potrivită. Încearcă să reformulezi.")


if __name__ == '__main__':
    main()