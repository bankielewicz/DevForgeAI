# Phase 05: Integration & Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=4.5 --to=05
# Exit 0: proceed | Exit 1: Phase 4.5 incomplete
```

## Contract

PURPOSE: Validate cross-component integration, coverage thresholds, and system-level behavior.
REQUIRED SUBAGENTS: integration-tester
REQUIRED ARTIFACTS: None
STEP COUNT: 5 mandatory steps

## Reference Loading [MANDATORY]

```
# No required references for this phase. Self-contained — delegates to
# integration-tester + diagnostic-analyst subagents; no static skill
# reference, context file, memory entry, or story Read in mandatory steps.
```

---

## Mandatory Steps

### Step 1: Anti-Gaming Validation (RUN FIRST — BLOCKING)

EXECUTE: Check for test gaming patterns before running integration tests. Gaming invalidates coverage scores.
Note: In remediation mode, this is the sole anti-gaming gate (Phase 04 check removed per optimization R-001).
```bash
devforgeai-validate anti-gaming --test-dir=tests/ --project-root=${PROJECT_ROOT} --baseline=tests/.anti-gaming-baseline.json
```
VERIFY: Exit code 0 = no gaming detected.
```
IF exit code == 1: HALT — "Anti-gaming validation failed. Coverage scores would be invalid."
```

### Step 1.5: Build Integration Contract (STORY-649)

EXECUTE: Build the work contract for integration-tester. The CLI reads phase-state.json,
story file, and test artifacts; emits schema-valid contract JSON.

```bash
devforgeai-validate build-test-contract ${STORY_ID} \
    --phase=05-integration \
    --subagent=integration-tester \
    --project-root=${PROJECT_ROOT} \
    --format=json
```

VERIFY: Exit code semantics:
```
Exit 0: contract written at tmp/${STORY_ID}/test-contract-05-integration-integration-tester.json — proceed
Exit 1: HALT — source data insufficient; display halt_code and remediation hint
Exit 2: HALT — operator intervention required (I/O error)
Exit 3: HALT — schema validation failed (CLI bug)
Exit 4: HALT + AskUserQuestion per askuserquestion_payload in stderr; after user answers, re-run Step 1.5
Exit 5: HALT — phase×subagent mismatch (orchestrator bug)
```

Store `$CONTRACT_PATH` (parse from stdout `{"status":"ok","contract_path":"..."}`).

Build the registry-protected Phase 05 handoff for `integration-tester`. Derive
the changed-files list from the integration contract's test-file inputs so the
handoff can include source-tree coverage for the files the subagent validates.

```bash
INTEGRATION_CHANGED_FILES_PHASE05="tmp/${STORY_ID}/changed-files-phase05-integration-tester.txt"
mkdir -p "$(dirname "${INTEGRATION_CHANGED_FILES_PHASE05}")"
jq -r '.inputs.test_files[]? // empty' "${CONTRACT_PATH}" > "${INTEGRATION_CHANGED_FILES_PHASE05}"

HANDOFF_OUTPUT_INTEGRATION_TESTER=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
    --workflow=spec-driven-dev \
    --phase=05 \
    --subagent=integration-tester \
    --changed-files-file="${INTEGRATION_CHANGED_FILES_PHASE05}" \
    --project-root=${PROJECT_ROOT})
HANDOFF_PATH_INTEGRATION_TESTER=$(echo "$HANDOFF_OUTPUT_INTEGRATION_TESTER" | jq -r '.handoff_md_path')
```

VERIFY before dispatch:
- `$HANDOFF_PATH_INTEGRATION_TESTER` is non-empty and exists.
- `tmp/${STORY_ID}/handoffs/phase-05-integration-tester-handoff.manifest.json` exists.
- The manifest has `context_pack.unresolved == []`.

RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --step=1.5 --project-root=.`

### Step 2: Invoke Integration Tester

EXECUTE: Delegate integration testing to specialist subagent with the lean-pointer Task() prompt (per contract-specification proposal §4.2).

