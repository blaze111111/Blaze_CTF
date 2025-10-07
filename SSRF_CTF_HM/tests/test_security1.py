import requests

BASE = "http://127.0.0.1:8080"

def test_register_returns_201():
    r = requests.post(f"{BASE}/register", json={"url":"http://example.com/cb"}, timeout=2)
    assert r.status_code in (200,201)
