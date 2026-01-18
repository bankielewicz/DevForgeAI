# RCA-002: QA CLI Execution and Gaps File Validation Missing

**Date:** 2026-01-15
**Reporter:** User
**Component:** devforgeai-qa skill
**Severity:** HIGH

---

## Issue Description

Two related issues discovered during STORY-004 QA validation:

1. **CLI Execution Not Tested:** QA validation passed STORY-004 and marked it "QA Approved" despite the CLI being non-functional (`python -m treelint` failed due to missing `__main__.py`). Tests passed because `typer.testing.CliRunner` bypasses the entry point.

2. **gaps.json Not Created:** When user discovered the CLI failure and pointed it out, the mandatory `gaps.json` file was not automatically created when status changed to "QA Failed" - it required explicit user prompting.

**Impact:** Story incorrectly marked as ready for release; remediation file not available for `/dev` command to fix issues.

---

## 5 Whys Analysis

### Issue 1: CLI Execution Not Tested

| Why | Question | Answer | Evidence |
|-----|----------|--------|----------|
| #1 | Why did QA pass without catching CLI failure? | QA only runs pytest with CliRunner, not actual `python -m` execution | Executed `pytest tests/integration/test_cli.py` - tests use CliRunner |
| #2 | Why doesn't QA workflow include actual CLI execution? | Phase 1 Validation only defines test runner execution and coverage - no smoke test step | SKILL.md lines 357-448: Only Steps 1.1 (Traceability) and 1.2 (Coverage) |
| #3 | Why doesn't QA skill include runtime validation? | QA designed around test-first (TDD artifacts), not runtime verification | Deep mode (lines 67-74): coverage, anti-patterns, spec compliance - no runtime |
| #4 | Why was runtime testing not part of QA design? | Runtime validation implicitly deferred to Release phase | quality-gates.md: Gate 3 has no runtime requirement |
| **#5** | **Why no connection between QA and runtime verification?** | **ROOT CAUSE: QA skill lacks mandatory runtime smoke test step** | SKILL.md examined - no such step exists |

### Issue 2: gaps.json Not Created

| Why | Question | Answer | Evidence |
|-----|----------|--------|----------|
| #1 | Why wasn't gaps.json created when CLI failed? | Failure discovered post-QA workflow, not during execution | User manual challenge, not workflow detection |
| #2 | Why didn't I create gaps.json when updating status? | Was in "correction mode" not "QA workflow mode" | Status changed but Phase 3 requirements not followed |
| #3 | Why did I skip mandatory gaps.json creation? | Outside normal workflow execution context | SKILL.md line 668: "MANDATORY if FAILED" - but I wasn't in workflow |
| #4 | Why no enforcement of gaps.json on status change? | gaps.json creation buried in Phase 3 logic, not status transition | Atomic protocol (Step 3.4) doesn't trigger gaps.json |
| **#5** | **Why isn't gaps.json linked to QA Failed status?** | **ROOT CAUSE: gaps.json creation not tied to status transition** | Atomic protocol examined - no gaps.json trigger |

---

## Evidence Collected

### Files Examined

#### 1. `.claude/skills/devforgeai-qa/SKILL.md` (PRIMARY)

**Lines 59-74 - Validation Modes:**
```markdown
### Deep (~35K tokens, 8-12 min)
- Complete coverage analysis (95%/85%/80% thresholds)
- Comprehensive anti-pattern detection
- Full spec compliance (AC, API, NFRs)
- Code quality metrics
- Security scanning (OWASP Top 10)
- Deferral validation (if deferrals exist)
```
**Significance:** No "runtime smoke test" or "CLI execution validation" listed

**Lines 357-448 - Phase 1 Validation:**
```markdown
### Step 1.1: AC-DoD Traceability Validation
...
### Step 1.2: Test Coverage Analysis
```
**Significance:** Only two validation steps - no Step 1.3 for runtime

