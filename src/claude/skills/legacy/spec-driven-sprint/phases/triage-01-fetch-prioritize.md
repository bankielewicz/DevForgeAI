# Triage Phase T01: Fetch + Prioritize

## Entry Gate

```bash
devforgeai-validate phase-check ${TRIAGE_ID} --workflow=spec-sprint-triage --from=00 --to=01 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase T00 incomplete → HALT
```

## Contract

PURPOSE: Fetch OPEN issues from GitHub matching `$BACKLOG_SELECTOR`, persist to `tmp/${TRIAGE_ID}/issues.json`, write per-issue rationale strings to `tmp/${TRIAGE_ID}/priorities.json`, and write manual readiness classifications to `tmp/${TRIAGE_ID}/readiness.json`.
DELEGATES TO: none.
GATE: `tmp/${TRIAGE_ID}/issues.json` exists and contains a valid JSON array; `tmp/${TRIAGE_ID}/priorities.json` exists; `tmp/${TRIAGE_ID}/readiness.json` exists.

---

## Mandatory Steps

### Step 1: Fetch issues

EXECUTE: Fetch OPEN issues matching `$BACKLOG_SELECTOR`:
- **Issue range** `NNN-MMM`: `gh issue list --state open --limit 200 --json number,title,body,labels,url,createdAt,state --repo <org>/<repo>` then filter by number range.
- **Label filter** `label:<name>`: `gh issue list --state open --label <name> --limit 200 --json number,title,body,labels,url,createdAt,state`
- **gh search query**: `gh issue list --state open --search '<query>' --limit 200 --json number,title,body,labels,url,createdAt,state`

Write result to `tmp/${TRIAGE_ID}/issues.json` (JSON array of issue objects).
VERIFY: `tmp/${TRIAGE_ID}/issues.json` exists AND is valid JSON AND is an array. If the gh command fails or returns zero issues → HALT → ask the user (confirm repo/selector).

### Step 2: Author per-issue rationale strings

EXECUTE: For each issue in `issues.json`, draft a one-sentence `rationale` string that explains why this issue is prioritized at its class (bug / enhancement / other) and relative position. Rationale is prose-only — it documents the reasoning but DOES NOT override the deterministic `priority_rank` output from T02.

Write `tmp/${TRIAGE_ID}/priorities.json` as a JSON object keyed by issue number: `{"<number>": "<rationale>", ...}`.
VERIFY: `tmp/${TRIAGE_ID}/priorities.json` exists AND has one entry per OPEN issue in `issues.json`.

### Step 3: Author manual readiness classifications

EXECUTE: For each issue in `issues.json`, classify execution readiness from the issue body, labels, linked PRs, and current repo evidence. Write `tmp/${TRIAGE_ID}/readiness.json` as a JSON object keyed by issue number:

```json
{
  "<number>": {
    "readiness_status": "execute-existing-issue",
    "resolution_path": "one concrete action path",
    "readiness_evidence": ["verified evidence string", "..."],
    "manual_preflight_required": false
  }
}
```

Allowed `readiness_status` values:
- `execute-existing-issue`
- `complete-partial-issue`
- `close-as-implemented`
- `close-as-superseded`
- `blocked-by-dependency`
- `needs-user-decision`

Use `needs-user-decision` with `manual_preflight_required: true` when evidence is insufficient to select a concrete path. `manual_preflight_required: true` means T03 excludes the issue from executable sprint prompts.

VERIFY: `tmp/${TRIAGE_ID}/readiness.json` is a JSON object with one entry per OPEN issue, every entry contains exactly the four fields above, and every `readiness_status` is in the allowed set.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${TRIAGE_ID} --workflow=spec-sprint-triage --phase=01 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to T02 | Exit != 0: HALT
```
