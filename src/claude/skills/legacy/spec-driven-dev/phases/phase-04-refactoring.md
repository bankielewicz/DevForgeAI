# Phase 04: Refactoring

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=03 --to=04
# Exit 0: proceed | Exit 1: Phase 03 incomplete
```

## Contract

PURPOSE: Improve code quality through refactoring, coverage validation, code review, and light QA — without changing behavior.
REQUIRED SUBAGENTS: refactoring-specialist, code-reviewer
REQUIRED ARTIFACTS: None
STEP COUNT: 6 mandatory steps plus contract/handoff build gates

**Test-file writes are hook-blocked** by `phase-gate-write.sh` (exit 2). Spec-file writes are likewise hook-blocked per `.claude/rules/workflow/spec-file-protection.md`.

## Reference Loading [MANDATORY]

```
# No static references for this phase. Build registry-protected handoff packs
# before the refactoring-specialist and code-reviewer dispatches. Subagents read
# tmp/${STORY_ID}/handoffs/phase-04-<subagent>-handoff.md first and report
# H-CONTEXT-MISS if the context_pack.coverage_matrix or role-domain rules are
# incomplete. Light QA still invokes the qa skill in light mode.
```

---

## Mandatory Steps

### Step 1a (BA-018): Build Work Contract

EXECUTE: Compose the refactoring-specialist work contract before the Task() call. The subagent has the contract schema preloaded via its `skills:` frontmatter (entry `backend-architect-contract-spec` added BA-018.3); the contract replaces the prose-flattening path where primary session state was stringified into the Task() prompt.

Contract fields required for `phase_mode: "refactor"` (per `src/claude/scripts/devforgeai_cli/schemas/contract.schema.json` `allOf`/`if-then`):
- Always-required top-level fields (14 fields — see skill SKILL.md §"Top-level required fields")
- Phase-specific conditionally-required: `refactor_targets[]` (list of code smells, complexity thresholds, or file::class identifiers) and `files_to_modify[]` (authorized write paths with `op: modify`)
- Optional `subagent_extensions.test_green_invariant: true` (asserts ALL tests must stay green after refactor)
- Optional `subagent_extensions.before_complexity` / `after_complexity_target` per target

Template skeleton: copy `src/claude/skills/backend-architect-contract-spec/assets/templates/contract-template.yaml`. Substitute placeholders with story-specific values. Compute `primary_context_hash = sha256(concat(6 context files + story file + phase-state.json))`.

```bash
CONTRACT_PATH="tmp/${STORY_ID}/contracts/phase-04-refactoring-specialist.yaml"
mkdir -p "$(dirname "${CONTRACT_PATH}")"
# Compose contract (pseudo-code — primary Claude session writes the YAML directly):
#   schema_version: "1.0"
#   work_id: "phase-04-refactoring-specialist-${STORY_ID}-$(date -u +%Y%m%dT%H%M%SZ)"
#   story_id: "${STORY_ID}"
#   phase: "04"
#   phase_mode: "refactor"
#   subagent: "refactoring-specialist"
#   ... (see template)
#   refactor_targets: [{target, smell, before_complexity, after_complexity_target}]
#   files_to_modify: [{path, layer, op: modify}]
#   subagent_extensions:
#     test_green_invariant: true
Write(file_path="${CONTRACT_PATH}", content="<full YAML contract body>")
```

VERIFY: The PreToolUse hook `contract-schema-validator.sh` fires on the Write. Exit 0 = contract is schema-valid; Exit 2 = contract rejected with violations on stderr — HALT and fix.

### Step 1b (ISSUE-966): Build Refactoring Specialist Handoff

EXECUTE: Build the protected handoff before dispatching `refactoring-specialist`. This is a code-mutating dispatch, so the changed-file preflight MUST use the contract's `files_to_modify[].path` values as the dependency-parsing input.

```bash
REFACTOR_CHANGED_FILES="tmp/${STORY_ID}/dev-phase04-refactoring-specialist-changed-files.txt"
mkdir -p "tmp/${STORY_ID}"
# Primary Claude session writes one repo-relative files_to_modify[].path per line.
# Manual preflight: each line must be repo-relative, must exist or be authorized
# by the contract, and must match the selected lane "spec-driven-dev" phase "04".
devforgeai-validate build-subagent-handoff "${STORY_ID}" \
  --workflow=spec-driven-dev \
  --phase=04 \
  --subagent=refactoring-specialist \
  --changed-files-file="${REFACTOR_CHANGED_FILES}" \
  --project-root="${PROJECT_ROOT}"
