# Phase 03: Implementation (TDD Green)

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=02 --to=03
# Exit 0: proceed | Exit 1: Phase 02 incomplete
```

## Contract

PURPOSE: Write minimum code to make all failing tests pass.
REQUIRED SUBAGENTS: backend-architect OR frontend-developer, context-validator
REQUIRED ARTIFACTS: None (code files created/modified)
STEP COUNT: 6 mandatory steps

**Test-file writes are hook-blocked** by `phase-gate-write.sh` (exit 2). Recovery: see SKILL.md § Phase Regression (Backward Transition).

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/memory/learning/friction-catalog.md")
```

IF any Read fails: HALT -- "Phase 03 reference files not loaded."

---

## Mandatory Steps

### Step 1: Load Friction Catalog

EXECUTE: Check for learned friction patterns from previous stories.
```
Glob(pattern=".claude/memory/learning/friction-catalog.md")
IF exists: Read(file_path=".claude/memory/learning/friction-catalog.md")
# Surface top 3 friction warnings relevant to this story type
```
VERIFY: Display "Friction warnings loaded: N relevant" or "No catalog yet — proceeding."
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=03.1 --project-root=${PROJECT_ROOT}`

### Step 2a (BA-018): Build Work Contract(s)

EXECUTE: Compose the implementation-subagent work contract(s) before the Task() call. Each dispatched subagent gets its own contract file (per proposal §3.2 filename pattern `phase-${PHASE}-${SUBAGENT}.yaml`). For full-stack stories, write TWO contracts (one for backend-architect, one for frontend-developer).

The subagents have the contract schema preloaded via their `skills:` frontmatter (entry `backend-architect-contract-spec` added BA-018.3).

**EXECUTE (BA-003):** Read pre-detected tech stack from Phase 01 state BEFORE composing the contract. This populates `contract.tech_stack_snapshot` deterministically.
```bash
DETECTED_TECH_STACK=$(devforgeai-validate phase-status ${STORY_ID} --format=json --project-root=. | jq -c '.detected_tech_stack')
```
VERIFY: `DETECTED_TECH_STACK` is a non-empty JSON object. If empty, HALT — "Phase 01 Step 4 did not persist tech stack to phase-state.json; re-run preflight."

Contract fields required for `phase_mode: "implementation"`:
- Always-required top-level fields (14 fields — see skill SKILL.md)
- Phase-specific conditionally-required: `ac_list[]` (parsed from story; `implementation_hints` from v3.0+ `<implementation>` XML when present), `files_to_modify[]` (authorized write paths per subagent layer map), `test_files[]` (from Phase 02 red-phase output)
- Optional `friction_catalog_excerpt` (from Phase 01 lookup)
- Optional `context_ai_rules` (from phase-state.json Phase 01 Step 2.5)
- Optional `subagent_extensions`:
  - backend-architect: `files_to_modify[].layer` uses `domain / application / infrastructure`
  - frontend-developer: `files_to_modify[].layer` uses `component / container / page / hook / store`; `ui_source_of_truth_ref` (design.md pointer if extracted)

Template skeleton: copy `src/claude/skills/backend-architect-contract-spec/assets/templates/contract-template.yaml` once per subagent.

```bash
# For backend story or full-stack (backend first):
BACKEND_CONTRACT="tmp/${STORY_ID}/contracts/phase-03-backend-architect.yaml"
mkdir -p "$(dirname "${BACKEND_CONTRACT}")"
# Compose contract per schema (see template)
Write(file_path="${BACKEND_CONTRACT}", content="<backend-architect YAML contract>")