**Lines 666-684 - gaps.json Requirement:**
```markdown
**3. Generate gaps.json (FAILED Only):**

**MANDATORY if overall_status == "FAILED":**
...
# Verify creation
Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
IF NOT found:
    HALT: "gaps.json not created - required for /dev remediation mode"
```
**Significance:** Documented as MANDATORY but only within workflow context

#### 2. `.claude/rules/core/quality-gates.md`

**Lines 14-20 - Gate 3 Criteria:**
```markdown
**Gate 3: QA Approval** (QA Approved → Releasing)
- Criteria: Coverage meets thresholds, zero CRITICAL/HIGH violations
- Validated by: devforgeai-qa skill (deep validation)
- Blocks: Release if quality insufficient
```
**Significance:** No runtime execution requirement in gate criteria

### Context Files Status

| File | Status | Notes |
|------|--------|-------|
| tech-stack.md | ✅ EXISTS | Not violated |
| source-tree.md | ✅ EXISTS | Not violated |
| dependencies.md | ✅ EXISTS | Not violated |
| coding-standards.md | ✅ EXISTS | Not violated |
| architecture-constraints.md | ✅ EXISTS | Not violated |
| anti-patterns.md | ✅ EXISTS | Not violated |

**Conclusion:** Issue is workflow gap, not constraint violation

---

## Recommendations

### CRITICAL (Implement Immediately)

#### REC-1: Add Runtime Smoke Test to QA Deep Validation

**Implemented in:** STORY-257

**Problem:** QA passes stories without verifying actual runtime execution

**Solution:** Add "Step 1.3: Runtime Smoke Test" to Phase 1

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Location:** After Step 1.2 (line 448)

**Implementation:**
```markdown
### Step 1.3: Runtime Smoke Test [NEW - RCA-002]

**Purpose:** Verify deliverable can actually execute, not just pass tests.

**MANDATORY for CLI/API projects.**

```
# Detect project type from story and files
IF story mentions "CLI" OR files include "cli.py":
    PROJECT_TYPE = "cli"

# Execute runtime smoke test
IF PROJECT_TYPE == "cli":
    package_name = extract_from_pyproject_toml()

    result = Bash(command="python -m {package_name} --help", timeout=10000)

    IF result.exit_code != 0:
        Display: "❌ CRITICAL: CLI not executable"
        Display: "   Command: python -m {package_name} --help"
        Display: "   Error: {result.stderr}"

        runtime_violations.append({
            type: "RUNTIME_EXECUTION_FAILURE",
            severity: "CRITICAL",
            message: "CLI cannot be invoked via python -m",
            remediation: "Create src/{package}/__main__.py"
        })

        overall_status = "FAILED"
    ELSE:
        Display: "✓ CLI smoke test passed"
```

**Rationale:** CliRunner bypasses `__main__.py` - actual execution required

**Testing:**
1. Create project with tests passing but missing `__main__.py`
2. Run `/qa STORY-XXX deep`
3. Verify QA fails with "CLI not executable"

**Effort:** Medium (1-2 hours)

---

### HIGH (Implement This Sprint)

#### REC-2: Link gaps.json Creation to QA Failed Status Transition

**Implemented in:** STORY-258

**Problem:** gaps.json not created when QA fails outside normal workflow

**Solution:** Add gaps.json creation to atomic status update protocol

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Location:** Step 3.4, Step 2 (after line 722)

**Implementation:**
```markdown
# Determine target status
IF overall_status == "PASSED" OR overall_status == "PASS WITH WARNINGS":
    target_status = "QA Approved"
ELSE:
    target_status = "QA Failed"

    # MANDATORY: Create gaps.json BEFORE status update [RCA-002]
    IF NOT exists("devforgeai/qa/reports/{STORY-ID}-gaps.json"):
        Write(file_path="devforgeai/qa/reports/{STORY-ID}-gaps.json",
              content=gaps_json_from_current_violations)
        Display: "✓ gaps.json created (required for QA Failed status)"
