import os
from typing import List, Tuple, Optional
# openai and chromadb imported lazily inside the online Retriever to avoid import-time
# hard dependency for offline-only usage.
OpenAI = None
chromadb = None
Settings = None

from smart_librarian.utils import load_env

# Optional scikit-learn imports for offline TF-IDF retriever
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

cfg = load_env()
OPENAI_API_KEY = cfg.get('OPENAI_API_KEY')
CHROMA_DB_DIR = cfg.get('CHROMA_DB_DIR')
EMBEDDING_MODEL = cfg.get('EMBEDDING_MODEL')
COLLECTION_NAME = cfg.get('COLLECTION_NAME')


class Retriever:
    """Online Retriever using OpenAI embeddings + ChromaDB."""
    def __init__(self, top_k: int = 3):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set — online retriever requires a key")
    # Lazy import to avoid requiring openai/chromadb for offline mode
    from openai import OpenAI as _OpenAI
    import chromadb as _chromadb
    from chromadb.config import Settings as _Settings
    self.openai = _OpenAI(api_key=OPENAI_API_KEY)
    self.client = _chromadb.Client(_Settings(persist_directory=CHROMA_DB_DIR, anonymized_telemetry=False))
    self.collection = self.client.get_or_create_collection(COLLECTION_NAME)
    self.top_k = top_k

    def embed(self, text: str) -> List[float]:
        r = self.openai.embeddings.create(model=EMBEDDING_MODEL, input=text)
        return r.data[0].embedding

    def retrieve(self, query: str):
        emb = self.embed(query)
        results = self.collection.query(query_embeddings=[emb], n_results=self.top_k)
        # return list of metadata titles
        titles = []
        for md_list in results.get('metadatas', []):
            for md in md_list:
                titles.append(md.get('title'))
        return titles


class OfflineRAG:
    """Simple TF-IDF based retriever for offline testing.

    retrieve(query) -> List[Tuple[title, score]]
    """
    def __init__(self, summaries: dict, top_k: int = 3):
        if not SKLEARN_AVAILABLE:
            raise RuntimeError("scikit-learn is required for offline mode. Install requirements.txt")
        self.titles = list(summaries.keys())
        self.docs = [summaries[t] for t in self.titles]
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.doc_matrix = self.vectorizer.fit_transform(self.docs)
        self.top_k = top_k

    def retrieve(self, query: str):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.doc_matrix).flatten()
        idxs = sims.argsort()[::-1][: self.top_k]
        return [(self.titles[i], float(sims[i])) for i in idxs]


def build_retriever(use_offline: bool = False, summaries: Optional[dict] = None, top_k: int = 3):
    """Factory: returns OfflineRAG when use_offline=True, otherwise online Retriever."""
    if use_offline:
        if summaries is None:
            raise ValueError("summaries dict required for offline retriever")
        return OfflineRAG(summaries=summaries, top_k=top_k)
    return Retriever(top_k=top_k)