# For frontend story or full-stack (frontend second, after backend completes):
FRONTEND_CONTRACT="tmp/${STORY_ID}/contracts/phase-03-frontend-developer.yaml"
Write(file_path="${FRONTEND_CONTRACT}", content="<frontend-developer YAML contract>")
```

VERIFY: The PreToolUse hook `contract-schema-validator.sh` fires on each Write. Both writes must pass schema validation. On exit 2, HALT — fix and retry.

### Step 2b: Build Scoped Handoff(s)

EXECUTE: For each implementation subagent that will be dispatched in Step 2, build a scoped handoff before the Task() call. The handoff is mandatory for the registry-protected Phase 03 `backend-architect` and `frontend-developer` dispatches.

Write one changed-file list per dispatched implementation subagent:
- Backend: `tmp/${STORY_ID}/changed-files-phase03-backend-architect.txt`
- Frontend: `tmp/${STORY_ID}/changed-files-phase03-frontend-developer.txt`

Each file contains one repo-relative implementation path per line, sourced from that subagent contract's `files_to_modify[]`. Do not include Phase 02 test files unless Phase 03 is explicitly authorized to modify them.

```bash
HANDOFF_OUTPUT_BACKEND_ARCHITECT=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
  --workflow=spec-driven-dev --phase=03 \
  --subagent=backend-architect \
  --changed-files-file=tmp/${STORY_ID}/changed-files-phase03-backend-architect.txt \
  --project-root=.)
HANDOFF_PATH_BACKEND_ARCHITECT=$(echo "$HANDOFF_OUTPUT_BACKEND_ARCHITECT" | jq -r '.handoff_md_path')

HANDOFF_OUTPUT_FRONTEND_DEVELOPER=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
  --workflow=spec-driven-dev --phase=03 \
  --subagent=frontend-developer \
  --changed-files-file=tmp/${STORY_ID}/changed-files-phase03-frontend-developer.txt \
  --project-root=.)
HANDOFF_PATH_FRONTEND_DEVELOPER=$(echo "$HANDOFF_OUTPUT_FRONTEND_DEVELOPER" | jq -r '.handoff_md_path')
```

Only run the backend command when dispatching `backend-architect`; only run the frontend command when dispatching `frontend-developer`. For full-stack stories, run both sequentially, matching the Step 2 dispatch order.

VERIFY: Each executed command exits 0, each `$HANDOFF_PATH_*` variable is non-empty, and the referenced handoff `.md` file exists. On failure, HALT; do not dispatch a registry-protected implementation subagent without a handoff.

### Step 2: Invoke Implementation Subagent

EXECUTE: Determine story type and invoke appropriate subagent(s) with the lean-pointer Task() prompt (per contract-specification proposal §4.2).

```
IF backend story:
  Task(
    subagent_type="backend-architect",
    description="TDD Green for ${STORY_ID}",
    prompt="Work contract: tmp/${STORY_ID}/contracts/phase-03-backend-architect.yaml\nHandoff: ${HANDOFF_PATH_BACKEND_ARCHITECT}\n\nRead the work contract and handoff first, then execute the contract end-to-end. Schema reference is preloaded as skill 'backend-architect-contract-spec'. Use the handoff context_pack for covered domains instead of re-reading full context files. Write ONLY what the tests in contract.test_files require; no premature optimization. Apply contract.ac_list[].implementation_hints if present (v3.0+ story element). Append your completion_record to the contract file when done."
  )

IF frontend story:
  Task(
    subagent_type="frontend-developer",
    description="TDD Green (frontend) for ${STORY_ID}",
    prompt="Work contract: tmp/${STORY_ID}/contracts/phase-03-frontend-developer.yaml\nHandoff: ${HANDOFF_PATH_FRONTEND_DEVELOPER}\n\nRead the work contract and handoff first, then execute the contract end-to-end. Schema reference is preloaded as skill 'backend-architect-contract-spec'. Use the handoff context_pack for covered domains instead of re-reading full context files. Write ONLY what the tests in contract.test_files require. If contract.subagent_extensions.ui_source_of_truth_ref is present, honor it. Append your completion_record to the contract file when done."
  )

IF full-stack: Invoke both sequentially (backend first, then frontend).

