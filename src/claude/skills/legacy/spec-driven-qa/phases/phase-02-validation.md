# Phase 02: Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=01 --to=02 --project-root=.
# Exit 0: proceed | Exit 1: Phase 01 incomplete
```

## Contract

| | |
|---|---|
| **PURPOSE** | Execute tests, analyze coverage, validate AC-DoD traceability. |
| **REQUIRED SUBAGENTS** | none |
| **REQUIRED ARTIFACTS** | Traceability score, coverage metrics (or structural verification for non-code), flaky quarantine verdict when a flaky report exists |
| **STEP COUNT** | 3 mandatory steps |

---

## Reference Loading

Load these references BEFORE executing steps:
```
Read(file_path=".claude/skills/spec-driven-qa/references/traceability-validation-algorithm.md")
Read(file_path=".claude/skills/spec-driven-qa/assets/traceability-report-template.md")
Read(file_path=".claude/skills/spec-driven-qa/references/coverage-analysis.md")
Read(file_path=".claude/skills/spec-driven-qa/assets/config/coverage-thresholds.md")
Read(file_path="devforgeai/specs/context/test-plan.ai.yaml")
# Project test policy (ADR-054 — 7th constitutional file). Drives Step 2.2.7 mocking
# checks (never_mock, mock_boundaries, auto_spec). If absent (older project predating
# ADR-054), test-plan policy checks are skipped; framework-default heuristics still
# run. Report as "test plan: not found".
```

---

## Mandatory Steps

### Step 2.1: AC-DoD Traceability Validation

EXECUTE: Extract ACs and DoD items, map AC→DoD, compute traceability.

**Sub-step 2.1.1: Extract AC Requirements**
```
Read(file_path="${STORY_FILE}")
ac_headers = Grep(pattern="^### AC#[0-9]+", path="${STORY_FILE}", output_mode="content")
Extract: Then/And clauses, bullet requirements, metrics → ac_requirements[]
```

**Sub-step 2.1.2: Extract DoD Items**
```
dod_section = extract_between("^## Definition of Done", "^## Workflow")
Parse: checkbox lines "^- \[(x| )\] (.+)$" → dod_items[] with section, status, text
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
IF traceability_score < 100: HALT — "Traceability below 100% (missing mappings)"
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

**If `$DELIVERABLE_TYPE == "non-code"`:**

