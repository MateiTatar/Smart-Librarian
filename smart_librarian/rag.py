import os
from typing import List
from openai import OpenAI
import chromadb
from chromadb.config import Settings

from smart_librarian.utils import load_env

cfg = load_env()
OPENAI_API_KEY = cfg['OPENAI_API_KEY']
CHROMA_DB_DIR = cfg['CHROMA_DB_DIR']
EMBEDDING_MODEL = cfg['EMBEDDING_MODEL']
COLLECTION_NAME = cfg['COLLECTION_NAME']

openai = OpenAI(api_key=OPENAI_API_KEY)
client = chromadb.Client(Settings(persist_directory=CHROMA_DB_DIR, anonymized_telemetry=False))


class Retriever:
    def __init__(self, top_k: int = 3):
        self.collection = client.get_or_create_collection(COLLECTION_NAME)
        self.top_k = top_k

    def embed(self, text: str) -> List[float]:
        r = openai.embeddings.create(model=EMBEDDING_MODEL, input=text)
        return r.data[0].embedding

    def retrieve(self, query: str):
        emb = self.embed(query)
        results = self.collection.query(query_embeddings=[emb], n_results=self.top_k)
        # return list of metadata titles
        titles = []
        for md_list in results['metadatas']:
            for md in md_list:
                titles.append(md.get('title'))
        return titles