HANDOFF_PATH_REFACTORING_SPECIALIST="tmp/${STORY_ID}/handoffs/phase-04-refactoring-specialist-handoff.md"
```

VERIFY: Exit code 0, `tmp/${STORY_ID}/handoffs/phase-04-refactoring-specialist-handoff.manifest.json` exists, and the manifest has `workflow=spec-driven-dev`, `phase=04`, `subagent_type=refactoring-specialist`, and non-stale `context_pack.coverage_matrix` entries for changed source files.

### Step 1: Invoke Refactoring Specialist

EXECUTE: Delegate refactoring to specialist subagent with the lean-pointer Task() prompt (per contract-specification proposal §4.2). The subagent reads the contract and handoff, executes the work, and appends `completion_record` to the contract file when done.

```
Task(
  subagent_type="refactoring-specialist",
  description="TDD Refactor for ${STORY_ID}",
  prompt="Work contract: ${CONTRACT_PATH}
Handoff: ${HANDOFF_PATH_REFACTORING_SPECIALIST}

Read the work contract and handoff first. Use handoff context_pack.coverage_matrix and role-domain rules before reading broader repo context. If a required domain or artifact is missing, return H-CONTEXT-MISS and stop. Schema reference is preloaded as skill 'backend-architect-contract-spec'. Preserve test-green invariant (contract subagent_extensions.test_green_invariant). Do NOT modify test files. Append your completion_record to the contract file when done, including subagent-result-v1 coverage_attestation with context_pack_path='${HANDOFF_PATH_REFACTORING_SPECIALIST}', context_pack_consumed=true, and context_miss=[]."
)
```

VERIFY: Task result returned with refactoring summary. No test files modified. Contract file at `${CONTRACT_PATH}` now contains populated `completion_record`.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --subagent=refactoring-specialist --step=04.1`

### Step 2: Early Coverage Validation (BLOCKING — ADR-010)

EXECUTE: Run coverage analysis and validate against thresholds via CLI test harness.
```bash
devforgeai-validate run-tests ${STORY_ID} --coverage --project-root=${PROJECT_ROOT} --format=json
```
Thresholds: Business Logic >= 95%, Application >= 85%, Infrastructure >= 80% (MVP mode: 60%/50%/40%).

