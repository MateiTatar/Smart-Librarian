import openai
import os
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Folosește modelul text-embedding-3-small
EMBEDDING_MODEL = "text-embedding-3-small"

def get_embedding(text: str) -> List[float]:
    response = openai_client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding
