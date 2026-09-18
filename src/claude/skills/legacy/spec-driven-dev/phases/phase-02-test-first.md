# Phase 02: Test-First Design (TDD Red)

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=02
# Exit 0: proceed | Exit 1: Phase 01 incomplete | Exit 2: missing subagents
```

## Contract

PURPOSE: Write failing tests from acceptance criteria before any implementation code exists.
REQUIRED SUBAGENTS: test-automator
REQUIRED ARTIFACTS: `devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json`
STEP COUNT: 7 mandatory steps

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/memory/learning/tdd-patterns.md")
```

IF any Read fails: HALT -- "Phase 02 reference files not loaded."

---

## Mandatory Steps

### Step 1: Load TDD Patterns

EXECUTE: Check for learned TDD patterns from previous stories.
```
Glob(pattern=".claude/memory/learning/tdd-patterns.md")
IF exists: Read(file_path=".claude/memory/learning/tdd-patterns.md")
# Surface top 3 relevant patterns (confidence >= low, 3+ occurrences)
```
VERIFY: Display "Patterns loaded: N relevant" or "No patterns file yet — proceeding."
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=02.1 --project-root=${PROJECT_ROOT}`

### Step 1.5: Fetch Remediation REC Entries (Sprint 5, conditional)

This step runs ONLY when `$REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations"` (set by Phase 01 Step 01.9.6). In normal mode, skip to Step 2.2 with `$OPEN_REC_ENTRIES = []`.

EXECUTE (conditional):
```
IF $REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations":
    devforgeai-validate qa-recommendations-get \
        --story-id=${STORY_ID} \
        --rec-ids="$(comma-join $OPEN_REC_IDS)" \
        --project-root=${PROJECT_ROOT} \
        --format=json
```

VERIFY: Exit 0 = success. Store returned `payload.entries` as `$OPEN_REC_ENTRIES` (list of full REC entry dicts).
- Exit 1 with `missing_rec_ids` populated → HALT with the missing list verbatim. The REC-IDs in phase-state.json cycles[].rec_ids do not match qa-recommendations.md.
- Exit 2 → HALT with IO/parse error.

Display (remediation mode): `"Fetched ${len($OPEN_REC_ENTRIES)} REC entries for remediation."`

RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=1.5 --project-root=${PROJECT_ROOT}`

### Step 2.2: Coverage Planning

EXECUTE: Generate a layer-classified coverage plan for target files BEFORE invoking test-automator.
```python
# Step 2.2 EXECUTE (pseudocode)
# Parser order for extract_target_files (first non-empty result wins):
# 1. YAML fence in Technical Specification with file_path: entries
# 2. Markdown table with "Source Files Guidance" or | File | column header
# 3. "### Files Created/Modified" section bullet list
# 4. DoD inline backtick paths (.py/.md/.ts/.js/.sh)
# 5. Fallback: targets=[], fallback_reason="target-extraction-failed"

story_content = Read(story_file)
target_files = extract_target_files(story_content)

plan = {
    "$schema": "coverage-plan-v1",
    "story_id": story_id,
    "generated_at": iso_utc_now(),
    "fallback_reason": None if target_files else "target-extraction-failed",
    "targets": [],
    "total_expected_coverage_pct": None,
    "plan_version": "1.0",
}
for f in target_files:
    layer, source = classify_layer(f)
    # Classification rules: see .claude/skills/spec-driven-dev/references/coverage-planning.md
    threshold = {"business-logic": 95, "application": 85, "infrastructure": 80}[layer]
    error_branches = max(2, min(8, 2 + edge_cases + func_count))
    plan["targets"].append({
        "file": f, "layer": layer, "threshold_pct": threshold,
        "required_error_branch_tests": error_branches,
        "classification_source": source,
    })
if plan["targets"]:
    plan["total_expected_coverage_pct"] = sum(t["threshold_pct"] for t in plan["targets"]) / len(plan["targets"])