VERIFY: Exit code 0 = all thresholds met.
```
IF exit code == 1 (coverage below thresholds):
  # Step 2a — Persist failing tests data
  FAILING_TESTS_FILE="tmp/${STORY_ID}/failing-tests-phase-04.json"
  devforgeai-validate run-tests ${STORY_ID} --coverage --project-root=${PROJECT_ROOT} --format=json > "${FAILING_TESTS_FILE}"

  # Step 2b — Build contract for coverage-gap remediation
  devforgeai-validate build-test-contract ${STORY_ID} \
      --phase=04-coverage-gap \
      --subagent=test-automator \
      --failing-tests-file="${FAILING_TESTS_FILE}" \
      --project-root=${PROJECT_ROOT} \
      --format=json
  # Exit codes as per Phase 02 Step 2.25:
  #   0: contract written at tmp/${STORY_ID}/test-contract-04-coverage-gap-test-automator.json — proceed
  #   1: HALT — source data insufficient
  #   2: HALT — operator intervention required (I/O error)
  #   3: HALT — schema validation failed (CLI bug)
  #   4: HALT + AskUserQuestion per askuserquestion_payload
  #   5: HALT — phase×subagent mismatch (orchestrator bug)
  RECORD: devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=2b --project-root=${PROJECT_ROOT}

  # Step 2c — Invoke test-automator with contract (lean-pointer form)
  Task(
    subagent_type="test-automator",
    prompt="Work contract: tmp/${STORY_ID}/test-contract-04-coverage-gap-test-automator.json

    Read contract. Execute per contract.inputs.failing_tests and contract.inputs.coverage_plan.
    Return TestAutomatorReturn JSON. Halts per contract.halt_triggers."
  )

  # Step 2d — Re-run coverage
  devforgeai-validate run-tests ${STORY_ID} --coverage --project-root=${PROJECT_ROOT}
  IF still failing after 2 remediation cycles: HALT — "Coverage thresholds not met."

IF exit code == 2 (coverage tool unavailable): Log warning "Coverage tool not available — graceful fallback" and proceed.
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=04.2 --project-root=${PROJECT_ROOT}`

### Step 2b: Coverage Drift Detection

EXECUTE: Read the coverage plan from Phase 02 Step 2.2 and compare actual measured coverage against planned baseline. This step is ADDITIVE and OBSERVATIONAL — it does not replace or modify ADR-010 blocking behavior.

```python
# Step 2b EXECUTE (pseudocode)
# Graceful fallback: if plan missing or targets=[], skip drift detection
try:
    plan_content = Read(file_path=f"tmp/{story_id}/coverage-plan.json")
    plan = json.loads(plan_content)
    targets = plan.get("targets", [])
except FileNotFoundError:
    targets = []  # no plan available — fall back to current behavior

if not targets:
    # targets=[] or plan missing: skip drift detection entirely
    # ADR-010 enforcement already handled by Step 2 above (unchanged)
    pass
else:
    drift_report = {
        "story_id": story_id,
        "generated_at": iso_utc_now(),
        "drifts": [],
    }
    for target in targets:
        actual_pct = get_actual_coverage(target["file"])  # from Step 2 run-tests output
        if actual_pct is not None and actual_pct < target["threshold_pct"]:
            drift_report["drifts"].append({
                "file": target["file"],
                "planned_threshold_pct": target["threshold_pct"],
                "actual_coverage_pct": actual_pct,
                "gap_pct": target["threshold_pct"] - actual_pct,
                "planned_error_branch_tests": target["required_error_branch_tests"],
                "actual_error_branch_tests": None,  # populated by spec-driven-rca
            })
    if drift_report["drifts"]:
        Write(file_path=f"tmp/{story_id}/coverage-drift-report.json",
              content=json.dumps(drift_report, indent=2))
        # coverage-drift-report.json is consumable by spec-driven-rca skill
```

VERIFY:
- If `targets=[]` or plan missing: step completes silently (no drift report written)
- If drifts detected: `Glob(pattern="tmp/${STORY_ID}/coverage-drift-report.json")` returns 1 match
- ADR-010 blocking behavior from Step 2 is PRESERVED — drift detection is additive and does not replace existing coverage enforcement

Drift detection is observational only — it writes a report but does not trigger phase regression. ADR-010 blocking from Step 2 stands; the drift report feeds spec-driven-rca. Schema: `.claude/skills/spec-driven-dev/references/coverage-planning.md`.

### Step 3: Verify Tests Still GREEN

