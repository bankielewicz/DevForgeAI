---
id: STORY-055
title: devforgeai-ideation Skill Integration with User Input Guidance
epic: EPIC-011
sprint: SPRINT-2
status: Ready for Dev
points: 3
priority: Medium
assigned_to: TBD
created: 2025-01-20
updated: 2025-01-20
format_version: "2.0"
---

# Story: devforgeai-ideation Skill Integration with User Input Guidance

## Description

**As a** DevForgeAI workflow participant,
**I want** the ideation skill to use user-input-guidance.md patterns before asking discovery questions,
**so that** I receive contextual, clear prompts that reduce back-and-forth iterations and ambiguity during requirements gathering.

---

## Acceptance Criteria

### 1. [ ] Pre-Discovery Guidance Loading

**Given** a user invokes the devforgeai-ideation skill (via /ideate command or orchestration)
**When** the skill enters Phase 1 (Requirements Discovery)
**Then** Step 0 loads user-input-guidance.md using Read tool before proceeding to Step 1

---

### 2. [ ] Pattern Application in Discovery Questions

**Given** the guidance is loaded in Phase 1 Step 0
**When** the skill formulates AskUserQuestion prompts in Phase 1 (business goals, constraints) and Phase 2 (feature elicitation)
**Then** all prompts incorporate appropriate patterns:
- Problem Scope questions use "Tell me about..." open-ended pattern
- Feature Priority questions use "Rank 1-5" comparative pattern
- Timeline questions use "Select range: 1-2 weeks, 1-3 months..." bounded pattern
- User Persona questions use "Primary user: [Admin/Developer/End User]" explicit classification pattern

---

### 3. [ ] Subagent Invocation Quality

**Given** Phase 1-2 questions incorporate guidance patterns
**When** the requirements-analyst subagent is invoked in Phase 3 (Epic Decomposition)
**Then** the subagent receives higher quality context (complete problem scope, ranked features, known constraints) reducing need for re-invocation by ≥30%

---

### 4. [ ] Token Overhead Constraint

**Given** Step 0 loads user-input-guidance.md (~2,500 lines)
**When** Phase 1 executes with guidance loaded
**Then** total token overhead for Phase 1 increases by ≤1,000 tokens (measured via token counting in isolated skill context)

---

### 5. [ ] Backward Compatibility

**Given** existing ideation workflow tests (if any)
**When** all tests are re-run after integration
**Then** 100% of tests pass with identical functional outcomes (same epic documents, same requirements specs, same validation results)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Skill"
      name: "devforgeai-ideation"
      file_path: "src/claude/skills/devforgeai-ideation/SKILL.md"
      requirements:
        - id: "SKILL-001"
          description: "Add Phase 1 Step 0: Load user-input-guidance.md before discovery workflow"
          testable: true
          test_requirement: "Test: Read SKILL.md, grep for 'Step 0.*user-input-guidance', verify present in Phase 1"
          priority: "Critical"

        - id: "SKILL-002"
          description: "Apply Open-Ended Discovery pattern to problem scope questions"
          testable: true
          test_requirement: "Test: Grep Phase 1 for 'Tell me about' or open-ended question syntax"
          priority: "High"

        - id: "SKILL-003"
          description: "Apply Comparative Ranking pattern to feature priority questions"
          testable: true
          test_requirement: "Test: Grep Phase 2 for 'Rank 1-5' or priority ordering syntax"
          priority: "High"

        - id: "SKILL-004"
          description: "Apply Bounded Choice pattern to timeline questions"
          testable: true
          test_requirement: "Test: Grep for 'Select range' or bounded timeline options"
          priority: "Medium"

        - id: "SKILL-005"
          description: "Apply Explicit Classification to user persona questions"
          testable: true
          test_requirement: "Test: Grep for 'Primary user' classification with defined roles"
          priority: "Medium"

    - type: "Documentation"
      name: "user-input-integration-guide"
      file_path: "src/claude/skills/devforgeai-ideation/references/user-input-integration-guide.md"
      requirements:
        - id: "DOC-001"
          description: "Document Step 0 implementation details (load mechanism, error handling)"
          testable: true
          test_requirement: "Test: Read reference file, verify 'Step 0 Implementation' section exists with code examples"
          priority: "High"

        - id: "DOC-002"
          description: "Map patterns to Phase 1-2 questions (which pattern for which question)"
          testable: true
          test_requirement: "Test: Read reference file, verify pattern mapping table exists with 5+ entries"
          priority: "High"

        - id: "DOC-003"
          description: "Document edge case handling (guidance unavailable, version mismatch)"
          testable: true
          test_requirement: "Test: Read reference file, verify 'Edge Case Handling' section with graceful degradation"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Guidance loading must not halt skill execution if file unavailable (graceful degradation)"
      test_requirement: "Test: Delete guidance file temporarily, invoke skill, verify completes successfully with standard prompts"

    - id: "BR-002"
      rule: "Pattern application must preserve existing question intent (enhancement, not replacement)"
      test_requirement: "Test: Compare Phase 1-2 questions before/after, verify same information collected, different phrasing"

    - id: "BR-003"
      rule: "Subagent receives structured context (not raw pattern names)"
      test_requirement: "Test: Inspect requirements-analyst invocation prompt, verify contains collected metadata (not 'used Open-Ended pattern')"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Step 0 guidance loading must be fast"
      metric: "< 500ms to execute Read(file_path='user-input-guidance.md')"
      test_requirement: "Test: Measure Read tool response time, assert <500ms"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Subagent re-invocation frequency must decrease"
      metric: "≥ 30% reduction in requirements-analyst re-calls (baseline 2.5 → target ≤1.75 per ideation)"
      test_requirement: "Test: Execute /ideate on 10 test business ideas, measure re-invocation count before/after, assert ≥30% reduction"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Guidance unavailability must not fail workflow"
      metric: "100% workflow completion rate even if guidance file missing"
      test_requirement: "Test: Delete guidance file, run /ideate, assert epic documents still created (graceful degradation)"

    - id: "NFR-004"
      category: "Maintainability"
      requirement: "Integration changes must be minimal and isolated"
      metric: "≤ 5 lines changed in SKILL.md (add Step 0 reference), ≤300 lines in new reference file"
      test_requirement: "Test: Git diff SKILL.md shows ≤5 line changes, wc -l on reference file ≤300"

    - id: "NFR-005"
      category: "Testability"
      requirement: "Pattern application must be verifiable via automated tests"
      metric: "≥ 80% pattern usage detectable via Grep (prompts contain pattern keywords)"
      test_requirement: "Test: Grep skill execution logs for pattern keywords (Open-Ended, Bounded, Classification), assert ≥4/5 patterns found"
