---
id: BRAINSTORM-005
title: "100% Spec Compliance for DevForgeAI"
category: framework-improvement
status: complete
created: 2026-01-19
confidence_level: HIGH
source_research: RESEARCH-002
stakeholders:
  - Framework developers
  - End users of DevForgeAI
  - Quality assurance teams
primary_goal: "100% AC compliance"
---

# BRAINSTORM-005: 100% Spec Compliance for DevForgeAI

## Executive Summary

This brainstorm transforms RESEARCH-002 findings into actionable improvements for achieving 100% acceptance criteria compliance in the DevForgeAI framework. Through stakeholder analysis, problem exploration, and story file examination, we identified that **QA has a 100% miss rate on AC compliance issues** because it lacks fresh context, systematic AC-by-AC review, and direct source code inspection. The user's manual workaround (separate session AC review) works perfectly - this brainstorm codifies that technique into the workflow.

---

## Stakeholder Map

### Primary Stakeholders
| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| Framework developers | 100% AC compliance | Breaking existing workflows |
| End users | Reliable, predictable framework | Token/cost overhead |
| QA teams | Effective quality gates | Missing issues |

### Stakeholder Conflicts
- **Quality vs. Speed:** More verification = slower workflow
- **Thoroughness vs. Cost:** Fresh context subagents = token overhead
- **Resolution:** User prioritizes quality over cost

---

## Problem Statement

**DevForgeAI developers experience AC compliance gaps escaping to production because:**

1. **AC parsing ambiguity** - Technical Specification and AC Checklist are parallel documents without explicit linking
2. **No verification gaps** - QA doesn't perform fresh-context, one-by-one AC review against source code
3. **Phase skipping** - Under pressure, workflow phases get compressed

**Resulting in:** Manual workaround where user asks Claude in a separate session to "review the acceptance criteria checklist one-by-one and tell me if they are complete by reviewing the actual source code."

**Evidence:** Examined STORY-264, STORY-257, STORY-268 - found no explicit AC#X → COMP-XXX mapping in Technical Specifications.

---

## Root Cause Analysis (5 Whys)

1. **Why do AC compliance gaps escape to production?**
   → QA doesn't catch them

2. **Why doesn't QA catch them?**
   → QA relies on test results, not direct source code inspection against AC

3. **Why doesn't QA inspect source code against AC?**
   → The workflow doesn't include a fresh-context verification step

4. **Why doesn't the workflow include fresh-context verification?**
   → It was assumed test passing = AC complete (incorrect assumption)

5. **Why was this assumed?**
   → Original design focused on TDD compliance, not AC-by-AC verification

**Root Cause:** Workflow design gap - no independent verification that AC requirements are actually met in source code.

---

## Current State

| Aspect | Current State | Pain Level |
|--------|---------------|------------|
| AC parsing | Markdown text, ambiguous boundaries | HIGH |
| AC → Tech Spec mapping | Implicit, no explicit IDs | HIGH |
| AC verification | Test results only | CRITICAL |
| Fresh context review | Manual workaround | CRITICAL |
| Phase enforcement | Documented but not validated | MEDIUM |

### Failed Solution History
- AC Verification Checklist added (STORY-268) - helps tracking but doesn't verify compliance
- QA deep validation - checks coverage, not AC-by-AC source compliance
- DoD checkboxes - self-reported, no independent verification

---

## Opportunities

### Opportunity 1: Phase 4.5 Verification Subagent (MUST HAVE)

**Description:** Automated replication of user's manual workaround

**Implementation:**
```markdown
## Phase 4.5: AC Compliance Verification Bridge

**[MANDATORY] Invoke Verification Subagent:**
Task(
  subagent_type="ac-compliance-verifier",  // New subagent
  description="Fresh context AC compliance verification",
  prompt="""
You are verifying AC compliance for STORY-XXX.

TECHNIQUE (proven effective):
1. Fresh context - you have NO knowledge of implementation decisions
2. One-by-one - review EACH AC criterion separately
3. Source inspection - READ the actual source code files
4. Enhanced - also check coverage and anti-patterns

FOR EACH AC:
1. Read the AC requirement (Given/When/Then)
2. Read the source files that implement it
3. Verify the source code ACTUALLY implements the AC
4. Check test coverage for the AC
5. Check for anti-pattern violations

RETURN:
- AC#X: PASS/FAIL with specific evidence
- Files inspected: [list]
- Issues found: [list with line numbers]
- Overall: PASS/FAIL
"""
)

**HALT Condition:** If ANY AC returns FAIL, HALT and report specific issues.
Do NOT proceed to Phase 05 until all ACs pass verification.
```

**Benefits:**
- Fresh context eliminates implementation bias
- Systematic AC-by-AC review catches all gaps
- Source code inspection verifies actual compliance
- Issues caught BEFORE integration tests

### Opportunity 2: XML-Tagged AC Blocks (SHOULD HAVE)

**Description:** Machine-readable AC format for improved parsing

**Implementation:**
```xml
### AC#1: User Authentication

<acceptance_criteria id="AC1" implements="COMP-001,COMP-002">
  <given>User has valid credentials</given>
  <when>User submits login form</when>
  <then>System returns JWT token with 24-hour expiry</then>
  <verification>
    <test_file>tests/test_auth.py</test_file>
    <coverage_threshold>95</coverage_threshold>
    <source_files>
      - src/auth/handler.py
      - src/auth/jwt_utils.py
    </source_files>
  </verification>
</acceptance_criteria>
```

