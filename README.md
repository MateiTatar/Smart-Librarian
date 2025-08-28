# Smart Librarian

Proiectul oferă un prototip RAG (ChromaDB + OpenAI embeddings) cu un fallback OFFLINE (TF‑IDF) pentru testare locală fără cheie API.

## 1) Presupuneri
- Python 3.10+ (recomandat 3.11/3.12)
- Un virtualenv în `./.venv` (ex: `python -m venv .venv`)

## 2) Instalare dependențe
Activează mediul virtual și instalează dependențele:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

Note: `scikit-learn` este folosit pentru modul offline (TF‑IDF).

## 3) Test rapid OFFLINE (fără cheia OpenAI)
Acesta e fluxul recomandat pentru a verifica funcționalitatea fără a avea cheia OpenAI:

```powershell
# pornește CLI în offline mode
python .\app_cli.py --offline
# sau rulează test non-interactiv
& ".\.venv\Scripts\python.exe" .\scripts\run_offline_test.py
```

Veți primi recomandări bazate pe TF‑IDF și scoruri (title + similarity score).

## 4) Cum folosești ONLINE (cu OpenAI + ChromaDB)
1. Creează o cheie API în OpenAI: https://platform.openai.com/account/api-keys
2. Rulează helper-ul PowerShell (scrie `.env` în repo root):

```powershell
.\scripts\set_api_key.ps1
```

3. Populează (ingest) ChromaDB cu embeddings:

```powershell
python .\scripts\ingest.py
```

4. Rulează CLI (online):

```powershell
python .\app_cli.py
```

5. Sau pornește Streamlit UI:

```powershell
& ".\.venv\Scripts\streamlit.exe" run .\app_streamlit.py
```

## 5) Notes and troubleshooting
- Dacă `scripts/ingest.py` spune că `OPENAI_API_KEY not set`, verifică `.env` în root și asigură-te că rulezi scriptul cu același shell/venv în care ai creat `.env`.
- Dacă OpenAI returnează 401 — cheia este invalidă/expirată: regenerează/rotește cheia în dashboard-ul OpenAI.
- Nu posta cheia în chat sau în issue tracker; folosește `scripts/set_api_key.ps1` pentru a o salva local.

## 6) Fișiere utile
- `data/book_summaries.md` — dataset uman citibil
- `data/book_summaries_dict.py` — dict folosit de tool
- `scripts/ingest.py` — upload embeddings -> ChromaDB (necesită OpenAI key)
- `scripts/run_offline_test.py` — rulează câteva interogări TF‑IDF (non-interactive demo)
- `app_cli.py` — CLI (folosește `--offline` pentru TF‑IDF)
- `app_streamlit.py` — interfață Streamlit
- `smart_librarian/rag.py` — retriever online + factory
- `smart_librarian/offline.py` — retriever TF‑IDF offline

## 7) Securitate
- Dacă ai pus cheia în chat, rotește/regenerează cheia imediat în OpenAI dashboard.

## 8) Commit și workflow

```powershell
# verifică starea
git status
# adaugă modificările
git add README.md
# commit
git commit -m "docs: add README with offline/online quickstart and commands"
# push
git push origin main
```

Structură:
- CLI: app_cli.py
- Streamlit UI: app_streamlit.py (opțional)
- Ingest: scripts/ingest.py
- Module: smart_librarian/

Instrucțiuni rapide:
1. Copiați .env.example -> .env și completați OPENAI_API_KEY
2. pip install -r requirements.txt
3. python scripts/ingest.py # pentru a popula ChromaDB
4. python app_cli.py # pentru a rula CLI

Exemple de întrebări:
- Vreau o carte despre prietenie și magie
- Ce recomanzi pentru cineva care iubește povești de război?
- Ce este 1984?
