import requests
import os
BASE = os.getenv("BASE", "http://127.0.0.1:8080")

def test_index_exists():
    r = requests.get(f"{BASE}/", timeout=2)
    assert r.status_code == 200

def test_fetch_no_url():
    r = requests.get(f"{BASE}/fetch", timeout=2)
    assert "Tell me who to fetch" in r.text
