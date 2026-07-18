# INTENTIONAL VULNERABILITY: Weak Hash (CWE-916 / py/weak-sensitive-data-hashing - Medium)
# DUPLICATE_GROUP: py-hash-001
# This file exists for CodeQL SAST baseline testing only.
import hashlib
from flask import request


def weak_hash_api_key():
    value = request.args.get('token', '').encode('utf-8')
    # VULN: weak hashing is used for sensitive data.
    return hashlib.sha1(value).hexdigest()
