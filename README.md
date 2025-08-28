# Smart Librarian

Proiect demonstrativ: Chatbot AI cu RAG (ChromaDB) + tool pentru rezumate detaliate.

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
