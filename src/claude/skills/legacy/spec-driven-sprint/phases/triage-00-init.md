# Triage Phase T00: Init

## Entry Gate

```bash
# Phase T00 has no predecessor — phase-init IS the entry gate; skip phase-check.
devforgeai-validate phase-init ${TRIAGE_ID} --workflow=spec-sprint-triage --project-root=${PROJECT_ROOT}
# Exit 0: state created at phase 00 | Exit 2: invalid workflow/id
```

`${TRIAGE_ID}` is `TRIAGE-YYYYMMDD-HHMMSS`, generated from the current UTC timestamp in Phase 00.

## Contract

PURPOSE: Parse the `--backlog <selector>` argument, generate the `$TRIAGE_ID`, run the gh auth pre-flight, and initialize the triage phase-state.
DELEGATES TO: none.
GATE: gh auth authenticated AND `$BACKLOG_SELECTOR` is non-empty. HALT if unauthenticated — triage is meaningless offline.

---

## Mandatory Steps

### Step 1: Parse the selector argument → TRIAGE_ID

EXECUTE: Parse `$BACKLOG_SELECTOR` from the `/spec-sprint --backlog <selector>` argument. Set `$TRIAGE_ID = TRIAGE-$(date -u +%Y%m%d-%H%M%S)` (per-run UTC timestamp — follows the W3_ID_PATTERN timestamp shape; `gh#433`).
VERIFY: `$TRIAGE_ID` matches `^TRIAGE-[0-9]{8}-[0-9]{6}$`. If the selector is missing → HALT → AskUserQuestion.

### Step 2: gh auth pre-flight

EXECUTE: `gh auth status` — verify authenticated to the target org/repo.
VERIFY: Exit 0. If unauthenticated → **HALT** via AskUserQuestion. Triage requires live `gh issue list/search` calls; proceeding unauthenticated produces an empty manifest with no diagnostic value.

### Step 3: Validate the selector grammar

EXECUTE: Validate `$BACKLOG_SELECTOR` against the supported forms (from `references/backlog-triage.md`):
- **Issue range:** `399-430` (bare range, both inclusive)
- **Label filter:** `label:<name>` (single label, URL-safe)
- **gh search query:** any string starting with a `gh` search keyword

VERIFY: Selector matches one supported form. Unknown form → HALT → AskUserQuestion.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${TRIAGE_ID} --workflow=spec-sprint-triage --phase=00 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: proceed to T01 | Exit != 0: HALT
```
