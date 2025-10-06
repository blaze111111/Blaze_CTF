# tests/test_security.py
import requests, time

BASE = "http://localhost:5000"

def test_block_local_download():
    # This should be blocked by a secure solution
    payload = "http://127.0.0.1:8080/secret"
    r = requests.get(f"{BASE}/download", params={"url": payload}, timeout=5)
    # acceptable public behaviour: return 400 or 403 or not leak internal content
    assert r.status_code in (400, 403, 200)
    if r.status_code == 200:
        # if it is 200, ensure it doesn't contain our known internal marker "INTERNAL_OK"
        assert b"INTERNAL_OK" not in r.content
