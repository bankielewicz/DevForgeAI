---
title: Parallel Patterns Quick Reference
format: Developer Cheat Sheet
version: 1.0
---

# Parallel Patterns Quick Reference Card

## When to Use Parallel

**✓ PARALLEL GOOD FOR:**
- Independent subagent tasks
- Multiple file reads
- Long-running operations
- Pattern searches across codebase

**✗ SEQUENTIAL FOR:**
- Task dependencies (B needs output from A)
- Shared state modifications
- Critical error paths
- Sequential validation (lint → review → deploy)

---

## Pattern 1: Parallel Subagents (Native)

### Copy-Paste Template

```python
# Invoke N independent subagents in SINGLE MESSAGE
# (All Task() calls must be together)

Task(
    subagent_type="subagent-name-1",
    description="What task 1 does",
    prompt="Task 1 prompt here..."
)

Task(
    subagent_type="subagent-name-2",
    description="What task 2 does",
    prompt="Task 2 prompt here..."
)

Task(
    subagent_type="subagent-name-3",
    description="What task 3 does",
    prompt="Task 3 prompt here..."
)

# ^ All 3 execute in PARALLEL automatically
# Main thread waits here (implicit synchronization)
# Results returned after all complete
```

### Safety Rules

| Rule | Value |
|------|-------|
| Recommended max | 4-6 concurrent |
| Hard limit | 10 concurrent |
| Beyond 10 | Batch them |
| Timeout | None (framework handles) |

### Error Recovery

```python
# Try parallel, fallback to sequential
try:
    invoke_parallel(tasks)
except ParallelExecutionError:
    logger.warning("Parallel failed, retrying sequential")
    invoke_sequential(tasks)
```

---

## Pattern 2: Background Tasks (Bash)

### Copy-Paste Template

```python
# Start long-running operation in background
task_id = Bash(
    command="npm test -- --coverage",
    run_in_background=True,
    timeout=600000  # milliseconds
).task_id

logger.info(f"Tests running in background (ID: {task_id})")

# ... continue with other work ...

# Later: Retrieve results
output = BashOutput(bash_id=task_id)
coverage = extract_coverage(output.content)
```

### Safety Rules

| Rule | Value |
|------|-------|
| Max parallel background tasks | 3-4 concurrent |
| Timeout required | Yes (60-600 sec) |
| Must retrieve results | Before next phase |
| Cleanup on skip/defer | Yes (KillBash) |

### Retrieve Results

```python
# Check if complete
output = BashOutput(bash_id="bash_1")
if output.is_complete:
    parse_results(output.content)

# Kill hanging task
KillBash(shell_id="bash_1")
```

---

## Pattern 3: Parallel Tool Calling (Automatic)

### No Code Needed - Model Decides

Just ask for parallelism in prompt:

```markdown
Read these files IN PARALLEL:
- file1.md
- file2.md
- file3.md

Then search IN PARALLEL for:
- Pattern A
- Pattern B
- Pattern C
```

Model automatically calls all tools concurrently.

### When It Works Best

- Multiple independent Read operations
- Multiple independent Grep searches
- Multiple independent Bash queries
- Any combination of independent tools

---

## Task Count Guidelines

```
1-4 tasks:    ✅ Always safe
5-6 tasks:    ✅ Recommended sweet spot
7-10 tasks:   ⚠️  Maximum, use with caution
11-20 tasks:  ❌ Batch into groups of 6
21+ tasks:    ❌ Batch into groups of 6
```

### Batching Example

```python
# Split into batches of 6
BATCH_SIZE = 6

for batch_start in range(0, len(tasks), BATCH_SIZE):
    batch = tasks[batch_start : batch_start + BATCH_SIZE]

    # Invoke batch
    for task in batch:
        Task(subagent_type=task.type, prompt=task.prompt)

    # Implicit sync point (wait for batch completion)
    logger.info(f"Batch {batch_start}-{batch_start+len(batch)} complete")
```

---

## Dependency Detection Checklist

**Check if tasks are independent:**

- [ ] Task B doesn't use output from Task A
- [ ] Task A doesn't use output from Task B
- [ ] No shared state between tasks
- [ ] No order dependency (A must complete first)
- [ ] No resource conflicts (same file modifications)

**If ANY item is FALSE → Execute sequentially**

---

## Troubleshooting

### Tasks Get Stuck

**Symptom:** Parallel invocation, no progress for 30+ seconds

