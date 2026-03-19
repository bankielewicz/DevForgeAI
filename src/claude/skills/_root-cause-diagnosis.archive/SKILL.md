---
name: root-cause-diagnosis
description: Systematic root cause diagnosis enforcing investigation before fix attempts. 4-phase methodology prevents shotgun debugging by requiring evidence-based analysis.
allowed-tools: Read Grep Glob Task
---

# Root Cause Diagnosis Skill

## Purpose

Enforce systematic root cause investigation before any fix attempts. This skill prevents shotgun debugging by requiring structured diagnosis through 4 mandatory phases executed in strict order.

**Core Principle:** Understanding WHY a failure occurred is mandatory before attempting HOW to fix it.

---

## Execution Model

This skill expands inline. After invocation, YOU (Claude) execute these phases sequentially.

**Do NOT:**
- Attempt fixes before the investigation phase completes
- Skip phases or reorder them
- Guess at root causes without evidence

---

## When to Use This Skill

**Automatic triggers:**
- TDD Green phase fails after implementation attempt
- Integration tests fail unexpectedly
- QA deep analysis finds violations
- Pre-commit hook blocks commit
- 2+ consecutive fix attempts fail on same issue

**Manual invocation:**
- `/rca` command
- When developer suspects systemic issue
- When failure cause is non-obvious

---

## HALT: NO FIX ATTEMPTS UNTIL Phase 2 COMPLETES

This is a blocking requirement. Any code changes, edits, or operations targeting production or test files are FORBIDDEN until the investigation phase produces a report. Violation of this rule constitutes shotgun debugging and invalidates the diagnosis.

---

## Phase 1: CAPTURE

**Purpose:** Collect all failure artifacts before analysis begins.

**Duration:** 2-5 minutes. Read-only operations.

### Step 1.1: Collect Error Output

Capture the exact failure output:
- Error messages (full text, not summaries)
- Stack traces (complete, not truncated)
- Test output (including assertion details)
- Exit codes

```
artifacts = {
  error_message: <exact error text>,
  stack_trace: <full stack trace if available>,
  test_output: <complete test runner output>,
  exit_code: <numeric exit code>,
  failing_file: <path to file that failed>,
  failing_function: <function/test name>
}
```

### Step 1.2: Collect Phase State

Read current workflow state:
```
Read(file_path="devforgeai/workflows/{STORY_ID}-phase-state.json")
```

Document:
- Current phase (Red/Green/Refactor/Integration/QA)
- Previous phase result
- Number of prior fix attempts for this issue
- Story ID and acceptance criteria being tested

### Step 1.3: Collect Recent Changes

Identify what changed since last passing state:
```
Bash(command="git diff HEAD~3 --stat")
Bash(command="git log --oneline -5")
```

### Step 1.4: Artifact Summary

Produce a structured capture summary:
```
CAPTURE SUMMARY
===============
Story: {STORY_ID}
Phase: {current_phase}
Failure: {one-line description}
Error: {error_message first line}
Files Changed: {list of recently modified files}
Fix Attempts: {count of prior attempts}
```

**Phase 1 Complete Gate:** All artifacts collected. Proceed to Phase 2.

---

## Phase 2: INVESTIGATE

**Purpose:** Cross-reference failure against constitutional context files and trace code-level causation.

### HALT ENFORCEMENT

**HALT: NO FIX ATTEMPTS UNTIL THIS PHASE COMPLETES.**

If prior fix attempts >= 3 without completing Phase 2, escalate to user:
```
AskUserQuestion: "{count} fix attempts have failed without diagnosis.
Systematic investigation is required. Proceed with full diagnosis? [Y/n]"
```

### Step 2a: Spec Compliance Check

**Invoke diagnostic-analyst subagent:**

```
Task(
  subagent_type="diagnostic-analyst",
  description="Investigate failure against constitutional context files",
  prompt="Analyze failure artifacts for spec drift and constraint violations.
    Error: {error_message}
    File: {failing_file}
    Phase: {current_phase}

    Check all 6 context files:
    1. devforgeai/specs/context/tech-stack.md - unapproved technology?
    2. devforgeai/specs/context/source-tree.md - file in wrong location?
    3. devforgeai/specs/context/dependencies.md - wrong version?
    4. devforgeai/specs/context/coding-standards.md - naming/pattern violation?
    5. devforgeai/specs/context/architecture-constraints.md - layer boundary violation?
    6. devforgeai/specs/context/anti-patterns.md - forbidden pattern detected?

    Return structured diagnosis."
)
```

### Step 2b: Code-Level Tracing

Trace the failure through the code:

1. **Read the failing test** - Understand what behavior is expected
2. **Read the implementation** - Understand what behavior is produced
3. **Trace the gap** - Identify where expected diverges from actual
4. **Check imports/dependencies** - Verify all imports resolve
5. **Check data flow** - Trace input through transformations to output

```
# Read failing test
Read(file_path="{test_file}")

# Read implementation under test
Read(file_path="{implementation_file}")

# Search for related patterns
Grep(pattern="{error_keyword}", path="src/")
```

### Step 2c: Investigation Report

Produce structured findings:
```
INVESTIGATION REPORT
====================
Spec Compliance: {PASS | FAIL with details}
Context Violations: {list of violated context files}
Code Trace: {description of where expected diverges from actual}
Root Location: {file:line where root cause exists}
Contributing Factors: {list of secondary issues}
```

