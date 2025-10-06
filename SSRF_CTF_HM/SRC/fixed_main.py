# src/fixed_main.py  (SECURE REFERENCE for instructors)
from flask import Flask, request, Response, jsonify
import requests, socket, ipaddress, urllib.parse

app = Flask(__name__)
ALLOWED_HOSTS = {"example.com", "images.examplecdn.com"}

def is_private_host(host):
    # resolve host -> all IPs and check private ranges
    try:
        infos = socket.getaddrinfo(host, None)
    except Exception:
        return True
    for fam, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
            return True
    return False

def canonical_host_from_url(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname

@app.route("/download")
def download():
    url = request.args.get("url")
    host = canonical_host_from_url(url)
    if host not in ALLOWED_HOSTS:
        return jsonify({"error": "host not allowed"}), 400
    if is_private_host(host):
        return jsonify({"error":"private host blocked"}), 400
    r = requests.get(url, timeout=5)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type"))

# ... other endpoints secured similarly ...
