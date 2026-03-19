# Workflow Integration

Reference file for integrating the spec-driven-rca skill into existing DevForgeAI workflow phases.

---

## Integration Hook 1: Phase 03 (Green) Integration

**Context:** During TDD Green phase, implementation is written to make failing tests pass. When the implementation fails tests, diagnosis should be invoked before retrying.

### Trigger Condition

```
IF phase == "Green" (Phase 03)
AND test_run.exit_code != 0
AND fix_attempts >= 2
THEN invoke spec-driven-rca
```

The trigger activates after 2 failed fix attempts to allow normal iterative development while catching persistent failures early.

### Invocation Pseudocode

```python
# Inside spec-driven-dev Phase 03 (Green)

def green_phase_with_diagnosis(story_id, test_command, max_attempts=5):
    fix_attempts = 0

    while fix_attempts < max_attempts:
        # Run tests
        result = Bash(command=test_command)

        if result.exit_code == 0:
            # Tests pass - Green phase complete
            return SUCCESS

        fix_attempts += 1

        if fix_attempts >= 2:
            # Invoke diagnosis before next fix attempt
            diagnosis = Task(
                subagent_type="spec-driven-rca",
                description=f"Diagnose persistent test failure in Green phase for {story_id}",
                prompt=f"""Phase: Green (03)
                    Story: {story_id}
                    Fix Attempts: {fix_attempts}
                    Test Command: {test_command}
                    Error Output: {result.output}

                    Execute all 4 phases: CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE.
                    Return prescription with specific file paths and changes."""
            )

            # Apply prescribed fix from diagnosis
            apply_prescription(diagnosis.prescription)
        else:
            # First 2 attempts: normal iterative fix
            apply_iterative_fix(result.output)

    # Max attempts exceeded
    HALT: "Green phase failed after {max_attempts} attempts. Escalate to user."
    return FAILURE
```

### Expected Output

The diagnosis returns a structured prescription:
```
PRESCRIPTION
  Target: H1 - {hypothesis description} [0.85]
  Fix Actions:
    1. File: /absolute/path/to/file.py
       Line: 42-48
       Action: Edit
       Change: {specific change description}
  Verification: pytest tests/STORY-XXX/test_ac1.py -v
```

### Error Handling

- If diagnosis itself fails (subagent error), log warning and allow one more manual fix attempt
- If diagnosis returns INCONCLUSIVE, escalate to user with AskUserQuestion
- If prescribed fix does not resolve failure, try next hypothesis (H2, H3)
- After exhausting all hypotheses, HALT and escalate

---

## Integration Hook 2: Phase 05 (Integration) Integration

**Context:** During integration testing, cross-component failures may occur that are not visible in unit tests. These failures often involve spec drift or dependency mismatches.

### Trigger Condition

```
IF phase == "Integration" (Phase 05)
AND integration_test.exit_code != 0
AND failure_type NOT IN ["environment_setup", "docker_unavailable"]
THEN invoke spec-driven-rca
```

Integration failures invoke diagnosis immediately (no 2-attempt buffer) because integration failures are typically more complex and benefit from systematic investigation.

### Invocation Pseudocode

```python
# Inside spec-driven-dev Phase 05 (Integration)

def integration_phase_with_diagnosis(story_id, integration_tests):
    result = Bash(command=integration_tests)

    if result.exit_code == 0:
        return SUCCESS

    # Check for environment issues first (not diagnosis-worthy)
    if is_environment_issue(result.output):
        fix_environment(result.output)
        return retry_integration(story_id, integration_tests)

    # Invoke diagnosis immediately for integration failures
    diagnosis = Task(
        subagent_type="spec-driven-rca",
        description=f"Diagnose integration test failure for {story_id}",
        prompt=f"""Phase: Integration (05)
            Story: {story_id}
            Test Command: {integration_tests}
            Error Output: {result.output}

            Focus investigation on:
            - Cross-component interface mismatches
            - Dependency version conflicts (check dependencies.md)
            - Layer boundary violations (check architecture-constraints.md)
            - API contract drift

            Execute all 4 phases: CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE."""
    )

    # Apply prescription
    apply_prescription(diagnosis.prescription)

    # Verify fix
    verify_result = Bash(command=integration_tests)
    if verify_result.exit_code == 0:
        return SUCCESS

    # Escalate if first prescription fails
    AskUserQuestion(
        question=f"Integration diagnosis applied but tests still fail.\n"
                 f"Hypothesis: {diagnosis.top_hypothesis}\n"
                 f"Options:\n"
                 f"1. Try next hypothesis\n"
                 f"2. Provide additional context\n"
                 f"3. Skip integration tests (requires justification)"
    )
```

### Expected Output

