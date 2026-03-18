# Phase 06: Post-Deployment Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=05 --to=06 --project-root=.
```

## Contract

PURPOSE: Execute comprehensive parallel smoke tests and health checks on production. Trigger rollback if success rate below threshold.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Parallel validation results, success_rate, PartialResult model
STEP COUNT: 6 mandatory steps

---

## Mandatory Steps

### Step 6.1: Check Phase Applicability

EXECUTE: Check if this phase should be skipped for library projects.
```
IF 06 in $SKIP_PHASES:
    Read(file_path=".claude/skills/spec-driven-release/references/parallel-smoke-tests.md")
    # Reference loaded even for skipped phases (mandatory)

    Write(file_path="devforgeai/workflows/.release-phase-06.marker",
          content="phase: 06\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Library project - no post-deployment validation needed\ntimestamp: ${ISO_8601}")

    Display: "Phase 06 skipped: Library project - no post-deployment validation needed"
    EXIT phase early (proceed to Exit Gate with skip status)

Display: "Phase 06 active - proceeding with post-deployment validation"
```
VERIFY: Either phase is active (proceed) OR skip marker written and phase exits early.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=06 --step=6.1 --project-root=.`

---

### Step 6.2: Load Parallel Smoke Tests Reference

EXECUTE: Load all references needed for parallel validation.
```
Read(file_path=".claude/skills/spec-driven-release/references/parallel-smoke-tests.md")
Read(file_path=".claude/skills/spec-driven-release/references/post-deployment-validation.md")
Read(file_path=".claude/skills/spec-driven-release/references/smoke-testing-guide.md")
```
VERIFY: All three reference files loaded successfully.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=06 --step=6.2 --project-root=.`

---

### Step 6.3: Load Parallel Configuration

EXECUTE: Load parallel orchestration configuration for concurrent test execution.
```
Read(file_path="devforgeai/config/parallel-orchestration.yaml")

IF file not found:
    $PARALLEL_CONFIG = {
        max_concurrent: 4,
        timeout_ms: 30000,
        min_success_rate: 0.5
    }
    Display: "Parallel config not found, using defaults (max_concurrent=4, timeout=30s)"
ELSE:
    $PARALLEL_CONFIG = {
        max_concurrent: config.profiles[active_profile].max_concurrent_tasks,
        timeout_ms: config.profiles[active_profile].timeout_ms,
        min_success_rate: config.min_success_rate OR 0.5
    }
    Display: "Parallel config loaded: max_concurrent=${PARALLEL_CONFIG.max_concurrent}"
```
VERIFY: $PARALLEL_CONFIG populated with max_concurrent, timeout_ms, and min_success_rate.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=06 --step=6.3 --project-root=.`

---

### Step 6.4: Execute Parallel Health Checks + Smoke Tests

EXECUTE: Execute health checks AND smoke tests in SINGLE parallel batch (concurrent).
```
# Execute ALL checks in a single message (parallel batch):

# Health checks
FOR each endpoint in $PRODUCTION_DEPLOY_RESULT.endpoints:
    Bash(command="python .claude/skills/spec-driven-release/scripts/health_check.py --url=${endpoint} --timeout=${PARALLEL_CONFIG.timeout_ms/1000}")

# Smoke tests
Bash(command="python .claude/skills/spec-driven-release/scripts/smoke_test_runner.py --env=production --config=devforgeai/smoke-tests/config.json", timeout=${PARALLEL_CONFIG.timeout_ms})

# Performance metrics
Bash(command="python .claude/skills/spec-driven-release/scripts/metrics_collector.py --endpoints=${endpoints} --duration=30")

# Collect results as they complete
$VALIDATION_RESULTS = []
FOR each completed_task:
    $VALIDATION_RESULTS[] = {
        type: task.type,  # "health", "smoke", "metrics"
        name: task.name,
        success: (task.exit_code == 0),
        duration_ms: task.elapsed,
        details: task.stdout
    }
    Display: "[${task.type}] ${task.name}: ${task.success ? 'PASSED' : 'FAILED'} (${task.duration_ms}ms)"
```
VERIFY: All parallel tasks completed (success or failure recorded for each).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=06 --step=6.4 --project-root=.`

---

### Step 6.5: Aggregate Results

EXECUTE: Calculate success rate and determine if rollback is needed.
```
total_checks = $VALIDATION_RESULTS.length
passed_checks = $VALIDATION_RESULTS.filter(r => r.success).length
$SUCCESS_RATE = passed_checks / total_checks

Display: "Validation results: ${passed_checks}/${total_checks} passed (${SUCCESS_RATE * 100}%)"

IF $SUCCESS_RATE < $PARALLEL_CONFIG.min_success_rate:
    Display: "CRITICAL: Success rate ${SUCCESS_RATE * 100}% below threshold ${PARALLEL_CONFIG.min_success_rate * 100}%"

    Read(file_path=".claude/skills/spec-driven-release/references/rollback-procedures.md")

    AskUserQuestion:
        Question: "Post-deployment validation failed (${SUCCESS_RATE * 100}% < ${PARALLEL_CONFIG.min_success_rate * 100}%). Trigger rollback?"
        Header: "Rollback"
        Options:
            - label: "Trigger rollback (Recommended)"
              description: "Revert to previous stable version"
            - label: "Keep current deployment"
              description: "Accept risk and keep the failing deployment"
        multiSelect: false

    IF user selects rollback:
        Bash(command="${PRODUCTION_DEPLOY_RESULT.rollback_command}")
        HALT: "Production rolled back. Success rate: ${SUCCESS_RATE * 100}%"
ELSE:
    Display: "Post-deployment validation PASSED: ${SUCCESS_RATE * 100}% >= ${PARALLEL_CONFIG.min_success_rate * 100}%"
```
VERIFY: Success rate calculated. Either above threshold (proceed) OR rollback triggered (HALT).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=06 --step=6.5 --project-root=.`

---

### Step 6.6: Display Validation Summary

EXECUTE: Show comprehensive validation summary with performance comparison.
```
health_passed = VALIDATION_RESULTS.filter(r => r.type == "health" && r.success).length
health_total = VALIDATION_RESULTS.filter(r => r.type == "health").length
smoke_passed = VALIDATION_RESULTS.filter(r => r.type == "smoke" && r.success).length
smoke_total = VALIDATION_RESULTS.filter(r => r.type == "smoke").length
total_duration = VALIDATION_RESULTS.reduce((sum, r) => sum + r.duration_ms, 0)
sequential_estimate = total_duration  # If run sequentially
parallel_duration = max(VALIDATION_RESULTS.map(r => r.duration_ms))  # Actual parallel time

Display:
"
Post-Deployment Validation Summary
  Health checks: ${health_passed}/${health_total} passed
  Smoke tests: ${smoke_passed}/${smoke_total} passed
  Overall success rate: ${SUCCESS_RATE * 100}% (threshold: ${PARALLEL_CONFIG.min_success_rate * 100}%)
  Parallel duration: ${parallel_duration}ms
  Sequential estimate: ${sequential_estimate}ms
  Speedup: ${(sequential_estimate / parallel_duration).toFixed(1)}x
"
```
VERIFY: Summary displayed with accurate counts and timing comparison.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=06 --step=6.6 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=06 --checkpoint-passed --project-root=.
```

## Phase 06 Completion Display

```
Phase 06 Complete: Post-Deployment Validation
  Health: ${health_passed}/${health_total} passed
  Smoke: ${smoke_passed}/${smoke_total} passed
  Success Rate: ${SUCCESS_RATE * 100}%
  Status: PASSED
```
