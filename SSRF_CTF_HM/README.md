# SSRF Challenge — Medium

Goal: Fix `src/main.py` so that the server rejects SSRF payloads and does not leak internal data.
- Run locally: `make run` or `make docker-run`
- Public tests: `pytest -q tests/`
- You should not modify tests in `tests/` directory (but you may add your own).
- Do NOT push any flags to the public repo.