NOTE: This is an **exclusive-branch** selection, not a parallel group.
For full-stack, invoke backend-architect FIRST, then frontend-developer
SECOND. Never invoke them in parallel — frontend depends on backend's
API contracts. See BA-002 in
docs/Optimization/agents/backend-architect/optimization-recommendations.md
for the terminology rationale.
```

VERIFY: Code files exist on disk. Task result confirms implementation created. Contract file(s) at `tmp/${STORY_ID}/contracts/phase-03-*.yaml` now contain populated `completion_record`.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --subagent=backend-architect --step=03.2` (or frontend-developer)

### Step 2.5: Apply Remediation Entries (Sprint 5, conditional)

This step runs ONLY when `$REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations"`. In normal mode, skip to Step 3.

EXECUTE (conditional):
```
IF $REMEDIATION_MODE == true AND $REMEDIATION_SOURCE == "qa-recommendations":

    IF len($OPEN_REC_ENTRIES) == 0:
        HALT — "$OPEN_REC_ENTRIES is empty. Phase 02 Step 1.5 did not populate it. Re-enter Phase 02."

    Display: "Applying remediation for ${len($OPEN_REC_ENTRIES)} REC entries..."
    $CLOSED_REC_IDS = []
    $FAILED_REC_IDS = []

    FOR EACH entry IN $OPEN_REC_ENTRIES:
        Display: "  Applying ${entry.id}: ${entry.title}"

        IF entry.before_code is not null:
            # Code-change path
            Read(file_path=entry.file)
            VERIFY: file contains entry.before_code verbatim (trim leading indent
                    to compare; accept if full match after indent normalization).
            IF verification fails:
                append entry.id to $FAILED_REC_IDS
                continue

            Edit(
                file_path=entry.file,
                old_string=entry.before_code,
                new_string=entry.after_code
            )

        ELSE IF entry.remediation_steps is not null:
            # Remediation-steps path (non-code changes)
            Display: "  Remediation steps (${len(entry.remediation_steps)}):"
            FOR EACH step IN entry.remediation_steps:
                Display: "    - ${step}"
            # Orchestrator interprets each step and invokes appropriate Edit/Write/Bash.
            # HALT for any step that requires destructive git operations per
            # .claude/rules/core/git-operations.md.

        ELSE:
            # Schema violation — neither path present
            append entry.id to $FAILED_REC_IDS
            Display: "  ⚠️  Entry ${entry.id} has neither before_code nor remediation_steps; skipping."
            continue

        # Verify via the entry.verification.command
        EXECUTE: entry.verification.command
        VERIFY: output contains entry.verification.expected
        IF verification passes:
            append entry.id to $CLOSED_REC_IDS
        ELSE:
            append entry.id to $FAILED_REC_IDS

    Display: "Applied ${len($CLOSED_REC_IDS)}/${len($OPEN_REC_ENTRIES)} REC entries successfully"
    IF len($FAILED_REC_IDS) > 0:
        Display: "Failed: ${FAILED_REC_IDS}"
        IF len($FAILED_REC_IDS) == len($OPEN_REC_ENTRIES):
            HALT — "All REC entries failed application. Invoke spec-driven-rca per diagnosis-before-fix rule."
        # Partial success: continue; $FAILED_REC_IDS will NOT be closed in Phase 10

    RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=2.5 --project-root=${PROJECT_ROOT}`
