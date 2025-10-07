# src/main.py  (INTENTIONALLY VULNERABLE)
# Players will edit this file to secure it.
from flask import Flask, request, Response, jsonify
import requests,os



app = Flask(__name__)

registered_callbacks = []

    
if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

    
# Simulated internal endpoint that is supposed to be internal-only.
# NOTE: This endpoint does NOT contain the real flag string.
# Instructor's grader/flag file is stored separately in flags/flag.txt (hidden).
@app.route("/internal/secret")
def internal_secret():
    # This imitates an internal service exposing a token (NOT the real flag).
    return "ADMIN_TOKEN=LOCAL_ADMIN_TOKEN_12345"

@app.route("/fetch")
def fetch():
    """
    Vulnerable endpoint:
    - Accepts ?url=... and naive-checks it (only checks that 'http' substring exists)
    - Follows redirects and fetches the supplied URL with requests.get.
    - If the fetched content contains ADMIN_TOKEN=..., the server will attempt to
      read flags/flag.txt and return the first half of the flag (if present).
    """
    url = request.args.get("url", "")
    if not url:
        return "specify ?url=", 400

    # VERY naive validation (intentional vulnerability)
    if "http" not in url.lower():
        return "only http(s) allowed (naive check)", 400

    try:
        # vulnerable: no IP checks, follows redirects, no safe handling of content
        resp = requests.get(url, allow_redirects=True, timeout=5)
    except Exception as e:
        return f"error fetching: {e}", 500

    text = resp.text

    if "ADMIN_TOKEN=" in text:
        # If an admin token is found, read the hidden flag file (if present) and return only the first half.
        # This keeps the flag out of code — the file is instructor-controlled.
        flag_path = os.path.join(os.path.dirname(__file__), "..", "flags", "flag.txt")
        try:
            with open(flag_path, "r", encoding="utf-8") as f:
                full_flag = f.read().strip()
            if full_flag:
                # split into two halves and return only the first half to players
                # simple split: first half is first len//2 chars (instructor decides format)
                mid = len(full_flag) // 2
                first_half = full_flag[:mid]
                return jsonify({
                    "message": "Congrats — you found an admin token! Use it to access /become_admin",
                    "hint": "You have the FIRST HALF of the flag. Fix the app, then push for hidden tests to reveal the second half.",
                    "first_half": first_half
                }), 200
        except FileNotFoundError:
            # If the flag file isn't present on the machine, still show the exploit result
            return jsonify({
                "message": "Congrats — you found an admin token! Use it to access /become_admin",
                "hint": "Instructor flag file missing on this instance. Contact a host."
            }), 200

    return f"fetched {len(text)} bytes", 200

@app.route("/become_admin", methods=["POST"])
def become_admin():
    """
    Players will present the first half they obtained to try become_admin.
    For simplicity in this CTF, becoming admin is trivial because the half is just
    data that the grader matches later — this endpoint is for usability flow.
    """
    token = request.json.get("token") if request.is_json else request.form.get("token")
    if not token:
        return "no token provided", 400

    # In the vulnerable version we accept the LOCAL_ADMIN_TOKEN_12345 token (simulated)
    # This endpoint does not reveal the full flag.
    if token == "LOCAL_ADMIN_TOKEN_12345" or token.startswith("CTF_"):
        return jsonify({"message": "You are now admin (simulated). Check tests/ for next steps."}), 200
    return "invalid token", 403

@app.route("/register", methods=["POST"])
def register():
    """
    Register arbitrary callback URLs. Vulnerable because it accepts anything.
    Players can register internal callback endpoints to test callback behavior.
    """
    url = request.json.get("url") if request.is_json else request.form.get("url")
    if not url:
        return "no url provided", 400
    registered_callbacks.append(url)
    return jsonify({"registered": url}), 201

@app.route("/notify", methods=["POST"])
def notify():
    """
    Blindly POSTs to every registered callback (vulnerable).
    Players will need to fix this to validate callback URLs and avoid proxy/passthrough.
    """
    payload = {"event": "ctf_notify"}
    results = []
    for cb in registered_callbacks:
        try:
            r = requests.post(cb, json=payload, timeout=5)
            results.append({"url": cb, "status": r.status_code})
        except Exception as e:
            results.append({"url": cb, "error": str(e)})
    return jsonify(results), 200

# Simple health endpoint used by 'make status'
@app.route("/status")
def status():
    return "ok", 200

if __name__ == "__main__":
    # default port as in your description: 8080
    app.run(host="0.0.0.0", port=8080, debug=True)