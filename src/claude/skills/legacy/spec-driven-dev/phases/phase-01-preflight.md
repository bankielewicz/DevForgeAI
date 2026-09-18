# Phase 01: Pre-Flight Validation

## Entry Gate

Phase 01 has no entry gate — state is created by `dev-preflight` (called by `/dev`) or by the Entry Dispatcher in SKILL.md when invoked outside `/dev`. The legacy `phase-init` invocation was removed by STORY-658; that command's "state already exists" failure is the very bug the dispatcher fixes.

## Contract

PURPOSE: Validate environment, context files, story specification, and session state before development begins.
REQUIRED SUBAGENTS: git-validator, tech-stack-detector, context-preservation-validator
REQUIRED ARTIFACTS: None
STEP COUNT: 9 mandatory steps

## Reference Loading [MANDATORY]

```
Read(file_path="devforgeai/specs/context/tech-stack.ai.md")
Read(file_path="devforgeai/specs/context/dependencies.ai.md")
Read(file_path="devforgeai/specs/context/coding-standards.ai.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.ai.md")
Read(file_path="devforgeai/specs/context/anti-patterns.ai.md")
```

IF any Read fails: HALT -- "Phase 01 reference files not loaded."

---

## Mandatory Steps

### Step 1: Validate Git Status

EXECUTE: Run git check CLI (replaces git-validator subagent -- 0 LLM tokens).
```bash
devforgeai-validate git-check --project-root=. --format=json
```
VERIFY: Parse JSON result. IF assessment.status == "READY" or "UNCOMMITTED": proceed.
```
IF assessment.uncommitted_changes > 10: AskUserQuestion "10+ uncommitted changes detected. Proceed?"
IF assessment.status == "GIT_MISSING" or "NOT_INITIALIZED": Display warning, proceed with fallback.
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=git-validator --step=01.1`

### Step 2: Validate 6 Context Files

EXECUTE: Validate all 6 constitutional context files via CLI.
```bash
devforgeai-validate context-check --directory=${PROJECT_ROOT}
```
Expected files: tech-stack.md, source-tree/, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

