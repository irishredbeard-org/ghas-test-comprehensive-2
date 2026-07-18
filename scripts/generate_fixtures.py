#!/usr/bin/env python3
"""Generate the comprehensive CodeQL fixture repository contents."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WORKFLOW = '''name: "CodeQL"

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  schedule:
    - cron: "0 6 * * 1"

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: [atom-sandbox-poc, preprod]
    permissions:
      security-events: write
      actions: read
      contents: read

    strategy:
      fail-fast: false
      matrix:
        include:
          - language: javascript-typescript
            build-mode: none
          - language: python
            build-mode: none
          - language: java
            build-mode: none
          - language: csharp
            build-mode: none
          - language: go
            build-mode: autobuild

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v4
        with:
          languages: ${{ matrix.language }}
          build-mode: ${{ matrix.build-mode }}
          queries: security-extended

      - name: Autobuild
        if: matrix.build-mode == 'autobuild'
        uses: github/codeql-action/autobuild@v4

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v4
        with:
          category: "/language:${{ matrix.language }}"
'''

GITIGNORE = '''node_modules/
dist/
coverage/
*.class
target/
__pycache__/
*.pyc
bin/
obj/
.env
.DS_Store
'''

CODEOWNERS = '''* @spgi-project-atom-sandbox/mock-security-team
/javascript/ @spgi-project-atom-sandbox/mock-frontend-web
/typescript/ @spgi-project-atom-sandbox/mock-frontend-web
/python/ @spgi-project-atom-sandbox/mock-backend-python
/java/ @spgi-project-atom-sandbox/mock-services-java
/csharp/ @spgi-project-atom-sandbox/mock-enterprise-dotnet
/go/ @spgi-project-atom-sandbox/mock-infrastructure-go
/.github/ @spgi-project-atom-sandbox/mock-security-team
/docs/ @spgi-project-atom-sandbox/mock-security-team
'''

OWNER_TEAM_BY_PATH = {
    "javascript": "@spgi-project-atom-sandbox/mock-frontend-web",
    "typescript": "@spgi-project-atom-sandbox/mock-frontend-web",
    "python": "@spgi-project-atom-sandbox/mock-backend-python",
    "java": "@spgi-project-atom-sandbox/mock-services-java",
    "csharp": "@spgi-project-atom-sandbox/mock-enterprise-dotnet",
    "go": "@spgi-project-atom-sandbox/mock-infrastructure-go",
}

TARGET_REPOSITORY = "spgi-project-atom-sandbox/codeql-test-comprehensive"

FIXTURES = [
    # JavaScript: 14
    ("javascript/sql_injection_user_lookup.js", "JavaScript", "Medium", "CWE-89", "js/sql-injection", "js-sqli-001", "SQL Injection", "User lookup query concatenates a request parameter into SQL"),
    ("javascript/sql_injection_order_search.js", "JavaScript", "Medium", "CWE-89", "js/sql-injection", "js-sqli-001", "SQL Injection", "Order search query concatenates a request parameter into SQL"),
    ("javascript/sql_injection_report_filter.js", "JavaScript", "Medium", "CWE-89", "js/sql-injection", "js-sqli-001", "SQL Injection", "Report filter query concatenates a request parameter into SQL"),
    ("javascript/code_injection_eval_admin.js", "JavaScript", "Critical", "CWE-95", "js/code-injection", "js-code-001", "Code Injection", "Admin expression is evaluated from user input"),
    ("javascript/code_injection_eval_formula.js", "JavaScript", "Critical", "CWE-95", "js/code-injection", "js-code-001", "Code Injection", "Formula expression is evaluated from user input"),
    ("javascript/code_injection_function_body.js", "JavaScript", "Critical", "CWE-95", "js/code-injection", "js-code-001", "Code Injection", "Function body is constructed from user input"),
    ("javascript/path_injection_download.js", "JavaScript", "High", "CWE-22", "js/path-injection", "js-path-001", "Path Injection", "Download path is built from a request parameter"),
    ("javascript/path_injection_template.js", "JavaScript", "High", "CWE-22", "js/path-injection", "js-path-001", "Path Injection", "Template path is built from a request parameter"),
    ("javascript/path_injection_log_viewer.js", "JavaScript", "High", "CWE-22", "js/path-injection", "js-path-001", "Path Injection", "Log file path is built from a request parameter"),
    ("javascript/xss_profile_render.js", "JavaScript", "Medium", "CWE-79", "js/xss", "js-xss-001", "Cross-Site Scripting", "Profile text is written to innerHTML"),
    ("javascript/xss_comment_preview.js", "JavaScript", "Medium", "CWE-79", "js/xss", "js-xss-001", "Cross-Site Scripting", "Comment preview is written to document output"),
    ("javascript/redos_email_validator.js", "JavaScript", "Medium", "CWE-1333", "js/redos", "js-redos-001", "Regular Expression DoS", "Email validator uses a catastrophic backtracking pattern"),
    ("javascript/redos_slug_parser.js", "JavaScript", "Medium", "CWE-1333", "js/redos", "js-redos-001", "Regular Expression DoS", "Slug parser uses a catastrophic backtracking pattern"),
    ("javascript/generated_sql_injection_report.js", "JavaScript", "Medium", "CWE-89", "js/sql-injection", "js-sqli-001", "SQL Injection", "Generated report query concatenates request input"),
    # TypeScript: 13
    ("typescript/xss_account_banner.ts", "TypeScript", "Medium", "CWE-79", "js/xss", "ts-xss-001", "DOM XSS", "Account banner writes query text to innerHTML"),
    ("typescript/xss_search_title.ts", "TypeScript", "Medium", "CWE-79", "js/xss", "ts-xss-001", "DOM XSS", "Search title writes query text to document output"),
    ("typescript/xss_notification_panel.ts", "TypeScript", "Medium", "CWE-79", "js/xss", "ts-xss-001", "DOM XSS", "Notification panel writes query text to outerHTML"),
    ("typescript/redos_password_policy.ts", "TypeScript", "Medium", "CWE-1333", "js/redos", "ts-redos-001", "Regular Expression DoS", "Password policy uses a catastrophic backtracking pattern"),
    ("typescript/redos_route_matcher.ts", "TypeScript", "Medium", "CWE-1333", "js/redos", "ts-redos-001", "Regular Expression DoS", "Route matcher uses a catastrophic backtracking pattern"),
    ("typescript/redos_log_tokenizer.ts", "TypeScript", "Medium", "CWE-1333", "js/redos", "ts-redos-001", "Regular Expression DoS", "Log tokenizer uses a catastrophic backtracking pattern"),
    ("typescript/sql_injection_customer.ts", "TypeScript", "Medium", "CWE-89", "js/sql-injection", "ts-sqli-001", "SQL Injection", "Customer lookup query concatenates request input"),
    ("typescript/sql_injection_invoice.ts", "TypeScript", "Medium", "CWE-89", "js/sql-injection", "ts-sqli-001", "SQL Injection", "Invoice lookup query concatenates request input"),
    ("typescript/sql_injection_audit.ts", "TypeScript", "Medium", "CWE-89", "js/sql-injection", "ts-sqli-001", "SQL Injection", "Audit query concatenates request input"),
    ("typescript/path_injection_import.ts", "TypeScript", "High", "CWE-22", "js/path-injection", "ts-path-001", "Path Injection", "Import file path uses request input"),
    ("typescript/path_injection_export.ts", "TypeScript", "High", "CWE-22", "js/path-injection", "ts-path-001", "Path Injection", "Export file path uses request input"),
    ("typescript/code_injection_calculator.ts", "TypeScript", "Critical", "CWE-95", "js/code-injection", "ts-code-001", "Code Injection", "Calculator expression is evaluated from user input"),
    ("typescript/code_injection_rules_engine.ts", "TypeScript", "Critical", "CWE-95", "js/code-injection", "ts-code-001", "Code Injection", "Rules engine function is built from user input"),
    # Python: 14
    ("python/sql_injection_user_lookup.py", "Python", "Medium", "CWE-89", "py/sql-injection", "py-sqli-001", "SQL Injection", "User lookup SQL concatenates request input"),
    ("python/sql_injection_ticket_search.py", "Python", "Medium", "CWE-89", "py/sql-injection", "py-sqli-001", "SQL Injection", "Ticket search SQL formats request input"),
    ("python/sql_injection_report_filter.py", "Python", "Medium", "CWE-89", "py/sql-injection", "py-sqli-001", "SQL Injection", "Report SQL interpolates request input"),
    ("python/command_injection_converter.py", "Python", "High", "CWE-78", "py/command-injection", "py-cmd-001", "Command Injection", "Converter command runs with shell=True"),
    ("python/command_injection_backup.py", "Python", "High", "CWE-78", "py/command-injection", "py-cmd-001", "Command Injection", "Backup command runs with shell=True"),
    ("python/command_injection_archive.py", "Python", "High", "CWE-78", "py/command-injection", "py-cmd-001", "Command Injection", "Archive command runs with shell=True"),
    ("python/path_traversal_download.py", "Python", "High", "CWE-22", "py/path-injection", "py-path-001", "Path Traversal", "Download path is built from request input"),
    ("python/path_traversal_template.py", "Python", "High", "CWE-22", "py/path-injection", "py-path-001", "Path Traversal", "Template path is built from request input"),
    ("python/path_traversal_log_viewer.py", "Python", "High", "CWE-22", "py/path-injection", "py-path-001", "Path Traversal", "Log path is built from request input"),
    ("python/xss_profile_page.py", "Python", "Medium", "CWE-79", "py/reflective-xss", "py-xss-001", "Reflective XSS", "Profile page renders request input without escaping"),
    ("python/xss_search_page.py", "Python", "Medium", "CWE-79", "py/reflective-xss", "py-xss-001", "Reflective XSS", "Search page renders request input without escaping"),
    ("python/weak_hash_password_reset.py", "Python", "Medium", "CWE-916", "py/weak-sensitive-data-hashing", "py-hash-001", "Weak Hash", "Password reset token uses MD5"),
    ("python/weak_hash_api_key.py", "Python", "Medium", "CWE-916", "py/weak-sensitive-data-hashing", "py-hash-001", "Weak Hash", "API key digest uses SHA1"),
    ("python/sql_injection_test_fixture.py", "Python", "Medium", "CWE-89", "py/sql-injection", "py-sqli-001", "SQL Injection", "Test fixture query interpolates request input"),
    # Java: 16
    ("java/xxe_invoice_parser.java", "Java", "Medium", "CWE-611", "java/xxe", "java-xxe-001", "XXE", "Invoice XML parser allows external entities"),
    ("java/xxe_profile_import.java", "Java", "Medium", "CWE-611", "java/xxe", "java-xxe-001", "XXE", "Profile XML parser allows external entities"),
    ("java/xxe_partner_feed.java", "Java", "Medium", "CWE-611", "java/xxe", "java-xxe-001", "XXE", "Partner feed XML parser allows external entities"),
    ("java/exec_tainted_diagnostics.java", "Java", "Critical", "CWE-78", "java/exec-tainted-command", "java-exec-001", "Command Injection", "Diagnostics command uses request input"),
    ("java/exec_tainted_archive.java", "Java", "Critical", "CWE-78", "java/exec-tainted-command", "java-exec-001", "Command Injection", "Archive command uses request input"),
    ("java/exec_tainted_image_tool.java", "Java", "Critical", "CWE-78", "java/exec-tainted-command", "java-exec-001", "Command Injection", "Image tool command uses request input"),
    ("java/sql_injection_customer.java", "Java", "Medium", "CWE-89", "java/sql-injection", "java-sqli-001", "SQL Injection", "Customer query concatenates request input"),
    ("java/sql_injection_order.java", "Java", "Medium", "CWE-89", "java/sql-injection", "java-sqli-001", "SQL Injection", "Order query concatenates request input"),
    ("java/sql_injection_audit.java", "Java", "Medium", "CWE-89", "java/sql-injection", "java-sqli-001", "SQL Injection", "Audit query concatenates request input"),
    ("java/path_traversal_download.java", "Java", "High", "CWE-22", "java/path-injection", "java-path-001", "Path Traversal", "Download path uses request input"),
    ("java/path_traversal_template.java", "Java", "High", "CWE-22", "java/path-injection", "java-path-001", "Path Traversal", "Template path uses request input"),
    ("java/ldap_injection_people.java", "Java", "High", "CWE-90", "java/ldap-injection", "java-ldap-001", "LDAP Injection", "People lookup filter concatenates request input"),
    ("java/ldap_injection_groups.java", "Java", "High", "CWE-90", "java/ldap-injection", "java-ldap-001", "LDAP Injection", "Group lookup filter concatenates request input"),
    ("java/unsafe_deserialization_request.java", "Java", "High", "CWE-502", "java/unsafe-deserialization", "java-deser-001", "Unsafe Deserialization", "Request body is deserialized without validation"),
    ("java/unsafe_deserialization_cookie.java", "Java", "High", "CWE-502", "java/unsafe-deserialization", "java-deser-001", "Unsafe Deserialization", "Cookie payload is deserialized without validation"),
    ("java/unsafe_deserialization_cache.java", "Java", "High", "CWE-502", "java/unsafe-deserialization", "java-deser-001", "Unsafe Deserialization", "Cache payload is deserialized without validation"),
    # C#: 13
    ("csharp/sql_injection_customer.cs", "C#", "Medium", "CWE-89", "cs/sql-injection", "cs-sqli-001", "SQL Injection", "Customer query concatenates request input"),
    ("csharp/sql_injection_invoice.cs", "C#", "Medium", "CWE-89", "cs/sql-injection", "cs-sqli-001", "SQL Injection", "Invoice query concatenates request input"),
    ("csharp/sql_injection_audit.cs", "C#", "Medium", "CWE-89", "cs/sql-injection", "cs-sqli-001", "SQL Injection", "Audit query concatenates request input"),
    ("csharp/hardcoded_secret_database.cs", "C#", "High", "CWE-798", "cs/hardcoded-credentials", "cs-secret-001", "Hardcoded Credentials", "Database password is hardcoded"),
    ("csharp/hardcoded_secret_api.cs", "C#", "High", "CWE-798", "cs/hardcoded-credentials", "cs-secret-001", "Hardcoded Credentials", "API token is hardcoded"),
    ("csharp/hardcoded_secret_storage.cs", "C#", "High", "CWE-798", "cs/hardcoded-credentials", "cs-secret-001", "Hardcoded Credentials", "Storage key is hardcoded"),
    ("csharp/ldap_injection_people.cs", "C#", "High", "CWE-90", "cs/ldap-injection", "cs-ldap-001", "LDAP Injection", "People lookup filter concatenates request input"),
    ("csharp/ldap_injection_groups.cs", "C#", "High", "CWE-90", "cs/ldap-injection", "cs-ldap-001", "LDAP Injection", "Group lookup filter concatenates request input"),
    ("csharp/ldap_injection_roles.cs", "C#", "High", "CWE-90", "cs/ldap-injection", "cs-ldap-001", "LDAP Injection", "Role lookup filter concatenates request input"),
    ("csharp/path_traversal_download.cs", "C#", "High", "CWE-22", "cs/path-injection", "cs-path-001", "Path Traversal", "Download path uses request input"),
    ("csharp/path_traversal_template.cs", "C#", "High", "CWE-22", "cs/path-injection", "cs-path-001", "Path Traversal", "Template path uses request input"),
    ("csharp/weak_crypto_md5.cs", "C#", "Medium", "CWE-327", "cs/weak-crypto", "cs-crypto-001", "Weak Cryptography", "MD5 is used for sensitive digesting"),
    ("csharp/weak_crypto_sha1.cs", "C#", "Medium", "CWE-327", "cs/weak-crypto", "cs-crypto-001", "Weak Cryptography", "SHA1 is used for sensitive digesting"),
    # Go: 13
    ("go/open_redirect_login.go", "Go", "High", "CWE-601", "go/unvalidated-url-redirection", "go-redirect-001", "Open Redirect", "Login redirect target uses request input"),
    ("go/open_redirect_logout.go", "Go", "High", "CWE-601", "go/unvalidated-url-redirection", "go-redirect-001", "Open Redirect", "Logout redirect target uses request input"),
    ("go/open_redirect_invite.go", "Go", "High", "CWE-601", "go/unvalidated-url-redirection", "go-redirect-001", "Open Redirect", "Invite redirect target uses request input"),
    ("go/insecure_tls_client.go", "Go", "High", "CWE-295", "go/insecure-tls", "go-tls-001", "Insecure TLS", "HTTP client disables TLS certificate verification"),
    ("go/insecure_tls_transport.go", "Go", "High", "CWE-295", "go/insecure-tls", "go-tls-001", "Insecure TLS", "Transport disables TLS certificate verification"),
    ("go/insecure_tls_proxy.go", "Go", "High", "CWE-295", "go/insecure-tls", "go-tls-001", "Insecure TLS", "Proxy transport disables TLS certificate verification"),
    ("go/sql_injection_customer.go", "Go", "Medium", "CWE-89", "go/sql-injection", "go-sqli-001", "SQL Injection", "Customer query formats request input into SQL"),
    ("go/sql_injection_order.go", "Go", "Medium", "CWE-89", "go/sql-injection", "go-sqli-001", "SQL Injection", "Order query formats request input into SQL"),
    ("go/sql_injection_audit.go", "Go", "Medium", "CWE-89", "go/sql-injection", "go-sqli-001", "SQL Injection", "Audit query formats request input into SQL"),
    ("go/path_traversal_download.go", "Go", "High", "CWE-22", "go/path-injection", "go-path-001", "Path Traversal", "Download path uses request input"),
    ("go/path_traversal_template.go", "Go", "High", "CWE-22", "go/path-injection", "go-path-001", "Path Traversal", "Template path uses request input"),
    ("go/command_injection_archive.go", "Go", "High", "CWE-78", "go/command-injection", "go-cmd-001", "Command Injection", "Archive command uses request input"),
    ("go/command_injection_converter.go", "Go", "High", "CWE-78", "go/command-injection", "go-cmd-001", "Command Injection", "Converter command uses request input"),
]


def symbol(path: str) -> str:
    return re.sub(r"[^0-9A-Za-z_]", "_", Path(path).stem)


def class_name(path: str) -> str:
    return Path(path).stem


def header(prefix: str, title: str, cwe: str, rule: str, severity: str, group: str) -> str:
    return f"{prefix} INTENTIONAL VULNERABILITY: {title} ({cwe} / {rule} - {severity})\n{prefix} DUPLICATE_GROUP: {group}\n{prefix} This file exists for CodeQL SAST baseline testing only.\n"


def owner_path(file_path: str) -> str:
    return file_path.split("/", 1)[0]


def owner_team(file_path: str) -> str:
    return OWNER_TEAM_BY_PATH.get(owner_path(file_path), "@spgi-project-atom-sandbox/mock-security-team")


def classifications(file_path: str) -> list[str]:
    stem = Path(file_path).stem
    if stem.startswith("generated_"):
        return ["generated"]
    if stem.startswith("test_") or "_test" in stem:
        return ["test"]
    return ["source"]


def js_content(item: dict[str, str]) -> str:
    name = symbol(item["file"])
    h = header("//", item["title"], item["cwe"], item["rule"], item["severity"], item["duplicate_group"])
    if "sql-injection" in item["rule"]:
        return h + f"const express = require('express');\nconst app = express();\n\napp.get('/{name}', (req, res) => {{\n  const db = require('./db');\n  const value = req.query.value;\n  // VULN: user input is concatenated directly into SQL.\n  db.query(\"SELECT * FROM records WHERE owner = '\" + value + \"'\", (err, rows) => {{\n    res.json(rows);\n  }});\n}});\n"
    if "code-injection" in item["rule"]:
        if "function_body" in item["file"]:
            return h + f"function {name}(req, res) {{\n  const expression = req.query.expression || '';\n  // VULN: user input becomes executable JavaScript.\n  const runner = new Function('context', expression);\n  res.json({{ result: runner({{ user: req.user }}) }});\n}}\n\nmodule.exports = {name};\n"
        return h + f"function {name}(req, res) {{\n  const expression = req.query.expression || '';\n  // VULN: user input is evaluated as code.\n  const result = eval(expression);\n  res.json({{ result }});\n}}\n\nmodule.exports = {name};\n"
    if "path-injection" in item["rule"]:
        return h + f"const fs = require('fs');\nconst path = require('path');\n\nfunction {name}(req, res) {{\n  const requested = req.query.file || '';\n  // VULN: request input controls the filesystem path.\n  const target = path.join('/var/app/data', requested);\n  res.send(fs.readFileSync(target, 'utf8'));\n}}\n\nmodule.exports = {name};\n"
    if "xss" in item["rule"]:
        sink = "document.write('<section>' + value + '</section>');" if "comment" in item["file"] else "document.getElementById('output').innerHTML = value;"
        return h + f"function {name}(req) {{\n  const value = req.query.message || '';\n  // VULN: request input is written to the DOM without escaping.\n  {sink}\n}}\n\nmodule.exports = {name};\n"
    return h + f"const vulnerablePattern = /^([a-zA-Z0-9]+)*$/;\n\nfunction {name}(input) {{\n  // VULN: nested quantifiers can cause catastrophic backtracking.\n  return vulnerablePattern.test(input);\n}}\n\nmodule.exports = {name};\n"


def ts_content(item: dict[str, str]) -> str:
    name = symbol(item["file"])
    h = header("//", item["title"], item["cwe"], item["rule"], item["severity"], item["duplicate_group"])
    req_type = "{ query: Record<string, string | undefined> }"
    if "xss" in item["rule"]:
        sink = "document.write('<h1>' + value + '</h1>');" if "search" in item["file"] else "document.getElementById('output')!.innerHTML = value;"
        if "notification" in item["file"]:
            sink = "document.getElementById('notice')!.outerHTML = value;"
        return h + f"function {name}(req: {req_type}): void {{\n  const value = req.query.message ?? '';\n  // VULN: request input is written to the DOM without escaping.\n  {sink}\n}}\n\nexport {{ {name} }};\n"
    if "redos" in item["rule"]:
        return h + f"const vulnerablePattern = /^([a-zA-Z0-9]+)*$/;\n\nfunction {name}(input: string): boolean {{\n  // VULN: nested quantifiers can cause catastrophic backtracking.\n  return vulnerablePattern.test(input);\n}}\n\nexport {{ {name} }};\n"
    if "sql-injection" in item["rule"]:
        return h + f"type Database = {{ query(sql: string): Promise<unknown> }};\n\nfunction {name}(db: Database, req: {req_type}): Promise<unknown> {{\n  const value = req.query.value ?? '';\n  // VULN: request input is concatenated directly into SQL.\n  return db.query(\"SELECT * FROM records WHERE owner = '\" + value + \"'\");\n}}\n\nexport {{ {name} }};\n"
    if "path-injection" in item["rule"]:
        return h + f"import * as fs from 'fs';\nimport * as path from 'path';\n\nfunction {name}(req: {req_type}): string {{\n  const requested = req.query.file ?? '';\n  // VULN: request input controls the filesystem path.\n  const target = path.join('/var/app/data', requested);\n  return fs.readFileSync(target, 'utf8');\n}}\n\nexport {{ {name} }};\n"
    return h + f"function {name}(req: {req_type}): unknown {{\n  const expression = req.query.expression ?? '';\n  // VULN: user input is evaluated as code.\n  return eval(expression);\n}}\n\nexport {{ {name} }};\n"


def py_content(item: dict[str, str]) -> str:
    name = symbol(item["file"])
    h = header("#", item["title"], item["cwe"], item["rule"], item["severity"], item["duplicate_group"])
    if "sql-injection" in item["rule"]:
        return h + f"from flask import request\n\n\ndef {name}(db):\n    value = request.args.get('value', '')\n    # VULN: request input is concatenated directly into SQL.\n    return db.execute(\"SELECT * FROM records WHERE owner = '\" + value + \"'\")\n"
    if "command-injection" in item["rule"]:
        return h + f"import subprocess\nfrom flask import request\n\n\ndef {name}():\n    target = request.args.get('target', '')\n    # VULN: shell=True runs a command that includes request input.\n    subprocess.call(f\"convert {{target}} output.png\", shell=True)\n    return 'done'\n"
    if "path-injection" in item["rule"]:
        return h + f"from pathlib import Path\nfrom flask import request\n\n\ndef {name}():\n    requested = request.args.get('file', '')\n    # VULN: request input controls the filesystem path.\n    target = Path('/var/app/data') / requested\n    return target.read_text()\n"
    if "reflective-xss" in item["rule"]:
        return h + f"from flask import request\n\n\ndef {name}():\n    value = request.args.get('message', '')\n    # VULN: request input is rendered without escaping.\n    return f\"<html><body>{{value}}</body></html>\"\n"
    algo = "sha1" if "api_key" in item["file"] else "md5"
    return h + f"import hashlib\nfrom flask import request\n\n\ndef {name}():\n    value = request.args.get('token', '').encode('utf-8')\n    # VULN: weak hashing is used for sensitive data.\n    return hashlib.{algo}(value).hexdigest()\n"


def java_content(item: dict[str, str]) -> str:
    cls = class_name(item["file"])
    h = header("//", item["title"], item["cwe"], item["rule"], item["severity"], item["duplicate_group"])
    if "unsafe-deserialization" in item["rule"]:
        if "cookie" in item["file"]:
            return h + f"import java.io.ByteArrayInputStream;\nimport java.io.ObjectInputStream;\nimport java.util.Base64;\nimport javax.servlet.http.HttpServletRequest;\n\npublic class {cls} {{\n    public Object deserialize(HttpServletRequest request) throws Exception {{\n        String payload = request.getParameter(\"session\");\n        byte[] data = Base64.getDecoder().decode(payload);\n        // VULN: cookie-controlled bytes are deserialized without validation.\n        ObjectInputStream stream = new ObjectInputStream(new ByteArrayInputStream(data));\n        return stream.readObject();\n    }}\n}}\n"
        if "cache" in item["file"]:
            return h + f"import java.io.ByteArrayInputStream;\nimport java.io.ObjectInputStream;\nimport javax.servlet.http.HttpServletRequest;\n\npublic class {cls} {{\n    public Object deserialize(HttpServletRequest request) throws Exception {{\n        String payload = request.getParameter(\"cache\");\n        byte[] data = payload.getBytes();\n        // VULN: request-controlled cache bytes are deserialized without validation.\n        ObjectInputStream stream = new ObjectInputStream(new ByteArrayInputStream(data));\n        return stream.readObject();\n    }}\n}}\n"
        return h + f"import java.io.ObjectInputStream;\nimport javax.servlet.http.HttpServletRequest;\n\npublic class {cls} {{\n    public Object deserialize(HttpServletRequest request) throws Exception {{\n        // VULN: request body bytes are deserialized without validation.\n        ObjectInputStream stream = new ObjectInputStream(request.getInputStream());\n        return stream.readObject();\n    }}\n}}\n"
    if "xxe" in item["rule"]:
        return h + f"import javax.xml.parsers.DocumentBuilderFactory;\nimport org.w3c.dom.Document;\nimport java.io.InputStream;\n\npublic class {cls} {{\n    public Document parse(InputStream input) throws Exception {{\n        // VULN: external entity resolution is not disabled.\n        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();\n        return factory.newDocumentBuilder().parse(input);\n    }}\n}}\n"
    if "exec" in item["rule"]:
        return h + f"import javax.servlet.http.HttpServletRequest;\nimport java.io.IOException;\n\npublic class {cls} {{\n    public void handle(HttpServletRequest request) throws IOException {{\n        String command = request.getParameter(\"cmd\");\n        // VULN: request input flows directly into exec().\n        Runtime.getRuntime().exec(command);\n    }}\n}}\n"
    if "sql-injection" in item["rule"]:
        return h + f"import javax.servlet.http.HttpServletRequest;\nimport java.sql.Connection;\nimport java.sql.ResultSet;\nimport java.sql.Statement;\n\npublic class {cls} {{\n    public ResultSet find(Connection connection, HttpServletRequest request) throws Exception {{\n        String value = request.getParameter(\"value\");\n        Statement statement = connection.createStatement();\n        // VULN: request input is concatenated directly into SQL.\n        return statement.executeQuery(\"SELECT * FROM records WHERE owner = '\" + value + \"'\");\n    }}\n}}\n"
    if "path-injection" in item["rule"]:
        return h + f"import javax.servlet.http.HttpServletRequest;\nimport java.nio.file.Files;\nimport java.nio.file.Path;\n\npublic class {cls} {{\n    public String read(HttpServletRequest request) throws Exception {{\n        String requested = request.getParameter(\"file\");\n        // VULN: request input controls the filesystem path.\n        Path target = Path.of(\"/var/app/data\", requested);\n        return Files.readString(target);\n    }}\n}}\n"
    return h + f"import javax.servlet.http.HttpServletRequest;\nimport javax.naming.directory.DirContext;\nimport javax.naming.directory.SearchControls;\n\npublic class {cls} {{\n    public Object search(DirContext context, HttpServletRequest request) throws Exception {{\n        String value = request.getParameter(\"value\");\n        // VULN: request input is concatenated into an LDAP filter.\n        String filter = \"(uid=\" + value + \")\";\n        return context.search(\"ou=people,dc=example,dc=com\", filter, new SearchControls());\n    }}\n}}\n"


def cs_content(item: dict[str, str]) -> str:
    cls = ''.join(part.capitalize() for part in symbol(item["file"]).split('_'))
    h = header("//", item["title"], item["cwe"], item["rule"], item["severity"], item["duplicate_group"])
    if "sql-injection" in item["rule"]:
        return h + f"using System.Data.SqlClient;\n\npublic class {cls}\n{{\n    public SqlCommand Build(string owner)\n    {{\n        // VULN: user input is concatenated directly into SQL.\n        return new SqlCommand(\"SELECT * FROM Records WHERE Owner = '\" + owner + \"'\");\n    }}\n}}\n"
    if "hardcoded" in item["rule"]:
        return h + f"public class {cls}\n{{\n    public string GetSecret()\n    {{\n        // VULN: credential is hardcoded in source.\n        return \"P@ssw0rd-Do-Not-Use-12345\";\n    }}\n}}\n"
    if "ldap" in item["rule"]:
        return h + f"using System.DirectoryServices;\n\npublic class {cls}\n{{\n    public DirectorySearcher Build(string value)\n    {{\n        // VULN: user input is concatenated into an LDAP filter.\n        return new DirectorySearcher(\"(uid=\" + value + \")\");\n    }}\n}}\n"
    if "path" in item["rule"]:
        return h + f"using System.IO;\n\npublic class {cls}\n{{\n    public string Read(string file)\n    {{\n        // VULN: user input controls the filesystem path.\n        string target = Path.Combine(\"/var/app/data\", file);\n        return File.ReadAllText(target);\n    }}\n}}\n"
    algo = "SHA1" if "sha1" in item["file"] else "MD5"
    return h + f"using System.Security.Cryptography;\nusing System.Text;\n\npublic class {cls}\n{{\n    public byte[] Digest(string value)\n    {{\n        // VULN: weak cryptography is used for sensitive data.\n        using var hash = {algo}.Create();\n        return hash.ComputeHash(Encoding.UTF8.GetBytes(value));\n    }}\n}}\n"


def go_content(item: dict[str, str]) -> str:
    name = ''.join(part.capitalize() for part in symbol(item["file"]).split('_'))
    h = header("//", item["title"], item["cwe"], item["rule"], item["severity"], item["duplicate_group"])
    if "redirection" in item["rule"]:
        return h + f"package main\n\nimport \"net/http\"\n\nfunc {name}(w http.ResponseWriter, r *http.Request) {{\n\ttarget := r.URL.Query().Get(\"next\")\n\t// VULN: request input controls the redirect destination.\n\thttp.Redirect(w, r, target, http.StatusFound)\n}}\n"
    if "insecure-tls" in item["rule"]:
        return h + f"package main\n\nimport (\n\t\"crypto/tls\"\n\t\"net/http\"\n)\n\nfunc {name}() *http.Client {{\n\t// VULN: certificate verification is disabled.\n\ttransport := &http.Transport{{TLSClientConfig: &tls.Config{{InsecureSkipVerify: true}}}}\n\treturn &http.Client{{Transport: transport}}\n}}\n"
    if "sql-injection" in item["rule"]:
        return h + f"package main\n\nimport (\n\t\"database/sql\"\n\t\"fmt\"\n\t\"net/http\"\n)\n\nfunc {name}(db *sql.DB, r *http.Request) (*sql.Rows, error) {{\n\tvalue := r.URL.Query().Get(\"value\")\n\t// VULN: request input is formatted directly into SQL.\n\tquery := fmt.Sprintf(\"SELECT * FROM records WHERE owner = '%s'\", value)\n\treturn db.Query(query)\n}}\n"
    if "path-injection" in item["rule"]:
        return h + f"package main\n\nimport (\n\t\"net/http\"\n\t\"os\"\n\t\"path/filepath\"\n)\n\nfunc {name}(r *http.Request) ([]byte, error) {{\n\trequested := r.URL.Query().Get(\"file\")\n\t// VULN: request input controls the filesystem path.\n\ttarget := filepath.Join(\"/var/app/data\", requested)\n\treturn os.ReadFile(target)\n}}\n"
    return h + f"package main\n\nimport (\n\t\"net/http\"\n\t\"os/exec\"\n)\n\nfunc {name}(r *http.Request) error {{\n\ttarget := r.URL.Query().Get(\"target\")\n\t// VULN: request input flows into an operating system command.\n\treturn exec.Command(\"sh\", \"-c\", \"convert \"+target+\" output.png\").Run()\n}}\n"


CONTENT_BUILDERS = {
    "JavaScript": js_content,
    "TypeScript": ts_content,
    "Python": py_content,
    "Java": java_content,
    "C#": cs_content,
    "Go": go_content,
}


def normalize_fixture(raw: tuple[str, str, str, str, str, str, str, str]) -> dict[str, str]:
    file, language, severity, cwe, rule, duplicate_group, title, description = raw
    return {
        "file": file,
        "language": language,
        "severity": severity,
        "cwe": cwe,
        "rule": rule,
        "duplicate_group": duplicate_group,
        "title": title,
        "description": description,
        "owner_team": owner_team(file),
        "owner_path": owner_path(file),
        "classifications": classifications(file),
        "confidence": "high",
        "target_repository": TARGET_REPOSITORY,
    }


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def vuln_line(content: str) -> int:
    for index, line in enumerate(content.splitlines(), start=1):
        if "VULN:" in line:
            return index
    return 1


def render_readme(fixtures: list[dict[str, str]]) -> str:
    rows = "\n".join(
        f"| {item['file']} | {item['language']} | {item['severity']} | {item['cwe']} | {item['rule']} | {item['duplicate_group']} | {item['owner_team']} | {item['owner_path']} | {', '.join(item['classifications'])} |"
        for item in fixtures
    )
    return f"""# codeql-test-comprehensive