Write(file_path=f"tmp/{story_id}/coverage-plan.json", content=json.dumps(plan, indent=2, sort_keys=True))
```
VERIFY:
```
Glob(pattern="tmp/${STORY_ID}/coverage-plan.json")
```
File MUST exist after write. Verify JSON is parseable and contains all 7 required fields: `$schema`, `story_id`, `generated_at`, `fallback_reason`, `targets`, `total_expected_coverage_pct`, `plan_version`. Log: plan_path, target_count, total_expected_coverage_pct, fallback_mode (true if targets=[]).

For full classification rules, see: `.claude/skills/spec-driven-dev/references/coverage-planning.md`

RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=02.2 --project-root=.`

### Step 2.3: Invoke test-automator

EXECUTE: Delegate test generation to test-automator subagent. The Task() prompt uses the lean-pointer form (per contract-specification proposal §4.2) — all primary-session state (story ID, parsed ACs, tech stack, coverage plan, REC entries, TDD patterns) is passed via the YAML work contract instead of a prose string prompt. The test-automator has the contract schema preloaded via `skills:` frontmatter (entry `backend-architect-contract-spec` added BA-018.3).

**EXECUTE (BA-003):** Read pre-detected tech stack from Phase 01 state BEFORE composing the contract. This populates `contract.tech_stack_snapshot`.
```bash
DETECTED_TECH_STACK=$(devforgeai-validate phase-status ${STORY_ID} --format=json --project-root=. | jq -c '.detected_tech_stack')
```
VERIFY: `DETECTED_TECH_STACK` is a non-empty JSON object (not `null`, not `{}`). If empty, HALT — "Phase 01 Step 4 did not persist tech stack to phase-state.json; re-run preflight."

### Step 2.25: Build Test Contract (STORY-649)

EXECUTE: Build the work contract for test-automator. The CLI reads phase-state.json,
story file, coverage-plan.json, and test-plan.ai.yaml; emits schema-valid contract JSON.

```bash
MODE=$([ "${REMEDIATION_MODE:-false}" = "true" ] && echo "02-remediation" || echo "02-normal")
REMEDIATION_ARG=""
if [ "$MODE" = "02-remediation" ]; then
  REMEDIATION_ARG="--remediation-rec-ids=$(comma_join $OPEN_REC_IDS)"
fi
devforgeai-validate build-test-contract ${STORY_ID} \
    --phase=${MODE} \
    --subagent=test-automator \
    --project-root=${PROJECT_ROOT} \
    ${REMEDIATION_ARG} \
    --format=json
```

VERIFY: Exit code semantics:
```
Exit 0: contract written at tmp/${STORY_ID}/test-contract-${MODE}-test-automator.json — proceed
Exit 1: HALT — source data insufficient; display halt_code and remediation hint
Exit 2: HALT — operator intervention required (I/O error)
Exit 3: HALT — schema validation failed (CLI bug)
Exit 4: HALT + AskUserQuestion per askuserquestion_payload in stderr; after user answers, re-run Step 2.25
Exit 5: HALT — phase×subagent mismatch (orchestrator bug)
```

Store the contract path as `$CONTRACT_PATH` (parse from stdout `{"status":"ok","contract_path":"..."}`).

RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=2.25 --project-root=.`

#### Step 2.3b: Invoke test-automator (lean-pointer Task)

```
Task(
  subagent_type="test-automator",
  description="TDD Red for ${STORY_ID} (mode=${MODE})",
  prompt="Work contract: ${CONTRACT_PATH}

Read the contract JSON. Validate against schema src/claude/scripts/devforgeai_cli/schemas/test-contract-v1.schema.json.
Execute per contract.inputs and contract.constraints.
Return JSON matching contract.expected_outputs.structured_return.schema_ref (TestAutomatorReturn).
On halt, return with status=\"halt-required\" and applicable halt_code from contract.halt_triggers."
)
```

VERIFY: Test files exist on disk.
```
Glob(pattern="tests/${STORY_ID}/*") OR Glob(pattern="tests/**/*${STORY_ID}*")
IF no test files found: HALT — "test-automator did not create test files."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --subagent=test-automator --step=02.3`

### Step 3: Verify RED State

EXECUTE: Verify all tests fail with business logic errors (not import/syntax/config).
```bash
devforgeai-validate verify-red-state --test-command="${TEST_COMMAND}" --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code semantics:
```
Exit 0: Valid RED state — proceed.
Exit 1: HALT — "Tests are passing. RED state not achieved."
Exit 2: HALT — "Test failures are environmental (import/syntax/config), not business logic."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=02.4 --project-root=${PROJECT_ROOT}`

### Step 4: Create Test Integrity Snapshot

EXECUTE: Create HMAC-signed checksum snapshot of all test files via CLI.

<!-- NOTE (Sprint 5, G10): In remediation mode, create-test-snapshot overwrites
     the prior cycle's red-phase-checksums.json. This is intentional — each cycle
     defines its own RED state. Prior-cycle snapshots are not retained. -->
```bash
devforgeai-validate create-test-snapshot ${STORY_ID} --project-root=${PROJECT_ROOT}
```
The CLI discovers test files, computes SHA-256 hashes, signs the snapshot with a CLI-embedded HMAC key, and writes it to disk. Claude MUST NOT create snapshots with inline Python — the HMAC signature verifies CLI provenance.

VERIFY: Exit code 0 = snapshot created and signed.
```
IF exit code != 0: HALT — "Test integrity snapshot was NOT created. This is MANDATORY (STORY-502)."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=02.5 --project-root=${PROJECT_ROOT}`

**IMMUTABILITY DECLARATION (RCA-046, RCA-047):** Test files are now IMMUTABLE until Phase 05. Do NOT modify test files during Phases 03 or 04. If test bugs are discovered: return to Phase 02, re-invoke test-automator, create new snapshot.

### Step 5: Update AC Checklist (Test Items) [CONDITIONAL: ac_checklist_updates_enabled]

CONDITIONAL: If `ac_checklist_updates_enabled` is false (configurable per-project), SKIP this step entirely. Rely on Phase 07 DoD tracking instead. Default: true (enabled).

EXECUTE: Mark test-related acceptance criteria as completed.
```bash
devforgeai-validate update-ac-checklist --story-file=${STORY_FILE} --category=test
```
VERIFY: Exit code 0 = items updated (or no items to update). Command displays progress summary.

### Step 6: Capture Observations

EXECUTE: Write observation file for this phase via CLI. Observations are returned in the agent's structured return; parse them from the Task result via `jq` before passing to write-observation (per §2.3 of 06-skill-phase-updates.md — the agent-direct observation Write path in `test-automator.md` was removed, making Step 6 the sole observation persistence path).

```bash
# Parse observations_returned from TASK_RESULT: jq -c .observations_returned // []
OBS_JSON=$(echo "${TASK_RESULT}" | jq -c '.observations_returned // []')
devforgeai-validate write-observation --story=${STORY_ID} --phase=02 --observations="${OBS_JSON}" --project-root=${PROJECT_ROOT}
```
OBS_JSON must be a JSON array where each object has these 7 required fields:
```json
[{"id":"obs-STORY-567-02-001","phase":"02","source":"test-automator","category":"success","note":"description here","severity":"low","timestamp":"2026-04-03T00:00:00Z"}]
```
Valid categories: friction, success, pattern, gap, idea, bug
Valid severities: low, medium, high
VERIFY: Exit code 0 = observation file written. Non-blocking on failure.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --step=02.7 --project-root=${PROJECT_ROOT}`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=02 --checkpoint-passed
# Exit 0: proceed to Phase 03 | Exit 1: tests not in RED state
```
