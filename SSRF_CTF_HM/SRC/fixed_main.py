# fixed server: rejects loopback/private addresses and percent-encoded tricks
from flask import Flask, request, jsonify
from urllib.parse import unquote, urlparse
import socket
import requests

app = Flask(__name__)
callbacks = []

PRIVATE_PREFIXES = ("127.", "10.", "192.168.", "169.254.", "172.16.")

def is_private_host(hostname):
    try:
        # Resolve hostname to IPs
        infos = socket.getaddrinfo(hostname, None)
        for info in infos:
            ip = info[4][0]
            if ip.startswith("::1") or ip.startswith("127.") or ip.startswith("169.254."):
                return True
            if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172.16."):
                return True
        return False
    except Exception:
        # If resolution fails, be conservative and block
        return True

@app.route("/")
def index():
    return "SSRF CTF - secure fetch"

@app.route("/fetch")
def fetch():
    raw = request.args.get("url", "")
    if not raw:
        return "Tell me who to fetch: /fetch?url=http://example.com", 200
    # Normalize: percent-decode before parsing
    url = unquote(raw)
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    if is_private_host(hostname):
        return "Blocked", 403
    try:
        r = requests.get(url, timeout=3)
        return r.text, r.status_code
    except Exception:
        return "Error fetching", 502

@app.route("/register", methods=["POST"])
def register():
    url = request.json.get("url", "")
    from urllib.parse import urlparse, unquote
    url = unquote(url)
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    if is_private_host(hostname):
        return jsonify({"error":"invalid callback"}), 400
    callbacks.append(url)
    return jsonify({"registered": url}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