```

---

## Edge Cases

1. **Guidance file missing or corrupted:** If Read fails, log warning "User input guidance unavailable, proceeding with standard prompts" and continue workflow without halting (graceful degradation).

2. **Guidance file outdated (version mismatch):** Ignore unknown patterns, use recognized patterns only, log "Skipping unrecognized pattern category: [name]".

3. **Ambiguous pattern selection for context:** Prefer bounded pattern (more structure). Document selection logic in Phase 1 reference file.

4. **User provides incomplete answers despite guidance:** Invoke pattern-specific follow-up with escalating specificity.

---

## Data Validation Rules

1. **Guidance file location:** Must exist at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`

2. **Pattern application mapping:**
   - Phase 1 business goals → Open-Ended Discovery
   - Phase 1 constraints → Closed Confirmation
   - Phase 2 feature priorities → Comparative Ranking
   - Phase 2 timelines → Bounded Choice
   - Phase 2 user personas → Explicit Classification

3. **Token measurement:** Approximate 1 token ≈ 4 characters. Max overhead: ≤1,000 tokens impact after optimization.

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-053:** Framework-Internal Guidance Reference
  - **Why:** devforgeai-ideation loads user-input-guidance.md (must exist)
  - **Status:** Created (same batch)

### External Dependencies

None

### Technology Dependencies

None - Markdown modification only

---

## Test Strategy

### Integration Tests

**Test Scenarios:**

1. **Step 0 Loads Guidance (AC1)**
   - Verify Read tool invoked with correct path
   - Verify no errors

2. **Patterns Applied (AC2)**
   - Grep Phase 1-2 for pattern keywords
   - Verify 4/5 patterns detected

3. **Subagent Re-Invocation Reduction (AC3)**
   - Run 10 test ideations before/after
   - Measure re-invocation count
   - Assert ≥30% reduction

4. **Token Overhead (AC4)**
   - Tokenize skill execution
   - Measure increase
   - Assert ≤1,000 tokens

5. **Backward Compatibility (AC5)**
   - Run existing tests
   - Compare outputs
   - Assert identical results

---

## Acceptance Criteria Verification Checklist

### AC#1: Pre-Discovery Guidance Loading

- [ ] Step 0 added to Phase 1 - **Phase:** 2 - **Evidence:** grep "Step 0.*Load.*guidance"
- [ ] Read tool invoked - **Phase:** 2 - **Evidence:** Read(file_path="user-input-guidance.md")
- [ ] Positioned before Step 1 - **Phase:** 2 - **Evidence:** Step 0 appears before "Generate Story ID"

### AC#2: Pattern Application

- [ ] Open-Ended pattern used - **Phase:** 2 - **Evidence:** grep "Tell me about"
- [ ] Comparative Ranking used - **Phase:** 2 - **Evidence:** grep "Rank 1-5"
- [ ] Bounded Choice used - **Phase:** 2 - **Evidence:** grep "Select range"
- [ ] Explicit Classification used - **Phase:** 2 - **Evidence:** grep "Primary user"

### AC#3: Subagent Quality

- [ ] ≥30% re-invocation reduction - **Phase:** 4 - **Evidence:** test-subagent-invocations.py

### AC#4: Token Overhead

- [ ] ≤1,000 tokens - **Phase:** 3 - **Evidence:** test-token-overhead.py

### AC#5: Backward Compatibility

- [ ] All tests pass - **Phase:** 3 - **Evidence:** test-backward-compatibility.sh

---

**Checklist Progress:** 0/12 items complete (0%)

---


## Implementation Notes

Status: Backlog - Story created and ready for development. All Definition of Done items will be completed during TDD cycle.
## Definition of Done

### Implementation
- [ ] Step 0 added to src/claude/skills/devforgeai-ideation/SKILL.md Phase 1
- [ ] Reference file created: src/claude/skills/devforgeai-ideation/references/user-input-integration-guide.md
- [ ] Pattern mapping documented
- [ ] Edge case handling implemented

### Quality
- [ ] All 5 acceptance criteria pass
- [ ] Edge cases handled (4 scenarios)
- [ ] Data validation rules enforced (3 rules)
- [ ] NFRs met (5 NFRs all validated)

### Testing
- [ ] Guidance loading test
- [ ] Pattern application test
- [ ] Subagent re-invocation test
- [ ] Token overhead test
- [ ] Backward compatibility test
- [ ] All tests passing (5/5)

### Documentation
- [ ] Integration guide reference created
- [ ] Synced to operational folder

---

## Workflow History

### 2025-01-20 20:45:00 - Status: Ready for Dev
- Added to SPRINT-2: User Input Guidance Implementation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 40 points (9 stories)
- Priority in sprint: [4 of 9] - Ideation skill integration

---

**Story Template Version:** 2.0
**Created:** 2025-01-20
