# run_hidden_security.py  (judge-private)
import pathlib
import sys
import pytest

HERE = pathlib.Path(__file__).parent
HIDDEN_TEST_FILE = HERE / "hidden_security.py"
FLAG_FILE = HERE / "flag.txt"

def read_flag():
    return FLAG_FILE.read_text(encoding="utf-8").strip()

def main():
    # Run pytest on the hidden tests - compact output
    rc = pytest.main(["-q", str(HIDDEN_TEST_FILE)])
    if rc == 0:
        flag = read_flag()
        if flag:
            # Print machine- and human-readable success output
            print("\n=== ALL HIDDEN TESTS PASSED ===")
            print(f"FLAG: {flag}")
            print("=== END FLAG ===\n")
            sys.exit(0)
        else:
            print("Hidden tests passed, but flag file missing.", file=sys.stderr)
            sys.exit(2)
    else:
        print("Hidden tests failed. No flag awarded.", file=sys.stderr)
        sys.exit(rc)

if __name__ == "__main__":
    main()