```

### Step 3: Verify GREEN State

**Preamble (ADR-074) — RCA prescription ingestion.** Before running the test suite, check whether a previous tactical RCA emitted a prescription for this story. This closes the /rca tactical loop:

```
PRESCRIPTION_FILE="tmp/${STORY_ID}/rca-prescription.json"
IF file_exists("${PRESCRIPTION_FILE}"):
    Read(file_path="${PRESCRIPTION_FILE}")
    # Hook `pre-rca-prescription-write.sh` already validated the schema at emit time.
    NEXT_ACTION=$(jq -r '.next_action' "${PRESCRIPTION_FILE}")

    IF NEXT_ACTION == "resume-phase-03":
        STATUS=$(jq -r '.status' "${PRESCRIPTION_FILE}")
        TOP_DESC=$(jq -r '.top_hypothesis.description' "${PRESCRIPTION_FILE}")
        TOP_CONF=$(jq -r '.top_hypothesis.confidence' "${PRESCRIPTION_FILE}")
        Display: "RCA prescription found (status=${STATUS}, confidence=${TOP_CONF})."
        Display: "Top hypothesis: ${TOP_DESC}"

        # Apply prescription[] entries via the same interpreter Step 2.5 uses.
        FOR EACH entry IN $(jq -c '.prescription[]' "${PRESCRIPTION_FILE}"):
            FILE=$(echo "${entry}" | jq -r '.file')
            LINE=$(echo "${entry}" | jq -r '.line')
            ACTION=$(echo "${entry}" | jq -r '.action')
            CHANGE=$(echo "${entry}" | jq -r '.change')
            RATIONALE=$(echo "${entry}" | jq -r '.rationale')
            Display: "  - ${ACTION} ${FILE}:${LINE} — ${CHANGE}"
            # Orchestrator interprets the entry and invokes the appropriate Edit/Write.
            # HALT for any entry that requires destructive git operations per
            # .claude/rules/core/git-operations.md.

        # Optional verification command from the envelope
        VERIFY_CMD=$(jq -r '.verification_command // empty' "${PRESCRIPTION_FILE}")
        IF non-empty: EXECUTE: ${VERIFY_CMD}

        # Unlink the prescription so a subsequent /dev run does not re-apply it.
        rm -f "${PRESCRIPTION_FILE}"
        Display: "Prescription applied. Proceeding to test run."

    ELIF NEXT_ACTION == "escalate" OR NEXT_ACTION == "halt":
        Display: "RCA prescription requires user attention (next_action=${NEXT_ACTION})."
        Display: "Read: ${PRESCRIPTION_FILE}"
        HALT — "Prescription cannot be auto-applied; user intervention required."
    # ELSE: malformed (unreachable — hook blocked this at emit time)
# ELSE: no prescription file — proceed normally (current behavior unchanged)
```

EXECUTE: Run the test suite via CLI test harness. ALL tests must PASS.
```bash
devforgeai-validate run-tests ${STORY_ID} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code == 0. All tests passing.
```
IF exit code != 0:
  DIAGNOSTIC_CHANGED_FILES_PHASE03="tmp/${STORY_ID}/changed-files-phase03-diagnostic-analyst.txt"
  mkdir -p "$(dirname "${DIAGNOSTIC_CHANGED_FILES_PHASE03}")"
  : > "${DIAGNOSTIC_CHANGED_FILES_PHASE03}"
  HANDOFF_OUTPUT_DIAGNOSTIC_ANALYST=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
    --workflow=spec-driven-dev --phase=03 \
    --subagent=diagnostic-analyst \
    --changed-files-file="${DIAGNOSTIC_CHANGED_FILES_PHASE03}" \
    --project-root=${PROJECT_ROOT})
  HANDOFF_PATH_DIAGNOSTIC_ANALYST=$(echo "$HANDOFF_OUTPUT_DIAGNOSTIC_ANALYST" | jq -r '.handoff_md_path')
  VERIFY: "$HANDOFF_PATH_DIAGNOSTIC_ANALYST" is non-empty and exists.
  # Diagnostic Hook (STORY-496): Fire on failure only, single invocation per phase cycle
  Task(subagent_type="diagnostic-analyst", prompt="Handoff: ${HANDOFF_PATH_DIAGNOSTIC_ANALYST}\n\nRead the handoff first. Use its context_pack for covered constitutional domains instead of re-reading full context files. Return the existing structured diagnosis and embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[]. Diagnose test failures for ${STORY_ID}. Test output: <output>")
  # Then retry implementation (max 5 iterations total)
  IF iteration_count >= 5: HALT — "Maximum iterations reached."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=03.3 --project-root=${PROJECT_ROOT}`

### Step 4: Context Validation (Checksum-Gated)

