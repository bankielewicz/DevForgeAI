---
id: STORY-053
title: Framework-Internal Guidance Reference
epic: EPIC-011
sprint: SPRINT-2
status: Ready for Dev
points: 8
priority: Medium
assigned_to: TBD
created: 2025-01-20
updated: 2025-01-20
format_version: "2.0"
---

# Story: Framework-Internal Guidance Reference

## Description

**As a** DevForgeAI skill executing requirements discovery workflows,
**I want** to access proven patterns for eliciting complete requirements from users,
**so that** I can reduce subagent re-invocations, minimize ambiguity, and improve requirement quality on the first pass.

---

## Acceptance Criteria

### 1. [ ] Pattern Completeness

**Given** a skill needs to elicit requirements for a feature
**When** the skill loads user-input-guidance.md
**Then** the guidance contains 10-15 distinct elicitation patterns covering:
- Functional requirement clarification (3-4 patterns)
- Non-functional requirement quantification (2-3 patterns)
- Edge case identification (2-3 patterns)
- Integration point discovery (2-3 patterns)
- Constraint clarification (1-2 patterns)

---

### 2. [ ] Template Usability

**Given** a skill needs to ask the user a clarifying question
**When** the skill selects an AskUserQuestion template from the guidance
**Then** the template includes:
- Pre-written question text (ready to use)
- Header text (contextual framing)
- 3-5 options with labels and descriptions
- Customization guidance (when to adjust options)
**And** 20-30 templates cover common scenarios (functional specs, NFRs, edge cases, integrations, constraints)

---

### 3. [ ] NFR Quantification Accuracy

**Given** a user provides vague non-functional requirements (e.g., "fast", "secure", "scalable")
**When** the skill consults the NFR quantification table
**Then** the table provides:
- Vague term (input)
- Measurable target range (output)
- Real-world example from DevForgeAI context
- AskUserQuestion template to elicit specific target
**And** the table covers ≥15 common vague terms (performance, security, reliability, scalability, usability categories)

---

### 4. [ ] Skill Integration Success

**Given** 5 skills need requirements elicitation (ideation, story-creation, architecture, ui-generator, orchestration)
**When** each skill loads user-input-guidance.md during execution
**Then** each skill:
- Successfully reads the guidance file (no parse errors)
- Finds relevant patterns via Grep in <30 seconds
- Successfully invokes AskUserQuestion using templates
- Reduces subagent re-invocations by ≥30% (measured over 10 story executions)
**And** all 5 skills report improved requirement quality (user feedback: fewer clarification loops)

---

### 5. [ ] Framework Alignment

