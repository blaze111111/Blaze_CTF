# hidden_tests/hidden_security.py  (INSTRUCTOR ONLY)
import requests, os, ipaddress, socket, urllib.parse

import unittest
from fixed_main import _validate_url
# hidden_tests/hidden_security.py
import requests
import pytest

BASE = "http://127.0.0.1:8080"

def fetch(url):
    r = requests.get(f"{BASE}/fetch", params={"url": url}, timeout=5)
    return r

def test_block_loopback_ip():
    r = fetch("http://127.0.0.1:8080/internal/secret")
    assert "ADMIN_TOKEN=" not in r.text

def test_block_localhost_name():
    r = fetch("http://localhost:8080/internal/secret")
    assert "ADMIN_TOKEN=" not in r.text

def test_percent_encoded_http_bypass():
    encoded = "%68%74%74%70%3A%2F%2F127.0.0.1%3A8080%2Finternal%2Fsecret"
    r = fetch(encoded)
    assert "ADMIN_TOKEN=" not in r.text

def test_block_private_range():
    r = fetch("http://10.0.0.5:8080/internal/secret")
    assert "ADMIN_TOKEN=" not in r.text

def test_register_block_local_callback():
    # try to register local callback; server should reject or not store it
    r = requests.post(f"{BASE}/register", json={"url": "http://127.0.0.1:9999/cb"}, timeout=5)
    # Mark as failure if it registers a local callback successfully
    assert not (r.status_code == 201 and "127.0.0.1" in r.text)

class HiddenSecurityChecks(unittest.TestCase):
    def test_ipv6_mapped_and_bracketed(self):
        # bracketed IPv6 loopback should be blocked
        with self.assertRaises(Exception):
            _validate_url("http://[::1]/")

    def test_decimal_and_hex_ip_block(self):
        with self.assertRaises(Exception):
            _validate_url("http://2130706433")   # decimal encoded IP
        with self.assertRaises(Exception):
            _validate_url("http://0x7f000001")  # hex encoded IP

    def test_percent_encoded_smuggle(self):
        # percent-encoded http inside query should be detected and blocked
        with self.assertRaises(Exception):
            _validate_url("http://example.com/?q=%68%74%74%70%3A%2F%2F127.0.0.1")

BASE = "http://localhost:5000"

# list of advanced payloads that must be blocked
PAYLOADS = [
    "http://127.0.0.1:8080/secret",
    "http://2130706433/",  # integer encoded 127.0.0.1
    "http://0x7f000001/",
    "http://[::ffff:127.0.0.1]/",
    "http://169.254.169.254/latest/meta-data/"
]

def is_leakage(resp):
    if resp.status_code != 200:
        return False
    body = resp.content
    return b"INTERNAL_OK" in body

def test_block_all_payloads():
    for p in PAYLOADS:
        r = requests.get(f"{BASE}/download", params={"url": p}, timeout=5)
        assert not is_leakage(r), f"Leak detected for payload {p}"

def test_flag_on_success():
    # If all security tests passed, reveal flag (read from file kept secret)
    flag_path = os.environ.get("FLAG_PATH", "/run/secret/flag.txt")
    with open(flag_path, "r") as fh:
        flag = fh.read().strip()
    assert flag.startswith("HackMacCTF{") and flag.endswith("}")
    print("CONGRATULATIONS — flag:", flag)
