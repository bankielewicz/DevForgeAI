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
STEP COUNT: 6 mandatory steps

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

### Step 2: Invoke test-automator

EXECUTE: Delegate test generation to test-automator subagent.
```
Task(
  subagent_type="test-automator",
  prompt="Generate failing tests for ${STORY_ID}.
  Story file: ${STORY_FILE}
  Tech stack: [from Phase 01 detection]

  Requirements:
  - Test naming: test_<function>_<scenario>_<expected>
  - One assertion per test (generally)
  - Mock external dependencies
  - Cover ALL acceptance criteria
  - Cover ALL technical specification sections
  - Use project test framework from tech-stack.md

  Return: test file paths and test count."
)
```
VERIFY: Test files exist on disk.
```
Glob(pattern="tests/${STORY_ID}/*") OR Glob(pattern="tests/**/*${STORY_ID}*")
IF no test files found: HALT — "test-automator did not create test files."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=02 --subagent=test-automator`

### Step 3: Verify RED State

EXECUTE: Run the test suite. ALL tests must FAIL.
```bash
# Use detected test command from Phase 01 (pytest, cargo test, npm test, dotnet test, etc.)
${TEST_COMMAND}
```
VERIFY: Exit code != 0. Failures are business logic failures (NOT import errors, config errors, or syntax errors).
```
IF exit code == 0: HALT — "Tests are passing. RED state not achieved."
IF failures are import/config: HALT — "Test failures are environmental, not business logic."
```

### Step 4: Create Test Integrity Snapshot

EXECUTE: Create checksum snapshot of all test files for tamper detection.
```
Read(file_path="references/test-integrity-snapshot.md")
# Follow the snapshot algorithm to generate checksums
# Write snapshot to: devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json
```
VERIFY: Snapshot file exists on disk.
```
Glob(pattern="devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json")
IF not found: HALT — "Test integrity snapshot was NOT created. This is MANDATORY (STORY-502)."
```

**IMMUTABILITY DECLARATION (RCA-046, RCA-047):** Test files are now IMMUTABLE until Phase 05. Do NOT modify test files during Phases 03 or 04. If test bugs are discovered: return to Phase 02, re-invoke test-automator, create new snapshot.

### Step 5: Update AC Checklist (Test Items)

EXECUTE: Mark test-related acceptance criteria as completed in the story file.
```
Edit(file_path="${STORY_FILE}", old_string="- [ ] <test item>", new_string="- [x] <test item>")
```
VERIFY: Grep confirms test items are checked.
```
Grep(pattern="- \\[x\\].*[Tt]est", path="${STORY_FILE}")
IF no matches: HALT — "AC checklist update was skipped (RCA-003)."
```

### Step 6: Capture Observations

EXECUTE: Write observation file for this phase.
```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-02-observations.json",
  content=<JSON with phase, category, note, files, severity>)
```
Reference schema: `references/observation-capture.md`
VERIFY: Observation file exists.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-02-observations.json")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=02 --checkpoint-passed
# Exit 0: proceed to Phase 03 | Exit 1: tests not in RED state
```
