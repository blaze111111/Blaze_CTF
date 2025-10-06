# tests/test_usability.py
import requests

BASE = "http://localhost:5000"

def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