**Given** user-input-guidance.md references DevForgeAI concepts
**When** skills use the guidance to elicit requirements
**Then** all terminology matches CLAUDE.md, skills-reference.md, and context files:
- Context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
- Quality gates (Gate 1-4)
- Workflow states (Backlog, Architecture, Ready for Dev, etc.)
- Story structure (YAML frontmatter, Given/When/Then AC, tech specs, UI specs)
**And** guidance cites specific DevForgeAI reference files (Read tool paths provided)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "UserInputGuidance"
      file_path: "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
      requirements:
        - id: "DOC-001"
          description: "Create 10-15 elicitation patterns with problem description, solution, AskUserQuestion template, and example"
          testable: true
          test_requirement: "Test: Grep for '### Pattern' headings, count matches (≥10, ≤15), verify each has Problem/Solution/Template/Example sections"
          priority: "Critical"

        - id: "DOC-002"
          description: "Create 20-30 AskUserQuestion templates covering functional specs, NFRs, edge cases, integrations, constraints"
          testable: true
          test_requirement: "Test: Grep for 'AskUserQuestion(' code blocks, count matches (≥20, ≤30), validate each has question/header/options"
          priority: "Critical"

        - id: "DOC-003"
          description: "Create NFR quantification table mapping ≥15 vague terms to measurable targets"
          testable: true
          test_requirement: "Test: Read quantification table section, parse rows, count vague terms (≥15), verify each has measurable range and example"
          priority: "Critical"

        - id: "DOC-004"
          description: "Document integration points for 5 skills (ideation, story-creation, architecture, ui-generator, orchestration)"
          testable: true
          test_requirement: "Test: Grep for skill names, verify 5 integration sections exist, each specifies workflow phase and Read command"
          priority: "High"

        - id: "DOC-005"
          description: "Ensure framework terminology consistency with CLAUDE.md and reference files"
          testable: true
          test_requirement: "Test: Extract all DevForgeAI terms from guidance, Grep CLAUDE.md for each, verify 100% match (no undefined terms)"
          priority: "High"

        - id: "DOC-006"
          description: "Add cross-references to effective-prompting-guide.md and claude-code-terminal-expert"
          testable: true
          test_requirement: "Test: Grep for 'effective-prompting-guide.md' and 'claude-code-terminal-expert', verify 2+ cross-references"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "All patterns must include AskUserQuestion template (not just conceptual guidance)"
      test_requirement: "Test: For each pattern (10-15 total), verify presence of AskUserQuestion code block with valid syntax"

    - id: "BR-002"
      rule: "All AskUserQuestion templates must have 3-5 options (not <3, not >5 due to framework limit)"
      test_requirement: "Test: Parse all AskUserQuestion blocks, count options per template, assert all in range [3,5]"

    - id: "BR-003"
      rule: "NFR quantification table must provide measurable targets (with numbers, percentiles, thresholds)"
      test_requirement: "Test: Parse table, Grep each 'measurable range' cell for numeric values or percentiles (p95, p99), assert all have numbers"

    - id: "BR-004"
      rule: "Patterns must cite DevForgeAI framework reference files (not external sources)"
      test_requirement: "Test: Extract all file path references in patterns, verify all start with '.claude/' or '.devforgeai/', no external URLs"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Guidance file must load quickly when skills invoke Read tool"
      metric: "< 500ms to load 2,500-line markdown file"
      test_requirement: "Test: Measure Read(file_path='user-input-guidance.md') response time, assert <500ms"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Skills must find relevant patterns quickly using Grep"
      metric: "< 30 seconds to search and extract pattern via Grep tool"
      test_requirement: "Test: Execute Grep(pattern='Pattern.*Functional', path='user-input-guidance.md', -C=10), measure time, assert <30s"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Token overhead from loading guidance must be minimal"
      metric: "≤ 3,000 tokens consumed when skill loads guidance"
      test_requirement: "Test: Count tokens in user-input-guidance.md file, assert ≤3,000 tokens (~2,500 lines × 1.2 tokens/line average)"

    - id: "NFR-004"
      category: "Usability"
      requirement: "Skills must successfully use templates without customization in majority of cases"
      metric: "≥ 90% of AskUserQuestion invocations use templates verbatim (no modifications)"
      test_requirement: "Test: Monitor 50 skill executions, count template usage vs custom AskUserQuestion, assert ≥45/50 use templates"

    - id: "NFR-005"
      category: "Usability"
      requirement: "Vague NFR terms must convert to measurable targets using quantification table"
      metric: "≥ 85% of vague NFRs successfully quantified (measured over 30 NFR clarifications)"
      test_requirement: "Test: Simulate 30 vague NFRs, apply quantification table, measure conversion success rate, assert ≥25/30 (83%+)"

    - id: "NFR-006"
      category: "Maintainability"
      requirement: "Patterns must be versioned and change-tracked"
      metric: "Document version incremented on each update (semver: major.minor.patch)"
      test_requirement: "Test: Verify version field in document header, Git log shows version increments match update commits"

    - id: "NFR-007"
      category: "Quality"
      requirement: "Patterns must cover ≥90% of requirements elicitation scenarios"
      metric: "≥ 90% pattern applicability (skills find relevant pattern for most scenarios)"
      test_requirement: "Test: Skill feedback survey after 20 story creations, measure 'found relevant pattern' rate, assert ≥18/20 (90%+)"

    - id: "NFR-008"
      category: "Quality"
      requirement: "Templates must result in complete answers (minimal follow-ups)"
      metric: "≥ 80% of AskUserQuestion invocations using templates get complete answers (no follow-up questions)"
      test_requirement: "Test: Monitor 50 template usages, count follow-ups needed, assert ≤10/50 (80%+ complete on first attempt)"

    - id: "NFR-009"
      category: "Reusability"
      requirement: "Single reference file must serve all 5 target skills (no duplication)"
      metric: "5 skills load same user-input-guidance.md file (verified via Read tool paths)"
      test_requirement: "Test: Grep all 5 skill SKILL.md files for 'user-input-guidance.md' Read commands, verify all point to same file path"

    - id: "NFR-010"
      category: "Scalability"
      requirement: "Guidance must support pattern growth without performance degradation"
      metric: "File supports 30-50 patterns with Grep search time remaining < 30 seconds"
      test_requirement: "Test: Create test file with 50 patterns, execute Grep searches, measure time, assert <30s per search"
