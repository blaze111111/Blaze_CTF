# tests/test_usability.py
import requests

BASE = "http://localhost:5000"

def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

import unittest
from main import _validate_url, Errors

class Usability(unittest.TestCase):

    def test_valid_url(self):
        result = _validate_url('https://www.google.com')
        self.assertIsNone(result)

    def test_invalid_url(self):
        with self.assertRaises(Errors.ErrInvalidURL):
            _validate_url('google.com')


if __name__ == '__main__':
    unittest.main()
    
import unittest
from main import _validate_url, Errors

class SecurityTest(unittest.TestCase):

    def test_long_url_should_fail(self):
        with self.assertRaises(Errors.ErrInvalidURL, msg='Invalid URL length'):
            _validate_url('www.google.com?q=http://something' * 100)

    def test_http_scheme_should_fail(self):
        with self.assertRaises(Errors.ErrInvalidURL, msg='Invalid scheme validation for http'):
            _validate_url('www.google.com?q=http://something')

    def test_https_scheme_should_fail(self):
        with self.assertRaises(Errors.ErrInvalidURL, msg='Invalid scheme validation for https'):
            _validate_url('www.google.com?q=https://something')


    # Some security tests are missing here
    # Where you push your code, you code will be tested against them.

if __name__ == '__main__':
    unittest.main()