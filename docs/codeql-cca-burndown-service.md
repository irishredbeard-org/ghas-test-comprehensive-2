# CodeQL CCA Burndown Service Plan

## Purpose

Create a repeatable service that uses GitHub CCA as the agentic remediation infrastructure for burning down existing CodeQL findings without overwhelming product teams or developers. The service should produce small, reviewable PRs, group related findings where it is safe to do so, and give security and product owners a clear operating model for prioritization, audit, and progress tracking.

This is not a plan to fix every alert in one run. The goal is controlled throughput: identify the right batch, create a high-quality fix PR, prove the fix, route it to the right owners, and move to the next batch.

## Design Principles

1. Keep each PR reviewable by one team.
2. Prefer root-cause fixes over suppressions or blanket dismissals.
3. Separate finding selection from code editing. A deterministic planner should choose the batch; CCA should remediate the chosen batch.
4. Prevent new findings while burning down old findings. The backlog cannot shrink if new alerts continue to enter main. (done outside of this project so ignore)
5. Use objective gates before automation touches code: severity, ownership, file paths, alert age, confidence, and expected blast radius.
6. Treat CodeQL state as data. Every campaign should be reproducible from an alert inventory snapshot.
7. Keep humans in the merge path. CCA opens PRs; repository owners approve and merge.

## Data Sources

Use the GitHub code scanning APIs and repository metadata to build a normalized finding inventory.

Primary alert fields:

- Organization, repository, default branch, archived status, and visibility.
- Alert number and URL.
- Alert state: open, fixed, dismissed.
- `rule.id`, `rule.name`, `rule.description`, `rule.help_uri`.
- `rule.security_severity_level` and `rule.severity`.
- `tool.name`, expected to be CodeQL for this service.
- `most_recent_instance.location.path`, start line, end line, and message.
- `most_recent_instance.classifications`, especially source, generated, test, and library.
- `created_at` and `updated_at`.
- Assignees, dismissal fields, and fixed timestamp where present.

Useful API entry points:

- `GET /orgs/{org}/code-scanning/alerts?tool_name=CodeQL&state=open&per_page=100`
- `GET /repos/{owner}/{repo}/code-scanning/alerts?tool_name=CodeQL&state=open&per_page=100`
- `GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}/instances`
- `GET /repos/{owner}/{repo}/code-scanning/analyses`

Supplemental metadata:

- CODEOWNERS, repository teams, topics, custom properties, and product ownership data.
- Language mix from repository languages or CodeQL analysis categories.
- Recent commit activity and open PR count.
- Branch protection and required status checks.
- Whether CodeQL is configured and healthy.

## Service Shape

The service should have five logical parts.

### 1. Inventory Collector

Runs on a schedule and on demand. It queries CodeQL alerts, normalizes them into a durable dataset, enriches them with repo ownership and path ownership, and stores snapshots for audit and trend reporting.

Output examples:

- `alerts-{date}.jsonl`
- `repo-summary-{date}.csv`
- `campaign-candidates-{date}.json`

### 2. Batch Planner

Builds proposed work items from the inventory. This is the key piece for avoiding one giant run or one alert per PR. The planner should generate a batch manifest that CCA must follow exactly.

Example batch manifest:

```json
{
  "campaign_id": "codeql-2026-q3-sql-injection-high",
  "repository": "org/example-service",
  "base_branch": "main",
  "strategy": "rule-family",
  "max_alerts": 5,
  "alerts": [
    {
      "number": 123,
      "rule_id": "java/sql-injection",
      "severity": "high",
      "path": "src/main/java/com/example/UserDao.java",
      "start_line": 84,
      "url": "https://github.com/org/example-service/security/code-scanning/123"
    }
  ],
  "allowed_paths": ["src/main/java/com/example/**"],
  "blocked_paths": [".github/**", "generated/**"],
  "validation_commands": ["mvn -q -DskipTests compile"],
  "owner_team": "team-example-platform"
}
```

