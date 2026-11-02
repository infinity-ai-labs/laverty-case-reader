"""The JSON shape Muse Spark fills in for one case file.

Kept flat and non-recursive, every field required, no null types: a missing
value is an empty string, an empty list, 0 or false.
"""

from __future__ import annotations

import re
from typing import Any

SOURCES = ["printed", "stamp", "handwriting", "computed"]
ROLES = [
    "claimant", "defendant", "claimant_lawyer", "defendant_lawyer",
    "claimant_representative", "defendant_representative",
    "judge", "clerk", "notary", "expert", "witness", "other",
]
CASE_TYPES = ["labour", "commercial", "tenancy", "civil", "criminal", "personal_status", "administrative", "other"]
LAW_KINDS = ["federal_decree_law", "federal_law", "local_law", "cabinet_resolution", "other"]
MARK_TYPES = ["stamp", "signature", "handwriting", "not_a_mark"]
SEVERITIES = ["high", "medium", "low"]


def _s() -> dict[str, Any]:
    return {"type": "string"}


def _i() -> dict[str, Any]:
    return {"type": "integer"}


def _b() -> dict[str, Any]:
    return {"type": "boolean"}


def _n() -> dict[str, Any]:
    return {"type": "number"}


def _enum(values: list[str]) -> dict[str, Any]:
    return {"type": "string", "enum": values}


def _arr(items: dict[str, Any]) -> dict[str, Any]:
    return {"type": "array", "items": items}


def _obj(props: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


CASE_SCHEMA: dict[str, Any] = _obj({
    "case_title_en": _s(),
    "case_title_ar": _s(),
    "case_type": _enum(CASE_TYPES),
    "summary_en": _s(),
    "summary_ar": _s(),
    "pages": _arr(_obj({"page": _i(), "document_en": _s(), "document_ar": _s()})),
    "court": _obj({
        "name_en": _s(), "name_ar": _s(), "case_number": _s(),
        "case_number_source": _enum(SOURCES), "pages": _arr(_i()),
    }),
    "parties": _arr(_obj({
        "role": _enum(ROLES), "role_en": _s(), "role_ar": _s(),
        "name_ar": _s(), "name_en": _s(), "details_en": _s(), "pages": _arr(_i()),
    })),
    "dates": _arr(_obj({
        "date": _s(), "what_en": _s(), "what_ar": _s(), "page": _i(),
        "source": _enum(SOURCES), "mark_ids": _arr(_s()),
    })),
    "deadlines": _arr(_obj({
        "date": _s(), "time": _s(), "who_en": _s(), "what_en": _s(), "what_ar": _s(), "page": _i(),
        "computed": _b(), "basis_en": _s(), "source": _enum(SOURCES), "mark_ids": _arr(_s()),
    })),
    "claims": _arr(_obj({
        "item_en": _s(), "item_ar": _s(), "has_amount": _b(), "amount_aed": _n(), "page": _i(),
    })),
    "key_facts": _arr(_obj({
        "fact_en": _s(), "fact_ar": _s(), "page": _i(), "source": _enum(SOURCES), "mark_ids": _arr(_s()),
    })),
    "citations": _arr(_obj({
        "text_ar": _s(), "law_kind": _enum(LAW_KINDS), "emirate": _s(), "law_number": _s(),
        "law_year": _i(), "law_title_en": _s(), "article": _s(), "clause": _s(),
        "quoted_text_ar": _s(), "page": _i(),
    })),
    "marks": _arr(_obj({
        "mark_id": _s(), "page": _i(), "type": _enum(MARK_TYPES), "text_ar": _s(),
        "meaning_en": _s(), "meaning_ar": _s(), "changes_printed_text": _b(),
    })),
    "flags": _arr(_obj({"flag_en": _s(), "flag_ar": _s(), "page": _i(), "severity": _enum(SEVERITIES)})),
})


SYNONYMS = {
    # mark types
    "printed": "not_a_mark", "printed_text": "not_a_mark", "text": "not_a_mark", "noise": "not_a_mark",
    "none": "not_a_mark", "not_mark": "not_a_mark", "no_mark": "not_a_mark", "false_positive": "not_a_mark",
    "seal": "stamp", "official_seal": "stamp", "rubber_stamp": "stamp", "ink_stamp": "stamp",
    "handwritten": "handwriting", "handwritten_note": "handwriting", "handwritten_text": "handwriting",
    "sign": "signature", "signed": "signature",
    # sources
    "print": "printed", "typed": "printed", "typed_text": "printed", "calculated": "computed", "derived": "computed",
    # roles
    "plaintiff": "claimant", "respondent": "defendant", "plaintiff_lawyer": "claimant_lawyer",
    "claimant_attorney": "claimant_lawyer", "defendant_attorney": "defendant_lawyer",
    "claimant_counsel": "claimant_lawyer", "defendant_counsel": "defendant_lawyer",
    "respondent_lawyer": "defendant_lawyer",
}


REPRESENTATIVE_WORDS = {"manager", "owner", "representative", "agent", "director", "partner"}


def _closest_enum(text: str, values: list[str]) -> str:
    """Map a near miss ("Handwritten", "claimant's lawyer") onto an allowed value.

    Only an exact, synonym or unique-prefix match is accepted; anything else becomes
    "other" where the list has it, or "" (unknown) where it doesn't, never a guess.
    """
    key = re.sub(r"[^a-z0-9]+", "_", text.strip().casefold().replace("'s ", " ").replace("’s ", " ")).strip("_")
    if key in values:
        return key
    if SYNONYMS.get(key) in values:
        return SYNONYMS[key]
    words = key.split("_")
    # "claimant_general_manager" -> claimant_representative
    if len(words) > 1 and words[0] in ("claimant", "defendant") and words[-1] in REPRESENTATIVE_WORDS \
            and f"{words[0]}_representative" in values:
        return f"{words[0]}_representative"
    if len(words) > 1 and words[-1] in values:  # "presiding_judge" -> judge; "handwritten_signature" -> signature
        return words[-1]
    leading = [v for v in values if key.startswith(v + "_")]  # "claimant_creditor" -> "claimant"
    if leading:
        return max(leading, key=len)
    if len(key) >= 5:
        prefixed = [v for v in values if v.startswith(key[:5])]
        if len(prefixed) == 1:
            return prefixed[0]
    return "other" if "other" in values else ""


def conform(value: Any, schema: dict[str, Any]) -> Any:
    """Coerce a model answer into the schema's shape: fill gaps, drop extras, fix simple types."""
    kind = schema.get("type")
    if kind == "object":
        value = value if isinstance(value, dict) else {}
        return {k: conform(value.get(k), sub) for k, sub in schema["properties"].items()}
    if kind == "array":
        if not isinstance(value, list):
            return []
        return [conform(v, schema["items"]) for v in value]
    if kind == "string":
        text = "" if value is None else str(value)
        if "enum" in schema and text not in schema["enum"]:
            return _closest_enum(text, schema["enum"])
        return text
    if kind == "integer":
        try:
            return int(float(str(value).strip()))
        except (TypeError, ValueError):
            return 0
    if kind == "number":
        try:
            return float(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return 0.0
    if kind == "boolean":
        if isinstance(value, str):
            return value.strip().lower() in {"true", "yes", "1"}
        return bool(value)
    return value
