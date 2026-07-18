# INTENTIONAL VULNERABILITY: SQL Injection (CWE-89 / py/sql-injection - Medium)
# DUPLICATE_GROUP: py-sqli-001
# This file exists for CodeQL SAST baseline testing only.
from flask import request


def sql_injection_user_lookup(db):
    value = request.args.get('value', '')
    # VULN: request input is concatenated directly into SQL.
    return db.execute("SELECT * FROM records WHERE owner = '" + value + "'")
