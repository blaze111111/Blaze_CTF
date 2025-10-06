# hidden_tests/hidden_security.py  (INSTRUCTOR ONLY)
import requests, os, ipaddress, socket, urllib.parse

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
