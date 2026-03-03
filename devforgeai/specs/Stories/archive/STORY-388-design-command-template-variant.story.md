---
id: STORY-388
title: "Design Command Template Variant with 15K Char Budget Compliance"
type: feature
epic: EPIC-061
sprint: Backlog
status: QA Approved
points: 3
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-06
updated: 2026-02-06
format_version: "2.8"
---

# Story: Design Command Template Variant with 15K Char Budget Compliance

## Description

**As a** command author (framework contributor creating or refactoring DevForgeAI slash commands),
**I want** a canonical command template variant that documents required sections, character budget allocation guidance, delegation patterns to skills, and error handling patterns within the 15K character constraint,
**so that** every new or refactored command follows a consistent, budget-compliant structure that maximizes orchestration quality while staying within token efficiency limits.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-010" section="problem-statement">
    <quote>"Current commands have varying structure and no standardized delegation patterns; lean orchestration budget compliance is inconsistent"</quote>
    <line_reference>EPIC-061, Feature 3</line_reference>
    <quantified_impact>24+ commands without standardized template; 15K char budget enforcement is manual</quantified_impact>
  </origin>
  <decision rationale="template-with-budget-guidance">
    <selected>Canonical command template with explicit character budget allocation targets per section and delegation patterns</selected>
    <rejected alternative="guidelines-only">Guidelines without concrete budget allocation targets would not prevent budget overruns</rejected>
    <trade_off>Template must itself fit within 500-line/15K char limit to serve as working example of compliance</trade_off>
  </decision>
  <stakeholder role="Framework Owner" goal="efficient-command-orchestration">
    <quote>"Commands are efficient orchestrators that maximize quality within token budget"</quote>
    <source>EPIC-061, Feature 3 User Value</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Template Defines Required and Optional Sections

```xml
<acceptance_criteria id="AC1">
  <given>The command template document exists at a documented location within the framework</given>
  <when>A command author reviews the template</when>
  <then>The template clearly distinguishes required sections (YAML frontmatter with description/argument-hint/model/allowed-tools, title with description, Quick Reference with 3-5 usage examples, Phase 0: Argument Validation, Phase 1: Skill Invocation with context markers, Phase 2: Display Results, Error Handling with 3-5 error types, Success Criteria, Integration metadata) from optional sections (Phase 3: Next Steps, Performance/Token Budget, multi-mode detection, batch workflow variant) and each section includes a brief purpose annotation</then>
  <verification>
    <source_files>
      <file hint="Command template">src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md</file>
    </source_files>
    <test_file>tests/STORY-388/test_ac1_required_sections.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Template Fits Within 500-Line / 15K Char Constraints

```xml
<acceptance_criteria id="AC2">
  <given>The completed command template markdown file</given>
  <when>Character count and line count are measured</when>
  <then>The template is under 500 lines AND under 15,000 characters AND the template itself serves as a working example of budget compliance</then>
  <verification>
    <source_files>
      <file hint="Command template">src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md</file>
    </source_files>
    <test_file>tests/STORY-388/test_ac2_size_constraints.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Character Budget Allocation Guidance Provided

```xml
<acceptance_criteria id="AC3">
  <given>The command template includes a Budget Allocation section</given>
  <when>A command author needs to allocate their 15K character budget across sections</when>
  <then>The template provides specific character allocation targets per section (e.g., YAML frontmatter: 200-400 chars, Quick Reference: 300-600 chars, Phase 0 argument validation: 800-1500 chars, Phase 1 skill invocation: 600-1200 chars, Phase 2 results display: 400-800 chars, Error Handling: 600-1200 chars, Integration/Performance: 400-800 chars) AND the maximum allocations sum to no more than 15,000 characters AND each allocation references the lean orchestration pattern 6K-12K optimal range</then>
  <verification>
    <source_files>
      <file hint="Command template">src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md</file>
      <file hint="Lean orchestration protocol">src/devforgeai/protocols/lean-orchestration-pattern.md</file>
    </source_files>
    <test_file>tests/STORY-388/test_ac3_budget_allocation.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Delegation Patterns to Skills Documented

```xml
<acceptance_criteria id="AC4">
  <given>The command template includes skill delegation instructions</given>
  <when>A command author reads the Phase 1: Skill Invocation section</when>
  <then>The template documents the Skill Invocation Checkpoint Pattern including: (a) explicit Skill(command="devforgeai-[skillname]") syntax, (b) context marker setting before invocation with **[Param]:** ${VALUE} format, (c) MANDATORY marker with warning emoji per lean orchestration protocol, (d) "DO NOT proceed with manual analysis" statement, and (e) clear statement that commands ONLY orchestrate while skills implement business logic</then>
  <verification>
    <source_files>
      <file hint="Command template">src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md</file>
      <file hint="Lean orchestration protocol">src/devforgeai/protocols/lean-orchestration-pattern.md</file>
    </source_files>
    <test_file>tests/STORY-388/test_ac4_delegation_patterns.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Error Handling Patterns Included