Large multi-language CodeQL SAST regression test repo. It contains {len(fixtures)} planned intentional findings across JavaScript, TypeScript, Python, Java, C#, and Go, with duplicate groups repeated across different files for later dedupe and burndown exercises.

| File | Language | Severity | CWE | CodeQL Rule | Duplicate Group | Owner Team | Owner Path | Classifications |
|------|----------|----------|-----|-------------|-----------------|------------|------------|-----------------|
{rows}

> Test repo only. All vulnerabilities are intentional for CodeQL rule validation.
"""


def render_vulnerabilities(fixtures: list[dict[str, str]]) -> str:
    rows = "\n".join(
        f"| {item['file']} | {item['line']} | {item['language']} | {item['severity']} | {item['cwe']} | {item['rule']} | {item['duplicate_group']} | {item['owner_team']} | {item['owner_path']} | {', '.join(item['classifications'])} | {item['description']} |"
        for item in fixtures
    )
    return f"""# Vulnerability Index

| File | Lines | Language | Severity | CWE | CodeQL Rule ID | Duplicate Group | Owner Team | Owner Path | Classifications | Description |
|------|-------|----------|----------|-----|----------------|-----------------|------------|------------|-----------------|-------------|
{rows}
"""


def main() -> None:
    fixtures = [normalize_fixture(item) for item in FIXTURES]
    for item in fixtures:
        content = CONTENT_BUILDERS[item["language"]](item)
        item["line"] = str(vuln_line(content))
        write(ROOT / item["file"], content)

    write(ROOT / ".github/workflows/codeql.yml", WORKFLOW)
    write(ROOT / ".gitignore", GITIGNORE)
    write(ROOT / ".github/CODEOWNERS", CODEOWNERS)
    write(ROOT / "go.mod", "module codeql-test-comprehensive\n\ngo 1.22\n")
    write(ROOT / "README.md", render_readme(fixtures))
    write(ROOT / "VULNERABILITIES.md", render_vulnerabilities(fixtures))
    write(ROOT / "fixtures.json", json.dumps(fixtures, indent=2) + "\n")


if __name__ == "__main__":
    main()