**Benefits:**
- Claude parses AC with higher accuracy (Anthropic-confirmed)
- Explicit `implements` attribute links to COMP-XXX
- `source_files` tells verifier exactly what to inspect

### Opportunity 3: AC → Tech Spec Traceability (SHOULD HAVE)

**Description:** Explicit bidirectional mapping between AC and COMP requirements

**Implementation:**
```yaml
technical_specification:
  components:
    - type: "Service"
      name: "AuthHandler"
      requirements:
        - id: "COMP-001"
          implements_ac: ["AC#1"]  # NEW: Explicit AC link
          description: "Validate user credentials"
          testable: true
        - id: "COMP-002"
          implements_ac: ["AC#1"]  # NEW: Explicit AC link
          description: "Generate JWT token"
          testable: true
```

**Benefits:**
- No ambiguity about what COMP-XXX implements
- Verification subagent can cross-check mapping
- Implementation drift is immediately detectable

### Opportunity 4: Phase 5.5 Verification Confirmation (COULD HAVE)

**Description:** Second verification checkpoint after integration tests

**Implementation:** Same as Phase 4.5 but runs after Phase 05 (Integration Testing)

**Benefits:**
- Safety net catches issues missed in Phase 4.5
- Verifies integration didn't break AC compliance
- Final check before deferral challenge

---

## Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Backward compatible | High | Graceful skip for stories without XML/traceability |
| Token efficiency | Medium | User prioritizes quality; acceptable overhead |
| Claude Code Terminal only | High | All solutions use native tools (Task, Read, Grep) |

---

## Hypotheses

| ID | Hypothesis | Success Metric | Validation Approach |
|----|------------|----------------|---------------------|
| H1 | XML AC tags improve parsing accuracy | 0 AC misinterpretations | Test on 5 stories |
| H2 | AC-TechSpec traceability eliminates drift | 100% COMP → AC mapping | Template enforcement |
| H3 | Phase 4.5 verification catches gaps | Issues found BEFORE integration | Compare to current state |
| H4 | Phase 5.5 confirmation is safety net | 0 issues in manual review | Eliminate manual workaround |

**Critical Hypothesis:** H3 - If implemented correctly, should eliminate need for manual workaround.

---

## Prioritization

### MoSCoW Classification

| Initiative | Classification | Rationale |
|------------|---------------|-----------|
| H3: Phase 4.5 Verification Subagent | **MUST HAVE** | Directly addresses root cause |
| H1: XML-tagged AC Blocks | **SHOULD HAVE** | Improves parsing accuracy |
| H2: AC → Tech Spec Traceability | **SHOULD HAVE** | Eliminates spec mismatch |
| H4: Phase 5.5 Verification | **COULD HAVE** | Safety net |

### Implementation Sequence

| Order | Initiative | Effort | Timeline | Dependencies |
|-------|-----------|--------|----------|--------------|
| 1 | H3: Phase 4.5 Verification Subagent | Medium | 3-5 days | None |
| 2 | H1: XML-tagged AC Blocks | Medium | 3-5 days | Story template |
| 3 | H2: AC → Tech Spec Traceability | Medium | 3-5 days | H1 |
| 4 | H4: Phase 5.5 Verification | Low | 1-2 days | H3 |

**Total Estimated Effort:** 10-17 days (can be parallelized)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Verification subagent increases token cost | 80% | LOW | User accepts this tradeoff |
| XML tags require template migration | 60% | MEDIUM | Gradual migration, backward compatible |
| Phase 4.5 slows workflow | 70% | LOW | Quality prioritized over speed |
| Fresh context misses context | 20% | MEDIUM | Pass story file as context |

---

## Next Steps

### Immediate (Sprint 1)
1. Create `ac-compliance-verifier` subagent spec
2. Add Phase 4.5 to devforgeai-development SKILL.md
3. Test on STORY-250 through STORY-268 retrospectively

### Short-term (Sprint 2)
4. Update story template with XML AC format
5. Add `implements_ac` to Technical Specification schema
6. Migrate 5 high-priority stories to new format

### Medium-term (Sprint 3)
7. Add Phase 5.5 verification checkpoint
8. Create migration guide for existing stories
9. Measure impact on AC compliance rate

---

## Handoff to Ideation

This brainstorm is ready for `/ideate` to transform into formal requirements.

**Key inputs for ideation:**
- Primary initiative: Phase 4.5 Verification Subagent
- Stakeholders: Framework developers, end users, QA teams
- Constraints: Backward compatible, Claude Code Terminal only
- Success metric: 0 AC compliance issues escaping to production

**Recommended command:**
```bash
/ideate "Phase 4.5 AC Compliance Verification Subagent"
```

---

## Source Research

- **RESEARCH-002:** DevForgeAI Spec-Driven Framework Reliability & Prompt Engineering Best Practices
- **Story Analysis:** STORY-264, STORY-257, STORY-268

---

## Change Log

| Date | Change |
|------|--------|
| 2026-01-19 | Initial brainstorm created from RESEARCH-002 |
