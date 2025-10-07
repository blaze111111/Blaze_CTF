# src/fixed_main.py  (SECURE REFERENCE for instructors)
from flask import Flask, request, Response, jsonify
import requests, socket, ipaddress, urllib.parse

# src/fixed_main.py
"""
Secure reference (INSTRUCTOR-ONLY).
Implements:
 - percent-decoding + urlparse
 - DNS resolution + private IP blocking
 - prevents redirect-driven SSRF
 - validated callback registration + notify
"""
from flask import Flask, request, jsonify
import requests
import socket
import ipaddress
from urllib.parse import urlparse, unquote
import os

app = Flask(__name__)
registered_callbacks = []

def is_private_host(hostname):
    try:
        infos = socket.getaddrinfo(hostname, None)
        for info in infos:
            addr = info[4][0]
            ip = ipaddress.ip_address(addr)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return True
        return False
    except Exception:
        # If we can't resolve, block to be safe
        return True

def validate_url(raw):
    url = unquote(raw)
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("scheme must be http or https")
    if not parsed.hostname:
        raise ValueError("no hostname")
    if is_private_host(parsed.hostname):
        raise ValueError("host resolves to private address")
    return parsed.geturl()

@app.route("/fetch")
def fetch():
    url = request.args.get("url", "")
    if not url:
        return "specify ?url=", 400
    try:
        normalized = validate_url(url)
    except ValueError as e:
        return f"invalid url: {e}", 400

    # Do not follow redirects to unknown places
    try:
        resp = requests.get(normalized, allow_redirects=False, timeout=5)
    except Exception as e:
        return f"error fetching: {e}", 500

    # never reveal tokens
    return f"fetched {len(resp.text)} bytes", 200

@app.route("/register", methods=["POST"])
def register():
    url = request.json.get("url") if request.is_json else request.form.get("url")
    if not url:
        return "no url provided", 400
    try:
        normalized = validate_url(url)
    except ValueError as e:
        return f"invalid url: {e}", 400
    registered_callbacks.append(normalized)
    return jsonify({"registered": normalized}), 201

@app.route("/notify", methods=["POST"])
def notify():
    payload = {"event": "ctf_notify"}
    results = []
    for cb in list(registered_callbacks):
        try:
            # validate before posting
            parsed = urlparse(cb)
            if is_private_host(parsed.hostname):
                results.append({"url": cb, "error": "blocked_private"})
                continue
            r = requests.post(cb, json=payload, timeout=5)
            results.append({"url": cb, "status": r.status_code})
        except Exception as e:
            results.append({"url": cb, "error": str(e)})
    return jsonify(results), 200

@app.route("/status")
def status():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
