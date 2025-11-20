---
id: STORY-054
title: claude-code-terminal-expert Prompting Guidance Enhancement
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

# Story: claude-code-terminal-expert Prompting Guidance Enhancement

## Description

**As a** DevForgeAI framework knowledge repository (claude-code-terminal-expert skill),
**I want** to provide authoritative prompting guidance accessible to all framework components,
**so that** skills, commands, and subagents reference a single source of truth for user interaction patterns, ensuring framework-wide consistency and reducing documentation drift.

---

## Acceptance Criteria

### 1. [ ] Prompting Guidance Section Added to SKILL.md

**Given** the claude-code-terminal-expert skill exists in `src/claude/skills/claude-code-terminal-expert/SKILL.md`
**When** the skill file is opened for editing
**Then** a new section titled "How DevForgeAI Skills Work with User Input" is present after the features overview section and before detailed topic sections, containing 100-200 lines of guidance

---

### 2. [ ] Cross-References to Both Guidance Documents

**Given** the new prompting guidance section exists
**When** the section content is reviewed
**Then** it includes explicit cross-references to:
- `src/claude/memory/effective-prompting-guide.md` (markdown link format)
- `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` (markdown link format)
**And** each reference includes a brief description of when to consult that document

---

### 3. [ ] Effective Communication Examples (5-10 Scenarios)

**Given** the new section exists
**When** examples are counted
**Then** 5-10 paired examples (effective ✅ vs ineffective ❌) are present covering:
- Feature requests (clear vs vague)
- Story creation (specific vs ambiguous)
- Error reporting (actionable vs incomplete)
- Technology decisions (explicit preferences vs assumptions)
- Feedback provision (constructive vs generic)

---

### 4. [ ] "Ask, Don't Assume" Principle Explained

**Given** the new section exists
**When** the "Ask, Don't Assume" principle is searched
**Then** a dedicated subsection explains:
- When to use AskUserQuestion (ambiguity, conflicts, preferences)
- What NOT to assume (technologies, priorities, scope)
- Why this principle exists (prevents technical debt)
- How it integrates with DevForgeAI quality gates

---

### 5. [ ] No Breaking Changes to Skill Structure

