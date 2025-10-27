import importlib.util
import os
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Load the module by file path to avoid package import issues
MODULE_PATH = Path(__file__).parent / "main.py"

spec = importlib.util.spec_from_file_location("main_module", str(MODULE_PATH))
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


@pytest.fixture(autouse=True)
def use_tmp_log(tmp_path, monkeypatch):
    """Redirect logs to a temporary file for tests and ensure directory exists."""
    tmp_log = tmp_path / "api_logs.txt"
    # ensure parent exists
    tmp_log.parent.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(main, "LOG_FILE", str(tmp_log))
    monkeypatch.setattr(main, "LOG_DIR", str(tmp_log.parent))

    # yield the path so tests can inspect it
    yield tmp_log


def read_log(path, timeout=1.0):
    """Read file contents with a short timeout to allow background tasks to flush."""
    end = time.time() + timeout
    while time.time() < end:
        if path.exists():
            try:
                return path.read_text(encoding="utf-8")
            except Exception:
                pass
        time.sleep(0.05)
    return ""


def test_root_logs_and_response(use_tmp_log):
    client = TestClient(main.app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Async FastAPI API running 🚀"}

    contents = read_log(use_tmp_log)
    assert "Root endpoint called" in contents


def test_status_logs_and_response(use_tmp_log):
    client = TestClient(main.app)
    resp = client.get("/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "Status endpoint called successfully." in body["message"]

    contents = read_log(use_tmp_log)
    assert "Status endpoint called successfully." in contents


def test_greet_logs_and_response(use_tmp_log):
    client = TestClient(main.app)
    name = "Alice"
    resp = client.get(f"/greet/{name}")
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Hello, {name}!"}

    contents = read_log(use_tmp_log)
    assert f"Greeted user: {name}" in contents
    assert f"/greet/{name}" in contents


def test_process_post_logs_and_response(use_tmp_log):
    client = TestClient(main.app)
    resp = client.post("/process")
    assert resp.status_code == 200
    assert resp.json() == {"task": "processing", "status": "started"}

    contents = read_log(use_tmp_log)
    assert "Data processing initiated." in contents


def test_save_log_to_file_direct(use_tmp_log):
    # ensure the helper function writes to the monkeypatched LOG_FILE
    main.save_log_to_file("/direct", "direct-call")
    contents = read_log(use_tmp_log)
    assert "direct-call" in contents

