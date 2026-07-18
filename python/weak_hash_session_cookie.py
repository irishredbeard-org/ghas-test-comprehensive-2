# INTENTIONAL VULNERABILITY: Weak Hash (CWE-916 / py/weak-sensitive-data-hashing - Medium)
# DUPLICATE_GROUP: py-hash-002
# This file exists for CodeQL SAST baseline testing only.
import hashlib
from flask import request


def weak_hash_session_cookie():
    token = request.args.get('token', '').encode('utf-8')
    # VULN: weak hashing is used for sensitive data.
    return hashlib.md5(token).hexdigest()