Integration diagnosis emphasizes cross-component issues:
```
INVESTIGATION REPORT
  Spec Compliance: FAIL
    - architecture-constraints.md: Layer boundary violated at src/domain/service.py:15
    - dependencies.md: Package X version 2.1 installed but 2.0 specified
  Code Trace: Service A calls Repository B directly instead of through interface
  Root Location: src/domain/order_service.py:15

PRESCRIPTION
  Fix Actions:
    1. File: src/domain/order_service.py
       Line: 15
       Action: Edit
       Change: Replace direct import of SqlRepository with IRepository interface
    2. File: src/domain/interfaces/repository.py
       Action: Add
       Change: Create IRepository interface if missing
```

### Error Handling

- Environment setup failures (Docker, database) are handled separately, not through diagnosis
- If diagnosis identifies a dependency version mismatch, flag for dependencies.md update (may require ADR)
- If diagnosis identifies architectural drift, flag for architecture review before fixing

---

## Integration Hook 3: QA Phase 2 Integration

**Context:** During QA deep analysis, the validation skill may find violations that were not caught during development. These require diagnosis to understand why they were missed and how to fix them.

### Trigger Condition

```
IF phase == "QA" (Phase 2 - Deep Analysis)
AND qa_violations.severity IN ["CRITICAL", "HIGH"]
AND violation_type NOT IN ["documentation_gap", "style_inconsistency"]
THEN invoke spec-driven-rca
```

QA-phase diagnosis focuses on understanding why violations were missed during development, not just fixing them.

### Invocation Pseudocode

```python
# Inside spec-driven-qa Phase 2 (Deep Analysis)

def qa_deep_analysis_with_diagnosis(story_id, violations):
    critical_violations = [v for v in violations if v.severity in ("CRITICAL", "HIGH")]

    if not critical_violations:
        return PASS

    # Group violations by category for batch diagnosis
    grouped = group_by_category(critical_violations)

    for category, category_violations in grouped.items():
        diagnosis = Task(
            subagent_type="spec-driven-rca",
            description=f"Diagnose QA violations ({category}) for {story_id}",
            prompt=f"""Phase: QA Deep Analysis (Phase 2)
                Story: {story_id}
                Violation Category: {category}
                Violations:
                {format_violations(category_violations)}

                Focus investigation on:
                - Why these violations were not caught during TDD phases
                - Whether violations indicate spec drift or implementation gaps
                - Whether test coverage missed these paths

                Execute all 4 phases: CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE.
                Include preventive recommendations to avoid recurrence."""
        )

        # Record diagnosis in QA report
        qa_report.add_diagnosis(category, diagnosis)

        # Apply prescription if severity is CRITICAL
        if any(v.severity == "CRITICAL" for v in category_violations):
            apply_prescription(diagnosis.prescription)

            # Re-run affected tests to verify
            retest_result = Bash(command=f"pytest tests/{story_id}/ -v")
            if retest_result.exit_code != 0:
                HALT: "Critical QA fix broke existing tests. Manual intervention required."

    return qa_report
```

### Expected Output

QA diagnosis includes preventive analysis:
```
ROOT CAUSE DIAGNOSIS REPORT
  Phase: QA Deep Analysis

  INVESTIGATION:
    Why Missed: Test coverage for error handling path was 72% (below 95% threshold)
    Spec Compliance: FAIL - anti-patterns.md Category 3 violated

  HYPOTHESES:
    H1: Error handler catches generic Exception instead of specific types [0.9]
    H2: Missing test for invalid input edge case [0.7]

  PRESCRIPTION:
    Fix Actions:
      1. File: src/application/services/order_service.py
         Line: 88-92
         Action: Edit
         Change: Replace bare except with specific ValueError, KeyError handlers

    Preventive:
      - Add error-path coverage check to TDD Red phase checklist
      - Add anti-pattern pre-scan before Green phase implementation

  VERIFICATION:
    Command: pytest tests/STORY-XXX/ -v --cov=src/application --cov-fail-under=95
```

### Error Handling

- Non-blocking violations (MEDIUM, LOW) are logged but do not trigger diagnosis
- If diagnosis prescription conflicts with existing passing tests, HALT and escalate
- Documentation gaps and style issues are handled by standard QA remediation, not diagnosis
- If multiple violation categories exist, process CRITICAL first, then HIGH

---

## Integration Summary

| Hook | Phase | Trigger | Diagnosis Focus |
|------|-------|---------|-----------------|
| Hook 1 | Green (03) | 2+ failed fix attempts | Implementation correctness |
| Hook 2 | Integration (05) | Any non-environment failure | Cross-component compatibility |
| Hook 3 | QA Deep (02) | CRITICAL/HIGH violations | Violation root cause + prevention |

All hooks follow the same 4-phase methodology (CAPTURE, INVESTIGATE, HYPOTHESIZE, PRESCRIBE) but with phase-appropriate investigation focus.
