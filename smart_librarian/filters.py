# -*- coding: utf-8 -*-
import re


# listă minimală (poți extinde după nevoie)
BAD_WORDS = [
    r"\bidiot\b", r"\bprost\b", r"\bdu-te dracu\b", r"\bnaiba\b",
    r"\bfuck\b", r"\bshit\b", r"\basshole\b", r"\bbitch\b",
]

BAD_RE = re.compile("|".join(BAD_WORDS), flags=re.IGNORECASE)


def is_clean_text(text: str) -> bool:
    """Returnează True dacă textul nu conține cuvinte din lista neadecvată."""
    return not bool(BAD_RE.search(text or ""))