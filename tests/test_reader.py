import json
from pathlib import Path

from PIL import Image

from case_reader.meta_api import MetaAPIError, chat_output_text, responses_output_text
from case_reader.pages import Page
from case_reader.reader import build_messages, normalize_date, parse_json_text, read_case
from case_reader.schema import CASE_SCHEMA, conform


def _page(tmp_path: Path) -> Page:
    path = tmp_path / "page-1.jpg"
    Image.new("RGB", (400, 560), "white").save(path)
    return Page(number=1, path=path, width=400, height=560)


def test_normalize_date():
    assert normalize_date("٠٦/١٠/٢٠٢٦") == "2026-10-06"
    assert normalize_date("2026/11/5") == "2026-11-05"
    assert normalize_date("2026-02-30") == "2026-02-30"  # impossible dates are left for a person to see
    assert normalize_date("next week") == "next week"


def test_parse_json_text():
    assert parse_json_text('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json_text('Here it is: {"a": 1} done') == {"a": 1}
    assert parse_json_text("no json") is None


def test_conform_fills_gaps_and_fixes_types():
    out = conform({"parties": [{"role": "Claimant", "pages": ["1", 2]}], "claims": [{"amount_aed": "45,000"}]},
                  CASE_SCHEMA)
    assert out["parties"][0]["role"] == "claimant"
    assert out["parties"][0]["pages"] == [1, 2]
    assert out["claims"][0]["amount_aed"] == 45000.0
    assert out["citations"] == [] and out["court"]["case_number"] == ""


def test_messages_put_pages_then_mark_closeups(tmp_path):
    page = _page(tmp_path)
    marks = [{"mark_id": "M1", "page": 1, "type": "stamp", "box": [0.1, 0.1, 0.4, 0.2], "confidence": 0.9}]
    system, user = build_messages([page], marks)
    assert system["role"] == "system" and "citation check" in system["content"]
    kinds = [part["type"] for part in user["content"]]
    assert kinds.count("image_url") == 2
    assert user["content"][2]["image_url"]["url"].startswith("data:image/jpeg;base64,")
    assert any("Mark M1: page 1, found as stamp" in part.get("text", "") for part in user["content"])


def test_output_text_helpers():
    assert chat_output_text({"choices": [{"message": {"content": "hi"}}]}) == "hi"
    data = {"output": [{"type": "message", "content": [{"type": "output_text", "text": "<0f>"}]}]}
    assert responses_output_text(data) == "<0f>"


class _FallbackClient:
    """Refuses the JSON-schema mode with a 400, then answers in JSON-object mode."""

    def __init__(self):
        self.modes = []

    def chat(self, model, messages, response_format=None, **kwargs):
        mode = (response_format or {}).get("type", "plain")
        self.modes.append(mode)
        if mode == "json_schema":
            raise MetaAPIError(400, "schema not supported")
        answer = {"case_title_en": "Test", "dates": [{"date": "06/10/2026", "page": 1}]}
        return {"choices": [{"message": {"content": json.dumps(answer)}}]}


def test_read_case_falls_back_when_a_mode_is_refused(tmp_path):
    client = _FallbackClient()
    summary, mode = read_case(client, [_page(tmp_path)], [], out_dir=tmp_path)
    assert client.modes == ["json_schema", "json_object"]
    assert mode == "json_object"
    assert summary["case_title_en"] == "Test"
    assert summary["dates"][0]["date"] == "2026-10-06"
    assert (tmp_path / "reader.json_schema.error.txt").exists()