EXECUTE: Run the full test suite after refactoring via CLI test harness.
```bash
devforgeai-validate run-tests ${STORY_ID} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code == 0.
```
IF exit code != 0: HALT — "Refactoring broke tests. Fix regressions before proceeding."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=04.3 --project-root=${PROJECT_ROOT}`

### Step 4: Invoke Code Reviewer

EXECUTE: Build the protected code-reviewer handoff before dispatch. `code-reviewer` is a non-mutating review dispatch, so this handoff uses the role-domain floor only and does not run a changed-file dependency walk.

```bash
CODE_REVIEW_CHANGED_FILES="tmp/${STORY_ID}/dev-phase04-code-reviewer-changed-files.txt"
mkdir -p "tmp/${STORY_ID}"
: > "${CODE_REVIEW_CHANGED_FILES}"
devforgeai-validate build-subagent-handoff "${STORY_ID}" \
  --workflow=spec-driven-dev \
  --phase=04 \
  --subagent=code-reviewer \
  --changed-files-file="${CODE_REVIEW_CHANGED_FILES}" \
  --project-root="${PROJECT_ROOT}"
HANDOFF_PATH_CODE_REVIEWER="tmp/${STORY_ID}/handoffs/phase-04-code-reviewer-handoff.md"
```

VERIFY: Exit code 0, `tmp/${STORY_ID}/handoffs/phase-04-code-reviewer-handoff.manifest.json` exists, and the manifest has `workflow=spec-driven-dev`, `phase=04`, `subagent_type=code-reviewer`, and role-domain coverage for coding-standards, anti-patterns, tech-stack, and architecture-constraints.

EXECUTE: Delegate code review to specialist subagent.
```
Task(subagent_type="code-reviewer", prompt="Handoff: ${HANDOFF_PATH_CODE_REVIEWER}

Review code changes for ${STORY_ID}. Read the handoff first. Use handoff context_pack.coverage_matrix and role-domain rules before reading broader repo context. If a required domain or artifact is missing, return H-CONTEXT-MISS and stop.

Focus: Code quality, maintainability, security vulnerabilities, pattern compliance, standards adherence. Embed subagent-result-v1 coverage_attestation in the review findings and conviction worklog payload with context_pack_path='${HANDOFF_PATH_CODE_REVIEWER}', context_pack_consumed=true, and context_miss=[].")
```
VERIFY: Task result returned with review findings. No CRITICAL blocking issues.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --subagent=code-reviewer --step=04.4`
PERSIST: Write code review findings to disk for Phase 09 consumption:
```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-04-code-reviewer.json",
  content=${CODE_REVIEW_FINDINGS_JSON})
# Format: {"findings": [{"severity": "...", "category": "...", "file": "...", "line": N, "description": "..."}]}
```

### Step 5: Light QA Validation (MANDATORY)

EXECUTE: Invoke QA skill in light mode.
```
Skill(command="qa --mode=light --story=${STORY_ID}")
```
VERIFY: QA returns with no CRITICAL/HIGH violations.
```
IF CRITICAL/HIGH violations: HALT — "Light QA failed. Fix violations before proceeding."
```

### Step 6: Update AC Checklist (Quality Items) [CONDITIONAL: ac_checklist_updates_enabled]

CONDITIONAL: If `ac_checklist_updates_enabled` is false, SKIP this step. Rely on Phase 07 DoD tracking instead. Default: true.

EXECUTE: Mark quality-related acceptance criteria as completed.
```bash
devforgeai-validate update-ac-checklist --story-file=${STORY_FILE} --category=quality
```
VERIFY: Exit code 0 = items updated. Command displays progress summary. If checklist updates are disabled, record this step after the skip decision.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=04 --step=04.6 --project-root=${PROJECT_ROOT}`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=04 --checkpoint-passed
# Exit 0: proceed to Phase 4.5 | Exit 1: quality issues detected
```

## Optional Captures (Non-Blocking)

```bash
devforgeai-validate write-observation --story=${STORY_ID} --phase=04 --observations='${OBS_JSON}' --project-root=${PROJECT_ROOT}
```
OBS_JSON must be a JSON array. Each object requires 7 fields: `id` (obs-STORY-NNN-04-001), `phase` (04), `source` (agent name), `category` (friction|success|pattern|gap|idea|bug), `note` (description), `severity` (low|medium|high), `timestamp` (ISO 8601).
Non-blocking on failure.
