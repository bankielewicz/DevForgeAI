# EPIC-046 AC Compliance Verification System - Requirements Specification

**Version:** 1.0
**Date:** 2026-01-19
**Status:** Draft
**Author:** DevForgeAI Ideation Skill
**Complexity Score:** 25/60 (Tier 2 - Moderate)
**Source Brainstorm:** BRAINSTORM-005
**Source Research:** RESEARCH-002

---

## 1. Project Overview

### 1.1 Project Context

**Type:** Brownfield (extending existing DevForgeAI framework)
**Domain:** Software Development Framework / Quality Assurance Tooling
**Timeline:** 2 sprints (estimated 10-17 days)
**Team:** Single developer (framework internal)

### 1.2 Problem Statement

DevForgeAI developers experience AC compliance gaps escaping to production because:

1. **AC parsing ambiguity** - Technical Specification and AC Checklist are parallel documents without explicit linking
2. **No verification gaps** - QA doesn't perform fresh-context, one-by-one AC review against source code
3. **Phase skipping** - Under pressure, workflow phases get compressed

**Current Workaround:** User manually asks Claude in a separate session: "review the acceptance criteria checklist one-by-one and tell me if they are complete by reviewing the actual source code."

**Evidence:** Examined STORY-264, STORY-257, STORY-268 - found no explicit AC#X → COMP-XXX mapping in Technical Specifications. QA has 100% miss rate on AC compliance issues.

### 1.3 Solution Overview

Automate the proven manual workaround by creating:

1. **ac-compliance-verifier subagent** - Fresh-context verification with source code inspection
2. **Phase 4.5 insertion point** - After TDD refactor, before integration tests
3. **Phase 5.5 insertion point** - After integration tests, before deferral challenge
4. **XML AC format** - Machine-readable acceptance criteria for improved parsing
5. **AC-TechSpec traceability** - Explicit `implements_ac` linking

### 1.4 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| AC compliance gaps escaping to production | 0 | Post-release defect tracking |
| Manual workaround usage | Eliminated | User feedback |
| Verification evidence per AC | 100% | JSON report audit |
| Source code inspection per AC | 100% | Subagent execution logs |

---

## 2. User Roles & Personas

### 2.1 Primary Users

1. **Framework Developers** - Build features using DevForgeAI /dev workflow
2. **QA Reviewers** - Validate implementations meet acceptance criteria
3. **End Users** - Rely on reliable, predictable framework behavior

### 2.2 User Personas

**Persona 1: Framework Developer**
- **Role:** Implements user stories using TDD workflow
- **Goals:** Ship features that fully meet acceptance criteria
- **Needs:** Automated verification that catches gaps before integration
- **Pain Points:** Manual AC review is tedious and error-prone; issues discovered late in workflow

**Persona 2: QA Reviewer**
- **Role:** Validates story implementations before release
- **Goals:** Confidence that all ACs are met with evidence
- **Needs:** Audit trail showing per-AC verification results
- **Pain Points:** QA validation currently misses AC compliance issues (100% miss rate)

**Persona 3: Framework End User**
- **Role:** Uses DevForgeAI to build applications
- **Goals:** Reliable framework behavior that matches documentation
- **Needs:** Trust that framework features work as specified
- **Pain Points:** Framework bugs due to incomplete AC implementation

---

## 3. Functional Requirements

### 3.1 User Stories

#### Feature 1: Verification Subagent Core

**US-1.1: Subagent File Creation**
```
As a framework developer,
I want the ac-compliance-verifier subagent to have proper YAML frontmatter,
So that Claude Code Terminal can discover and invoke it correctly.

Acceptance Criteria:
- File location: .claude/agents/ac-compliance-verifier.md
- YAML frontmatter includes: name, description, tools (Read, Grep, Glob), model
- System prompt explains fresh-context verification technique
- Single responsibility: AC verification only
```

**US-1.2: XML AC Parsing**
```
As a verification subagent,
I want to parse XML-tagged acceptance criteria from story files,
So that I can systematically verify each AC one-by-one.

Acceptance Criteria:
- Parse <acceptance_criteria id="ACX"> blocks
- Extract Given/When/Then statements
- Extract source_files hints (if provided)
- HALT if story lacks XML AC format
```

