# src/main.py  (INTENTIONALLY VULNERABLE)
# Players will edit this file to secure it.
from flask import Flask, request, Response, jsonify
import requests

app = Flask(__name__)

# === 1) File download / image fetching ===
@app.route("/download")
def download():
    # Danger: fetches arbitrary user-supplied URL without validation
    url = request.args.get("url")
    # TODO: players should validate / whitelist / resolve IPs / block metadata
    resp = requests.get(url, timeout=5)
    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type", "application/octet-stream"))

# === 2) Rendering preview (simulated) ===
@app.route("/render")
def render_url():
    url = request.args.get("url")
    # Danger: naive fetch used to "render" a page
    resp = requests.get(url, timeout=5)
    return jsonify({"title": "preview", "body": resp.text[:100]})

# === 3) Register webhook (server will POST to callback later) ===
registered_webhooks = []
@app.route("/register_webhook", methods=["POST"])
def register_webhook():
    url = request.json.get("url")
    registered_webhooks.append(url)
    return jsonify({"ok": True})

@app.route("/trigger_webhooks")
def trigger_webhooks():
    data = {"event":"test"}
    # Danger: server will POST to every registered URL (which might be internal)
    for u in registered_webhooks:
        try:
            requests.post(u, json=data, timeout=5)
        except Exception:
            pass
    return jsonify({"sent": len(registered_webhooks)})

# === 4) Proxy ===
@app.route("/proxy")
def proxy():
    target = request.args.get("target")
    # Danger: naive pass-through proxy
    r = requests.get(target, timeout=5)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/octet-stream"))

# === 5) Simple health endpoint
@app.route("/health")
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
