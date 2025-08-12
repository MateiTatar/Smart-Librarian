import chromadb
from chromadb.config import Settings
from openai import OpenAI
import os

# Configurare ChromaDB
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), '../chroma_db')

client = chromadb.Client(Settings(
    persist_directory=CHROMA_DB_DIR,
    anonymized_telemetry=False
))

def get_chroma_client():
    return client