EXECUTE: Check if context files changed since Phase 01 via CLI.
```bash
devforgeai-validate context-checksums ${STORY_ID} --compare --project-root=${PROJECT_ROOT} --format=json
```
```
IF exit 0 (all match):
  Display "Context files unchanged since Phase 01 — skipping re-validation (saves ~63k tokens)."
  Skip subagent invocation.

IF exit 1 (mismatch):
  Parse JSON for changed files list.
  Display "Context file(s) changed — running full validation."
  <!-- VALIDATION SANDWICH (intentional, BA-004): backend-architect enforces
       context constraints during implementation; context-validator re-audits
       in a fresh context here at Step 03.4. This is NOT redundant — the
       fresh-context re-audit is defensive reinforcement against the
       documented LLM bias to skip context-loading steps under token
       pressure. See docs/Optimization/agents/backend-architect/redundancy-analysis.md
       Signal 5 for the rationale. -->
  CONTEXT_CHANGED_FILES_PHASE03="tmp/${STORY_ID}/changed-files-phase03-context-validator.txt"
  mkdir -p "$(dirname "${CONTEXT_CHANGED_FILES_PHASE03}")"
  git -C ${PROJECT_ROOT} diff --name-only HEAD > "${CONTEXT_CHANGED_FILES_PHASE03}" || : > "${CONTEXT_CHANGED_FILES_PHASE03}"
  HANDOFF_OUTPUT_CONTEXT_VALIDATOR=$(devforgeai-validate build-subagent-handoff ${STORY_ID} \
    --workflow=spec-driven-dev --phase=03 \
    --subagent=context-validator \
    --changed-files-file="${CONTEXT_CHANGED_FILES_PHASE03}" \
    --project-root=${PROJECT_ROOT})
  HANDOFF_PATH_CONTEXT_VALIDATOR=$(echo "$HANDOFF_OUTPUT_CONTEXT_VALIDATOR" | jq -r '.handoff_md_path')
  VERIFY: "$HANDOFF_PATH_CONTEXT_VALIDATOR" is non-empty and exists.
  Task(subagent_type="context-validator", prompt="Handoff: ${HANDOFF_PATH_CONTEXT_VALIDATOR}\n\nRead the handoff first. Use its context_pack for covered constitutional domains instead of re-reading full context files. Return the existing validation report and embed subagent-result-v1 coverage_attestation with context_pack_consumed=true and context_miss=[]. Validate code changes for ${STORY_ID} against the handoff-scoped context. Report any violations.")
  VERIFY: No CRITICAL or HIGH violations.
  IF violations found: HALT — "Context constraint violations detected."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --subagent=context-validator --step=03.4`

### Step 5: Update AC Checklist (Implementation Items) [CONDITIONAL: ac_checklist_updates_enabled]

CONDITIONAL: If `ac_checklist_updates_enabled` is false, SKIP this step. Rely on Phase 07 DoD tracking instead. Default: true.

EXECUTE: Mark implementation-related acceptance criteria as completed.
```bash
devforgeai-validate update-ac-checklist --story-file=${STORY_FILE} --category=implementation
```
VERIFY: Exit code 0 = items updated. Command displays progress summary.

### Step 6: Capture Observations

EXECUTE: Write observation file for this phase via CLI.
```bash
devforgeai-validate write-observation --story=${STORY_ID} --phase=03 --observations='${OBS_JSON}' --project-root=${PROJECT_ROOT}
```
OBS_JSON must be a JSON array. Each object requires 7 fields: `id` (obs-STORY-NNN-03-001), `phase` (03), `source` (agent name), `category` (friction|success|pattern|gap|idea|bug), `note` (description), `severity` (low|medium|high), `timestamp` (ISO 8601).
VERIFY: Exit code 0 = observation file written. Non-blocking on failure.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --step=03.6 --project-root=${PROJECT_ROOT}`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03 --checkpoint-passed
# Exit 0: proceed to Phase 04 | Exit 1: tests not GREEN
```