VERIFY: Exit code 0 = all 6 files valid.
```
IF exit code != 0: HALT — "Context validation failed. Run /create-system-architecture first."
```
PERSIST: Compute and store SHA-256 checksums of all 6 context files via CLI (R-004):
```bash
devforgeai-validate context-checksums ${STORY_ID} --project-root=${PROJECT_ROOT}
```
VERIFY: Exit code 0 = checksums stored in phase-state.json `context_checksums` field.
Fast-path: reads pre-computed hashes from `.ai.md` companion file headers when available (instant, no file hashing).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=01.2 --project-root=${PROJECT_ROOT}`

### Step 2.5: Load AI Companion Files (.ai.md)

EXECUTE: Load the 5 .ai.md AI companion files from `devforgeai/specs/context/*.ai.md` using all-or-nothing validation. These files contain pre-extracted YAML rules optimized for subagent consumption, reducing token usage in downstream phases.

**All-or-nothing validation:** Check all 5 exist first. If any are missing, skip all and log WARNING. Never HALT on missing .ai.md files — they are optional enhancements.

```
# Step 1: Glob the 5 .ai.md files (same set as the Reference Loading block at the top of this phase).
Glob(pattern="devforgeai/specs/context/*.ai.md")

IF fewer than 5 .ai.md files found:
  Log WARNING: "Not all 5 .ai.md companion files found — skipping AI companion loading. Subagents will read original context files directly."
  Set CONTEXT_AI_RULES = "" (empty)
  Skip to Step 3.

IF all 5 .ai.md files found:
  # Step 2: Read all 5 (already loaded by the Reference Loading block; concatenate with file-boundary delimiters).
  CONTEXT_AI_RULES = concatenate(
    "--- tech-stack.ai.md ---\n{content}\n" +
    "--- dependencies.ai.md ---\n{content}\n" +
    "--- coding-standards.ai.md ---\n{content}\n" +
    "--- architecture-constraints.ai.md ---\n{content}\n" +
    "--- anti-patterns.ai.md ---\n{content}\n"
  )
```
PERSIST: Store CONTEXT_AI_RULES in the phase-state checkpoint for downstream phase consumption. Save the concatenation from Step 2 to `tmp/${STORY_ID}/context-ai-rules.txt`, then hand that path to the atomic CLI — `--from-file` avoids inline shell-escaping of a five-file concatenation, which is precisely what made the previous approach fragile. Use `--value` only for short inline strings. `context_ai_rules` is stored as a plain STRING, never JSON-parsed.
```bash
Write(file_path="tmp/${STORY_ID}/context-ai-rules.txt", content="${CONTEXT_AI_RULES}")
devforgeai-validate phase-set-context-rules ${STORY_ID} --workflow=dev \
  --from-file=tmp/${STORY_ID}/context-ai-rules.txt --project-root=.
# Key: context_ai_rules — consumed by Phase 03, 04, 05 subagent prompts
```
Latent-bug note: the former string-replacement anchor targeted a `context_ai_rules` key set to an empty string, but nothing ever seeded that key — so the replacement could never match and Phases 03/04/05 have always received no context rules. This migration repairs that, and completes the same Edit()-to-CLI move already made for tech-stack persistence in Step 4 (BA-017).
VERIFY: CONTEXT_AI_RULES is either populated (all 5 loaded) or empty (graceful degradation). Never HALT on missing .ai.md files — they are optional enhancements.

### Step 3: Load Story Specification

EXECUTE: Read the story file.
```
Read(file_path="devforgeai/specs/Stories/${STORY_ID}-*.story.md")
# Use Glob first if exact filename unknown
```
VERIFY: File exists and contains `## Acceptance Criteria` and `## Technical Specification` sections.
```
Grep(pattern="## Acceptance Criteria", path="${STORY_FILE}")
Grep(pattern="## Technical Specification", path="${STORY_FILE}")
IF either missing: HALT — "Story file incomplete."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=01.3 --project-root=${PROJECT_ROOT}`

### Step 4: Detect Tech Stack

EXECUTE: Run tech stack detection CLI (replaces tech-stack-detector subagent -- 0 LLM tokens).
```bash
devforgeai-validate detect-tech-stack --project-root=. --format=json
```
VERIFY: Parse JSON result. IF validation.status == "PASS": proceed.
```
IF validation.status == "FAIL" with CRITICAL conflicts: HALT — "Tech stack conflict with tech-stack.md."
IF validation.status == "WARN": Display warnings, proceed.
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=tech-stack-detector --step=01.4`
PERSIST (BA-017): Write detected tech stack to phase-state.json via the atomic CLI — replaces the earlier fragile `Edit()`-string-replacement. Idempotent; concurrency-safe; re-invocation overwrites prior value.
```bash
devforgeai-validate phase-set-tech-stack ${STORY_ID} --json="${TECH_STACK_RESULT_JSON}" --project-root=.
```
VERIFY (BA-017): State contains a non-empty tech-stack object.
```bash
devforgeai-validate phase-status ${STORY_ID} --format=json --project-root=. \
  | jq -e '.detected_tech_stack | type == "object" and length > 0' > /dev/null
```
IF jq exits non-zero: HALT — "phase-set-tech-stack write did not persist; inspect state file."

### Step 5: Technical Debt Threshold Check

EXECUTE: Read technical debt register if it exists.
```
Glob(pattern="devforgeai/technical-debt-register.md")
# IF exists: Read and parse thresholds
# Thresholds: warning=5, critical=10, blocking=15
```
VERIFY: Check total_open against thresholds.
```
IF >= 15 AND NOT $IGNORE_DEBT_FLAG: HALT with AskUserQuestion
IF 10-14: Display warning, set $DEBT_OVERRIDE_BANNER if user consents
IF 5-9: Display notice
IF < 5: Silent proceed
```

### Step 6: Context Preservation Validation

EXECUTE: Invoke context-preservation-validator subagent.
```
Task(subagent_type="context-preservation-validator", prompt="Validate context linkage for ${STORY_ID}. Check brainstorm-to-epic-to-story provenance chain. Report any context loss.")
```
VERIFY: Task result returned. No critical context loss detected.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=context-preservation-validator --step=01.6`

### Step 7: Bootstrap Iteration Log (Non-Blocking)

EXECUTE: Initialize the iteration log for this story. This step is **non-blocking** — if the CLI fails, log a WARNING and continue. Never HALT on iteration log bootstrap failure.
```bash
devforgeai-validate iteration-log-init ${STORY_ID} --project-root=.
```
VERIFY: If exit code != 0, display: "WARNING: Iteration log bootstrap failed — continuing workflow."
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=7`

### Step 8: Spinning Wheels Detection (Non-Blocking)

EXECUTE: Read the iteration log to detect spinning wheels. This step is **non-blocking** — the dev workflow continues after display regardless of result.
```bash
devforgeai-validate iteration-log-status ${STORY_ID} --format=json
```

PARSE JSON response:
```
IF iteration log read fails or log is missing: skip silently, continue to Exit Gate.
IF spinning_wheels.detected == false: continue.
IF spinning_wheels.confidence == "low": no warning, continue.
IF spinning_wheels.confidence is "medium" or "high":
  Display WARNING banner:
    "WARNING: Story has been through N cycles with repeated approaches (confidence: {confidence}).
     Consider: /collaborate for external AI perspective, /rca for root cause analysis,
     or splitting the story into smaller units."
```

VERIFY: Step completed (warning displayed or skipped silently). Non-blocking — never HALT on this step.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=01 --step=8`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=01 --checkpoint-passed
# Exit 0: proceed to Phase 02 | Exit 1: HALT
```

## Optional Captures (Non-Blocking)

- Capture observations: friction, success, pattern, gap, idea, bug
- Reference: `references/observation-capture.md`

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