```

**Effort:** Low (30-60 min)

---

#### REC-3: Add gaps.json Verification to Phase 4 Execution Summary

**Implemented in:** STORY-259

**Problem:** No validation that gaps.json exists when QA failed

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Location:** Step 4.3 (around line 1000)

**Implementation:**
```markdown
**Validation Checkpoint:**
- [ ] Execution summary displayed?
- [ ] All phases marked complete?
- [ ] Story file update confirmed?
- [ ] **IF QA FAILED: gaps.json exists?** [RCA-002]

IF overall_status == "FAILED":
    Glob(pattern="devforgeai/qa/reports/{STORY-ID}-gaps.json")
    IF NOT found:
        Display: "❌ CRITICAL: gaps.json missing for failed QA"
        HALT: "Create gaps.json before completing QA workflow"
```

**Effort:** Low (15-30 min)

---

### MEDIUM (Next Sprint)

#### REC-4: Document Runtime Smoke Test in Deep Validation Workflow Reference

**Implemented in:** STORY-260

**File:** `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md`

Add section "1.4 Runtime Smoke Test" with:
- Language-specific smoke test commands
- Project type detection logic
- Expected outputs

**Effort:** Low (30 min)

---

#### REC-5: Add Runtime Executable to Quality Gate 3 Criteria

**Implemented in:** STORY-261

**File:** `.claude/rules/core/quality-gates.md`

**Change:**
```markdown
**Gate 3: QA Approval** (QA Approved → Releasing)
- Criteria: Coverage meets thresholds, zero CRITICAL/HIGH violations, **runtime smoke test passes**
```

**Effort:** Low (15 min)

---

### LOW (Backlog)

None

---

## Implementation Checklist

- [ ] **REC-1:** Add Step 1.3 Runtime Smoke Test to SKILL.md → **STORY-257**
- [ ] **REC-2:** Add gaps.json creation to atomic status protocol → **STORY-258**
- [ ] **REC-3:** Add gaps.json verification to Phase 4 → **STORY-259**
- [ ] **REC-4:** Document in deep-validation-workflow.md → **STORY-260**
- [ ] **REC-5:** Update quality-gates.md → **STORY-261**
- [ ] Mark RCA-002 as RESOLVED
- [ ] Commit changes to git

**Epic:** EPIC-040 (QA Runtime Validation Enhancements)

---

## Prevention Strategy

### Short-Term
1. Add runtime smoke test to QA workflow (REC-1)
2. Link gaps.json to status transition (REC-2)

### Long-Term
1. Consider adding smoke test to development workflow (Phase 6 in /dev)
2. Create automated test for "entry point exists" during build
3. Add pre-release checklist validation

### Monitoring
- Watch for future "tests pass but runtime fails" scenarios
- Audit QA reports for runtime validation completion
- Track gaps.json creation rate for failed QA runs

---

## Related RCAs

- **RCA-001:** Phase state module missing (similar workflow gap pattern)
- **RCA-006:** Autonomous deferrals (similar "mandatory step skipped" pattern)

---

## Resolution Status

**Status:** STORIES CREATED

**Epic:** EPIC-040 (QA Runtime Validation Enhancements)

**Stories Created:**
| Story | Recommendation | Priority | Status |
|-------|----------------|----------|--------|
| STORY-257 | REC-1: Runtime Smoke Test | Critical | Backlog |
| STORY-258 | REC-2: gaps.json Status Link | High | Backlog |
| STORY-259 | REC-3: gaps.json Verification | High | Backlog |
| STORY-260 | REC-4: Documentation | Medium | Backlog |
| STORY-261 | REC-5: Quality Gate Update | Medium | Backlog |

**Next Action:** Implement STORY-257 (REC-1: Runtime Smoke Test) as highest priority

---

**RCA Author:** devforgeai-rca skill
**RCA Date:** 2026-01-15
