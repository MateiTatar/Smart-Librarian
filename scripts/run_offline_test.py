import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.book_summaries_dict import book_summaries_dict
from smart_librarian.offline import OfflineRAG

queries = [
    "carte despre prietenie si magie",
    "ficțiune istorică despre război",
    "dezvoltare personală și obiceiuri"
]

retriever = OfflineRAG(summaries=book_summaries_dict, top_k=3)

for q in queries:
    print(f"\nQuery: {q}")
    res = retriever.retrieve(q)
    for title, score in res:
        print(f" - {title} (score={score:.4f})")