```

---

## Edge Cases

1. **Guidance loaded but not used by skill:** Skill reads user-input-guidance.md but follows hardcoded logic instead of consulting patterns. Mitigation: Skill SKILL.md references guidance file in workflow phases, includes "Consult user-input-guidance.md for patterns" instructions.

2. **Pattern doesn't fit user's specific scenario:** User's requirement is unique and no predefined pattern applies directly. Mitigation: Guidance includes "Pattern Customization" section with instructions for adapting closest pattern or creating ad-hoc AskUserQuestion.

3. **AskUserQuestion template needs customization:** Template's options don't match user's technology stack or domain. Mitigation: Each template includes "Customization Notes" section explaining which parts to adjust (e.g., replace "React" with user's frontend framework).

4. **Multiple patterns could apply:** Skill identifies 2-3 relevant patterns for same requirement. Mitigation: Guidance includes "Pattern Selection Logic" flowchart: (1) Match requirement type, (2) Check user context (greenfield vs brownfield), (3) Prefer most specific pattern, (4) Combine patterns if needed.

5. **Quantification table missing user's vague term:** User says "efficient" but table only covers "fast", "scalable", "performant". Mitigation: Table includes "Unmapped Terms" fallback section with generic quantification template.

6. **Skill misinterprets guidance and creates poor AskUserQuestion:** Skill uses template but options are confusing or don't cover user's likely choices. Mitigation: Each template includes "Quality Checklist": (1) ≥3 options, (2) Options mutually exclusive, (3) Options cover 90% of likely responses, (4) Descriptions explain implications of each choice.

---

## Data Validation Rules

1. **Pattern Structure:** Each pattern must include: Problem Description (2-3 sentences), Solution (step-by-step), AskUserQuestion Template (copy-paste ready), Example (real DevForgeAI scenario), Related Patterns (1-3 links).

2. **Template Structure:** Each AskUserQuestion template must include: question (1-2 sentences), header (context framing), options array (3-5 items with label + description), Customization Notes.

3. **Quantification Table Format:** Each row must include: Vague Term, Measurable Range (with units/percentiles), Example (DevForgeAI context), AskUserQuestion Template link.

4. **Skill Integration Points:** Each integration must document: Skill Name, Workflow Phase, Use Cases (3-5 scenarios), Read Command (exact invocation).

5. **Framework Terminology Validation:** All terms must match CLAUDE.md and reference files (context files, quality gates, workflow states, story structure). No undefined abbreviations.

6. **Reference File Paths:** All file path citations must be absolute and exist in framework. Validated via Grep extraction → file existence check.

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-052:** User-Facing Prompting Guide
  - **Why:** user-input-guidance.md cross-references effective-prompting-guide.md for user-facing examples and terminology alignment
  - **Status:** Created (same batch)

### External Dependencies

None - Self-contained framework reference.

### Technology Dependencies

None - Markdown format requires no additional packages.

---

## Test Strategy

### Documentation Validation Tests

**Coverage Target:** 100% validation coverage (all patterns, templates, table entries validated)

**Test Scenarios:**

1. **Pattern Validation (DOC-001, BR-001)**
   - Count patterns (10-15 range check)
   - Verify each pattern has all required sections
   - Validate AskUserQuestion syntax in templates
   - Test pattern completeness checklist

2. **Template Validation (DOC-002, BR-002)**
   - Count templates (20-30 range check)
   - Validate option count per template (3-5 range)
   - Check template syntax (valid Python/YAML structure)
   - Verify customization notes present

3. **Quantification Table Validation (DOC-003, BR-003)**
   - Count vague terms (≥15)
   - Verify measurable ranges have numbers
   - Check examples cite DevForgeAI scenarios
   - Validate template links resolve

4. **Skill Integration Validation (DOC-004)**
   - Verify 5 skill integration sections exist
   - Check Read commands are syntactically correct
   - Validate workflow phase references
   - Test that skills can actually load file

5. **Framework Alignment Validation (DOC-005, BR-004)**
   - Extract all DevForgeAI terms
   - Grep CLAUDE.md for each term
   - Assert 100% match (no undefined terms)
   - Verify file path references exist

6. **Performance Validation (NFR-001, NFR-002, NFR-003)**
   - Measure Read tool load time (<500ms)
   - Measure Grep pattern search time (<30s)
   - Count tokens in file (≤3,000)

**Test File Locations:**
- `tests/user-input-guidance/test-pattern-structure.sh`
- `tests/user-input-guidance/test-template-syntax.py`
- `tests/user-input-guidance/test-quantification-table.py`
- `tests/user-input-guidance/test-skill-integration.sh`
- `tests/user-input-guidance/test-framework-alignment.sh`
- `tests/user-input-guidance/test-performance.py`

---

## Acceptance Criteria Verification Checklist

### AC#1: Pattern Completeness

- [ ] Pattern count (10-15) - **Phase:** 2 - **Evidence:** grep -c "^### Pattern" user-input-guidance.md
- [ ] Functional patterns (3-4) - **Phase:** 2 - **Evidence:** grep "Pattern.*Functional"
- [ ] NFR patterns (2-3) - **Phase:** 2 - **Evidence:** grep "Pattern.*NFR"
- [ ] Edge case patterns (2-3) - **Phase:** 2 - **Evidence:** grep "Pattern.*Edge"
- [ ] Integration patterns (2-3) - **Phase:** 2 - **Evidence:** grep "Pattern.*Integration"
- [ ] Constraint patterns (1-2) - **Phase:** 2 - **Evidence:** grep "Pattern.*Constraint"

### AC#2: Template Usability

- [ ] Template count (20-30) - **Phase:** 2 - **Evidence:** grep -c "AskUserQuestion" user-input-guidance.md
- [ ] Pre-written question text - **Phase:** 2 - **Evidence:** Each template has "question:" field
- [ ] Header text for context - **Phase:** 2 - **Evidence:** Each template has "header:" field
- [ ] 3-5 options per template - **Phase:** 2 - **Evidence:** Parse options arrays, assert len(options) in [3,5]
- [ ] Customization guidance - **Phase:** 2 - **Evidence:** Each template has "Customization Notes" section
- [ ] Scenarios coverage - **Phase:** 2 - **Evidence:** Templates cover functional/NFR/edge/integration/constraint

### AC#3: NFR Quantification Accuracy

- [ ] ≥15 vague terms in table - **Phase:** 2 - **Evidence:** Count table rows
- [ ] Measurable ranges provided - **Phase:** 2 - **Evidence:** Each row has numeric targets (< Xms, ≥Y%)
- [ ] DevForgeAI examples - **Phase:** 2 - **Evidence:** Examples cite QA times, story creation metrics
- [ ] Template links functional - **Phase:** 2 - **Evidence:** Links resolve to actual templates

### AC#4: Skill Integration Success

- [ ] 5 skill integration sections - **Phase:** 2 - **Evidence:** grep "Integration: devforgeai-" count = 5
- [ ] Read commands correct - **Phase:** 2 - **Evidence:** Parse Read(...) invocations, validate syntax
- [ ] Workflow phases specified - **Phase:** 2 - **Evidence:** Each integration notes "Phase X Step Y"
- [ ] Use cases documented - **Phase:** 2 - **Evidence:** Each integration lists 3-5 use cases
- [ ] File loads in all skills - **Phase:** 3 - **Evidence:** test-skill-integration.sh passes (5/5 skills)
- [ ] Pattern search <30s - **Phase:** 3 - **Evidence:** Grep performance test
- [ ] ≥30% reduction in re-invocations - **Phase:** 4 - **Evidence:** Measure over 10 stories (baseline vs enhanced)

### AC#5: Framework Alignment

- [ ] Context file terms match - **Phase:** 2 - **Evidence:** Grep for tech-stack/source-tree/etc., verify exist
- [ ] Quality gate terms match - **Phase:** 2 - **Evidence:** Grep for "Gate 1" through "Gate 4"
- [ ] Workflow state terms match - **Phase:** 2 - **Evidence:** Grep for "Backlog", "Ready for Dev", etc.
- [ ] Story structure terms match - **Phase:** 2 - **Evidence:** Grep for "YAML frontmatter", "Given/When/Then"
- [ ] Reference file paths provided - **Phase:** 2 - **Evidence:** Read commands cite .claude/ and .devforgeai/ paths
- [ ] Terminology validated - **Phase:** 3 - **Evidence:** test-framework-alignment.sh passes (100% match)

---

**Checklist Progress:** 0/32 items complete (0%)

---


## Implementation Notes

Status: Backlog - Story created and ready for development. All Definition of Done items will be completed during TDD cycle.
## Definition of Done

### Implementation
- [ ] src/claude/skills/devforgeai-ideation/references/user-input-guidance.md created (2,000-3,000 lines)
- [ ] 10-15 elicitation patterns documented (each with Problem/Solution/Template/Example)
- [ ] 20-30 AskUserQuestion templates included (copy-paste ready)
- [ ] NFR quantification table created (≥15 vague terms mapped to measurable targets)
- [ ] 5 skill integration sections documented (ideation, story-creation, architecture, ui-generator, orchestration)
- [ ] Cross-references to effective-prompting-guide.md and claude-code-terminal-expert added
- [ ] Framework terminology validated (100% match with CLAUDE.md)

### Quality
- [ ] All 5 acceptance criteria have passing validation tests
- [ ] Edge cases documented (6 scenarios with mitigations)
- [ ] Data validation rules enforced (6 rules with test assertions)
- [ ] NFRs met (10 NFRs covering performance, usability, maintainability, quality, reusability, scalability)
- [ ] Document coverage 100% (all patterns, templates, integrations documented)

### Testing
- [ ] Pattern structure test (DOC-001, BR-001)
- [ ] Template syntax test (DOC-002, BR-002)
- [ ] Quantification table test (DOC-003, BR-003)
- [ ] Skill integration test (DOC-004)
- [ ] Framework alignment test (DOC-005, BR-004)
- [ ] Performance tests (NFR-001, NFR-002, NFR-003)
- [ ] Usability tests (NFR-004, NFR-005)
- [ ] Quality tests (NFR-007, NFR-008)
- [ ] All tests passing (8/8 test categories)

### Documentation
- [ ] Document is framework-internal reference (loaded by skills during execution)
- [ ] Cross-referenced from 5 skill SKILL.md files (Phase 1 Step 0 instructions)
- [ ] Cross-referenced from effective-prompting-guide.md (user-facing counterpart)
- [ ] Versioned (includes version: 1.0.0 in header)
- [ ] Synced to operational folder (copied from src/ to .claude/ during deployment)

---

## Workflow History

### 2025-01-20 20:45:00 - Status: Ready for Dev
- Added to SPRINT-2: User Input Guidance Implementation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 40 points (9 stories)
- Priority in sprint: [2 of 9] - Framework-internal guidance reference

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

## Notes

**Design Decisions:**
- **Location:** src/claude/skills/devforgeai-ideation/references/ chosen as authoritative location (ideation is entry point skill)
- **Reusability:** Single file shared across 5 skills (progressive disclosure pattern - loaded once, benefits multiple workflows)
- **Format:** Markdown with YAML code blocks for AskUserQuestion templates (copy-paste into skill execution)
- **Structure:** Patterns first (what to ask), templates second (how to ask), quantification table third (how to measure), integration fourth (where to use)

**Framework Cohesion Strategy:**
- **effective-prompting-guide.md:** User-facing (what users should provide)
- **user-input-guidance.md:** Framework-internal (how skills should elicit)
- **claude-code-terminal-expert:** Knowledge repository (authoritative framework reference)
- All three cross-reference each other for cohesion

**Success Metrics (from EPIC-011):**
- 52% reduction in subagent re-invocations (2.5 → 1.2 average)
- 30%+ reduction measured per skill integration
- ≥90% pattern applicability across 20 story creations

**Related ADRs:**
None required (documentation reference, not architectural change)

**References:**
- EPIC-011: User Input Guidance System
- effective-prompting-guide.md: User-facing counterpart
- claude-code-terminal-expert: Framework knowledge base
- acceptance-criteria-patterns.md: AC pattern reference for comparison

---

**Story Template Version:** 2.0
**Created:** 2025-01-20