**US-1.3: Source Code Inspection**
```
As a verification subagent,
I want to read and inspect actual source code files,
So that I can verify the code implements the AC requirements.

Acceptance Criteria:
- Use Read() to load source files referenced in AC
- Search for implementation patterns matching AC requirements
- Identify specific lines/functions that implement AC
- Document evidence (file path, line numbers, code snippets)
```

**US-1.4: Coverage Verification**
```
As a verification subagent,
I want to verify test coverage exists for each AC,
So that I can confirm the AC is properly tested.

Acceptance Criteria:
- Locate test files for the story (tests/STORY-XXX/)
- Verify tests exist for each AC
- Check test naming follows convention: test_ac{N}_*
- Flag ACs without corresponding tests
```

**US-1.5: Anti-Pattern Detection**
```
As a verification subagent,
I want to check for anti-pattern violations in implementation,
So that I can catch quality issues during verification.

Acceptance Criteria:
- Check against devforgeai/specs/context/anti-patterns.md
- Flag any anti-pattern violations found in implementation
- Include violation details in verification report
```

**US-1.6: JSON Report Generation**
```
As a verification subagent,
I want to generate a JSON verification report,
So that there is an audit trail of AC compliance.

Acceptance Criteria:
- Report location: devforgeai/qa/verification/{STORY-ID}-ac-verification.json
- Include per-AC pass/fail status with evidence
- Include files inspected list
- Include issues found with line numbers
- Include overall pass/fail determination
- Include timestamp and verification duration
```

#### Feature 2: Phase Integration

**US-2.1: Phase 4.5 Insertion Point**
```
As a framework developer,
I want AC verification to run after TDD refactor phase,
So that compliance issues are caught before integration tests.

Acceptance Criteria:
- Add Phase 4.5 between Phase 04 (Refactor) and Phase 05 (Integration)
- Invoke ac-compliance-verifier subagent via Task()
- Pass story ID and story file path as context
- Wait for verification to complete before proceeding
```

**US-2.2: Phase 5.5 Insertion Point**
```
As a framework developer,
I want a second AC verification after integration tests,
So that integration changes don't break AC compliance.

Acceptance Criteria:
- Add Phase 5.5 between Phase 05 (Integration) and Phase 06 (Deferral)
- Use same subagent invocation pattern as Phase 4.5
- Verify all ACs still pass after integration
```

**US-2.3: HALT Behavior on Failure**
```
As a framework developer,
I want the workflow to HALT if any AC fails verification,
So that I must fix issues before proceeding.

Acceptance Criteria:
- HALT /dev workflow if verification returns ANY failure
- Display detailed failure report (AC ID, issue, evidence)
- Do NOT proceed to next phase until issues resolved
- Allow user to re-run verification after fixes
```

**US-2.4: Phase Documentation Update**
```
As a framework maintainer,
I want updated documentation for the new phases,
So that developers understand the verification workflow.

Acceptance Criteria:
- Update devforgeai-development SKILL.md with Phase 4.5/5.5
- Create reference file: references/ac-verification-workflow.md
- Update coding-standards.md phase naming table
```

#### Feature 3: XML AC Format

**US-3.1: XML Schema Design**
```
As a framework architect,
I want a well-defined XML schema for acceptance criteria,
So that parsing is consistent and accurate.

Acceptance Criteria:
- Define <acceptance_criteria> element with attributes: id, implements
- Define <given>, <when>, <then> child elements
- Define optional <verification> element with source_files hints
- Document schema in coding-standards.md
```

**US-3.2: Story Template Update**
```
As a framework maintainer,
I want the story template to use XML AC format,
So that new stories have machine-readable acceptance criteria.

Acceptance Criteria:
- Update .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
- Include XML AC format with example
- Include guidance for populating source_files hints
```

