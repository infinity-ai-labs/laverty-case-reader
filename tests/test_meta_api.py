"""The API client against a local stand-in server that checks each request's shape."""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from case_reader import meta_api
from case_reader.meta_api import MetaAPIError, MetaClient

SAM_TEXT = "<0f>0<|box;x1=10;y1=20;x2=109;y2=59;w=400;h=560;c=0.88|><|mask;x=0;y=0;data=1,1,!A|>"


class _Handler(BaseHTTPRequestHandler):
    calls: list = []
    fail_next_with: list = []

    def log_message(self, *args):
        pass

    def _send(self, status, body, headers=None):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        assert self.headers["Authorization"] == "Bearer test-key"
        self._send(200, {"data": [{"id": "muse-spark-1.3"}, {"id": "sam-3.1"}]})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        type(self).calls.append((self.path, body, self.headers["Authorization"]))
        if type(self).fail_next_with:
            status = type(self).fail_next_with.pop(0)
            return self._send(status, {"error": {"message": f"test {status}", "code": "test"}}, {"Retry-After": "0"})
        if self.path == "/v1/responses":
            return self._send(200, {"output": [{"type": "message", "content": [{"type": "output_text", "text": SAM_TEXT}]}]})
        if self.path == "/v1/chat/completions":
            return self._send(200, {"choices": [{"message": {"content": "{\"ok\": true}"}}], "usage": {"prompt_tokens": 5}})
        self._send(404, {"error": {"message": "no such path"}})


@pytest.fixture()
def server(monkeypatch):
    monkeypatch.setenv("MODEL_API_KEY", "test-key")
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    monkeypatch.setattr(meta_api.time, "sleep", lambda s: None)
    _Handler.calls = []
    _Handler.fail_next_with = []
    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}/v1"
    httpd.shutdown()


def test_sam_request_shape_and_retry(server, tmp_path):
    _Handler.fail_next_with = [429]
    client = MetaClient(base_url=server, usage_log=tmp_path / "usage.jsonl")
    text = client.segment("rubber stamp", "data:image/jpeg;base64,AAAA")
    assert text == SAM_TEXT
    assert len(_Handler.calls) == 2  # one 429, then the retry
    path, body, auth = _Handler.calls[-1]
    assert path == "/v1/responses" and auth == "Bearer test-key"
    assert body["model"] == "sam-3.1"
    content = body["input"][0]["content"]
    assert content[0] == {"type": "input_text", "text": "rubber stamp"}
    assert content[1] == {"type": "input_image", "image_url": "data:image/jpeg;base64,AAAA"}
    assert body["metadata"] == {"include_confidence": "true", "mask_encoding": "one_bit"}
    log = (tmp_path / "usage.jsonl").read_text()
    assert "test-key" not in log


def test_chat_request_shape(server):
    client = MetaClient(base_url=server)
    data = client.chat("muse-spark-1.3", [{"role": "user", "content": "hi"}],
                       response_format={"type": "json_object"}, reasoning_effort="high", max_completion_tokens=100)
    assert data["choices"][0]["message"]["content"] == '{"ok": true}'
    _, body, _ = _Handler.calls[-1]
    assert body["reasoning_effort"] == "high" and body["max_completion_tokens"] == 100
    assert "temperature" not in body


def test_errors_are_reported_without_retrying_a_bad_request(server):
    _Handler.fail_next_with = [400]
    client = MetaClient(base_url=server)
    with pytest.raises(MetaAPIError) as err:
        client.chat("muse-spark-1.3", [{"role": "user", "content": "hi"}])
    assert err.value.status == 400 and "test 400" in str(err.value)
    assert len(_Handler.calls) == 1


def test_check_access(server):
    assert MetaClient(base_url=server).check_access() == ["muse-spark-1.3", "sam-3.1"]


def test_missing_key(monkeypatch):
    monkeypatch.delenv("MODEL_API_KEY", raising=False)
    monkeypatch.delenv("META_API_KEY", raising=False)
    with pytest.raises(meta_api.MissingKeyError):
        MetaClient(base_url="http://127.0.0.1:9/v1")
