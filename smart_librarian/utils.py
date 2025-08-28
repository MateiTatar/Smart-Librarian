# -*- coding: utf-8 -*-
import os


def _try_load_dotenv(path: str):
    try:
        from dotenv import load_dotenv
        load_dotenv(path)
    except Exception:
        # python-dotenv not available or failed; fallback to environment only
        return


def load_env(env_path: str = None):
    if env_path is None:
        env_path = os.path.join(os.getcwd(), '.env')
    _try_load_dotenv(env_path)
    config = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'CHROMA_DB_DIR': os.getenv('CHROMA_DB_DIR', './chroma_db'),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
        'CHAT_MODEL': os.getenv('CHAT_MODEL', 'gpt-4o-mini'),
        'COLLECTION_NAME': os.getenv('COLLECTION_NAME', 'book_summaries'),
        'TOP_K': int(os.getenv('TOP_K', '3')),
        'LANG': os.getenv('LANG', 'ro')
    }
    return config


# Stubs pentru funcționalități opționale (TTS / Image generation)

def tts_save(text: str, basename: str = 'output') -> str | None:
    """În mod implicit nu produce TTS. Dacă doriți, implementați cu OpenAI TTS
    sau pyttsx3/local TTS. Returnează calea fișierului audio dacă e salvat, altfel None.
    """
    try:
        from pathlib import Path
        out_dir = Path('outputs')
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"{basename}.mp3"
        # implementare fallback simplă: salvează text simplu (nu audio)
        with open(out_path.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write(text)
        return str(out_path)  # note: file is not a real audio but placeholder
    except Exception:
        return None


def generate_cover(prompt: str, basename: str = 'cover') -> str | None:
    """Stub pentru generare imagine. Poate fi implementat cu OpenAI Images sau DALL·E.
    Returnează calea către fișierul generat sau None.
    """
    try:
        from pathlib import Path
        out_dir = Path('outputs')
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"{basename}.png"
        # creează un fișier gol placeholder
        if not out_path.exists():
            out_path.write_bytes(b'')
        return str(out_path)
    except Exception:
        return None
