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

**TEST FILE IMMUTABILITY (RCA-046, RCA-047):** Do NOT modify test files in this phase. If test bugs are found: mark Phase 03 incomplete, return to Phase 02, re-invoke test-automator, create new snapshot, then re-enter Phase 03.

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

### Step 2: Invoke Implementation Subagent

EXECUTE: Determine story type and invoke appropriate subagent.
```
IF backend story:
  Task(subagent_type="backend-architect", prompt="Implement minimum code to pass tests for ${STORY_ID}.
    Story file: ${STORY_FILE}
    Test files: [from Phase 02]
    Constraints: Follow tech-stack.md, coding-standards.md, source-tree.md, architecture-constraints.md.
    Write ONLY what tests require. No premature optimization. No feature additions beyond test scope.")

IF frontend story:
  Task(subagent_type="frontend-developer", prompt=<same structure, frontend focus>)

IF full-stack: Invoke both sequentially.
```
VERIFY: Code files exist on disk. Task result confirms implementation created.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --subagent=backend-architect` (or frontend-developer)

### Step 3: Verify GREEN State

EXECUTE: Run the test suite. ALL tests must PASS.
```bash
${TEST_COMMAND}
```
VERIFY: Exit code == 0. All tests passing.
```
IF exit code != 0:
  # Diagnostic Hook (STORY-496): Fire on failure only, single invocation per phase cycle
  Task(subagent_type="diagnostic-analyst", prompt="Diagnose test failures for ${STORY_ID}. Test output: <output>")
  # Then retry implementation (max 5 iterations total)
  IF iteration_count >= 5: HALT — "Maximum iterations reached."
```

### Step 4: Invoke Context Validator

EXECUTE: Validate implementation against all 6 context files.
```
Task(subagent_type="context-validator", prompt="Validate code changes for ${STORY_ID} against all 6 context files: tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md. Report any violations.")
```
VERIFY: Task result returned. No CRITICAL or HIGH violations.
```
IF violations found: HALT — "Context constraint violations detected. Fix before proceeding."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03 --subagent=context-validator`

### Step 5: Update AC Checklist (Implementation Items)

EXECUTE: Mark implementation-related acceptance criteria as completed.
```
Edit(file_path="${STORY_FILE}", old_string="- [ ] <impl item>", new_string="- [x] <impl item>")
```
VERIFY: Grep confirms implementation items are checked.
```
Grep(pattern="- \\[x\\].*[Ii]mplementation", path="${STORY_FILE}")
IF no matches: HALT — "AC checklist update was skipped (RCA-003)."
```

### Step 6: Capture Observations

EXECUTE: Write observation file for this phase.
```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-03-observations.json",
  content=<JSON with phase, category, note, files, severity>)
```
VERIFY: Observation file exists.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-03-observations.json")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03 --checkpoint-passed
# Exit 0: proceed to Phase 04 | Exit 1: tests not GREEN
```