### 3. CCA Remediation Runner

CCA receives only one manifest at a time. It checks out the target repository, reads the manifest, fixes only the specified alerts, runs bounded validation, and opens a PR. For the initial POC lets just have human in the loop to assign to CCA.

Expected behavior:

- Create branch named `codeql-burndown/{campaign_id}/{batch_id}`.
- Modify only allowed paths unless the manifest explicitly permits support files.
- Do not suppress alerts with CodeQL ignore comments unless the campaign explicitly allows a dismissal-only workflow.
- Do not reformat unrelated code.
- Include alert links and validation output in the PR body.
- Open draft PR if validation is incomplete or confidence is low.

### 4. Verification Gate

Every PR should prove that it is likely to close the intended findings.

Minimum gates:

- Local build or language-specific fast check, when available.
- CodeQL rerun or code scanning status on the PR.
- No net-new CodeQL findings in the PR.
- Changed file count and diff size under configured thresholds.
- Human review from CODEOWNERS or mapped product team.

Most of this is probably in the default CCA flow but do verify

### 5. Reporting And Audit

Skip this in POC as we are workin on this outside of this project.

Track both throughput and quality.

Metrics:

- Open CodeQL alerts by org, repo, severity, rule, and owner.
- Alerts selected, PRs opened, PRs merged, PRs closed without merge.
- Median time from campaign selection to PR open.
- Median time from PR open to merge.
- Rework rate: PRs requiring major changes, failing builds, or causing reverted fixes.
- Alert closure confirmation after merge.
- CCA token and runner cost per merged alert.

Audit records:

- Inventory snapshot used for planning.
- Batch manifest sent to CCA.
- CCA run logs and sandbox/network logs where available.
- PR URL, reviewers, checks, and merge SHA.
- Alerts confirmed fixed after merge.

## Burndown Methodology Options

### Option 1: Risk-First Fixed Batch

Pick the highest-risk findings first, but cap each PR by alert count, file count, and owner scope.

Batching rule:

- Same repository.
- Same owner team.
- Critical before high before medium.
- Application code before test/generated/library code.
- Maximum 3 critical alerts or 5 high alerts per PR.
- Maximum 5 files or 300 changed lines per PR unless manually approved.

Best for:

- Executive-visible risk reduction.
- Repositories with a small number of severe findings.
- Early pilots where trust in automation is still forming.

Pros:

- Easy to explain.
- Optimizes for risk reduction.
- Keeps PRs small.

Cons:

- May jump between rule types, languages, and code areas.
- Can miss efficiency gains from fixing many similar issues together.

Action path:

1. Inventory all open critical and high CodeQL alerts.
2. Exclude generated/test/library classifications for the first wave unless the product team asks to include them.
3. Sort by severity, repo criticality, and age.
4. Build one manifest per repository and owner team.
5. Run CCA for the top 10 batches and measure acceptance rate.

### Option 2: Rule-Family Campaigns

Group alerts by CodeQL rule ID or rule family, then fix the same vulnerability pattern across one repo or a small set of closely related repos.

Batching rule:

- Same `rule.id` or same remediation pattern.
- Same language ecosystem.
- Prefer same repository; allow multiple repos only when the owning team and build model are the same.
- Maximum 5 to 10 alerts per PR if the fix is repetitive and low-risk.

Example campaigns:

- SQL injection parameterization.
- Unsafe path traversal checks.
- Weak hash replacement.
- XSS output encoding.
- Unsafe deserialization cleanup.

Best for:

- Backlogs with many repeated findings.
- Creating reusable CCA prompts and validation playbooks.
- Training product teams on one secure coding pattern at a time.

Pros:

- Efficient for repeated issues.
- CCA can apply a consistent fix pattern.
- Easier to create reusable remediation guidance.

Cons:

- Some rules require deep business-context judgment.
- Multi-repo campaigns can become noisy if build/test systems differ.

Action path:

