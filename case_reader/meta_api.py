"""Small client for the Meta Model API (https://api.meta.ai/v1).

The key comes from the MODEL_API_KEY environment variable (META_API_KEY also
works). It is sent only in the Authorization header and is never printed,
logged or written to disk.
"""

from __future__ import annotations

import json
import os
import random
import time
from pathlib import Path
from typing import Any

import requests

API_BASE = os.environ.get("META_API_BASE", "https://api.meta.ai/v1").rstrip("/")
SAM_MODEL = "sam-3.1"
RETRY_STATUSES = {408, 409, 429, 500, 502, 503, 504}


class MetaAPIError(RuntimeError):
    def __init__(self, status: int, message: str, code: str | None = None):
        label = f" ({code})" if code else ""
        super().__init__(f"Meta Model API error {status}{label}: {message}")
        self.status = status
        self.code = code


class MissingKeyError(RuntimeError):
    pass


def api_key_from_env() -> str:
    key = (os.environ.get("MODEL_API_KEY") or os.environ.get("META_API_KEY") or "").strip()
    if not key:
        raise MissingKeyError(
            "No Meta Model API key found. Set MODEL_API_KEY; in GitHub Actions it comes "
            "from the repository secret META_API_KEY."
        )
    return key


def _error_details(response: requests.Response) -> tuple[str, str | None]:
    try:
        body = response.json()
    except ValueError:
        return (response.text or response.reason or "no details")[:500], None
    err = body.get("error") if isinstance(body, dict) else None
    if isinstance(err, dict):
        return str(err.get("message") or err)[:500], err.get("code") or err.get("type")
    return json.dumps(body, ensure_ascii=False)[:500], None


def responses_output_text(data: dict[str, Any]) -> str:
    """The text a Responses API call returned (for SAM 3.1, the special-token lines)."""
    text = data.get("output_text")
    if isinstance(text, str) and text:
        return text
    parts: list[str] = []
    for item in data.get("output") or []:
        for block in (item or {}).get("content") or []:
            if (block or {}).get("type") == "output_text":
                parts.append(block.get("text") or "")
    return "".join(parts)


def chat_output_text(data: dict[str, Any]) -> str:
    """The assistant's text from a Chat Completions response."""
    choices = data.get("choices") or [{}]
    message = (choices[0] or {}).get("message") or {}
    content = message.get("content")
    if isinstance(content, list):
        return "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content or ""


class MetaClient:
    """Calls Muse Spark (Chat Completions) and SAM 3.1 (Responses API)."""

    def __init__(
        self,
        *,
        base_url: str = API_BASE,
        timeout: float = 600,
        max_retries: int = 5,
        usage_log: Path | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.usage_log = usage_log
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {api_key_from_env()}", "Content-Type": "application/json"}
        )

    # -- plumbing ---------------------------------------------------------

    def _sleep_before_retry(self, attempt: int, retry_after: str | None) -> None:
        wait = min(60.0, 2.0 * (2 ** attempt)) + random.uniform(0, 1.5)
        if retry_after:
            try:
                wait = max(wait, min(120.0, float(retry_after)))
            except ValueError:
                pass
        time.sleep(wait)

    def _log(self, entry: dict[str, Any]) -> None:
        if not self.usage_log:
            return
        self.usage_log.parent.mkdir(parents=True, exist_ok=True)
        with self.usage_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _post(self, path: str, payload: dict[str, Any], label: str, timeout: float | None = None,
              retry_read_timeouts: bool = True) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        for attempt in range(self.max_retries + 1):
            started = time.time()
            try:
                response = self._session.post(url, data=body, timeout=timeout or self.timeout)
            except requests.RequestException as exc:
                self._log({"label": label, "model": payload.get("model"), "error": type(exc).__name__,
                           "attempt": attempt})
                if isinstance(exc, requests.exceptions.ReadTimeout) and not retry_read_timeouts:
                    # The model may have finished; asking again would generate (and bill) the answer twice.
                    raise MetaAPIError(0, f"no answer within {timeout or self.timeout:.0f} seconds") from None
                if attempt >= self.max_retries:
                    raise MetaAPIError(0, f"network error ({type(exc).__name__})") from None
                self._sleep_before_retry(attempt, None)
                continue
            seconds = round(time.time() - started, 2)
            if response.status_code == 200:
                data = response.json()
                self._log({"label": label, "model": payload.get("model"), "seconds": seconds,
                           "request_bytes": len(body), "usage": data.get("usage")})
                return data
            message, code = _error_details(response)
            self._log({"label": label, "model": payload.get("model"), "seconds": seconds,
                       "status": response.status_code, "error": message[:200], "attempt": attempt})
            if response.status_code in RETRY_STATUSES and attempt < self.max_retries:
                self._sleep_before_retry(attempt, response.headers.get("retry-after"))
                continue
            raise MetaAPIError(response.status_code, message, code)
        raise MetaAPIError(0, "gave up after retries")

    # -- models -----------------------------------------------------------

    def check_access(self) -> list[str]:
        """List the model ids this key can use (a cheap first check that the key works)."""
        response = self._session.get(f"{self.base_url}/models", timeout=60)
        if response.status_code != 200:
            message, code = _error_details(response)
            raise MetaAPIError(response.status_code, message, code)
        data = response.json()
        return sorted(str(m.get("id")) for m in data.get("data") or [] if isinstance(m, dict))

    def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        *,
        response_format: dict[str, Any] | None = None,
        reasoning_effort: str | None = None,
        max_completion_tokens: int | None = None,
        temperature: float | None = None,
        seed: int | None = None,
        label: str = "chat",
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": model, "messages": messages}
        if response_format is not None:
            payload["response_format"] = response_format
        if reasoning_effort:
            payload["reasoning_effort"] = reasoning_effort
        if max_completion_tokens:
            payload["max_completion_tokens"] = max_completion_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if seed is not None:
            payload["seed"] = seed
        return self._post("/chat/completions", payload, label, retry_read_timeouts=False)

    def segment(self, concept: str, image_url: str, *, include_confidence: bool = True,
                label: str = "sam") -> str:
        """Ask SAM 3.1 for every instance of `concept` in one image; returns the raw output text."""
        payload = {
            "model": SAM_MODEL,
            "input": [
                {
                    "type": "message",
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": concept},
                        {"type": "input_image", "image_url": image_url},
                    ],
                }
            ],
            "metadata": {
                "include_confidence": "true" if include_confidence else "false",
                # Only the boxes are used, so take the smaller mask encoding.
                "mask_encoding": "one_bit",
            },
        }
        data = self._post("/responses", payload, label, timeout=300)
        return responses_output_text(data)