**US-3.3: Migration Guide**
```
As a framework developer,
I want a guide for migrating existing stories to XML format,
So that I can update my stories to use the new format.

Acceptance Criteria:
- Create docs/guides/ac-xml-migration-guide.md
- Include before/after examples
- Include regex patterns for automated conversion (if applicable)
- Include validation checklist
```

#### Feature 4: AC-TechSpec Traceability

**US-4.1: Technical Specification Schema Update**
```
As a framework architect,
I want COMP-XXX requirements to link to AC#X,
So that there is bidirectional traceability.

Acceptance Criteria:
- Add implements_ac field to COMP-XXX requirements
- Field accepts array of AC IDs: ["AC#1", "AC#2"]
- Validation: all referenced ACs must exist in story
```

**US-4.2: Story Creation Automation**
```
As a framework developer,
I want devforgeai-story-creation to generate traceability links,
So that I don't have to manually maintain them.

Acceptance Criteria:
- Update story creation to auto-generate implements_ac when creating COMP
- Cross-reference with AC section
- Warn if COMP has no implements_ac link
```

**US-4.3: Traceability Validation**
```
As a QA reviewer,
I want validation that all ACs have corresponding COMPs,
So that nothing is missed in the technical specification.

Acceptance Criteria:
- Add validation: every AC#X should appear in at least one implements_ac
- Add validation: every implements_ac reference should point to existing AC
- Flag orphaned ACs and COMPs
```

### 3.2 Feature Requirements Matrix

| Feature | Stories | Estimated Points | Priority |
|---------|---------|------------------|----------|
| F1: Verification Subagent Core | 6 | 13 | P0 MUST |
| F2: Phase Integration | 4 | 8 | P0 MUST |
| F3: XML AC Format | 3 | 8 | P1 SHOULD |
| F4: AC-TechSpec Traceability | 3 | 5 | P1 SHOULD |
| **TOTAL** | **16** | **34** | |

---

## 4. Data Requirements

### 4.1 Data Model

#### Entity: Story File (Existing)

**File Path:** `devforgeai/specs/Stories/STORY-XXX-title.story.md`

**Relevant Sections:**
- YAML frontmatter (id, title, epic, status)
- Acceptance Criteria (XML format - new)
- Technical Specification (COMP-XXX requirements)

#### Entity: Acceptance Criteria (New XML Format)

