# INTENTIONAL VULNERABILITY: Path Traversal (CWE-22 / py/path-injection - High)
# DUPLICATE_GROUP: py-path-002
# This file exists for CodeQL SAST baseline testing only.
from pathlib import Path
from flask import request


def path_traversal_archive_restore():
    requested = request.args.get('file', '')
    # VULN: request input controls the filesystem path.
    target = Path('/var/app/archive') / requested
    return target.read_text()
