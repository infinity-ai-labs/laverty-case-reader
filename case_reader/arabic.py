"""Arabic text helpers: digits, letter forms and diacritics."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
# Short vowels and other diacritics, Quranic marks, and the tatweel (ـ).
_MARKS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_ALEF = re.compile(r"[أإآٱ]")
_NOT_WORD = re.compile(r"[^\w\s]")
_SPACES = re.compile(r"\s+")


def to_ascii_digits(text: str) -> str:
    """Turn Arabic-Indic digits (٠-٩, ۰-۹) into 0-9."""
    return (text or "").translate(_DIGITS)


def normalize(text: str, *, keep_punctuation: bool = False) -> str:
    """Normalise Arabic (and English) text so the same words compare equal.

    Removes diacritics and the tatweel, unifies alef, yaa, taa marbuta, hamza
    carriers and digits, drops punctuation, folds case and collapses spaces.
    """
    s = unicodedata.normalize("NFKC", text or "")
    s = to_ascii_digits(s)
    s = _MARKS.sub("", s)
    s = _ALEF.sub("ا", s)
    s = s.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    if not keep_punctuation:
        s = _NOT_WORD.sub(" ", s.replace("_", " "))
    return _SPACES.sub(" ", s).strip().casefold()


def similarity(a: str, b: str) -> float:
    """Similarity of two names or phrases after normalisation, from 0 to 1."""
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    whole = SequenceMatcher(None, na, nb).ratio()
    # Word order can differ ("شركة X ذ.م.م" / "X ذ م م شركة"); compare sorted words too.
    words = SequenceMatcher(None, " ".join(sorted(na.split())), " ".join(sorted(nb.split()))).ratio()
    return max(whole, words)


def compare_quote(quote: str, official: str) -> tuple[float, list[dict[str, str]]]:
    """Compare a quoted passage with the official text, word by word.

    Returns (similarity from 0 to 1, the differing words). The similarity is 1.0
    only when the quote appears word for word in the official text (after
    normalising letter forms and diacritics); any changed word lowers it and is
    listed, because one word ("agreed" rate or "legal" rate) can change the law.
    """
    q_words = normalize(quote).split()
    o_words = normalize(official).split()
    if not q_words or not o_words:
        return 0.0, []
    if f" {' '.join(q_words)} " in f" {' '.join(o_words)} ":
        return 1.0, []
    best_ratio, best_window = 0.0, o_words[: len(q_words)]
    for size in range(max(1, len(q_words) - 3), len(q_words) + 4):
        for start in range(0, max(1, len(o_words) - size + 1)):
            window = o_words[start:start + size]
            ratio = SequenceMatcher(None, q_words, window, autojunk=False).ratio()
            if ratio > best_ratio:
                best_ratio, best_window = ratio, window
    differences = []
    matcher = SequenceMatcher(None, q_words, best_window, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            differences.append({"in_file": " ".join(q_words[i1:i2]), "official": " ".join(best_window[j1:j2])})
    return min(best_ratio, 0.999), differences


def best_window_ratio(needle: str, haystack: str) -> float:
    """How closely `needle` matches the best run of words in `haystack` (0 to 1)."""
    return compare_quote(needle, haystack)[0]