```xml
<acceptance_criteria id="AC5">
  <given>The command template includes an Error Handling section</given>
  <when>A command author implements error handling for a new command</when>
  <then>The template provides 3-5 standard error categories (argument validation failure, context file not found, skill invocation failure, story/resource not found, unexpected error) with each category showing: error detection pattern, user-facing message format, recovery action, and a note that complex error recovery belongs in skills not commands</then>
  <verification>
    <source_files>
      <file hint="Command template">src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md</file>
    </source_files>
    <test_file>tests/STORY-388/test_ac5_error_handling.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Template Validated Against Existing Commands

```xml
<acceptance_criteria id="AC6">
  <given>The command template has been designed</given>
  <when>The template structure is compared against at least 2 existing refactored commands</when>
  <then>Both commands' structures can be mapped to the template sections (required sections present, optional sections identified) AND the template does not introduce sections that contradict existing command patterns AND a validation note documents the mapping for each command</then>
  <verification>
    <source_files>
      <file hint="Command template">src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md</file>
      <file hint="QA command reference">src/claude/commands/qa.md</file>
      <file hint="Dev command reference">src/claude/commands/dev.md</file>
    </source_files>
    <test_file>tests/STORY-388/test_ac6_command_validation.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "command-template.md"
      file_path: "src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md"
      purpose: "Canonical command template defining required/optional sections, budget allocation, and delegation patterns"
      required_keys:
        - key: "YAML Frontmatter"
          type: "object"
          example: "description, argument-hint, model, allowed-tools"
          required: true
          validation: "Must contain all 4 required fields"
          test_requirement: "Test: Grep for description:, argument-hint:, model:, allowed-tools: in YAML block"
        - key: "Quick Reference"
          type: "string"
          example: "3-5 usage examples with description"
          required: true
          validation: "Must contain 3-5 examples"
          test_requirement: "Test: Count example entries in Quick Reference section, verify >= 3 and <= 5"
        - key: "Phase 0: Argument Validation"
          type: "string"
          example: "Argument parsing, mode detection, context loading"
          required: true
          validation: "Must include argument parsing pattern"
          test_requirement: "Test: Grep for Phase 0 or Argument Validation heading"
        - key: "Phase 1: Skill Invocation"
          type: "string"
          example: "Skill(command=...) with MANDATORY marker"
          required: true
          validation: "Must include Skill() invocation syntax and MANDATORY marker"
          test_requirement: "Test: Grep for Skill(command= and MANDATORY in Phase 1 section"
        - key: "Phase 2: Display Results"
          type: "string"
          example: "Results verification and display"
          required: true
          validation: "Must include results verification pattern"
          test_requirement: "Test: Grep for Phase 2 or Display Results heading"
        - key: "Error Handling"
          type: "string"
          example: "3-5 categorized error patterns"
          required: true
          validation: "Must contain 3-5 error categories"
          test_requirement: "Test: Count error categories under Error Handling section, verify >= 3"
        - key: "Budget Allocation"
          type: "string"
          example: "Per-section character allocation targets"
          required: true
          validation: "Maximum allocations must sum to <= 15000"
          test_requirement: "Test: Parse budget table and verify sum of max allocations <= 15000"
      requirements:
        - id: "CFG-001"
          description: "Template must define all required sections with purpose annotations"
          implements_ac: ["AC1"]
          testable: true
          test_requirement: "Test: Verify 9 required section headers present with purpose annotations"
          priority: "Critical"
        - id: "CFG-002"
          description: "Template must fit within 500-line / 15K char constraints"
          implements_ac: ["AC2"]
          testable: true
          test_requirement: "Test: wc -c returns <= 15000 AND wc -l returns <= 500"
          priority: "Critical"
        - id: "CFG-003"
          description: "Template must provide character budget allocation table with per-section targets"
          implements_ac: ["AC3"]
          testable: true
          test_requirement: "Test: Budget allocation table exists and max allocations sum to <= 15000"
          priority: "High"
        - id: "CFG-004"
          description: "Template must document Skill Invocation Checkpoint Pattern with explicit syntax"
          implements_ac: ["AC4"]
          testable: true
          test_requirement: "Test: Grep for Skill(command=, MANDATORY, and DO NOT proceed in skill invocation section"
          priority: "High"
        - id: "CFG-005"
          description: "Template must include 3-5 categorized error handling patterns"
          implements_ac: ["AC5"]
          testable: true
          test_requirement: "Test: Count error categories under Error Handling, verify >= 3 and <= 5"
          priority: "High"
        - id: "CFG-006"
          description: "Template must validate against 2+ existing refactored commands with mapping notes"
          implements_ac: ["AC6"]
          testable: true
          test_requirement: "Test: Validation notes reference at least 2 command files with section mapping"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Commands must ONLY orchestrate — all implementation logic belongs in skills"
      trigger: "When template defines command scope boundaries"
      validation: "Template explicitly states orchestration-only principle"
      error_handling: "Flag if command logic exceeds 50 lines — extract to skill"
      test_requirement: "Test: Template contains orchestration-only statement and 50-line extraction threshold"
      priority: "Critical"
    - id: "BR-002"
      rule: "Character budget allocations must sum to no more than 15,000 characters"
      trigger: "When budget allocation table is defined"
      validation: "Sum of maximum allocation column <= 15000"
      error_handling: "HALT if budget exceeds limit — trim sections per priority order"
      test_requirement: "Test: Parse budget table, sum max column, verify <= 15000"
      priority: "Critical"
    - id: "BR-003"
      rule: "Template is additive — existing commands continue to work without modification"
      trigger: "When template is published"
      validation: "No existing command file is modified during template creation"
      error_handling: "If template contradicts existing pattern, adjust template not command"
      test_requirement: "Test: Git diff shows only new template file, no modifications to existing command files"
      priority: "High"
    - id: "BR-004"
      rule: "User interaction (AskUserQuestion) stays in commands, not skills"
      trigger: "When template defines interaction boundaries"
      validation: "Template documents that AskUserQuestion belongs in commands per lean orchestration"
      error_handling: "Warning if template moves user interaction to skills"
      test_requirement: "Test: Template mentions AskUserQuestion stays in commands"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Template file size within optimal range"
      metric: "6,000-12,000 characters (optimal), maximum 15,000 characters"
      test_requirement: "Test: wc -c returns value between 6000 and 15000"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Template adds zero runtime overhead"
      metric: "Template is reference documentation only, not loaded at command execution time"
      test_requirement: "Test: No existing command references or loads the template at runtime"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Template compatible with all existing commands"
      metric: "0 existing commands broken after template creation"
      test_requirement: "Test: Git diff shows no modifications to existing .claude/commands/ files"
      priority: "Critical"
    - id: "NFR-004"
      category: "Scalability"
      requirement: "Template accommodates command size range"
      metric: "Supports commands from 150 lines (minimal) to 500 lines (complex) without modification"
      test_requirement: "Test: Budget allocation guidance includes proportional scaling for different command sizes"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this template design story
