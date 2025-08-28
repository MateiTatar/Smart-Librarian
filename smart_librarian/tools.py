# -*- coding: utf-8 -*-
from typing import Optional
from data.book_summaries_dict import book_summaries_dict


def get_summary_by_title(title: str) -> Optional[str]:
    """Returnează rezumatul complet pentru un titlu exact (case-insensitive fallback).

    Returnează None dacă titlul nu este găsit.
    """
    if title in book_summaries_dict:
        return book_summaries_dict[title]
    # fallback case-insensitive
    for k, v in book_summaries_dict.items():
        if k.lower() == title.lower():
            return v
    return None


# Spec pentru înregistrarea ca tool (pentru function-calling dacă folosit)
TOOL_SPEC = {
    "name": "get_summary_by_title",
    "description": "Returnează rezumatul complet pentru un titlu exact de carte.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Titlul exact al cărții"}
        },
        "required": ["title"]
    }
}