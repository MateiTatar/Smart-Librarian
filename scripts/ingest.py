# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.config import Settings
import sys

# Load .env explicitly from repository root (two levels up from this script)
BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / '.env'
loaded = load_dotenv(dotenv_path=DOTENV_PATH)

# Ensure the repository root is on sys.path so imports like `from data...` work
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Try to read OPENAI_API_KEY from environment (load_dotenv should set it).
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Fallback: if dotenv didn't populate the env var but the .env file exists,
# parse it manually and set os.environ. This handles encoding or parsing
# edge-cases on some Windows setups.
if not OPENAI_API_KEY and DOTENV_PATH.exists():
    try:
        raw = DOTENV_PATH.read_text(encoding='utf-8')
    except Exception:
        # fallback to a more permissive encoding if UTF-8 fails
        raw = DOTENV_PATH.read_text(encoding='latin-1')
    for ln in raw.splitlines():
        # strip common whitespace, then remove BOM or zero-width chars that
        # can make the line start with invisible characters on Windows
        line = ln.strip()
        if not line or line.startswith('#'):
            continue
        # remove possible BOM/ZWSP characters
        line = line.lstrip('\ufeff\u200b')
        if '=' not in line:
            continue
        key, val = line.split('=', 1)
        if key.strip().upper() != 'OPENAI_API_KEY':
            continue
        val = val.strip().strip('"\'')
        # sanitize value from stray control chars
        try:
            val = val.encode('utf-8', 'ignore').decode('utf-8', 'ignore').strip()
        except Exception:
            val = val.strip()
        if val:
            os.environ['OPENAI_API_KEY'] = val
            OPENAI_API_KEY = val
        break
CHROMA_DB_DIR = os.getenv('CHROMA_DB_DIR', './chroma_db')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'book_summaries')

if not OPENAI_API_KEY:
    # helpful diagnostic
    exists = DOTENV_PATH.exists()
    raise RuntimeError(
        f"OPENAI_API_KEY not set in environment. Checked .env at: {DOTENV_PATH} (exists={exists}). "
        "Copy .env.example -> .env and add your key, or run scripts/set_api_key.ps1"
    )

openai = OpenAI(api_key=OPENAI_API_KEY)
client = chromadb.Client(Settings(persist_directory=CHROMA_DB_DIR, anonymized_telemetry=False))

from data.book_summaries_dict import book_summaries_dict


def build_documents():
    docs = []
    ids = []
    metadatas = []
    for title, summary in book_summaries_dict.items():
        docs.append(summary)
        ids.append(title)
        metadatas.append({'title': title})
    return docs, ids, metadatas


def ingest():
    docs, ids, metadatas = build_documents()
    # compute embeddings with OpenAI
    embeddings = []
    for d in docs:
        try:
            r = openai.embeddings.create(model=EMBEDDING_MODEL, input=d)
            embeddings.append(r.data[0].embedding)
        except Exception as e:
            msg = str(e)
            # common sign of an invalid key from OpenAI
            if 'Incorrect API key' in msg or 'invalid_api_key' in msg or '401' in msg:
                raise RuntimeError(
                    "OpenAI authentication failed: the API key in .env appears invalid or revoked.\n"
                    "Please create a valid API key at https://platform.openai.com/account/api-keys,\n"
                    "then run scripts/set_api_key.ps1 again (or edit .env), and re-run this script.\n"
                    "Do NOT paste the key in chat."
                ) from e
            raise
    # create collection and add
    collection = client.get_or_create_collection(COLLECTION_NAME)
    collection.add(documents=docs, embeddings=embeddings, ids=ids, metadatas=metadatas)
    print('Ingest complet. Documente adăugate:', len(docs))


if __name__ == '__main__':
    ingest()