```

---

## Non-Functional Requirements (NFRs)

### Performance

**File Size:**
- Template size: 6,000-12,000 characters (optimal range per lean orchestration pattern)
- Maximum: 15,000 characters / 500 lines
- Template is reference documentation only — zero runtime overhead

### Security

**Authentication:** None required (framework documentation file)
**Authorization:** None required
**Data Protection:** No sensitive data in template

### Scalability

**Command Size Range:**
- Template accommodates commands from 150 lines (minimal orchestrator) to 500 lines (complex multi-mode command)
- Budget allocation guidance scales proportionally for different command sizes

### Reliability

**Backward Compatibility:**
- Template is purely additive — no breaking changes to existing commands
- All 24+ existing commands continue to work without modification
- Template defines what new/refactored commands should follow

### Observability

**Not applicable** — this is a static documentation template, not a runtime component.

---

## Dependencies

### Prerequisite Stories

- None — template design can proceed independently

### External Dependencies

- None — all work within Claude Code Terminal

### Technology Dependencies

- None — template is a Markdown file per tech-stack.md

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for template validation

**Test Scenarios:**
1. **Happy Path:** Template contains all required sections with proper headings
2. **Edge Cases:**
   - Template at exactly 15,000 characters
   - Template at exactly 500 lines
   - Budget allocation at maximum sum
3. **Error Cases:**
   - Missing required section
   - Budget allocation exceeds 15,000
   - Template exceeds line limit

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Command Mapping Validation:** Map /qa and /dev command structure to template sections
2. **Lean Orchestration Compliance:** Verify template references match lean-orchestration-pattern.md

### E2E Tests

**Not applicable** — static documentation template

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Template Defines Required and Optional Sections

- [ ] Required sections list defined - **Phase:** 2 - **Evidence:** command-template.md
- [ ] Optional sections list defined - **Phase:** 2 - **Evidence:** command-template.md
- [ ] Purpose annotations present for each section - **Phase:** 3 - **Evidence:** command-template.md

### AC#2: Template Fits Within Constraints

- [ ] Character count under 15,000 - **Phase:** 3 - **Evidence:** wc -c output
- [ ] Line count under 500 - **Phase:** 3 - **Evidence:** wc -l output

### AC#3: Budget Allocation Guidance

- [ ] Per-section allocation targets documented - **Phase:** 3 - **Evidence:** command-template.md
- [ ] Max allocations sum to <= 15,000 - **Phase:** 3 - **Evidence:** test_ac3_budget_allocation.sh
- [ ] Optimal range referenced (6K-12K) - **Phase:** 3 - **Evidence:** command-template.md

### AC#4: Delegation Patterns

- [ ] Skill() invocation syntax documented - **Phase:** 3 - **Evidence:** command-template.md
- [ ] MANDATORY marker with warning emoji - **Phase:** 3 - **Evidence:** command-template.md
- [ ] Context marker format documented - **Phase:** 3 - **Evidence:** command-template.md

### AC#5: Error Handling Patterns

- [ ] 3-5 error categories defined - **Phase:** 3 - **Evidence:** command-template.md
- [ ] Each category has detection/message/recovery - **Phase:** 3 - **Evidence:** command-template.md

### AC#6: Validated Against Existing Commands

- [ ] /qa mapped to template sections - **Phase:** 5 - **Evidence:** validation notes
- [ ] /dev mapped to template sections - **Phase:** 5 - **Evidence:** validation notes

---

**Checklist Progress:** 0/14 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Command template file created at documented location
- [x] All 9 required sections present with purpose annotations
- [x] All optional sections documented with usage guidance
- [x] Character budget allocation table complete
- [x] Delegation patterns documented with Skill() syntax
- [x] Error handling patterns (3-5 categories) documented
- [x] Template self-validates within 500-line / 15K char constraints

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (standalone command, budget limit, multi-mode)
- [x] Budget allocation validated (sum <= 15,000)
- [x] NFRs met (file size, backward compatibility)
- [x] Code coverage >95% for template validation tests

### Testing
- [x] Unit tests for required section presence
- [x] Unit tests for character/line count constraints
- [x] Unit tests for budget allocation sum
- [x] Unit tests for delegation pattern syntax
- [x] Integration tests mapping /qa and /dev to template

### Documentation
- [x] Template serves as its own documentation (self-documenting)
- [x] Migration notes for pre-template commands included
- [x] References to lean orchestration protocol linked

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-12
**Branch:** main

- [x] Command template file created at documented location - Completed: Created at src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md
- [x] All 9 required sections present with purpose annotations - Completed: YAML frontmatter, title, Quick Reference, Phase 0, Phase 1, Phase 2, Error Handling, Success Criteria, Integration metadata all present with annotations
- [x] All optional sections documented with usage guidance - Completed: Phase 3 Next Steps, Performance/Token Budget, multi-mode detection, batch workflow variant documented
- [x] Character budget allocation table complete - Completed: Per-section allocation targets with max sum <= 15,000 chars
- [x] Delegation patterns documented with Skill() syntax - Completed: Skill Invocation Checkpoint Pattern with MANDATORY marker, context markers, and DO NOT proceed statement
- [x] Error handling patterns (3-5 categories) documented - Completed: 5 categories: argument validation, context file missing, skill invocation failure, resource not found, unexpected error
- [x] Template self-validates within 500-line / 15K char constraints - Completed: Template fits within both constraints
- [x] All 6 acceptance criteria have passing tests - Completed: 6 test files in tests/STORY-388/ covering all ACs
- [x] Edge cases covered (standalone command, budget limit, multi-mode) - Completed: Tests cover exact-limit, missing sections, budget overflow scenarios
- [x] Budget allocation validated (sum <= 15,000) - Completed: Budget allocation table sum verified in test_ac3_budget_allocation.sh
- [x] NFRs met (file size, backward compatibility) - Completed: File size in optimal range, no existing commands modified
- [x] Code coverage >95% for template validation tests - Completed: All 6 ACs covered with comprehensive test scenarios
- [x] Unit tests for required section presence - Completed: test_ac1_required_sections.sh validates all 9 required sections
- [x] Unit tests for character/line count constraints - Completed: test_ac2_size_constraints.sh validates <500 lines and <15K chars
- [x] Unit tests for budget allocation sum - Completed: test_ac3_budget_allocation.sh validates sum <= 15,000
- [x] Unit tests for delegation pattern syntax - Completed: test_ac4_delegation_patterns.sh validates Skill() syntax and MANDATORY marker
- [x] Integration tests mapping /qa and /dev to template - Completed: test_ac6_command_validation.sh maps both commands to template structure
- [x] Template serves as its own documentation (self-documenting) - Completed: Template includes purpose annotations and inline guidance
- [x] Migration notes for pre-template commands included - Completed: Template notes that existing commands continue to work without modification
- [x] References to lean orchestration protocol linked - Completed: References to lean-orchestration-pattern.md included throughout

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-06 18:00 | claude/story-requirements-analyst | Created | Story created from EPIC-061 Feature 3 | STORY-388.story.md |
| 2026-02-12 04:10 | .claude/opus | DoD Update (Phase 07) | Development complete, DoD validated, Implementation Notes added | STORY-388.story.md |
| 2026-02-12 10:55 | .claude/qa-result-interpreter | QA Deep | PASSED: 39/39 tests, 100% traceability, 0 violations | STORY-388-qa-report.md |

## Notes

**Design Decisions:**
- Template location TBD during development (likely `src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md` or dedicated template directory)
- Template itself must serve as a working example of 15K budget compliance
- Lean orchestration protocol is the authoritative reference; template provides concrete patterns from it

**Open Questions:**
- [ ] Template file location — use existing templates/ directory or create new? - **Owner:** Framework Owner - **Due:** Sprint start

**Related ADRs:**
- None yet (template is additive, no breaking changes expected)

**References:**
- `src/devforgeai/protocols/lean-orchestration-pattern.md` (authoritative delegation patterns)
- `.claude/commands/qa.md` (reference command for validation)
- `.claude/commands/dev.md` (reference command for validation)
- EPIC-061 Feature 3 (parent feature)

---

Story Template Version: 2.8
Last Updated: 2026-02-06
