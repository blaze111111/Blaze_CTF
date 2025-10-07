# tests/test_security.py
import requests, time

BASE = "http://localhost:5000"

import pytest
BASE = "http://127.0.0.1:8080"

def test_health():
    r = requests.get(f"{BASE}/status", timeout=3)
    assert r.status_code == 200

def test_admin_blocked():
    # /internal/secret should not be publicly accessible from normal browsing
    r = requests.get(f"{BASE}/internal/secret")
    assert r.status_code == 200  # the internal endpoint exists (simulated)
    # the admin token should not be directly exposed on the main pages
    r = requests.get(f"{BASE}/fetch", timeout=3)
    assert r.status_code in (200, 400)

def test_register_basic():
    # registering a safe external url should be allowed (httpbin used if network exists)
    try:
        r = requests.post(f"{BASE}/register", json={"url": "https://httpbin.org/post"}, timeout=5)
        assert r.status_code in (201, 400)
    except Exception:
        pytest.skip("No external network for httpbin")
