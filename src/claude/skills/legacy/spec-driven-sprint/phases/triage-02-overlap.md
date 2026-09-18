# Triage Phase T02: Compute Overlap + Waves

## Entry Gate

```bash
devforgeai-validate phase-check ${TRIAGE_ID} --workflow=spec-sprint-triage --from=01 --to=02 --project-root=${PROJECT_ROOT}
# Exit 0: proceed | Exit != 0: Phase T01 incomplete → HALT
```

## Contract

PURPOSE: Run the `triage-backlog` CLI subcommand on `tmp/${TRIAGE_ID}/issues.json` plus `tmp/${TRIAGE_ID}/readiness.json` to produce `tmp/${TRIAGE_ID}/backlog-manifest.json`. The CLI is deterministic, offline, and stdlib-only; readiness judgment is manual input from T01 and is preserved as data.
DELEGATES TO: none (pure CLI invocation).
GATE: `devforgeai-validate triage-backlog` exits 0 AND `backlog-manifest.json` schema equals `backlog-manifest-v1` AND every `issues[]` entry has readiness fields.

---

## Mandatory Steps

### Step 1: Run triage-backlog CLI

EXECUTE:
```bash
devforgeai-validate triage-backlog \
  --input tmp/${TRIAGE_ID}/issues.json \
  --readiness-input tmp/${TRIAGE_ID}/readiness.json \
  --output tmp/${TRIAGE_ID}/backlog-manifest.json
```

VERIFY: Exit 0 AND `tmp/${TRIAGE_ID}/backlog-manifest.json` exists AND `jq -r '.schema' tmp/${TRIAGE_ID}/backlog-manifest.json` equals `backlog-manifest-v1`.

If exit 1 (zero OPEN issues): log the empty manifest and HALT → ask the user (selector may be too narrow).
If exit 2 (malformed input): `issues.json` or `readiness.json` from T01 is corrupt → re-run T01 or HALT.

### Step 2: Verify manifest structure

EXECUTE: Confirm the manifest contains `issues[]`, `overlap_matrix[]`, `clusters[]`, `waves[]`, and `parallelism{}` keys. For every `issues[]` entry, confirm `readiness_status`, `resolution_path`, `readiness_evidence`, and `manual_preflight_required` are present.
VERIFY: All required top-level keys and per-issue readiness keys are present. If missing → HALT.

### Step 3: Verify readiness vocabulary

EXECUTE: Confirm every `issues[].readiness_status` is one of:
- `execute-existing-issue`
- `complete-partial-issue`
- `close-as-implemented`
- `close-as-superseded`
- `blocked-by-dependency`
- `needs-user-decision`

VERIFY: No out-of-vocabulary status exists. If any status is outside this set → HALT.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${TRIAGE_ID} --workflow=spec-sprint-triage --phase=02 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to T03 | Exit != 0: HALT
```
