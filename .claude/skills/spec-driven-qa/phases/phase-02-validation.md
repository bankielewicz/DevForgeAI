# Phase 02: Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=01 --to=02 --project-root=.
# Exit 0: proceed | Exit 1: Phase 01 incomplete
```

## Contract

PURPOSE: Execute tests, analyze coverage, validate AC-DoD traceability.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Traceability score, coverage metrics (or structural verification for non-code)
STEP COUNT: 2 mandatory steps

---

## Reference Loading

Load these references BEFORE executing steps:
```
Read(file_path=".claude/skills/spec-driven-qa/references/traceability-validation-algorithm.md")
Read(file_path=".claude/skills/spec-driven-qa/assets/traceability-report-template.md")
Read(file_path=".claude/skills/spec-driven-qa/references/coverage-analysis.md")
```

---

## Mandatory Steps

### Step 2.1: AC-DoD Traceability Validation

EXECUTE: Extract AC requirements and DoD items from story file. Map each AC to its corresponding DoD item. Calculate traceability score.

**Sub-step 2.1.1: Extract AC Requirements**
```
Read(file_path="${STORY_FILE}")
ac_headers = Grep(pattern="^### AC#[0-9]+", path="${STORY_FILE}", output_mode="content")
Extract: Then/And clauses, bullet requirements, metrics
Store: ac_requirements[]
```

**Sub-step 2.1.2: Extract DoD Items**
```
dod_section = extract_between("^## Definition of Done", "^## Workflow")
Parse: checkbox lines "^- \[(x| )\] (.+)$"
Store: dod_items[] with section, status, text
```

**Sub-step 2.1.3: Map AC to DoD**
```
FOR each ac_req:
    best_match = find_dod_match(ac_keywords, dod_items)
    IF match_score >= 0.5: mapped
    ELSE: missing_traceability
```

**Sub-step 2.1.4: Calculate Score**
```
traceability_score = (covered / total) * 100
Display: "Traceability score: {traceability_score}%"

IF traceability_score < 100:
    Display: "HALT: Traceability below 100% -- missing mappings detected"
    HALT workflow
```

**Sub-step 2.1.5: Validate Deferrals**
```
IF any DoD items unchecked:
    Check "## Approved Deferrals" section
    Match unchecked items to approved list
    IF unmatched: deferral_status = "INVALID"
```

VERIFY: traceability_score >= 100% OR workflow HALTED. Deferral status determined.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=02 --step=2.1 --project-root=.`

---

### Step 2.2: Test Coverage Analysis

**If $DELIVERABLE_TYPE == "non-code":**

EXECUTE: Skip language-specific coverage tooling. Verify structural test coverage instead.
```
# Confirm test files exist
Glob(pattern="tests/${STORY_ID}/**" OR "tests/**/*${STORY_ID}*")

# Verify assertions validate content structure
# Verify all ACs have corresponding tests
FOR each ac in ac_requirements:
    Grep(pattern="test.*ac.*{ac_number}", path="tests/", output_mode="files_with_matches", -i=true)

Display: "Coverage: N/A (non-code implementation, structural tests only)"
```
VERIFY: Test files exist and map to ACs. Report as "N/A (non-code)".
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=02 --step=2.2 --project-root=.`

---

**If $DELIVERABLE_TYPE == "code" or "mixed":**

EXECUTE: Run 7-step coverage analysis workflow from coverage-analysis.md.

**Sub-step 2.2.1: Load Thresholds**
```
Thresholds (strict defaults -- ADR-010, non-negotiable):
- Business Logic: 95%
- Application: 85%
- Infrastructure: 80%
- Overall: 80%
```

**Sub-step 2.2.2: Generate Coverage Reports**
```
Language-specific commands (use test_isolation_paths from Phase 01):

.NET:    dotnet test --collect:'XPlat Code Coverage' --results-directory={results_dir}
Python:  pytest --cov=src --cov-report=json:{coverage_dir}/coverage.json
Node.js: npm test -- --coverage --coverageDirectory={coverage_dir}
Go:      go test ./... -coverprofile={coverage_dir}/coverage.out
Rust:    cargo tarpaulin --out Json --output-dir {coverage_dir}
Java:    mvn test jacoco:report -Djacoco.destFile={coverage_dir}/jacoco.exec
```

**Sub-step 2.2.3: Classify Files by Layer**
```
Read(file_path="devforgeai/specs/context/source-tree.md")

Layer patterns (from source-tree):
- Business Logic: src/domain/*, src/core/*, src/services/*
- Application: src/api/*, src/controllers/*, src/handlers/*
- Infrastructure: src/data/*, src/repositories/*, src/external/*
```

**Sub-step 2.2.4: Calculate Coverage by Layer**
```
FOR each file in coverage_report:
    layer = classify_file(file, source_tree_patterns)
    layer_coverage[layer].add(file.coverage)

Calculate: business_avg, application_avg, infrastructure_avg, overall_avg
```

**Sub-step 2.2.5: Validate Against Thresholds**
```
IF business_coverage < 95%: CRITICAL violation (blocks QA)
IF application_coverage < 85%: CRITICAL violation (blocks QA)
IF infrastructure_coverage < 80%: HIGH violation (blocks QA)
IF overall_coverage < 80%: CRITICAL violation (blocks QA)
```

**Sub-step 2.2.6: Identify Coverage Gaps**
```
FOR each uncovered_block:
    test_suggestion = {
        file, function, lines,
        suggested_test: generate_test_name(),
        priority: HIGH (business) | MEDIUM (app) | LOW (infra)
    }
```

**Sub-step 2.2.7: Analyze Test Quality**
```
Checks:
- Assertion ratio (target: >= 1.5 per test)
- Over-mocking (mocks > tests * 2)
- Test pyramid (70% unit, 20% integration, 10% E2E)
```

VERIFY: Coverage meets all thresholds (95%/85%/80%) OR violations recorded as CRITICAL. Test quality metrics collected.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=02 --step=2.2 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=02 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 03 | Exit 1: HALT
```

## Phase 02 Completion Display

```
Phase 02 Complete: Validation
  Traceability: {traceability_score}%
  Business Logic: {biz_coverage}% (threshold: 95%)
  Application: {app_coverage}% (threshold: 85%)
  Infrastructure: {infra_coverage}% (threshold: 80%)
  Overall: {overall_coverage}% (threshold: 80%)
  Blocking violations: {count}
```