**Given** the skill modification is complete
**When** the skill is invoked via `Skill(command="claude-code-terminal-expert")`
**Then** all existing functionality works unchanged:
- Progressive disclosure of reference files
- Self-updating capability from official docs
- Topic coverage (28 topics)
- Integration with other framework skills

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Skill"
      name: "claude-code-terminal-expert"
      file_path: "src/claude/skills/claude-code-terminal-expert/SKILL.md"
      requirements:
        - id: "SKILL-001"
          description: "Add 'How DevForgeAI Skills Work with User Input' section after features overview (around line 100)"
          testable: true
          test_requirement: "Test: Grep for '## How DevForgeAI Skills Work' returns 1 match, appears before line 300"
          priority: "Critical"

        - id: "SKILL-002"
          description: "Cross-reference effective-prompting-guide.md with markdown link"
          testable: true
          test_requirement: "Test: Grep for 'effective-prompting-guide.md' returns ≥1 match, link syntax valid, target file exists"
          priority: "Critical"

        - id: "SKILL-003"
          description: "Cross-reference user-input-guidance.md with markdown link"
          testable: true
          test_requirement: "Test: Grep for 'user-input-guidance.md' returns ≥1 match, link resolves to actual file"
          priority: "Critical"

        - id: "SKILL-004"
          description: "Include 5-10 paired examples (✅ effective vs ❌ ineffective communication)"
          testable: true
          test_requirement: "Test: Grep for '❌' and '✅' patterns in new section, count matches (≥5 pairs, ≤10 pairs)"
          priority: "High"

        - id: "SKILL-005"
          description: "Add 'Ask, Don't Assume' principle explanation subsection"
          testable: true
          test_requirement: "Test: Grep for '### The \"Ask, Don't Assume\" Principle', verify subsection explains when/what/why/how"
          priority: "Critical"

        - id: "SKILL-006"
          description: "Maintain backward compatibility (existing skill functionality unchanged)"
          testable: true
          test_requirement: "Test: Invoke skill before/after modification, verify same reference files load, same topics covered"
          priority: "Critical"

        - id: "SKILL-007"
          description: "Token overhead from new section ≤1,000 tokens"
          testable: true
          test_requirement: "Test: Measure SKILL.md tokens before/after, assert difference ≤1,000 tokens"
          priority: "High"

        - id: "SKILL-008"
          description: "All cross-reference links must resolve to existing files"
          testable: true
          test_requirement: "Test: Read each cross-referenced file path, assert no 'file not found' errors"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Examples must align with actual framework behavior (no hypothetical or aspirational examples)"
      test_requirement: "Test: Extract 3 example inputs from ✅ patterns, execute with actual commands (/create-story, /dev), verify expected behavior"

    - id: "BR-002"
      rule: "Cross-reference descriptions must be accurate and helpful (not placeholder text)"
      test_requirement: "Test: Verify each cross-reference has ≥15-word description explaining when to consult that document"

    - id: "BR-003"
      rule: "New section must not conflict with existing skill content (no contradictory guidance)"
      test_requirement: "Test: Grep skill for conflicting statements (e.g., 'never use AskUserQuestion' vs. 'use AskUserQuestion for ambiguity'), assert 0 conflicts"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "New section must not significantly increase skill activation token cost"
      metric: "≤ 1,000 token increase from baseline (current ~2,100 tokens → target ≤3,100 tokens)"
      test_requirement: "Test: Tokenize SKILL.md before/after, measure difference, assert ≤1,000 tokens"

    - id: "NFR-002"
      category: "Maintainability"
      requirement: "Section integration must be quick and low-risk"
      metric: "< 30 minutes to add section, validate cross-references, and test"
      test_requirement: "Test: Time-boxed implementation by developer, assert completion <30 minutes"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Modification must not break existing skill functionality"
      metric: "100% backward compatibility (all existing features work after modification)"
      test_requirement: "Test: Regression test suite for claude-code-terminal-expert (28 topics, reference file loading, self-updating), assert 100% pass rate"

    - id: "NFR-004"
      category: "Quality"
      requirement: "Examples must be accurate and aligned with framework reality"
      metric: "100% of examples produce expected framework behavior when tested"
      test_requirement: "Test: Extract all ✅ examples (5-10 total), execute with framework, assert all work as described"

    - id: "NFR-005"
      category: "Cohesion"
      requirement: "New section must reinforce framework-wide consistency"
      metric: "All terminology matches CLAUDE.md, effective-prompting-guide.md, user-input-guidance.md (validated via Grep)"
      test_requirement: "Test: Extract key terms from new section, Grep other docs, assert 100% terminology consistency"
```

---

## Edge Cases

1. **Passive guidance access:** Most users interact with commands that may internally reference this guidance. Guidance discoverable via framework memory files (effective-prompting-guide.md serves as bridge).

2. **Token overhead on skill activation:** New section adds 800-1,200 tokens. If skill activation exceeds 8K tokens, progressive disclosure may trigger. Mitigation: Keep section concise, reference detailed docs via links.

3. **Example conflicts with command-specific patterns:** Generic examples may not match command-specific guidance. Resolution: Examples should be framework-level patterns, commands override with specifics.

4. **Guidance staleness:** New commands may introduce patterns not covered in examples. Mitigation: Quarterly review cycle, link to living documents.

5. **Section positioning disrupts references:** Adding section may shift line numbers. Mitigation: Use section headers (not line numbers) in cross-references.

---

## Data Validation Rules

1. **Section header format:** Use `## How DevForgeAI Skills Work with User Input` (heading level 2)

