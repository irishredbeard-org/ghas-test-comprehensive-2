# INTENTIONAL VULNERABILITY: Reflective XSS (CWE-79 / py/reflective-xss - Medium)
# DUPLICATE_GROUP: py-xss-001
# This file exists for CodeQL SAST baseline testing only.
from flask import request


def xss_profile_page():
    value = request.args.get('message', '')
    # VULN: request input is rendered without escaping.
    return f"<html><body>{value}</body></html>"