**Phase 2 Complete Gate:** Investigation report produced with root location identified.

---

## Phase 3: HYPOTHESIZE

**Purpose:** Generate ranked hypotheses with confidence scores based on Phase 2 evidence.

### Step 3.1: Generate Hypotheses

Based on investigation findings, generate 2-5 hypotheses:

```
HYPOTHESIS RANKING
==================
H1: {description} [Confidence: {0.0-1.0}]
    Evidence: {supporting evidence from Phase 2}
    Category: {spec-drift | test-assertion | import-dependency | coverage | anti-pattern | dod-validation}
    Affected Files: {list}

H2: {description} [Confidence: {0.0-1.0}]
    Evidence: {supporting evidence}
    Category: {category}
    Affected Files: {list}
```

### Step 3.2: Confidence Scoring Criteria

| Score | Meaning | Criteria |
|-------|---------|----------|
| 0.9-1.0 | Near certain | Direct evidence in error output + code trace confirms |
| 0.7-0.8 | High confidence | Strong evidence, one minor ambiguity |
| 0.5-0.6 | Moderate | Multiple possible causes, evidence supports this one |
| 0.3-0.4 | Low | Indirect evidence only |
| 0.0-0.2 | Speculative | No direct evidence, pattern-based guess |

### Step 3.3: Hypothesis Validation

For the top hypothesis (highest confidence):
- Verify it explains ALL observed symptoms
- Verify it is consistent with Phase 2 findings
- Verify the proposed root location matches the hypothesis
- If hypothesis does not explain all symptoms, re-rank

**Phase 3 Complete Gate:** At least one hypothesis with confidence >= 0.5 exists.

---

## Phase 4: PRESCRIBE

**Purpose:** Recommend targeted fixes with specific file paths, line numbers, and actions.

### Step 4.1: Generate Fix Prescription

For each hypothesis (starting with highest confidence):

```
PRESCRIPTION
============
Target Hypothesis: H{n} [{confidence}]
Root Cause: {one-line summary}

Fix Actions:
1. File: {absolute_path}
   Line: {line_number or range}
   Action: {Edit | Write | Delete | Add}
   Change: {specific description of what to change}
   Rationale: {why this fixes the root cause}

2. File: {absolute_path}
   ...

Verification:
  Command: {test command to verify fix}
  Expected: {expected output after fix}
```

### Step 4.2: Risk Assessment

For each prescribed fix:
- **Scope:** How many files affected?
- **Regression Risk:** Could this break other tests?
- **Reversibility:** Can this be undone easily?
- **Side Effects:** What else might change?

### Step 4.3: Fix Ordering

If multiple fixes required, specify execution order:
1. Fixes that address root cause FIRST
2. Fixes that address symptoms SECOND
3. Fixes that are preventive LAST

### Step 4.4: Handoff

Return prescription to invoking workflow phase for execution.

**Phase 4 Complete Gate:** At least one actionable prescription with specific file paths exists.

---

## Escalation Protocol

### 3-Attempt Escalation Rule

If the same failure persists after 3 fix attempts:

1. **Attempt 1-2:** Normal fix-test cycle
2. **Attempt 3:** HALT. Invoke full root-cause-diagnosis skill
3. **After diagnosis:** If prescribed fix fails, escalate to user:

```
AskUserQuestion: "Root cause diagnosis completed but prescribed fix did not resolve:
  Error: {error}
  Hypothesis: {top hypothesis}
  Fix Applied: {description}
  Result: Still failing

  Options:
  1. Try next hypothesis (H{n+1})
  2. Provide additional context
  3. Skip this acceptance criterion (requires justification)"
```

---

## Reference Files

| Reference | Path | Purpose |
|-----------|------|---------|
| Investigation Patterns | `references/investigation-patterns.md` | Failure category taxonomy with investigation steps |
| Workflow Integration | `references/workflow-integration.md` | Integration hooks for dev/QA workflows |

**Load on demand:**
```
Read(file_path=".claude/skills/root-cause-diagnosis/references/investigation-patterns.md")
Read(file_path=".claude/skills/root-cause-diagnosis/references/workflow-integration.md")
```

---

## Output Format

Final diagnosis output follows this structure:

```
ROOT CAUSE DIAGNOSIS REPORT
============================
Story: {STORY_ID}
Phase: {workflow_phase}
Timestamp: {ISO 8601}

CAPTURE:
  Error: {error summary}
  Phase State: {current phase}
  Fix Attempts: {count}

INVESTIGATION:
  Spec Compliance: {PASS/FAIL}
  Context Violations: {list or "None"}
  Root Location: {file:line}

HYPOTHESES:
  H1: {description} [{confidence}]
  H2: {description} [{confidence}]

PRESCRIPTION:
  Primary Fix: {description}
  Files: {list of files to modify}
  Verification: {test command}

STATUS: {DIAGNOSED | ESCALATED | INCONCLUSIVE}
```

---

## Integration with Subagents

| Subagent | Role | Phase |
|----------|------|-------|
| diagnostic-analyst | Read-only spec drift detection | Phase 2 (INVESTIGATE) |

---

## Success Criteria

- [ ] All 4 phases executed in order (CAPTURE -> INVESTIGATE -> HYPOTHESIZE -> PRESCRIBE)
- [ ] No fix attempts before Phase 2 completion
- [ ] At least one hypothesis with confidence >= 0.5
- [ ] Prescription includes specific file paths and actions
- [ ] Escalation triggered after 3 failed attempts
