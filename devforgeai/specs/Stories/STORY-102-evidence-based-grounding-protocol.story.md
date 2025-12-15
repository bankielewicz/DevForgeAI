---
id: STORY-102
title: Evidence-Based Grounding Protocol
epic: EPIC-016
sprint: Sprint-6
status: Backlog
points: 5
priority: Medium
assigned_to: Unassigned
created: 2025-12-01
format_version: "2.1"
depends_on:
  - STORY-101
---

# Story: Evidence-Based Grounding Protocol

## Description

**As a** DevForgeAI user,
**I want** Claude to follow a Read-Quote-Cite workflow before making framework recommendations,
**so that** all recommendations are grounded in actual documentation, reducing hallucinations and enabling me to verify accuracy through traced sources.

## Acceptance Criteria

### AC#1: Grounding Protocol Documentation in CLAUDE.md

**Given** STORY-101 citation format standards have been implemented (Critical Rule #12 exists)
**When** STORY-102 implementation is complete
**Then** Critical Rule #12 is extended with a "Grounding Protocol" subsection containing:
- Step 1: **Read** - "Use Read tool to access source file before making recommendation"
- Step 2: **Quote** - "Extract word-for-word relevant passage from file"
- Step 3: **Cite** - "Reference source using citation format from this rule"
- A verification step: "Confirm recommendation matches quoted content"

---

### AC#2: Technology Decision Grounding Example

**Given** the grounding protocol is documented in Critical Rule #12
**When** the examples section is reviewed
**Then** a complete technology decision example exists demonstrating:
- Read tool invocation for tech-stack.md
- Exact quoted passage (minimum 2 lines, word-for-word)
- Citation using framework file format: `(Source: .devforgeai/context/tech-stack.md, lines X-Y)`
- Final recommendation that directly references the quoted content
- Total example length between 15-25 lines

---

### AC#3: Architecture Decision Grounding Example

**Given** the grounding protocol is documented in Critical Rule #12
**When** the examples section is reviewed
**Then** a complete architecture decision example exists demonstrating:
- Read tool invocation for architecture-constraints.md
- Exact quoted passage (minimum 2 lines, word-for-word)
- Citation using framework file format: `(Source: .devforgeai/context/architecture-constraints.md, lines X-Y)`
- Final recommendation that directly references the quoted content
- Total example length between 15-25 lines

---

### AC#4: Verification Step Documentation

**Given** the grounding protocol is documented
**When** the verification section is reviewed
**Then** a verification checklist exists with:
- Checkbox: "Read tool was used to access source file"
- Checkbox: "Quoted text is word-for-word from source"
- Checkbox: "Citation format matches STORY-101 standards"
- Checkbox: "Recommendation directly relates to quoted content"

---

### AC#5: Backward Compatibility Verification

**Given** CLAUDE.md has been updated with the grounding protocol
**When** backward compatibility testing is performed
**Then** all tests pass:
- 9 skills load without error (Skill tool returns success message)
- 11 commands parse without error (command files validated)
- Critical Rule #12 total length remains 40-100 lines (including STORY-101 content + STORY-102 additions)
- No existing functionality references broken

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "GroundingProtocol"
      file_path: "CLAUDE.md"
      dependencies:
        - "STORY-101 (Citation Format Standards)"
      requirements:
        - id: "DOC-001"
          description: "Add Grounding Protocol subsection to Critical Rule #12"
          testable: true
          test_requirement: "Test: grep 'Grounding Protocol' CLAUDE.md returns match"
          priority: "Critical"
        - id: "DOC-002"
          description: "Document 4-step workflow (Read, Quote, Cite, Verify)"
          testable: true
          test_requirement: "Test: All 4 steps documented with clear descriptions"
          priority: "Critical"
        - id: "DOC-003"
          description: "Technology decision example with complete workflow"
          testable: true
          test_requirement: "Test: Example includes Read invocation, quote, citation, recommendation"
          priority: "High"
        - id: "DOC-004"
          description: "Architecture decision example with complete workflow"
          testable: true
          test_requirement: "Test: Example includes Read invocation, quote, citation, recommendation"
          priority: "High"
        - id: "DOC-005"
          description: "Verification checklist with 4 checkboxes"
          testable: true
          test_requirement: "Test: grep -c '[ ]' in verification section returns 4"
          priority: "High"
        - id: "DOC-006"
          description: "Backward compatibility with 9 skills + 11 commands"
          testable: true
          test_requirement: "Test: All skills and commands load/parse without error"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Read tool MUST be invoked before making technology or architecture recommendations"
      test_requirement: "Test: Recommendations without Read tool invocation flagged"
    - id: "BR-002"
      rule: "Quoted passages MUST be word-for-word from source (minimum 2 lines)"
      test_requirement: "Test: Paraphrased quotes flagged as violations"
    - id: "BR-003"
      rule: "Citations MUST use STORY-101 format standards"
      test_requirement: "Test: Non-compliant citation formats rejected"
    - id: "BR-004"
      rule: "Recommendations MUST directly relate to quoted content"
      test_requirement: "Test: Unrelated recommendations flagged"
    - id: "BR-005"
      rule: "If Read tool fails, HALT recommendation (do not proceed without evidence)"
      test_requirement: "Test: Missing source file prevents recommendation"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Read tool invocation time"
      metric: "< 500ms per file access"
      test_requirement: "Test: Time Read tool invocation, assert < 500ms"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Total grounding workflow overhead"
      metric: "< 2 seconds (Read + Quote + Cite)"
      test_requirement: "Test: Complete workflow time < 2000ms"
    - id: "NFR-003"
      category: "Security"
      requirement: "Sensitive file exclusion"
      metric: "Zero quotes from .env, secret, credential, password files"
      test_requirement: "Test: Blocklist pattern prevents sensitive file quotes"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Source file not found handling"
      metric: "100% of missing file cases produce HALT with error message"
      test_requirement: "Test: Missing file produces clear error, no recommendation"
    - id: "NFR-005"
      category: "Scalability"
      requirement: "Consistent workflow across skills and commands"
      metric: "Same 4-step workflow for all 9 skills and 11 commands"
      test_requirement: "Test: No skill-specific or command-specific variations"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Workflow Overhead:**
- Read tool invocation: < 500ms per file access (standard tool performance)
- Grounding workflow overhead: < 2 seconds total (Read + Quote extraction + Cite formatting)
- No additional network calls required (all sources are local files)

---

### Security

**Data Protection:**
- No sensitive file content quoted (exclude files matching `.env*`, `*secret*`, `*credential*`, `*password*`)
- Quote extraction uses Read tool only (no Bash file access that could bypass permissions)
- Citation format prevents path traversal (validate paths start with `.devforgeai/`, `.claude/`, or `src/`)

---

### Reliability

**Error Handling:**
- Graceful degradation: If Read tool fails, document failure and halt recommendation (do not guess)
- Idempotent workflow: Re-running grounding on same recommendation produces identical citations
- Error recovery: Clear error messages when source files missing or unreadable

---

### Scalability

**Consistency:**
- Workflow applies consistently across all 9 skills (no skill-specific variations)
- Workflow applies consistently across all 11 commands (no command-specific variations)
- Documentation length scales linearly: 2 examples = ~50 lines; future examples add ~20 lines each

---

### Maintainability

**Documentation:**
- Examples use existing context files (tech-stack.md, architecture-constraints.md)
- Grounding protocol references STORY-101 citation formats (single source of truth)
- Verification checklist reusable across all recommendation types

---

## Edge Cases

1. **Source File Not Found:** When the Read tool cannot find the referenced file (deleted, moved, renamed), the grounding workflow should document the failure and halt the recommendation rather than proceeding without evidence. Expected behavior: "HALT: Cannot provide recommendation - source file not found."

2. **Quoted Content Outdated:** When quoted content no longer matches the current file state (file was updated after quote captured), the workflow should re-read the file and update the quote with current line numbers.

3. **Multiple Relevant Sources:** When a recommendation requires evidence from multiple files (e.g., both tech-stack.md AND architecture-constraints.md), the workflow should chain Read-Quote-Cite for each source.

4. **Large File Partial Read:** When source file exceeds 10,000 characters and only a specific section is relevant, the workflow should quote only the relevant passage (minimum 2 lines, maximum 20 lines).

5. **Line Number Drift:** When file modifications cause line numbers in existing citations to become inaccurate, the workflow should identify by content match rather than line number alone, then update the citation.

---

## Data Validation Rules

1. **Grounding Protocol Section:** Must contain exactly 4 steps (Read, Quote, Cite, Verify) with clear action descriptions.

2. **Example Length:** Each example must be 15-25 lines (sufficient detail without excessive verbosity).

3. **Quote Minimum:** Quoted passages must be minimum 2 lines to provide adequate context.

4. **Citation Format Compliance:** All citations must match STORY-101 format patterns.

5. **Critical Rule #12 Total Length:** 40-100 lines after STORY-102 additions (balances completeness with readability).

6. **Verification Checklist:** Must contain exactly 4 checkboxes (Read, Quote, Cite format, Recommendation alignment).

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-101:** Citation Format Standards
  - **Why:** Grounding protocol references citation format standards
  - **Status:** Backlog

### External Dependencies

None

### Technology Dependencies

None - Updates existing CLAUDE.md documentation only.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Happy Path:** Complete Read-Quote-Cite workflow executed correctly
2. **Edge Cases:**
   - Source file not found
   - Multiple sources required
   - Large file partial read
3. **Error Cases:**
   - Quote extraction fails
   - Citation format invalid

---

### Integration Tests

**Coverage Target:** 80%+

**Test Scenarios:**
1. **CLAUDE.md integration:** Critical Rule #12 properly formatted after additions
2. **Backward compatibility:** All 9 skills + 11 commands work after update
3. **Workflow verification:** Technology and architecture examples execute correctly

---

## Acceptance Criteria Verification Checklist

### AC#1: Grounding Protocol Documentation in CLAUDE.md

- [ ] Grounding Protocol subsection exists - **Phase:** 2 - **Evidence:** grep test
- [ ] Step 1 (Read) documented - **Phase:** 2 - **Evidence:** CLAUDE.md content
- [ ] Step 2 (Quote) documented - **Phase:** 2 - **Evidence:** CLAUDE.md content
- [ ] Step 3 (Cite) documented - **Phase:** 2 - **Evidence:** CLAUDE.md content
- [ ] Verification step documented - **Phase:** 2 - **Evidence:** CLAUDE.md content

### AC#2: Technology Decision Grounding Example

- [ ] Read tool invocation shown - **Phase:** 2 - **Evidence:** example content
- [ ] Quoted passage (>=2 lines) - **Phase:** 2 - **Evidence:** example content
- [ ] Citation format correct - **Phase:** 2 - **Evidence:** example content
- [ ] Recommendation references quote - **Phase:** 2 - **Evidence:** example content
- [ ] Example length 15-25 lines - **Phase:** 4 - **Evidence:** wc -l output

### AC#3: Architecture Decision Grounding Example

- [ ] Read tool invocation shown - **Phase:** 2 - **Evidence:** example content
- [ ] Quoted passage (>=2 lines) - **Phase:** 2 - **Evidence:** example content
- [ ] Citation format correct - **Phase:** 2 - **Evidence:** example content
- [ ] Recommendation references quote - **Phase:** 2 - **Evidence:** example content
- [ ] Example length 15-25 lines - **Phase:** 4 - **Evidence:** wc -l output

### AC#4: Verification Step Documentation

- [ ] Checkbox 1: Read tool used - **Phase:** 2 - **Evidence:** grep test
- [ ] Checkbox 2: Quote word-for-word - **Phase:** 2 - **Evidence:** grep test
- [ ] Checkbox 3: Citation format correct - **Phase:** 2 - **Evidence:** grep test
- [ ] Checkbox 4: Recommendation relates to quote - **Phase:** 2 - **Evidence:** grep test

### AC#5: Backward Compatibility Verification

- [ ] All 9 skills load without error - **Phase:** 4 - **Evidence:** skill invocation tests
- [ ] All 11 commands parse without error - **Phase:** 4 - **Evidence:** command validation
- [ ] Critical Rule #12 length 40-100 lines - **Phase:** 4 - **Evidence:** wc -l output

---

**Checklist Progress:** 0/23 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Grounding Protocol subsection added to Critical Rule #12
- [ ] 4-step workflow documented (Read, Quote, Cite, Verify)
- [ ] Technology decision example (15-25 lines)
- [ ] Architecture decision example (15-25 lines)
- [ ] Verification checklist with 4 checkboxes

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases documented (file not found, outdated content, multiple sources)
- [ ] Data validation rules documented
- [ ] NFRs met (< 2s workflow, zero sensitive files)

### Testing
- [ ] Backward compatibility tests (9 skills + 11 commands)
- [ ] Example validation tests
- [ ] Workflow execution tests

### Documentation
- [ ] Grounding protocol in CLAUDE.md Critical Rule #12
- [ ] Technology decision example
- [ ] Architecture decision example
- [ ] Verification checklist

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Read-Quote-Cite workflow based on Claude Docs "Reduce hallucinations" guidance
- Verification step ensures recommendation matches evidence
- Examples use existing context files to avoid creating new dependencies

**Research Reference:**
- RESEARCH-001: Claude Code Memory Management Best Practices (2025-11-30)
- "For tasks involving long documents (>20K tokens), ask Claude to extract word-for-word quotes first before performing its task. This grounds its responses in the actual text, reducing hallucinations." (Source: Claude Docs)

**Related Stories:**
- STORY-099: Baseline Metrics Collection (captures baseline before grounding)
- STORY-100: Accuracy Tracking Log Setup (tracks ongoing accuracy)
- STORY-101: Citation Format Standards (defines formats used in grounding)

**Expected Outcome:**
- 2x reduction in hallucination rate (per RESEARCH-001 findings)
- ≥90% citation compliance for framework recommendations
- All recommendations traceable to source documentation

---

**Story Template Version:** 2.1
**Last Updated:** 2025-12-01