1. Rank rule IDs by count, severity, and affected repos.
2. Select the top rule family with high confidence and clear remediation guidance.
3. Create a campaign prompt addendum for that rule family.
4. Run CCA against one repo first.
5. Expand to more repos only after two or three successful merges.

### Option 3: Ownership And Path-Based Batches

Group findings by CODEOWNERS or product ownership so each PR lands with the team that understands the code.

Batching rule:

- Same repository.
- Same CODEOWNERS match or product component.
- Multiple rule IDs allowed only when they are in the same code area.
- Maximum 5 alerts per PR.

Best for:

- Large monorepos.
- Repositories where teams own distinct directories.
- Reducing review routing friction.

Pros:

- Best alignment with human review.
- Avoids PRs that span unrelated components.
- Helps product teams plan capacity.

Cons:

- May mix vulnerability types.
- Requires reliable ownership metadata.

Action path:

1. Parse CODEOWNERS and map every alert path to an owner.
2. Create owner-level queues.
3. Let teams opt into weekly capacity, such as two CCA PRs per week.
4. Use CCA to create PRs only within each owner's allowed path set.

### Option 4: Repository Wave Campaigns

Pick a set of repositories and burn each one down to a target threshold before moving on.

Batching rule:

- Select repos by business criticality, active development, or audit scope.
- Within a repo, use risk-first or rule-family batching.
- Stop when the repo reaches a target, such as zero critical/high alerts or 80 percent reduction.

Best for:

- Compliance programs.
- High-value applications.
- Product teams willing to reserve review time.

Pros:

- Clear repo-level outcome.
- Easier stakeholder communication.
- Good for before/after reporting.

Cons:

- Lower-severity findings in selected repos may be fixed before higher-risk findings elsewhere.
- Can overload one team if not paced.

Action path:

1. Choose 5 to 10 pilot repositories.
2. Baseline their CodeQL backlog.
3. Agree on a weekly PR budget per repo.
4. Run batches until each repo reaches the campaign exit target.

### Option 5: Age And SLA-Based Burndown

Prioritize alerts that are oldest or outside SLA, with severity weighting.

Batching rule:

- Critical alerts over SLA first.
- High alerts over SLA second.
- Group by owner and repository.
- Defer new alerts to the new-finding prevention workflow.

Best for:

- Organizations with formal vulnerability management deadlines.
- Audit evidence.
- Reducing long-tail backlog.

Pros:

- Maps naturally to policy.
- Easy to report.
- Prevents very old alerts from being ignored.

Cons:

- Old does not always mean highest risk.
- May send CCA into stale code with weak test coverage.

Action path:

1. Define severity SLAs.
2. Mark every alert as within SLA or over SLA.
3. Generate weekly over-SLA batches.
4. Report exceptions where CCA cannot safely remediate.


### Option 6: Native CodeQL Autofix API As A First Pass

For eligible single alerts, call GitHub's CodeQL autofix API to generate a candidate patch, then use CCA to review, adapt, validate, and package the PR.

Batching rule:

- Use for one alert at a time or for small same-rule batches where each alert has an autofix candidate.
- CCA remains responsible for validating and composing the final branch.

Best for:

- Alerts where GitHub already has high-confidence autofix support.
- Fast pilots.
- Comparing native autofix quality with full CCA remediation.

Pros:

- May reduce CCA token usage.
- Gives a baseline quality comparison.
- Useful for simple vulnerability classes.

Cons:

- Not every alert has an autofix.
- Native autofix may be too narrow or miss project-specific validation.
- Multi-alert coordination still needs the batch planner.

Action path:

1. Add an `autofix_available` probe to the inventory collector.
2. For eligible alerts, request native autofix.
3. Let CCA inspect the proposed patch, adjust if needed, run validation, and open the PR.
4. Track acceptance rate separately from full CCA fixes.

## Recommended Starting Model

Use a hybrid of Option 2 and Option 6:

1. Prevent new findings with a PR delta workflow.
2. Burn down existing findings through rule-family campaigns.
3. Keep repository ownership as a hard boundary for PR creation.
4. Use risk-first ordering inside each rule-family queue.

