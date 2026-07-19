# CodeQL CCA Burndown Grouping Test Matrix

## Purpose

This repository is a multi-language CodeQL fixture target for testing CCA burndown grouping strategies. The generated fixtures include repeated rule families, varied severities, path-based ownership, and classification examples so planners can prove they are creating useful batches before they touch real application repositories.

The primary grouping modes under test are:

- `rule-family`: group related findings by CodeQL rule ID and remediation pattern.
- `risk-first`: prioritize critical and high findings before lower-risk backlog items.
- `ownership-path`: route batches to the mock team that owns the affected source path.

## Mock Ownership Model

Ownership is generated into `.github/CODEOWNERS` and duplicated into `fixtures.json` for fixture-mode planners.

| Path | Mock team |
|------|-----------|
| `/javascript/` | `@example-org/mock-frontend-web` |
| `/typescript/` | `@example-org/mock-frontend-web` |
| `/python/` | `@example-org/mock-backend-python` |
| `/java/` | `@example-org/mock-services-java` |
| `/csharp/` | `@example-org/mock-enterprise-dotnet` |
| `/go/` | `@example-org/mock-infrastructure-go` |
| `/.github/`, `/docs/`, fallback | `@example-org/mock-security-team` |

## Rule-Family Coverage

Rule-family grouping should find repeated CodeQL rule IDs within one repository and produce bounded batches for similar fixes. The fixture set includes repeated examples of SQL injection, command injection, path traversal, XSS, LDAP injection, weak crypto, open redirect, insecure TLS, and other recurring patterns.

New coverage added for grouping tests:

| Rule family | Files | Why it matters |
|-------------|-------|----------------|
| `java/unsafe-deserialization` | 3 | Adds a high-severity Java rule family with request, cookie, and cache payload variants. |
| `js/sql-injection` | 4 | Adds one generated JavaScript fixture so planners can test classification filtering within a normal repeated rule family. |
| `py/sql-injection` | 4 | Adds one Python test fixture so planners can test excluding test-code findings from production burndown. |

## Risk-First Coverage

Risk-first grouping should sort critical and high findings ahead of medium findings while still preserving reviewable batch size. The fixture set has critical JavaScript and TypeScript code injection, critical Java command injection, high path traversal and command injection, and the new high Java unsafe deserialization set.

Expected severity behavior:

| Severity | Example rule families |
|----------|-----------------------|
| Critical | `js/code-injection`, `java/exec-tainted-command` |
| High | `java/unsafe-deserialization`, path traversal, LDAP injection, command injection, insecure TLS, open redirect |
| Medium | SQL injection, XSS, ReDoS, weak hash, weak crypto, XXE |

## Ownership-Path Coverage

Ownership-path grouping should keep batches inside a single owner boundary. This is especially useful for simulating monorepo review routing and human-in-the-middle CCA assignment.

Expected owner routing by generated fixture count:

| Owner path | Count | Mock team |
|------------|------:|-----------|
| `javascript` | 14 | `@example-org/mock-frontend-web` |
| `typescript` | 13 | `@example-org/mock-frontend-web` |
| `python` | 14 | `@example-org/mock-backend-python` |
| `java` | 16 | `@example-org/mock-services-java` |
| `csharp` | 13 | `@example-org/mock-enterprise-dotnet` |
| `go` | 13 | `@example-org/mock-infrastructure-go` |
| **Total** | **83** | |

## Classification Coverage

The generator assigns classifications using filename conventions so fixture behavior stays deterministic.

| Classification | Convention | Fixture example | Planner use |
|----------------|------------|-----------------|-------------|
| `source` | Default for normal generated vulnerable files | `java/sql_injection_customer.java` | Included in normal burndown batches. |
| `generated` | Filename starts with `generated_` | `javascript/generated_sql_injection_report.js` | Excluded by default for source-only campaigns. |
| `test` | Filename starts with `test_` or contains `_test` | `python/sql_injection_test_fixture.py` | Excluded by default for production-code burndown. |

## Validation Checklist

After running `python3 scripts/generate_fixtures.py`, validate that:

1. `fixtures.json` contains 83 findings.
2. Every fixture includes `owner_team`, `owner_path`, `classifications`, `confidence`, and `target_repository`.
3. `.github/CODEOWNERS` exists and maps each language path to a mock team.
4. `README.md` and `VULNERABILITIES.md` include owner and classification columns.
5. The five new fixture files exist and include `VULN:` markers.
6. A fixture-mode planner can exclude `generated` and `test` classifications while grouping remaining `source` findings.
