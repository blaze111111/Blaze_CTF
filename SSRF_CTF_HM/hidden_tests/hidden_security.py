import requests
import pytest

BASE = "http://127.0.0.1:8080"

def fetch(url: str):
    return requests.get(f"{BASE}/fetch", params={"url": url}, timeout=5)

BAD_URLS = [
    "http://127.0.0.1:8080/internal/secret",
    "http://localhost:8080/internal/secret",
    "%68%74%74%70%3A%2F%2F127.0.0.1%3A8080%2Finternal%2Fsecret",
    "http://10.0.0.5:8080/internal/secret",
]

@pytest.mark.parametrize("url", BAD_URLS)
def test_never_leak_admin_token(url):
    r = fetch(url)
    assert "ADMIN_TOKEN=" not in r.text

def test_register_rejects_local_callback():
    r = requests.post(f"{BASE}/register", json={"url": "http://127.0.0.1:9999/cb"}, timeout=5)
    assert not (r.status_code == 201 and "127.0.0.1" in r.text)