This gives the best balance of scale and reviewability. It lets the service learn one vulnerability pattern at a time, while the PR delta workflow stops the backlog from growing.

Recommended first campaign:

- Scope: one organization, 5 to 10 repositories, CodeQL only.
- Severity: critical and high.
- Code classification: application code only.
- Batch type: same rule ID, same repo, same owner.
- PR cap: 5 alerts, 5 files, 300 changed lines.
- Frequency: no more than two CCA burndown PRs per repo per week during pilot.
- Exit target: 80 percent reduction in pilot critical/high alerts or zero remaining high-confidence critical/high alerts.

## Batch Scoring Model

Use a simple scoring model so the planner can explain why a batch was selected.

Example score:

```text
score = severity_weight
      + repo_criticality_weight
      + age_weight
      + exploitability_hint_weight
      + repeatability_weight
      - blast_radius_penalty
      - ownership_uncertainty_penalty
      - validation_uncertainty_penalty
```

Suggested starting weights:

| Factor | Weight |
| --- | ---: |
| Critical severity | +100 |
| High severity | +60 |
| Medium severity | +25 |
| Tier 1/business-critical repo | +40 |
| Alert older than SLA | +30 |
| Same rule appears 5+ times in same repo | +25 |
| Clear CODEOWNER | +15 |
| Touches generated/test/library code | -30 |
| No obvious validation command | -20 |
| Would touch more than 5 files | -40 |
| Crosses owner boundaries | -50 |

## PR Size Rules

These limits should be configurable, but the pilot needs conservative defaults.

Default caps:

- Maximum 5 alerts per PR.
- Maximum 1 rule family per PR.
- Maximum 1 repository per PR.
- Maximum 1 owner team per PR.
- Maximum 5 changed files.
- Maximum 300 changed lines.
- Maximum 30 minutes of CCA runtime.
- Maximum one retry per failed batch before human triage.

Escalate to manual approval when:

- The fix requires dependency upgrades.
- The fix changes authentication, authorization, crypto, request routing, or data models.
- The fix requires broad refactoring.
- The same alert appears to be a false positive.
- Validation cannot run or CodeQL results are inconclusive.

## CCA Prompt Contract

The CCA agent should receive a narrow contract.

Required instructions:

- Read `codeql-burndown/manifest.json` first.
- Fix only the listed alert numbers.
- Edit only allowed paths.
- Do not dismiss or suppress findings unless the manifest says the batch is triage-only.
- Prefer minimal root-cause fixes.
- Run listed validation commands.
- Create one PR with alert links, summary, validation, and residual risk.
- If blocked, open an issue with the blocked reason and no code changes.

Useful output labels:

- `codeql-burndown`
- `security`
- `cca-generated`
- `needs-owner-review`
- `validation-incomplete`
- `autofix-blocked`

## Operating Modes

### Dry Run

Planner produces candidate batches only. No CCA run. This is for validating grouping, ownership, and PR sizing assumptions.

### Draft PR Mode

CCA opens draft PRs. Product owners review but are not expected to merge quickly. This is best for the pilot.

### Active Burndown Mode

CCA opens ready-for-review PRs with required checks. Teams agree to review within a defined window.

### Assisted Triage Mode

CCA does not edit code. It creates issues explaining why alerts may be false positives, require business context, or need larger refactoring. Use this for noisy or complex rule families.

## Implementation Plan

### Phase 0: Inventory And Baseline

Actions:

1. Build a script to export open CodeQL alerts for one org.
2. Normalize alerts into JSONL and CSV.
3. Add ownership enrichment from CODEOWNERS and repo metadata.
4. Produce top lists by repo, rule ID, severity, owner, and age.
5. Identify generated/test/library findings and exclude them from the first pilot.

Deliverables:

- Inventory snapshot.
- Top 20 campaign candidates.
- Recommended pilot repositories.

