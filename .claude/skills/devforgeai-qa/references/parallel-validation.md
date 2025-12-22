# Parallel Validation for QA Skill

**Story:** STORY-113
**Version:** 1.0
**Epic:** EPIC-017 (Parallel Task Orchestration)

---

## Overview

This reference defines the parallel validation pattern for the QA skill, enabling concurrent execution of test-automator, code-reviewer, and security-auditor subagents.

**Performance Impact:** 3x faster QA validation (90s sequential → 30s parallel)

**Key Principle:** One failed validator should not block two successful ones.

---

## Parallel Invocation Pattern

### Single Message with 3 Task Calls

Execute ALL three validators in ONE message (parallel execution):

```pseudocode
# All 3 Task calls in a SINGLE message - they execute in parallel
Task(
    subagent_type="test-automator",
    prompt="Analyze test coverage for {STORY_ID}. Check: test file existence, coverage percentage, assertion quality. Return: coverage metrics and gaps.",
    description="Run test analysis",
    run_in_background=true
)

Task(
    subagent_type="code-reviewer",
    prompt="Review code changes for {STORY_ID}. Check: code quality, maintainability, best practices. Return: review findings with severity.",
    description="Review code",
    run_in_background=true
)

Task(
    subagent_type="security-auditor",
    prompt="Scan code for {STORY_ID}. Check: OWASP Top 10, input validation, authentication. Return: security findings with severity.",
    description="Security scan",
    run_in_background=true
)
```

**CRITICAL:** All 3 Task calls MUST be in the same message for parallel execution.

---

## Result Aggregation

### Collect Results Using TaskOutput

After launching parallel tasks, collect results:

```pseudocode
# Wait for all results (blocking retrieval)
test_result = TaskOutput(task_id=test_task.id, block=true, timeout=120000)
review_result = TaskOutput(task_id=review_task.id, block=true, timeout=120000)
security_result = TaskOutput(task_id=security_task.id, block=true, timeout=120000)

# Aggregate using PartialResult model (from STORY-110)
partial_result = aggregate_parallel_results([test_result, review_result, security_result])
```

### PartialResult Model

Uses the `PartialResult` data model from error-handling-patterns.md (STORY-110):

```yaml
PartialResult:
  successes: List[TaskResult]       # Successfully completed validators
  failures: List[TaskFailure]       # Failed validator details
  total_tasks: 3                    # Always 3 for QA validation
  success_rate: Float               # 0.0-1.0 (e.g., 0.67 for 2/3)
```

---

## Success Threshold

### QA Requires 66% Success (2 of 3 Validators)

```pseudocode
min_success_rate = 0.66  # 2 of 3 validators must succeed

IF partial_result.success_rate < min_success_rate:
    Display: "⚠️ QA validation below threshold"
    Display: f"  Success rate: {partial_result.success_rate * 100}%"
    Display: f"  Required: 66% (2 of 3 validators)"
    Display: "  Failed validators:"
    FOR failure IN partial_result.failures:
        Display: f"    - {failure.task_id}: {failure.error_message}"
    HALT workflow

ELSE:
    Display: "✓ QA validation threshold met"
    Continue to result aggregation
```

### Threshold Rationale

| Scenario | Validators | Success Rate | Decision |
|----------|------------|--------------|----------|
| All pass | 3/3 | 100% | Continue (ideal) |
| 2 pass, 1 fail | 2/3 | 67% | Continue (acceptable) |
| 1 pass, 2 fail | 1/3 | 33% | **HALT** (below 66%) |
| All fail | 0/3 | 0% | **HALT** (critical failure) |

---

## Display Format

### Parallel Validation Phase Display

```
✓ Phase 2 Complete: Parallel validation
  test-automator: [PASS ✓ / FAIL ✗]
  code-reviewer: [PASS ✓ / FAIL ✗]
  security-auditor: [PASS ✓ / FAIL ✗]
  Success rate: [X]% (threshold: 66%)
  Duration: [X]s (vs ~[3X]s sequential)
```

### Example Output (2 of 3 Pass)

```
✓ Phase 2 Complete: Parallel validation
  test-automator: PASS ✓ (coverage: 92%)
  code-reviewer: PASS ✓ (no critical findings)
  security-auditor: FAIL ✗ (timeout after 120s)
  Success rate: 67% (threshold: 66%)
  Duration: 32s (vs ~90s sequential)

⚠️ Note: security-auditor failed - results excluded from report
```

---

## Error Handling

### Integration with error-handling-patterns.md (STORY-110)

This reference uses error handling patterns defined in:
`.claude/skills/devforgeai-orchestration/references/error-handling-patterns.md`

**Key concepts applied:**
1. **Partial Failure Recovery** - Continue if success_rate >= 0.66
2. **Result Aggregation** - Use PartialResult model for mixed results
3. **Failure Logging** - Log failed validators with correlation ID

### Failure Classification

| Error Type | Retryable | Action |
|------------|-----------|--------|
| Timeout | Yes | Log, continue with 2/3 |
| TransientError | Yes | Log, continue with 2/3 |
| PermanentError | No | Log, continue with 2/3 |
| All Failed | - | HALT, suggest sequential fallback |

---

## Configuration Reference

### Loading Parallel Config

```pseudocode
Read(file_path="devforgeai/config/parallel-orchestration.yaml")

# Extract timeout settings
timeout_ms = config.profiles[active_profile].timeout_ms  # Default: 120000
max_concurrent_tasks = config.profiles[active_profile].max_concurrent_tasks  # Default: 4
```

### Config Integration

The QA skill respects `parallel-orchestration.yaml` for:
- `timeout_ms`: Maximum wait time per validator
- `min_success_rate`: Configured threshold (override possible)

---

## Phase Integration

### Where This Runs in QA Workflow

This parallel validation replaces the sequential Phase 2 (Anti-Pattern Detection) with a comprehensive parallel phase:

```
Phase 0.0-0.9: Pre-validation (unchanged)
    ↓
Phase 1: Coverage Analysis (unchanged, but can run in parallel with Phase 2)
    ↓
Phase 2: Parallel Validation ← THIS REFERENCE
    - test-automator (parallel)
    - code-reviewer (parallel)
    - security-auditor (parallel)
    ↓
Phase 3-7: Continue with aggregated results
```

---

## Related Documentation

- `error-handling-patterns.md` (STORY-110) - PartialResult model, failure handling
- `parallel-config.md` (STORY-108) - Configuration schema
- `task-result-aggregation.md` (STORY-112) - TaskOutput blocking retrieval

---

**Last Updated:** 2025-12-19
**Story:** STORY-113
