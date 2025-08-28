import os
from pathlib import Path
import traceback

ROOT = Path(__file__).resolve().parent.parent
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from smart_librarian.utils import load_env


def mask_key(k: str) -> str:
    if not k:
        return '<NOT SET>'
    if len(k) <= 12:
        return k
    return k[:6] + '...' + k[-6:]


def main():
    print('Checking .env and OpenAI/Chroma connectivity...')
    cfg = load_env()
    env_key = os.getenv('OPENAI_API_KEY')
    cfg_key = cfg.get('OPENAI_API_KEY')
    print('OPENAI_API_KEY in config:', mask_key(cfg_key))
    print('OPENAI_API_KEY in os.environ:', mask_key(env_key))

    # Try to call OpenAI embeddings
    try:
        from openai import OpenAI
    except Exception as e:
        print('openai package not available:', e)
        return

    try:
        # prefer passing key explicitly from cfg to be deterministic
        client = OpenAI(api_key=cfg_key)
        resp = client.embeddings.create(model='text-embedding-3-small', input='test')
        print('OpenAI embeddings OK — received vector length:', len(resp.data[0].embedding))
    except Exception as e:
        print('OpenAI call failed:')
        traceback.print_exc()

    # Try Chroma
    try:
        import chromadb
        from chromadb.config import Settings
    except Exception as e:
        print('chromadb package not available:', e)
        return

    chroma_dir = cfg.get('CHROMA_DB_DIR') or './chroma_db'
    try:
        client = chromadb.Client(Settings(persist_directory=chroma_dir, anonymized_telemetry=False))
        coll = client.get_or_create_collection(cfg.get('COLLECTION_NAME', 'book_summaries'))
        print('Chroma DB OK — collection name:', coll.name if hasattr(coll, 'name') else '(unnamed)')
    except Exception:
        print('Chroma client failed:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
