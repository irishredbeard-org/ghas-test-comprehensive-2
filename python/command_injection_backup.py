# INTENTIONAL VULNERABILITY: Command Injection (CWE-78 / py/command-injection - High)
# DUPLICATE_GROUP: py-cmd-001
# This file exists for CodeQL SAST baseline testing only.
import subprocess
from flask import request


def command_injection_backup():
    target = request.args.get('target', '')
    # VULN: shell=True runs a command that includes request input.
    subprocess.call(f"convert {target} output.png", shell=True)
    return 'done'
