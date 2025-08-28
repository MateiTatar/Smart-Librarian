# -*- coding: utf-8 -*-
import streamlit as st
from smart_librarian.utils import load_env, tts_save, generate_cover
from smart_librarian.rag import Retriever
from smart_librarian.tools import get_summary_by_title
from smart_librarian.filters import is_clean_text


# Load configuration
cfg = load_env()
retriever = Retriever(top_k=cfg.get('TOP_K', 3))


st.set_page_config(page_title="Smart Librarian", page_icon="📚")
st.title("📚 Smart Librarian – RAG + Tool")


with st.sidebar:
    st.header("Setări")
    generate_img = st.checkbox("Generează imagine (opțional)", value=False)
    speak = st.checkbox("Text to Speech (salvează audio, opțional)", value=False)


q = st.text_input("Întreabă (ex: Vreau o carte despre prietenie și magie)")


if st.button("Recomandă") and q:
    if not is_clean_text(q):
        st.warning("Mesajul conține limbaj nepotrivit. Vă rugăm să reformulați.")
    else:
        titles = retriever.retrieve(q)
        if not titles:
            st.info("Nu am găsit o carte potrivită. Încearcă din nou.")
        else:
            title = titles[0]
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