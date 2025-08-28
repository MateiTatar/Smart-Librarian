from typing import List, Tuple

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


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