**Fix:**
```python
timeout = 120  # seconds
if not completed_within(timeout):
    logger.error("Parallel timeout, falling back to sequential")
    invoke_sequential(tasks)
```

### Background Task Never Finishes

**Symptom:** BashOutput shows running but never completes

**Fix:**
```python
# Kill after timeout
if not completed_within(300):  # 5 minutes
    KillBash(shell_id=task_id)
    raise TimeoutError("Background task hung")
```

### Too Many Tasks Causes Freeze

**Symptom:** 50+ tasks, 100% CPU, unresponsive

**Fix:** Never exceed 10 concurrent tasks

### Results Lost/Incomplete

**Symptom:** Some tasks don't return results

**Fix:** Always retrieve before proceeding
```python
BashOutput(bash_id=task_id)  # Must happen
```

---

## Performance Expectations

| Pattern | Time Savings | Token Impact | Complexity |
|---------|-------------|--------------|-----------|
| Parallel subagents | 30-40% | None | Low |
| Background tasks | 50-80% | None | Low |
| Parallel tools | 15-25% | None | Very Low |
| Combined | 35-40% overall | None | Low-Medium |

---

## Migration Checklist

Converting sequential → parallel:

- [ ] Identify independent tasks
- [ ] Group parallel tasks together
- [ ] Add explicit parallelism instruction
- [ ] Test with 4-6 tasks first
- [ ] Measure time improvement
- [ ] Add error recovery
- [ ] Document constraints
- [ ] Update coding-standards.md

---

## Common Patterns

### Pattern A: Parallel Feature Analysis

```python
# 3-5 features analyzed simultaneously
Task(subagent="requirements-analyst", prompt="Analyze feature 1...")
Task(subagent="requirements-analyst", prompt="Analyze feature 2...")
Task(subagent="requirements-analyst", prompt="Analyze feature 3...")
# All complete before proceeding
```

**Time:** 15 min (sequential) → 6 min (parallel)

---

### Pattern B: Code Generation + Review

```python
# Can't parallelize (review depends on code)
code = invoke_code_generator(...)  # Wait for completion
review = invoke_code_reviewer(...)  # Then review

# Better approach:
Task(subagent="code-generator", prompt="Generate code...")
Task(subagent="code-analyzer", prompt="Analyze parallel design...")
# Both run during code generation
```

---

### Pattern C: Tests + Linting + Coverage

```python
# Start all in background
bash_test = Bash(
    command="npm test",
    run_in_background=True
).task_id

bash_lint = Bash(
    command="npm run lint",
    run_in_background=True
).task_id

# Continue with implementation

# Later: retrieve all results
test_output = BashOutput(bash_id=bash_test)
lint_output = BashOutput(bash_id=bash_lint)
```

---

## Dos and Don'ts

### ✅ DO

- Start with 4-6 parallel tasks
- Test parallel implementation thoroughly
- Implement error recovery (fallback to sequential)
- Document task dependencies
- Monitor actual performance
- Use background tasks for long operations
- Let model parallelize tools automatically

### ❌ DON'T

- Parallelize dependent tasks
- Exceed 10 concurrent tasks without batching
- Ignore background task results
- Skip timeout on background tasks
- Forget cleanup on error
- Assume parallelism always faster
- Remove sequential constraints that matter

---

## Reference Docs

**Full Research:**
- `devforgeai/research/parallel-orchestration-research.md` (comprehensive)

**Implementation Guide:**
- `.claude/memory/parallel-orchestration-guide.md` (detailed patterns with code)

**This Document:**
- `devforgeai/research/PARALLEL-PATTERNS-QUICK-REFERENCE.md` (you are here)

**Executive Summary:**
- `devforgeai/research/RESEARCH-074-EXECUTIVE-SUMMARY.md` (overview)

---

## TL;DR - 30 Second Version

**Three ways to parallelize:**

1. **Multiple Task() calls** → All execute in parallel (4-6 recommended)
2. **Background Bash** → Long operations without blocking (`run_in_background=true`)
3. **Automatic tool parallelism** → Model does it automatically (just ask)

**Safe limits:** 10 concurrent max, recommend 4-6
**Performance:** 35-40% faster
**Tokens:** No additional cost

**When to use:** Independent tasks only
**When to avoid:** Dependent tasks, sequential validation

**Start:** Batch 4-6 independent subagents in Phase 3
**Test:** Measure time improvement
**Expand:** Add background tasks to Phase 2 when ready

---

## Questions?

See full documentation in `devforgeai/research/` or `.claude/memory/parallel-orchestration-guide.md`