### Phase 1: Planner Dry Run

Actions:

1. Implement batch grouping rules for risk-first, rule-family, and ownership strategies.
2. Generate manifests without invoking CCA.
3. Review sample manifests with security and product owners.
4. Tune PR size caps and exclusion rules.

Deliverables:

- Batch manifest schema.
- Dry-run campaign report.
- Selected strategy for pilot.

### Phase 2: CCA Pilot

Actions:

1. Create the CCA workflow/prompt for backlog burndown.
2. Run against 3 to 5 low-risk batches.
3. Open draft PRs.
4. Capture validation results, reviewer feedback, and merge rate.
5. Compare full CCA remediation with native CodeQL autofix where available.

Deliverables:

- Working CCA burndown workflow.
- Pilot PRs.
- Acceptance and rework metrics.
- Updated prompt guidance by rule family.

### Phase 3: Controlled Scale

Actions:

1. Expand to 5 to 10 repositories.
2. Establish weekly capacity with product teams.
3. Add dashboards for backlog and campaign progress.
4. Add automatic post-merge alert closure confirmation.
5. Add issue creation for blocked batches.

Deliverables:

- Weekly campaign report.
- Repo/team burndown metrics.
- Blocked batch queue.

### Phase 4: Organization Service

Actions:

1. Move inventory, planner, and CCA dispatch into a scheduled service.
2. Add policy controls per org/repo/team.
3. Add approval workflow for large batches.
4. Add cost reporting for CCA runs.
5. Add audit export for security governance.

Deliverables:

- Service runbook.
- Policy config.
- Audit package.
- Cost and throughput dashboard.

## Service Policy Configuration

Store policy as code so each org or repo can tune automation without changing the service.

Example:

```yaml
org: spglobal-innersource
defaults:
  max_alerts_per_pr: 5
  max_files_per_pr: 5
  max_changed_lines: 300
  allowed_severities: [critical, high]
  exclude_classifications: [generated, test, library]
  require_codeowners_match: true
  mode: draft-pr
repositories:
  example-service:
    owner_team: team-example-platform
    validation_commands:
      - mvn -q -DskipTests compile
    allowed_paths:
      - src/main/**
    blocked_paths:
      - .github/**
      - generated/**
```

## Risk Controls

- Never run CCA on the whole backlog without a manifest.
- Keep `security-events: read` for inventory and only grant write scopes where PR creation requires them.
- Use a dedicated GitHub App or service identity for branch and PR creation.
- Do not give CCA broad secret access.
- Keep network access constrained to GitHub and approved package/build endpoints.
- Require branch protection and CODEOWNER review.
- Log every manifest, run, PR, and final alert state.
- Rate-limit per repo and per team.
- Prefer draft PRs until the service has proven acceptance rates.

## Open Decisions

1. Which org should be the first pilot: `spglobal-innersource`, `market-intelligence`, or an atom sandbox org?
2. Is CCA expected to run in GitHub-hosted infrastructure or on existing self-hosted runner pools?
3. What product ownership source should be authoritative: CODEOWNERS, repo custom properties, team mapping CSV, or another internal system?
4. What is the initial severity scope: critical only, critical/high, or all security severity findings?
5. Should native CodeQL autofix API be used as an input to CCA, or should the first pilot use full CCA remediation only?
6. What weekly PR capacity can pilot teams tolerate?
7. Should blocked or likely-false-positive alerts create issues, dismissal requests, or a separate triage report?

## Recommended Next Actions

1. Create the inventory exporter for open CodeQL alerts at org scope.
2. Run a dry-run report grouped by severity, rule ID, repository, owner, and path classification.
3. Pick one rule-family pilot from the top critical/high findings.
4. Define the manifest schema and CCA prompt contract.
5. Run CCA in draft PR mode against 3 to 5 batches.
6. Measure merge rate, validation success, alert closure, reviewer feedback, and cost.
7. Decide whether to scale by rule-family campaigns or repository waves after the pilot.