EXECUTE: Skip language-specific coverage tooling; verify structural test coverage.
```
Glob(pattern="tests/${STORY_ID}/**" OR "tests/**/*${STORY_ID}*")
FOR each ac in ac_requirements:
    Grep(pattern="test.*ac.*{ac_number}", path="tests/", output_mode="files_with_matches", -i=true)
Display: "Coverage: N/A (non-code implementation, structural tests only)"
```
VERIFY: Test files exist and map to ACs. Report as "N/A (non-code)".
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=02 --step=2.2 --project-root=.`

---

**If `$DELIVERABLE_TYPE == "code" or "mixed":`**

EXECUTE: Run 7-step coverage analysis workflow from coverage-analysis.md.

**Sub-step 2.2.1: Load Thresholds**
```
# Source of truth: coverage-thresholds.md (loaded above). Extract from
# "## Minimum Coverage Requirements (STRICT)":
#   Business Logic (Domain/Services): 95%  |  Application Layer: 85%
#   Infrastructure Layer:            80%  |  Overall Project:    80%
# STRICT per ADR-010 (non-negotiable). Always read from config — never hardcode.
```

**Sub-step 2.2.2: Generate Coverage Reports** (use test_isolation_paths from Phase 01)
```
.NET:    dotnet test --collect:'XPlat Code Coverage' --results-directory={results_dir}
Python:  pytest --cov=src --cov-report=json:{coverage_dir}/coverage.json
Node.js: npm test -- --coverage --coverageDirectory={coverage_dir}
Go:      go test ./... -coverprofile={coverage_dir}/coverage.out
Rust:    cargo tarpaulin --out Json --output-dir {coverage_dir}
Java:    mvn test jacoco:report -Djacoco.destFile={coverage_dir}/jacoco.exec
```

**Sub-step 2.2.3: Classify Files by Layer**
```
Read(file_path="devforgeai/specs/context/source-tree/governance.json")
Layer patterns:
- Business Logic:  src/domain/*, src/core/*, src/services/*
- Application:     src/api/*, src/controllers/*, src/handlers/*
- Infrastructure:  src/data/*, src/repositories/*, src/external/*
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
IF business_coverage      < 95%: CRITICAL violation (blocks QA)
IF application_coverage   < 85%: CRITICAL violation (blocks QA)
IF infrastructure_coverage < 80%: HIGH    violation (blocks QA)
IF overall_coverage       < 80%: CRITICAL violation (blocks QA)
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

Two kinds of check: (a) FRAMEWORK-DEFAULT heuristics (numeric thresholds, no test-plan equivalent — always run) and (b) TEST-PLAN POLICY checks (read from `test-plan.ai.yaml` mocking_strategy; skipped if no test plan present).

```
mock_policy = test_plan["_test_plan_fragment"].mocking_strategy IF test_plan loaded ELSE None

Checks:
  (a) Assertion ratio   (target >= 1.5 per test; violation floor 1.0)  — framework default
  (a) Over-mocking      (> 3 mocks/test)                               — framework default
  (a) Test pyramid      (target 70/20/10; unit-test floor 50%)         — framework default
  (b) Never-mock breach (mock target matches mock_policy.never_mock)   — test-plan policy
  (b) Unsanctioned boundary (mock boundary NOT in mock_policy.mock_boundaries) — test-plan policy
  (b) Missing autospec  (when mock_policy.auto_spec_required and any mock w/o autospec) — test-plan policy

qa_report_data["test_quality"] = {
    "assertion_ratio": calculated_assertion_ratio,
    "over_mocking_ratio": mocks_per_test,
    "pyramid": {"unit_pct": unit_pct, "integration_pct": integration_pct, "e2e_pct": e2e_pct},
    "test_plan_source": "test-plan.ai.yaml" IF test_plan loaded ELSE "not-found"
}

# MEDIUM severity (non-blocking; contributes to PASS WITH WARNINGS)
test_quality_violations = []

# (a) framework-default — always:
IF assertion_ratio < 1.0:
    append "MEDIUM: Assertion ratio {assertion_ratio} < 1.0 per test"
IF unit_pct < 50:
    append "MEDIUM: Unit tests {unit_pct}% < 50% of total"
IF mocks_per_test > 3:
    append "MEDIUM: Over-mocking ratio {mocks_per_test} > 3 mocks/test"

# (b) test-plan policy — only when present:
IF mock_policy is not None:
    FOR each mock matching mock_policy.never_mock:
        append "MEDIUM: Test mocks a never-mock target (test plan mocking_strategy.never_mock)"
    FOR each mock whose boundary NOT in mock_policy.mock_boundaries:
        append "MEDIUM: Test mocks an unsanctioned boundary (not in test plan mock_boundaries)"
    IF mock_policy.auto_spec_required AND any mock without autospec:
        append "MEDIUM: Mock created without autospec (test plan auto_spec_required=true)"

qa_report_data["test_quality"]["violations"] = test_quality_violations
violations_medium += len(test_quality_violations)
```

VERIFY: Coverage meets all thresholds (95%/85%/80%) OR violations recorded as CRITICAL. Test quality metrics stored in `qa_report_data["test_quality"]`.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=02 --step=2.2 --project-root=.`

---

### Step 2.3: Flaky Quarantine Gate

EXECUTE: If `tmp/${STORY_ID}/flaky-report.json` exists, check every `FLAKY`
candidate against the project quarantine ledger with the `flaky-quarantine check`
mode.

```bash
devforgeai-validate flaky-quarantine --project-root=. check --report tmp/${STORY_ID}/flaky-report.json
```

If `tmp/${STORY_ID}/flaky-report.json` does not exist, record the gate as
`NOT_APPLICABLE` in the QA report.

VERIFY: Exit 0 when no flaky report exists or every `FLAKY` candidate has a
valid quarantine ledger entry. Exit non-zero blocks QA when any `FLAKY`
candidate is absent from the ledger. Malformed ledger entries are reported and
treated as absent.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=02 --step=2.3 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=02 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 03 | Exit 1: HALT
```

## Phase 02 Completion Display

```
Phase 02 Complete: Validation
  Traceability:     {traceability_score}%
  Business Logic:   {biz_coverage}%   (threshold: 95%)
  Application:      {app_coverage}%   (threshold: 85%)
  Infrastructure:   {infra_coverage}% (threshold: 80%)
  Overall:          {overall_coverage}% (threshold: 80%)
  Blocking violations: {count}
```