```xml
<acceptance_criteria id="AC1" implements="COMP-001,COMP-002">
  <given>User has valid credentials</given>
  <when>User submits login form</when>
  <then>System returns JWT token with 24-hour expiry</then>
  <verification>
    <test_file>tests/STORY-XXX/test_ac1_authentication.py</test_file>
    <coverage_threshold>95</coverage_threshold>
    <source_files>
      <file>src/auth/handler.py</file>
      <file>src/auth/jwt_utils.py</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

#### Entity: Verification Result (New)

**File Path:** `devforgeai/qa/verification/{STORY-ID}-ac-verification.json`

```json
{
  "story_id": "STORY-XXX",
  "verification_timestamp": "2026-01-19T12:34:56Z",
  "verification_duration_seconds": 75,
  "phase": "4.5",
  "overall_result": "PASS|FAIL",
  "acceptance_criteria": [
    {
      "ac_id": "AC1",
      "result": "PASS|FAIL",
      "evidence": {
        "source_files_inspected": [
          {"file": "src/auth/handler.py", "lines": [45, 67, 89]}
        ],
        "tests_found": ["test_ac1_authentication.py"],
        "coverage_met": true,
        "anti_patterns_detected": []
      },
      "issues": []
    }
  ],
  "files_inspected": ["src/auth/handler.py", "src/auth/jwt_utils.py"],
  "total_issues": 0
}
```

### 4.2 Data Constraints

| Constraint | Enforcement |
|------------|-------------|
| AC ID format: AC1, AC2, AC3... | Regex validation: `^AC\d+$` |
| COMP ID format: COMP-001, COMP-002... | Regex validation: `^COMP-\d{3}$` |
| Verification report must be valid JSON | JSON schema validation |
| source_files must be relative paths | Path validation (no absolute paths) |

---

## 5. Integration Requirements

### 5.1 Internal Framework Integration

| Integration Point | Protocol | Data Flow |
|-------------------|----------|-----------|
| devforgeai-development SKILL.md | Task() invocation | Story ID → Subagent → Verification Result |
| Story files | Read() | Subagent reads XML AC blocks |
| Source files | Read() | Subagent reads implementation code |
| QA reports directory | Write() | Subagent writes JSON verification report |

### 5.2 Subagent Invocation Pattern

```markdown
Task(
  subagent_type="ac-compliance-verifier",
  description="Fresh context AC compliance verification for STORY-XXX",
  prompt="""
  Verify AC compliance for STORY-XXX.

  Story file: devforgeai/specs/Stories/STORY-XXX-title.story.md

  TECHNIQUE:
  1. Fresh context - you have NO knowledge of implementation decisions
  2. One-by-one - review EACH AC criterion separately
  3. Source inspection - READ the actual source code files
  4. Coverage check - verify tests exist for each AC
  5. Anti-pattern check - scan for violations

  Return JSON verification report.
  """
)
```

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target | Rationale |
|--------|--------|-----------|
| Verification time per story | 60-120 seconds | Quality prioritized over speed |
| Parallel AC verification | Supported (≥5 ACs) | Faster for large stories |
| Token overhead per verification | ~5,000-15,000 | Acceptable per user |

### 6.2 Security

| Requirement | Implementation |
|-------------|----------------|
| Read-only access | Tools: Read, Grep, Glob only |
| No file modifications | Subagent cannot use Write or Edit |
| No external network | Subagent cannot use WebFetch or WebSearch |

### 6.3 Scalability

| Factor | Capacity |
|--------|----------|
| ACs per story | 1-20 supported |
| Parallel verification | 4-6 ACs concurrent |
| Stories per session | Unlimited (sequential) |

### 6.4 Availability

| Requirement | Implementation |
|-------------|----------------|
| Integration with /dev | Always available (part of workflow) |
| Optional bypass | Not supported (verification is mandatory) |
| Retry capability | User can re-run /dev after fixes |

---

## 7. Complexity Assessment

**Total Score:** 25/60
**Architecture Tier:** Tier 2 - Moderate Application

### 7.1 Score Breakdown

| Dimension | Score | Breakdown |
|-----------|-------|-----------|
| Functional Complexity | 20/20 | 3 roles, 3 entities, 0 integrations, branching workflow |
| Technical Complexity | 13/20 | Low data volume, low concurrency, no real-time |
| Team/Org Complexity | 5/10 | 1 developer, co-located |
| Non-Functional Complexity | 3/10 | Moderate performance, no compliance |

### 7.2 Tier Recommendation

**Tier 2: Moderate Application**
- Single subagent within existing framework
- Modular design with clear interfaces
- Standard file-based integration

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Subagent creation | Follows existing patterns (.claude/agents/) |
| Tool availability | Read, Grep, Glob available |
| Integration points | Task() invocation proven pattern |
| XML parsing | Claude handles XML well (Anthropic confirmed) |

### 8.2 Business Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Budget | Token overhead acceptable per user |
| Timeline | 2 sprints (10-17 days) achievable |
| ROI | Eliminates manual workaround, 100% AC compliance |

### 8.3 Resource Feasibility: ✅ FEASIBLE

| Factor | Assessment |
|--------|------------|
| Team capacity | Single developer sufficient |
| Skill requirements | Standard subagent development |
| Dependencies | None (can start immediately) |

### 8.4 Overall: ✅ PROCEED WITH IMPLEMENTATION

---

## 9. Risk Register

| Risk ID | Risk | Category | Probability | Impact | Severity | Mitigation |
|---------|------|----------|-------------|--------|----------|------------|
| R1 | Token overhead increases cost | Technical | 80% | LOW | LOW | User accepts tradeoff |
| R2 | XML format migration effort | Technical | 60% | MEDIUM | MEDIUM | Gradual migration, document guide |
| R3 | Phase 4.5 slows /dev workflow | Technical | 70% | LOW | LOW | Quality prioritized per user |
| R4 | Fresh context misses details | Technical | 20% | MEDIUM | LOW | Pass story file as context |
| R5 | Breaking existing /dev workflow | Technical | 30% | HIGH | MEDIUM | Feature flag initially |
| R6 | Testing verification accuracy | Technical | 50% | MEDIUM | MEDIUM | Retrospective test on STORY-250-268 |

---

## 10. Constraints & Assumptions

### 10.1 Technical Constraints

| Constraint | Source |
|------------|--------|
| Subagent must be Markdown file | source-tree.md (LOCKED) |
| Tools limited to Read, Grep, Glob | tech-stack.md (principle of least privilege) |
| No external dependencies | dependencies.md (LOCKED) |
| Single responsibility principle | architecture-constraints.md (LOCKED) |

### 10.2 Business Constraints

| Constraint | Impact |
|------------|--------|
| Token budget acceptable | User prioritizes quality over cost |
| Backward compatibility | XML format required (no graceful degradation) |
| Framework-only implementation | All solutions use Claude Code Terminal |

### 10.3 Assumptions (Require Validation)

| ID | Assumption | Validation Approach |
|----|------------|---------------------|
| A1 | XML AC format improves parsing accuracy | Test on 5 stories |
| A2 | Fresh context catches issues same-context misses | Compare verification results |
| A3 | 60-120 second verification time is acceptable | User feedback |
| A4 | Parallel AC verification is safe (no cross-AC dependencies) | Code review |

---

## 11. Implementation Roadmap

### Sprint 1 (Week 1-2)

| Story | Feature | Points | Dependencies |
|-------|---------|--------|--------------|
| Subagent file creation | F1 | 2 | None |
| XML AC parsing | F1 | 3 | Subagent file |
| Source code inspection | F1 | 3 | XML parsing |
| XML schema design | F3 | 2 | None (parallel) |
| Story template update | F3 | 3 | XML schema |
| Migration guide | F3 | 3 | Template update |

### Sprint 2 (Week 3-4)

| Story | Feature | Points | Dependencies |
|-------|---------|--------|--------------|
| Coverage verification | F1 | 2 | Source inspection |
| Anti-pattern detection | F1 | 2 | Source inspection |
| JSON report generation | F1 | 3 | All F1 stories |
| Phase 4.5 insertion | F2 | 2 | Subagent complete |
| Phase 5.5 insertion | F2 | 2 | Phase 4.5 |
| HALT behavior | F2 | 2 | Phase insertions |
| Phase documentation | F2 | 2 | Phase insertions |
| TechSpec schema update | F4 | 2 | None |
| Story creation automation | F4 | 2 | Schema update |
| Traceability validation | F4 | 1 | Automation |

---

## 12. Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| AC | Acceptance Criteria - testable condition that must be met |
| COMP | Component requirement in Technical Specification |
| Fresh context | New Claude session without prior implementation knowledge |
| Phase 4.5 | Verification checkpoint after TDD refactor |
| Phase 5.5 | Verification checkpoint after integration tests |
| TDD | Test-Driven Development (Red → Green → Refactor) |

### Appendix B: References

| Document | Location |
|----------|----------|
| BRAINSTORM-005 | devforgeai/specs/brainstorms/BRAINSTORM-005-spec-compliance-100-percent.brainstorm.md |
| RESEARCH-002 | devforgeai/specs/research/RESEARCH-002-spec-driven-framework-reliability.research.md |
| source-tree.md | devforgeai/specs/context/source-tree.md |
| tech-stack.md | devforgeai/specs/context/tech-stack.md |
| architecture-constraints.md | devforgeai/specs/context/architecture-constraints.md |

### Appendix C: Open Questions

| ID | Question | Status |
|----|----------|--------|
| Q1 | Should Phase 5.5 be optional or mandatory? | Answered: Mandatory |
| Q2 | Should legacy stories without XML work? | Answered: No, require XML |
| Q3 | Parallel or sequential AC verification? | Answered: Parallel for ≥5 ACs |

---

## Change Log

| Date | Version | Change |
|------|---------|--------|
| 2026-01-19 | 1.0 | Initial requirements specification created from /ideate |