```
Task(
  subagent_type="integration-tester",
  description="Integration validation for ${STORY_ID}",
  prompt="Handoff: ${HANDOFF_PATH_INTEGRATION_TESTER}
Work contract: ${CONTRACT_PATH}

Read the handoff first. Use its context_pack.coverage_matrix and role-domain rules as the context source. If a required domain or artifact is absent, return H-CONTEXT-MISS and stop.
Read the contract JSON. Validate against schema src/claude/scripts/devforgeai_cli/schemas/test-contract-v1.schema.json.
Execute per contract.inputs.integration_boundaries and contract.inputs.test_files.
Return JSON matching contract.expected_outputs.structured_return.schema_ref (IntegrationTesterReturn).
Append subagent-result-v1 coverage_attestation with context_pack_path='${HANDOFF_PATH_INTEGRATION_TESTER}', context_pack_consumed=true, and context_miss=[] to the completion_record.
On halt, return with status=\"halt-required\" and applicable halt_code from contract.halt_triggers."
)
```

VERIFY: Task result is IntegrationTesterReturn JSON with required fields. Contract file at `${CONTRACT_PATH}` now contains populated `completion_record`.
```
IF status == "halt-required" with code H-SUITE-TIMEOUT-EXCEEDED:
  HALT — split integration suite per subagent-prompt-overflow.md
IF integration test failures (passed_count < test_count):
  DIAGNOSTIC_CHANGED_FILES_PHASE05="tmp/${STORY_ID}/changed-files-phase05-diagnostic-analyst.txt"
  mkdir -p "$(dirname "${DIAGNOSTIC_CHANGED_FILES_PHASE05}")"
  : > "${DIAGNOSTIC_CHANGED_FILES_PHASE05}"
  HANDOFF_OUTPUT_DIAGNOSTIC_ANALYST=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
    --workflow=spec-driven-dev --phase=05 \
    --subagent=diagnostic-analyst \
    --changed-files-file="${DIAGNOSTIC_CHANGED_FILES_PHASE05}" \
    --project-root=${PROJECT_ROOT})
  HANDOFF_PATH_DIAGNOSTIC_ANALYST=$(echo "$HANDOFF_OUTPUT_DIAGNOSTIC_ANALYST" | jq -r '.handoff_md_path')
  VERIFY: "$HANDOFF_PATH_DIAGNOSTIC_ANALYST" is non-empty and exists.
  # Diagnostic Hook (STORY-496): Single-invocation guard.
  Task(subagent_type="diagnostic-analyst", prompt="Handoff: ${HANDOFF_PATH_DIAGNOSTIC_ANALYST}\n\nRead the handoff first. Use its context_pack for covered constitutional domains instead of re-reading full context files. Return the existing structured diagnosis and embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[]. Diagnose integration test failures for ${STORY_ID}. Failures: {failed_tests[] from IntegrationTesterReturn}.")
  # Graceful skip if diagnostic-analyst unavailable
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --subagent=integration-tester`

### Step 3: Validate Coverage Thresholds (BLOCKING — ADR-010)

EXECUTE: Validate coverage against layer thresholds via CLI test harness.
```bash
devforgeai-validate run-tests ${STORY_ID} --coverage --project-root=${PROJECT_ROOT} --format=json
```
VERIFY: Exit code 0 = all thresholds met.
```
IF exit code == 1: HALT — "Coverage below thresholds. Coverage gaps are CRITICAL blockers per ADR-010."
```

### Step 4: Update AC Checklist (Integration Items) [CONDITIONAL: ac_checklist_updates_enabled]

CONDITIONAL: If `ac_checklist_updates_enabled` is false, SKIP this step. Rely on Phase 07 DoD tracking instead. Default: true.

EXECUTE: Mark integration-related acceptance criteria as completed.
```bash
devforgeai-validate update-ac-checklist --story-file=${STORY_FILE} --category=integration
```
VERIFY: Exit code 0 = items updated. Command displays progress summary.

### Step 5: Capture Observations

EXECUTE: Write observation file for this phase via CLI.
```bash
devforgeai-validate write-observation --story=${STORY_ID} --phase=05 --observations='${OBS_JSON}' --project-root=${PROJECT_ROOT}
```
OBS_JSON must be a JSON array. Each object requires 7 fields: `id` (obs-STORY-NNN-05-001), `phase` (05), `source` (agent name), `category` (friction|success|pattern|gap|idea|bug), `note` (description), `severity` (low|medium|high), `timestamp` (ISO 8601).
VERIFY: Exit code 0 = observation file written. Non-blocking on failure.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=05 --checkpoint-passed
# Exit 0: proceed to Phase 5.5 | Exit 1: coverage thresholds not met
```
