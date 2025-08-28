# -*- coding: utf-8 -*-
import streamlit as st
from smart_librarian.utils import load_env, tts_save, generate_cover
from smart_librarian.tools import get_summary_by_title
from smart_librarian.filters import is_clean_text

# Lazy imports for heavy retriever dependencies

# Load configuration
cfg = load_env()
retriever = None


st.set_page_config(page_title="Smart Librarian", page_icon="📚")
st.title("📚 Smart Librarian – RAG + Tool")


with st.sidebar:
    st.header("Setări")
    mode_online = st.checkbox("Folosește modul ONLINE (Chroma + OpenAI)", value=False)
    generate_img = st.checkbox("Generează imagine (opțional)", value=False)
    speak = st.checkbox("Text to Speech (salvează audio, opțional)", value=False)


q = st.text_input("Întreabă (ex: Vreau o carte despre prietenie și magie)")


if st.button("Recomandă") and q:
    if not is_clean_text(q):
        st.warning("Mesajul conține limbaj nepotrivit. Vă rugăm să reformulezi.")
    else:
        # lazy build retriever depending on mode
        if mode_online:
            try:
                from smart_librarian.rag import build_retriever
                cfg = load_env()
                top_k = int(cfg.get('TOP_K', 3))
                retriever = build_retriever(use_offline=False, top_k=top_k)
            except Exception as e:
                st.warning("Nu am putut inițializa modul ONLINE. Folosiți OFFLINE în schimb.")
                from smart_librarian.offline import OfflineRAG
                from data.book_summaries_dict import book_summaries_dict
                retriever = OfflineRAG(summaries=book_summaries_dict, top_k=3)
        else:
            from smart_librarian.offline import OfflineRAG
            from data.book_summaries_dict import book_summaries_dict
            retriever = OfflineRAG(summaries=book_summaries_dict, top_k=3)

        results = retriever.retrieve(q)
        if not results:
            st.info("Nu am găsit o carte potrivită. Încearcă din nou.")
        else:
            # results may be list of (title, score) or list of titles
            if isinstance(results[0], tuple):
                st.write("Recomandări:")
                for t, s in results:
                    st.write(f" - {t} (score={s:.3f})")
                # allow user to pick one
                choice = st.selectbox("Alege o carte pentru detalii", [t for t, _ in results])
                title = choice
            else:
                title = results[0]

            st.subheader(f"Recomandare: {title}")
            summary = get_summary_by_title(title)
            if summary:
                st.write(summary)
            else:
                st.write("Rezumat detaliat indisponibil pentru acest titlu.")

            if generate_img:
                img_path = generate_cover(f"Cover for {title}", title.replace(' ', '_').lower())
                if img_path:
                    st.image(img_path, caption=title)

            if speak and summary:
                audio_path = tts_save(summary, basename=title.replace(' ', '_').lower())
                if audio_path:
                    st.audio(audio_path)
                else:
                    st.info("Text-to-speech nu este disponibil în această instalație.")