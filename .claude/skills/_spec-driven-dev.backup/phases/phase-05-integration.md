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

---

## Mandatory Steps

### Step 1: Anti-Gaming Validation (RUN FIRST — BLOCKING)

EXECUTE: Check for test gaming patterns before running integration tests. Gaming invalidates coverage scores.
```
Grep(pattern="@skip|@pytest.mark.skip|skip\\(|xfail|@ignore|@disabled", path="tests/")
Grep(pattern="assert True|assert 1|pass$", path="tests/")
```
VERIFY: No gaming patterns detected.
```
IF gaming patterns found: HALT — "Anti-gaming validation failed. Coverage scores would be invalid."
```

### Step 2: Invoke Integration Tester

EXECUTE: Delegate integration testing to specialist subagent.
```
Task(
  subagent_type="integration-tester",
  prompt="Run integration tests for ${STORY_ID}.
  Test: API contracts, database transactions, message flows, cross-component interactions.
  Coverage thresholds: Business Logic >= 95%, Application >= 85%, Infrastructure >= 80%.
  Report: test results, coverage percentages, any failures."
)
```
VERIFY: Task result returned with test results and coverage data.
```
IF integration test failures:
  # Diagnostic Hook (STORY-496): Single-invocation guard
  Task(subagent_type="diagnostic-analyst", prompt="Diagnose integration test failures for ${STORY_ID}.")
  # Graceful skip if diagnostic-analyst unavailable
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=05 --subagent=integration-tester`

### Step 3: Validate Coverage Thresholds (BLOCKING — ADR-010)

EXECUTE: Parse coverage data from integration tester results.
```
# Extract percentages for each layer:
# Business Logic: X% (threshold: 95%)
# Application: Y% (threshold: 85%)
# Infrastructure: Z% (threshold: 80%)
```
VERIFY: All thresholds met.
```
IF any threshold not met: HALT — "Coverage below thresholds: Business={X}% App={Y}% Infra={Z}%"
# Coverage gaps are CRITICAL blockers per ADR-010, NOT warnings.
```

### Step 4: Update AC Checklist (Integration Items)

EXECUTE: Mark integration-related acceptance criteria as completed.
```
Edit(file_path="${STORY_FILE}", old_string="- [ ] <integration item>", new_string="- [x] <integration item>")
```
VERIFY: Grep confirms integration items are checked.
```
Grep(pattern="- \\[x\\].*[Ii]ntegration", path="${STORY_FILE}")
IF no matches: HALT — "AC checklist update was skipped (RCA-003)."
```

### Step 5: Capture Observations

EXECUTE: Write observation file for this phase.
```
Write(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-05-observations.json",
  content=<JSON with phase, category, note, files, severity>)
```
VERIFY: Observation file exists.
```
Glob(pattern="devforgeai/feedback/ai-analysis/${STORY_ID}/phase-05-observations.json")
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=05 --checkpoint-passed
# Exit 0: proceed to Phase 5.5 | Exit 1: coverage thresholds not met
```
