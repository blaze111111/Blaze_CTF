import pathlib, sys, pytest
HERE = pathlib.Path(__file__).parent
TEST = HERE / "hidden_security.py"
FLAG = HERE / "flag.txt"

def main():
    rc = pytest.main(["-q", str(TEST)])
    if rc == 0:
        flag = FLAG.read_text(encoding="utf-8").strip()
        print("\\n=== ALL HIDDEN TESTS PASSED ===")
        print(f"FLAG: {flag}")
        print("=== END FLAG ===\\n")
        sys.exit(0)
    else:
        print("Hidden tests failed. No flag awarded.", file=sys.stderr)
        sys.exit(rc)

if __name__ == "__main__":
    main()