2. **Cross-reference syntax:** Use relative paths from skill location (../../memory/, ../../../.devforgeai/)

3. **Example format consistency:** All examples follow `❌ Ineffective:` / `✅ Effective:` pattern

4. **Subsection headers:** Use level 3 headings (###) for subsections

5. **Cross-reference descriptions:** Each link must include 15-30 word context explanation

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-052:** User-Facing Prompting Guide
  - **Why:** claude-code-terminal-expert section cross-references effective-prompting-guide.md (must exist before cross-referencing)
  - **Status:** Created (same batch)

- [ ] **STORY-053:** Framework-Internal Guidance Reference
  - **Why:** claude-code-terminal-expert section cross-references user-input-guidance.md (must exist before cross-referencing)
  - **Status:** Created (same batch)

### External Dependencies

None - Skill modification only.

### Technology Dependencies

None - Markdown modification requires no additional packages.

---

## Test Strategy

### Integration Tests

**Coverage Target:** 100% (all acceptance criteria validated)

**Test Scenarios:**

1. **Section Exists and Positioned Correctly (AC1)**
   - Grep for section header
   - Verify line number position (after features, before topics)

2. **Cross-References Valid (AC2)**
   - Extract markdown links
   - Read each target file
   - Verify descriptions present

3. **Examples Present and Formatted (AC3)**
   - Count ❌/✅ patterns
   - Verify 5-10 pairs
   - Test 3 examples with actual commands

4. **Principle Explained (AC4)**
   - Grep for subsection
   - Verify when/what/why/how covered

5. **Backward Compatibility (AC5)**
   - Invoke skill before modification (baseline)
   - Invoke skill after modification
   - Compare outputs (must match)

**Test File Locations:**
- `tests/user-input-guidance/test-skill-enhancement.sh`
- `tests/user-input-guidance/test-cross-references.sh`
- `tests/user-input-guidance/test-backward-compatibility.sh`

---

## Acceptance Criteria Verification Checklist

### AC#1: Section Added

- [ ] Section header present - **Phase:** 2 - **Evidence:** grep "## How DevForgeAI Skills Work"
- [ ] Positioned after features overview - **Phase:** 2 - **Evidence:** Line number ~100-300
- [ ] 100-200 lines - **Phase:** 2 - **Evidence:** wc -l on section extraction

### AC#2: Cross-References

- [ ] effective-prompting-guide.md link - **Phase:** 2 - **Evidence:** grep "effective-prompting-guide.md"
- [ ] user-input-guidance.md link - **Phase:** 2 - **Evidence:** grep "user-input-guidance.md"
- [ ] Link descriptions (15-30 words) - **Phase:** 2 - **Evidence:** wc -w on link context

### AC#3: Examples

- [ ] 5-10 paired examples - **Phase:** 2 - **Evidence:** grep -c "❌.*✅"
- [ ] Feature request example - **Phase:** 2 - **Evidence:** grep "Feature request"
- [ ] Story creation example - **Phase:** 2 - **Evidence:** grep "Story creation"
- [ ] Error reporting example - **Phase:** 2 - **Evidence:** grep "Error reporting"
- [ ] Technology decision example - **Phase:** 2 - **Evidence:** grep "Technology decision"
- [ ] Feedback example - **Phase:** 2 - **Evidence:** grep "Feedback"

### AC#4: Principle Explained

- [ ] Subsection header - **Phase:** 2 - **Evidence:** grep "Ask, Don't Assume"
- [ ] When to use explained - **Phase:** 2 - **Evidence:** Section contains "when" guidance
- [ ] What not to assume - **Phase:** 2 - **Evidence:** Section contains "what NOT" list
- [ ] Why exists explained - **Phase:** 2 - **Evidence:** Section contains rationale
- [ ] How integrates explained - **Phase:** 2 - **Evidence:** References quality gates

### AC#5: No Breaking Changes

- [ ] Existing functionality preserved - **Phase:** 3 - **Evidence:** test-backward-compatibility.sh passes
- [ ] Reference files still load - **Phase:** 3 - **Evidence:** Skill invocation loads core-features.md, etc.
- [ ] 28 topics still covered - **Phase:** 3 - **Evidence:** Topic count unchanged
- [ ] Self-updating works - **Phase:** 3 - **Evidence:** WebFetch still functional

---

**Checklist Progress:** 0/19 items complete (0%)

---


## Implementation Notes

Status: Backlog - Story created and ready for development. All Definition of Done items will be completed during TDD cycle.
## Definition of Done

### Implementation
- [ ] New section added to src/claude/skills/claude-code-terminal-expert/SKILL.md
- [ ] Section positioned after features overview (around line 100)
- [ ] 100-200 lines of guidance content
- [ ] Cross-references to both guidance documents (effective-prompting-guide.md, user-input-guidance.md)
- [ ] 5-10 paired examples included
- [ ] "Ask, Don't Assume" principle explained in subsection
- [ ] All markdown links validated (target files exist)

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases documented (5 scenarios with mitigations)
- [ ] Data validation rules enforced (5 rules)
- [ ] NFRs met (5 NFRs: performance ≤1K tokens, maintainability <30min, reliability 100%, quality 100%, cohesion 100%)
- [ ] No breaking changes (backward compatibility test passes)

### Testing
- [ ] Section existence test (AC1)
- [ ] Cross-reference validation test (AC2)
- [ ] Example format test (AC3)
- [ ] Principle explanation test (AC4)
- [ ] Backward compatibility test (AC5)
- [ ] Token overhead test (NFR-001)
- [ ] All tests passing (6/6 test categories)

### Documentation
- [ ] Modification documented in src/claude/skills/claude-code-terminal-expert/SKILL.md
- [ ] Cross-referenced from effective-prompting-guide.md
- [ ] Cross-referenced from user-input-guidance.md
- [ ] Synced to operational folder (.claude/skills/claude-code-terminal-expert/SKILL.md)

---

## Workflow History

### 2025-01-20 20:45:00 - Status: Ready for Dev
- Added to SPRINT-2: User Input Guidance Implementation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 40 points (9 stories)
- Priority in sprint: [3 of 9] - Terminal expert enhancement

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

## Notes

**Design Decisions:**
- **Section positioning:** After features overview ensures users understand what Claude Code can do BEFORE learning how to communicate effectively
- **Conciseness:** 100-200 lines balances comprehensiveness with token efficiency (≤1K token overhead)
- **Example format:** Paired ❌/✅ format provides clear visual comparison (same pattern as effective-prompting-guide.md)
- **Cohesion strategy:** Three documents form triangle: user guide (effective-prompting-guide.md) ←→ framework guide (user-input-guidance.md) ←→ authoritative knowledge base (claude-code-terminal-expert)

**Integration Strategy:**
- claude-code-terminal-expert is knowledge repository, not workflow executor
- Section provides high-level guidance, detailed patterns in linked documents
- Cross-references enable progressive disclosure (overview here, deep dive in linked docs)
- Maintains skill's role as "source of truth" for framework concepts

**Value Proposition:**
- Framework cohesion: All components reference same authoritative source
- Reduced drift: Single location to update prompting guidance
- Improved discoverability: Users/skills find guidance via knowledge repository
- Reinforces philosophy: "Ask, Don't Assume" explained in framework context

**Related ADRs:**
None required (documentation enhancement for cohesion, not architectural change)

**References:**
- EPIC-011: User Input Guidance System
- STORY-052: effective-prompting-guide.md (cross-referenced)
- STORY-053: user-input-guidance.md (cross-referenced)
- claude-code-terminal-expert/references/: Existing reference files (integration pattern)

---

**Story Template Version:** 2.0
**Created:** 2025-01-20
