# ADR-010: Strict Coverage Threshold Enforcement

**Status:** Accepted
**Date:** 2026-01-15
**Decision Makers:** DevForgeAI Framework Maintainers
**Related Stories:** N/A (Framework Consistency Fix)

---

## Context

A framework inconsistency was discovered where coverage gaps below thresholds (95%/85%/80%) were being treated as warnings ("PASS WITH WARNINGS") instead of blocking conditions ("QA FAILED").

### Observed Behavior (Incorrect)

```
QA Validation Complete ✅
STORY-004 is QA Approved with warnings about coverage thresholds being
slightly below strict targets.
- ✅ Functionally complete (all 5 AC verified)
- ⚠️ Coverage slightly below strict thresholds (non-blocking)
```

### Expected Behavior (Correct)

```
QA Validation Failed ❌
STORY-004 is QA Failed - coverage below strict thresholds.
- Coverage gaps must be remediated before QA approval.
```

### Root Cause

Two framework sources gave conflicting guidance:

| Source | Said Coverage Gaps Are... |
|--------|---------------------------|
| `SKILL.md` Phase 3 Step 3.1 | **BLOCKING** - `IF coverage < thresholds: overall_status = "FAILED"` |
| `qa-validation.md` | Listed under "HIGH" violations (ambiguously named "Block Before QA Approval") |

The "Block Before QA Approval" header was misleading - HIGH violations actually allowed "PASS WITH WARNINGS" progression.

---

## Decision

**Coverage gaps below thresholds are CRITICAL blockers, not warnings.**

### Enforcement Rules

1. Coverage below 95% (Business Logic) → QA FAILED (no exceptions)
2. Coverage below 85% (Application Layer) → QA FAILED (no exceptions)
3. Coverage below 80% (Infrastructure Layer) → QA FAILED (no exceptions)
4. test-automator returning WARN for coverage → escalates to FAILED at Phase 3
5. No deferral path exists for coverage gaps

### Changes Made

| File | Change |
|------|--------|
| `.claude/rules/workflow/qa-validation.md` | Moved "Coverage below thresholds" from HIGH to CRITICAL section |
| `.claude/skills/devforgeai-qa/SKILL.md` | Added clarifying comments at Phase 3 Step 3.1 |
| `.claude/skills/devforgeai-qa/references/parallel-validation.md` | Added "Coverage WARN Escalation" section |

---

## Rationale

### Why Strict (Not Warning)?

1. **Quality gates are architectural constraints** - Coverage thresholds exist to ensure code quality. Allowing exceptions undermines the purpose.

2. **Coverage gaps cannot be deferred** - Unlike documentation or minor issues, missing tests represent actual risk that compounds over time.

3. **"PASS WITH WARNINGS" creates false confidence** - Stories marked "QA Approved" should actually be ready for release.

4. **Framework consistency** - SKILL.md already had the correct logic (`coverage < thresholds → FAILED`). This decision aligns all documentation with that logic.

### Considered Alternatives

**Alternative A: Keep as Warning (Rejected)**
- Pros: Allows faster iteration, developer flexibility
- Cons: Quality degradation over time, inconsistent with stated thresholds

**Alternative B: Tiered Enforcement (Rejected)**
- 95% strict, 85%/80% as warnings
- Pros: Flexible for different layers
- Cons: Complexity, opens door to threshold erosion

**Alternative C: Strict for All (Accepted)**
- All thresholds are blocking conditions
- Pros: Consistent enforcement, clear expectations
- Cons: May slow initial development

---

## Consequences

### Positive

- QA FAILED status clearly indicates coverage must be remediated
- No ambiguity about threshold enforcement
- Framework documentation is now consistent

### Negative

- Stories with coverage gaps will fail QA (intentional)
- Developers must write more tests before QA passes
- May slow development velocity initially

### Neutral

- Existing "QA Approved" stories are not retroactively affected
- No changes to threshold values (95%/85%/80% unchanged)

---

## Verification

After implementation, verify:

1. Run `/qa` on a story with coverage below thresholds
2. Confirm result is "QA FAILED" (not "PASS WITH WARNINGS")
3. Confirm validator summary shows coverage as blocking condition
4. Confirm no path to QA Approved without meeting thresholds

---

## References

- `.claude/rules/workflow/qa-validation.md` - Coverage Threshold Enforcement section
- `.claude/skills/devforgeai-qa/SKILL.md` - Phase 3 Step 3.1
- `.claude/skills/devforgeai-qa/references/parallel-validation.md` - Coverage WARN Escalation section
