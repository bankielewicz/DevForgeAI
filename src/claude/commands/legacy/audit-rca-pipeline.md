---
description: Audit unimplemented RCA remediation debt across all RCA files
argument-hint: (no arguments required)
model: opus
allowed-tools: Bash, Read, Write, Glob
---

# Audit RCA Pipeline (Tier 3 — ADR-060)

Surfaces unimplemented framework debt by scanning all RCA files
(`devforgeai/RCA/` + `archive/`) and reporting which RCAs have ACTIONABLE
status whose cited remediation stories are unfilled (file missing OR status
not in {QA Approved, Released}).

This is the meta-debt visibility tool prescribed by RCA-065 §10 Option 3
(Tier 3). Run BEFORE deciding between Proposal A (Tier 1) or A+B (Tier 1+2).
Without this data, the next tier decision is blind.

**Carve-out (D24):** This command MUST NOT contradict `deferral-validator`
on deferral semantics. When an RCA cites a story that EXISTS AND has open
DoD deferrals, the audit reports `STORY_PRESENT_NOT_DONE` linkage and treats
deferral-validator's verdict as authoritative for remediation guidance.

## Phase 0: Validate

- Use Glob to confirm `devforgeai/RCA/*.md` exists. If no RCA files are found,
  HALT with: "No RCA files found at devforgeai/RCA/. Cannot audit pipeline."
- Use Glob to confirm `devforgeai/RCA/audit-reports/` directory exists.
  If absent, this is the first run — Bash creates it before Phase 2.

## Phase 1: Invoke CLI + Display Dashboard

Run the deterministic CLI:

```bash
.venv/bin/devforgeai-validate rca-status --format=json
```

Capture stdout. Parse the JSON. Render a dashboard table to the user:

| RCA ID | Status | Linkage Style | Unfilled Stories | Provenance |
|---|---|---|---|---|

Show summary metrics:
- Total RCAs scanned
- Successful parses vs parse errors
- Actionable RCAs count
- **debt_score** (ACTIONABLE × unfilled stories)
- **coverage_pct** (filled / total cited stories)
- Unique unfilled stories count (deduplicated)

If `patterns_md_last_updated` is non-null AND `patterns_md_rcas_since` > 0:
display single-line footer:
> PATTERNS.md last updated YYYY-MM-DD; N RCAs created since. Consider Tier 4
> pattern-freshness audit.

## Phase 2: Write Markdown Report

Generate a timestamped Markdown report:

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
REPORT_PATH="devforgeai/RCA/audit-reports/rca-status-audit-${TS}-$$.md"
.venv/bin/devforgeai-validate rca-status --format=text --report="${REPORT_PATH}"
```

**VERIFY block (D27 + RCA-002 mitigation):**
After the CLI returns, READ the report path with the Read tool. Confirm:
1. File exists at the expected path
2. File size > 0 bytes
3. First line starts with `# RCA Pipeline Audit —`

If ANY check fails, HALT with: "REPORT WRITE FAILED — audit incomplete."
If all checks pass, display: "REPORT WRITTEN: {path} ({bytes} bytes)"

## Phase 3: Suggest Next Steps

Based on the dashboard data, recommend:

1. **Top 3 RCAs by debt_score** (sorted descending). For each, show RCA ID
   and unfilled story count.
2. **Reference RCA-065 §10** for the tier decision:
   - Tier 1 (Proposal A): analyzer hook + conviction gate (~1-2 weeks)
   - Tier 1+2 (Proposal A+B): A + primary-orchestrator restrictions (~3-4 weeks)
   - Defer: continue audit-only iteration without structural changes
3. **If `debt_score` is large (>20)**: surface a warning that the framework
   has accumulated significant unimplemented RCA debt. The user should
   weigh whether to commit to Tier 1 / Tier 2 OR address the meta-failure
   (RCAs accepted but never executed) first.

## Behavior summary

- Read-only against RCA files and story files. No mutations.
- Atomic Markdown writes (D23) with secret-scan redaction (D22).
- Per-finding provenance (GROUNDED/DERIVED/INCONCLUSIVE) per Epistemic
  Integrity Protocol.
- Exit codes: 0 (clean), 2 (partial — some RCAs failed to parse), 1
  (catastrophic).
- Carve-out: defers to `deferral-validator` on deferral verdicts.

## References

- **ADR-060** (this command's governance): `devforgeai/specs/adrs/ADR-060-rca-audit-reports-directory-and-rca-status-cli.md`
- **RCA-065** (forcing function): `devforgeai/RCA/RCA-065-qa-skill-prose-only-enforcement-recurrence.md`
- **CLI source**: `src/claude/scripts/devforgeai_cli/commands/rca_status.py`
- **Parser source**: `src/claude/scripts/devforgeai_cli/commands/_rca_parser.py`
- **JSON schema**: `src/claude/scripts/devforgeai_cli/schemas/rca_status_schema.json`
- **Sibling audit command**: `.claude/commands/audit-deferrals.md`
