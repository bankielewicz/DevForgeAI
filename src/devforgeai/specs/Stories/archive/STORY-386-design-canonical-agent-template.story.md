---
id: STORY-386
title: "Design Canonical Agent Template with Required and Optional Sections"
type: feature
epic: EPIC-061
sprint: Backlog
status: QA Approved
points: 8
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-06
updated: 2026-02-06
format_version: "2.8"
---

# Story: Design Canonical Agent Template with Required and Optional Sections

## Description

**As a** Framework Owner,
**I want** a canonical agent template that defines required sections (identity, purpose, tools, output format, constraints, examples) and optional sections per agent category (validator, implementor, analyzer, formatter),
**so that** all 32+ subagents follow a consistent, research-backed prompt structure that reduces QA fix cycles, improves subagent output reliability, and enables automated compliance enforcement by agent-generator.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-010" section="problem-statement">
    <quote>"Current agents have inconsistent structure, varying section names, and no standardized prompt engineering patterns"</quote>
    <line_reference>EPIC-061, Feature 1</line_reference>
    <quantified_impact>32+ agents with inconsistent prompt structure; standardization enables automated enforcement</quantified_impact>
  </origin>
  <decision rationale="full-standardization-over-guidelines">
    <selected>Full standardization — single canonical template with required sections, optional sections, and validation rules enforced by agent-generator</selected>
    <rejected alternative="guidelines-only">Guidelines without enforcement would not prevent regression</rejected>
    <trade_off>Higher upfront design effort but zero ongoing compliance drift</trade_off>
  </decision>
  <stakeholder role="Framework Owner" goal="consistent-agent-quality">
    <quote>"All agents follow consistent prompt structure proven by Anthropic research"</quote>
    <source>EPIC-061, Business Goal</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Template Defines All Required Sections

```xml
<acceptance_criteria id="AC1">
  <given>The canonical agent template document exists at src/claude/agents/agent-generator/references/canonical-agent-template.md</given>
  <when>A framework maintainer reads the template</when>
  <then>It contains the following 10 required sections, each with a specification block defining purpose, format, and minimum content:
    1. YAML Frontmatter (fields: name, description, tools, model, color, permissionMode, skills, proactive_triggers)
    2. Title (H1 heading matching name field)
    3. Purpose (what the agent does, 2-5 sentences)
    4. When Invoked (proactive triggers, explicit invocation, automatic triggers)
    5. Input/Output Specification (what the agent receives and what it returns)
    6. Constraints and Boundaries (what the agent must NOT do, tool restrictions, read-only policies)
    7. Workflow (numbered steps for execution)
    8. Success Criteria (measurable checklist items)
    9. Output Format (structured format of agent deliverable)
    10. Examples (at least 1 invocation example with Task() pattern)</then>
  <verification>
    <source_files>
      <file hint="Canonical template">src/claude/agents/agent-generator/references/canonical-agent-template.md</file>
    </source_files>
    <test_file>tests/STORY-386/test_ac1_required_sections.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: YAML Frontmatter Schema Fully Specified

```xml
<acceptance_criteria id="AC2">
  <given>The canonical agent template's frontmatter specification section</given>
  <when>A developer validates an agent's frontmatter against the schema</when>
  <then>The schema specifies for each field:
    - name: string, lowercase-kebab-case, required, must match filename without .md extension
    - description: string, 20-200 words, required, first sentence is standalone summary
    - tools: array of strings, required (use empty array for tool-less agents), valid values from allowed tool set
    - model: enum [opus, sonnet, haiku], required, default opus
    - color: string, optional, default green
    - permissionMode: enum [default, acceptEdits], optional, default default
    - skills: string or array, optional, identifies parent skill(s)
    - proactive_triggers: array of strings, optional, list of trigger phrases
    - version: string (semver), optional, for change tracking</then>
  <verification>
    <source_files>
      <file hint="Canonical template frontmatter section">src/claude/agents/agent-generator/references/canonical-agent-template.md</file>
    </source_files>
    <test_file>tests/STORY-386/test_ac2_frontmatter_schema.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Optional Sections Defined Per Agent Category

```xml
<acceptance_criteria id="AC3">
  <given>The canonical template includes a category system for agents</given>
  <when>A developer determines which optional sections to include for a new agent</when>
  <then>The template provides 4 category definitions with category-specific optional sections:
    Validator category (e.g., context-validator, ac-compliance-verifier):
      - Validation Rules, Severity Classification, Pass/Fail Criteria
    Implementor category (e.g., backend-architect, test-automator):
      - Implementation Patterns, Code Generation Rules, Test Requirements
    Analyzer category (e.g., code-analyzer, coverage-analyzer):
      - Analysis Metrics, Scoring Rubrics, Threshold Definitions
    Formatter category (e.g., dev-result-interpreter, ui-spec-formatter):
      - Output Templates, Data Transformation Rules, Display Modes
    And includes a decision table mapping agent primary function to category and optional sections</then>
  <verification>
    <source_files>
      <file hint="Category definitions">src/claude/agents/agent-generator/references/canonical-agent-template.md</file>
    </source_files>
    <test_file>tests/STORY-386/test_ac3_category_sections.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Template Validated Against 3+ Diverse Existing Agents

```xml
<acceptance_criteria id="AC4">
  <given>The canonical template has been drafted</given>
  <when>It is validated against at least 3 structurally diverse existing agents (test-automator.md, code-reviewer.md, security-auditor.md)</when>
  <then>For each validation target:
    1. The agent's existing content maps to template sections without information loss
    2. Section gaps are identified (existing agent missing template-required sections)
    3. A gap analysis table documents: section name, present Y/N, gap severity
    4. The gap analysis is included in the template document as an appendix
    5. All 3 agents' frontmatter fields normalize to template schema without data loss</then>
  <verification>
    <source_files>
      <file hint="Test automator agent">src/claude/agents/test-automator.md</file>
      <file hint="Code reviewer agent">src/claude/agents/code-reviewer.md</file>
      <file hint="Security auditor agent">src/claude/agents/security-auditor.md</file>
      <file hint="Canonical template with appendix">src/claude/agents/agent-generator/references/canonical-agent-template.md</file>
    </source_files>
    <test_file>tests/STORY-386/test_ac4_validation_agents.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Template Fits Within 500-Line Subagent Size Limit

```xml
<acceptance_criteria id="AC5">
  <given>An agent created from the canonical template with ALL required sections populated AND all optional sections for one category populated</given>
  <when>The total line count is measured</when>
  <then>The populated agent file is between 100 and 500 lines inclusive, and the canonical template reference document itself may exceed 500 lines since it is a reference document, not a subagent file</then>
  <verification>
    <source_files>
      <file hint="Canonical template reference">src/claude/agents/agent-generator/references/canonical-agent-template.md</file>
    </source_files>
    <test_file>tests/STORY-386/test_ac5_line_limit.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Consistent Frontmatter Field Naming Convention

```xml
<acceptance_criteria id="AC6">
  <given>Existing agents use inconsistent field naming (tools as string vs array, proactive_triggers vs proactive-triggers)</given>
  <when>The canonical template specifies standard field names</when>
  <then>The template uses underscore-separated names for multi-word fields consistently, documents the canonical field name for each field, and provides a migration mapping table for known variants including: allowed-tools to tools, proactive-triggers to proactive_triggers, tools string to tools array</then>
  <verification>
    <source_files>
      <file hint="Migration mapping table">src/claude/agents/agent-generator/references/canonical-agent-template.md</file>
    </source_files>
    <test_file>tests/STORY-386/test_ac6_naming_convention.sh</test_file>
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
      name: "canonical-agent-template.md"
      file_path: "src/claude/agents/agent-generator/references/canonical-agent-template.md"
      required_keys:
        - key: "Required Sections"
          type: "array"
          example: "[Frontmatter, Title, Purpose, When Invoked, Input/Output, Constraints, Workflow, Success Criteria, Output Format, Examples]"
          required: true
          validation: "Must contain all 10 required section definitions"
          test_requirement: "Test: Grep for all 10 section headings in template document"
        - key: "Agent Categories"
          type: "object"
          example: "{Validator, Implementor, Analyzer, Formatter}"
          required: true
          validation: "Must contain 4 category definitions with 3 optional sections each"
          test_requirement: "Test: Grep for all 4 category headings with subsection count"
        - key: "Frontmatter Schema"
          type: "object"
          example: "{name: string, description: string, tools: array, ...}"
          required: true
          validation: "Must define type, required/optional, constraints, default for each of 9 fields"
          test_requirement: "Test: Parse schema section and validate all 9 fields have type and required attributes"
        - key: "Migration Mapping Table"
          type: "table"
          example: "| allowed-tools | tools | Rename field |"
          required: true
          validation: "Must contain at least 5 known variant mappings"
          test_requirement: "Test: Grep for migration mapping table with minimum 5 rows"
        - key: "Gap Analysis Appendix"
          type: "table"
          example: "| Section | test-automator | code-reviewer | security-auditor |"
          required: true
          validation: "Must contain gap analysis for 3 diverse agents"
          test_requirement: "Test: Grep for gap analysis tables covering 3 agent names"
        - key: "Size Guidance"
          type: "object"
          example: "{min: 100, target: 100-300, max: 500, warning: 400}"
          required: true
          validation: "Must specify line count ranges"
          test_requirement: "Test: Grep for line count constraints (100, 300, 400, 500)"

  business_rules:
    - id: "BR-001"
      rule: "All 10 required sections must be present in every agent created from the template"
      trigger: "Agent creation or agent update via agent-generator"
      validation: "Grep for all 10 H2 section headings in agent file"
      error_handling: "Block agent creation if any required section missing; display specific missing section name"
      test_requirement: "Test: Create agent with 9 of 10 sections, verify block with error message naming missing section"
      priority: "Critical"

    - id: "BR-002"
      rule: "Optional sections are additive — agents may include sections from multiple categories"
      trigger: "Agent creation with cross-category needs (e.g., test-automator is both Implementor and Analyzer)"
      validation: "Count optional sections by category; allow multiple categories"
      error_handling: "Warn if total line count approaches 400; suggest reference extraction if exceeding 300"
      test_requirement: "Test: Create agent with sections from 2 categories, verify acceptance and line count warning"
      priority: "High"

    - id: "BR-003"
      rule: "Frontmatter field name must use underscore convention for multi-word fields"
      trigger: "Agent frontmatter validation"
      validation: "Regex check: no hyphens in field names (except single-word fields like 'name')"
      error_handling: "Block with specific field name and suggested canonical name"
      test_requirement: "Test: Submit agent with 'proactive-triggers' field, verify block and suggestion to use 'proactive_triggers'"
      priority: "High"

    - id: "BR-004"
      rule: "Agent file line count must not exceed 500 lines"
      trigger: "Agent file size validation"
      validation: "wc -l on agent file"
      error_handling: "Block if > 500 lines; warn if > 400 lines; suggest reference extraction if > 300 lines"
      test_requirement: "Test: Create agent with 501 lines, verify block; create with 401 lines, verify warning"
      priority: "Critical"

    - id: "BR-005"
      rule: "Existing agents not yet migrated must continue to function without modification"
      trigger: "Template enforcement activation"
      validation: "Enforcement applies only to new/updated agents via agent-generator"
      error_handling: "Legacy agents bypass template validation until explicitly migrated"
      test_requirement: "Test: Verify existing agent without template compliance still loads and functions"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Template validation by agent-generator must complete within 5 seconds"
      metric: "< 5 seconds from Read of agent file to validation result output"
      test_requirement: "Test: Time agent-generator validation run against sample agent; verify < 5s"
      priority: "Medium"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Template validation rules must catch 100% of frontmatter schema violations"
      metric: "0 false negatives for missing required fields, invalid field types, invalid enum values"
      test_requirement: "Test: Submit 10+ deliberately malformed frontmatters; verify all violations caught"
      priority: "High"

    - id: "NFR-003"
      category: "Scalability"
      requirement: "Template must support 100+ agents without structural changes"
      metric: "Category decision table extensible via row addition; no template restructuring needed"
      test_requirement: "Test: Add hypothetical 5th category to decision table; verify table structure remains valid"
      priority: "Medium"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Backward compatibility with all existing agents"
      metric: "0 existing agents broken by template introduction"
      test_requirement: "Test: Verify all 32+ existing agents load without errors before and after template deployment"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "EPIC-060 Research Artifact"
    limitation: "Research patterns from EPIC-060 may not be complete at template design time"
    decision: "workaround:Design template based on available research; update template when EPIC-060 completes"
    discovered_phase: "Architecture"
    impact: "Template may need revision after full research patterns available"
```

## Non-Functional Requirements (NFRs)

### Performance

**Template Processing:**
- Template instantiation (populating all required sections for a new agent): < 15 minutes of active work
- Template validation (agent-generator compliance check): < 5 seconds per agent file
- Template reference document size: < 800 lines (fits in single Read() call)

### Security

- No secrets or credentials in template examples (use placeholder values)
- Template examples must demonstrate Bash with scope restriction (e.g., `Bash(git:*)`)
- Tool access patterns follow principle of least privilege

### Reliability

- Backward compatibility: Existing agents function without modification
- Migration path: Explicit checklist, estimated 10-20 minutes per agent
- Validation coverage: 100% of frontmatter schema violations caught
- Rollback: Prompt versioning system enables rollback within 2 minutes

### Scalability

- Support current 32+ agents, scale to 100+ without structural changes
- Category extensibility via decision table row addition
- Version tracking via `version` frontmatter field

---

## Edge Cases & Error Handling

1. **Minimal agent with no tools and no category sections:** Agent has `tools: []` and performs pure analysis. Template must produce valid agent with all required sections (80-120 lines minimum). Constraints section states "No tools available" and Workflow describes reasoning-only steps.

2. **Agent spanning multiple categories:** An agent may be both Implementor and Analyzer (e.g., test-automator). Template allows selecting optional sections from multiple categories. Warn when combined agent approaches 500-line limit; recommend reference extraction.

3. **Progressive disclosure via references/ subdirectory:** For agents exceeding 300 lines, document the extraction pattern: core file stays under 300 lines with Reference Loading table, detailed content moves to `references/*.md`. Specify extractable vs non-extractable sections.

4. **Legacy frontmatter field variants:** Agent uses `allowed-tools` instead of `tools`. During migration, both field names might coexist temporarily. Canonical field name takes precedence; agent-generator rejects agents with both `tools` and `allowed-tools` present.

5. **Unique domain-specific sections not in any category:** Template includes "Extension Sections" guidance — additional sections permitted but must follow naming convention (H2, action-oriented title) and must not duplicate required section content.

6. **Description length variance:** Current agents range from 20 to 200+ word descriptions. Template specifies 20-200 word target with first sentence usable as standalone summary (truncated at ~80 characters for CLAUDE.md Subagent Registry).

---

## Dependencies

### Prerequisite Stories

- [ ] **EPIC-060:** Research patterns must be available before template design
  - **Why:** Template design based on prompt engineering patterns from EPIC-060 research
  - **Status:** In Progress (some overlap allowed per EPIC-061 notes)

### External Dependencies

None — all work within Claude Code Terminal.

### Technology Dependencies

None — template is a Markdown reference document.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for validation rules

**Test Scenarios:**
1. **Happy Path:** Template document contains all 10 required sections
2. **Happy Path:** Template document contains all 4 category definitions
3. **Happy Path:** Frontmatter schema specifies all 9 fields
4. **Edge Cases:**
   - Minimal agent from template meets 80-120 line minimum
   - Multi-category agent stays under 500 lines
   - Template reference document stays under 800 lines
5. **Error Cases:**
   - Agent missing required section → blocked with specific error
   - Agent with invalid frontmatter field → blocked with field name
   - Agent exceeding 500 lines → blocked with line count

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Gap Analysis Validation:** Template validated against test-automator.md, code-reviewer.md, security-auditor.md with zero information loss
2. **Migration Mapping:** Known frontmatter variants correctly mapped to canonical names

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: Template Defines All Required Sections

- [ ] Template document created at canonical path - **Phase:** 2 - **Evidence:** src/claude/agents/agent-generator/references/canonical-agent-template.md
- [ ] All 10 required section headings present - **Phase:** 2 - **Evidence:** Grep for section headings
- [ ] Each section has Purpose subsection - **Phase:** 2 - **Evidence:** Grep for "Purpose:" under each section
- [ ] Each section has Format subsection - **Phase:** 2 - **Evidence:** Grep for "Format:" under each section
- [ ] Each section has minimum content specification - **Phase:** 2 - **Evidence:** Read template sections

### AC#2: YAML Frontmatter Schema Fully Specified

- [ ] Schema section present in template - **Phase:** 2 - **Evidence:** Grep for frontmatter schema heading
- [ ] All 9 fields documented with type - **Phase:** 2 - **Evidence:** Grep for field names with type annotations
- [ ] Required/optional designation for each field - **Phase:** 2 - **Evidence:** Grep for "required"/"optional" markers
- [ ] Validation rules for each field - **Phase:** 2 - **Evidence:** Read schema section

### AC#3: Optional Sections Defined Per Agent Category

- [ ] Validator category with 3 optional sections defined - **Phase:** 2 - **Evidence:** Grep for "Validator" category
- [ ] Implementor category with 3 optional sections defined - **Phase:** 2 - **Evidence:** Grep for "Implementor" category
- [ ] Analyzer category with 3 optional sections defined - **Phase:** 2 - **Evidence:** Grep for "Analyzer" category
- [ ] Formatter category with 3 optional sections defined - **Phase:** 2 - **Evidence:** Grep for "Formatter" category
- [ ] Decision table mapping function to category - **Phase:** 2 - **Evidence:** Grep for decision table

### AC#4: Template Validated Against 3+ Diverse Agents

- [ ] test-automator.md gap analysis complete - **Phase:** 2 - **Evidence:** Gap analysis table in appendix
- [ ] code-reviewer.md gap analysis complete - **Phase:** 2 - **Evidence:** Gap analysis table in appendix
- [ ] security-auditor.md gap analysis complete - **Phase:** 2 - **Evidence:** Gap analysis table in appendix
- [ ] No information loss in mapping - **Phase:** 2 - **Evidence:** Gap analysis shows zero data loss

### AC#5: Template Fits Within 500-Line Limit

- [ ] Template populated agent example ≤ 500 lines - **Phase:** 2 - **Evidence:** wc -l on populated example
- [ ] Template populated agent example ≥ 100 lines - **Phase:** 2 - **Evidence:** wc -l on populated example

### AC#6: Consistent Frontmatter Naming Convention

- [ ] Underscore convention documented - **Phase:** 2 - **Evidence:** Grep for naming convention section
- [ ] Migration mapping table present with 5+ entries - **Phase:** 2 - **Evidence:** Grep for migration table

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Canonical agent template document created at src/claude/agents/agent-generator/references/canonical-agent-template.md
- [x] All 10 required sections fully specified with purpose, format, and minimum content
- [x] All 4 agent categories defined with 3 optional sections each
- [x] YAML frontmatter schema with field-level validation rules documented
- [x] Gap analysis appendix for test-automator, code-reviewer, security-auditor included
- [x] Migration checklist with step-by-step instructions included
- [x] Migration mapping table for known frontmatter variants included

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (minimal agent, multi-category, progressive disclosure, legacy variants, extension sections, description length)
- [x] Template populated agent fits within 100-500 line range
- [x] Template reference document itself is < 800 lines (actual: 594 lines)
- [x] Code coverage > 95% for validation rules (bash test scripts)

### Testing
- [x] Unit tests for required section presence validation
- [x] Unit tests for frontmatter schema validation
- [x] Unit tests for category section definitions
- [x] Integration tests for gap analysis against 3 diverse agents
- [x] Integration tests for migration mapping

### Documentation
- [x] Template document is self-documenting (includes usage instructions)
- [x] Category decision table provides clear agent-to-category mapping
- [x] Migration checklist enables 10-20 minute conversion per agent

---

## Implementation Notes

- [x] Canonical agent template document created at src/claude/agents/agent-generator/references/canonical-agent-template.md - Completed: 2026-02-11 (594 lines)
- [x] All 10 required sections fully specified with purpose, format, and minimum content - Completed: 2026-02-11
- [x] All 4 agent categories defined with 3 optional sections each - Completed: 2026-02-11 (Validator, Implementor, Analyzer, Formatter)
- [x] YAML frontmatter schema with field-level validation rules documented - Completed: 2026-02-11 (9 fields)
- [x] Gap analysis appendix for test-automator, code-reviewer, security-auditor included - Completed: 2026-02-11
- [x] Migration checklist with step-by-step instructions included - Completed: 2026-02-11
- [x] Migration mapping table for known frontmatter variants included - Completed: 2026-02-11 (9 entries)
- [x] All 6 acceptance criteria have passing tests - Completed: 2026-02-11 (tests/STORY-386/*.sh)
- [x] Edge cases covered (minimal agent, multi-category, progressive disclosure, legacy variants, extension sections, description length) - Completed: 2026-02-11
- [x] Template populated agent fits within 100-500 line range - Completed: 2026-02-11
- [x] Template reference document itself is < 800 lines - Completed: 2026-02-11 (594 lines)
- [x] Code coverage > 95% for validation rules - Completed: 2026-02-11 (bash test scripts)
- [x] Unit tests for required section presence validation - Completed: 2026-02-11
- [x] Unit tests for frontmatter schema validation - Completed: 2026-02-11
- [x] Unit tests for category section definitions - Completed: 2026-02-11
- [x] Integration tests for gap analysis against 3 diverse agents - Completed: 2026-02-11
- [x] Integration tests for migration mapping - Completed: 2026-02-11
- [x] Template document is self-documenting (includes usage instructions) - Completed: 2026-02-11
- [x] Category decision table provides clear agent-to-category mapping - Completed: 2026-02-11
- [x] Migration checklist enables 10-20 minute conversion per agent - Completed: 2026-02-11

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-11

### TDD Workflow Summary

| Phase | Status | Key Evidence |
|-------|--------|--------------|
| Phase 01: Pre-Flight | ✓ Complete | git-validator, tech-stack-detector invoked |
| Phase 02: Test-First (Red) | ✓ Complete | 6 failing test scripts created |
| Phase 03: Implementation (Green) | ✓ Complete | Template created, all tests pass |
| Phase 04: Refactoring | ✓ Complete | Document improved (601→594 lines) |
| Phase 04.5: AC Verification | ✓ Complete | All 6 ACs verified |
| Phase 05: Integration | ✓ Complete | Cross-component validation passed |
| Phase 05.5: AC Verification | ✓ Complete | Post-integration verification passed |
| Phase 06: Deferral | ✓ Complete | No deferrals required |
| Phase 07: DoD Update | ✓ Complete | DoD marked complete |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-06 10:00 | claude/story-requirements-analyst | Created | Story created from EPIC-061 Feature 1 | STORY-386-design-canonical-agent-template.story.md |
| 2026-02-11 14:40 | .claude/qa-result-interpreter | QA Deep | PASSED: 6/6 ACs verified, 0 violations, DoD 100% | STORY-386-qa-report.md |

## Notes

**Design Decisions:**
- Template stored as reference file under agent-generator (not as standalone agent) because it's a specification document, not an executable agent
- 4 categories chosen based on observed agent function patterns across existing 32+ agents
- Underscore convention chosen over kebab-case for frontmatter field names to match existing majority pattern (proactive_triggers already uses underscores)
- 500-line limit from source-tree.md applies to agent files, not to the template reference document

**Open Questions:**
- [X] Exact prompt engineering patterns from EPIC-060 — available when research artifact completes - **Owner:** Framework Owner: Yes (Deferral not approved)
- [X] Whether `version` field should be required or optional — recommend optional initially - **Owner:** Framework Owner: No (Deferral not approved)

**Related ADRs:**
- None yet (template design may warrant ADR if significant deviation from current patterns)

**References:**
- EPIC-061: Unified Template Standardization & Enforcement
- BRAINSTORM-010: Prompt Engineering from Anthropic Repos
- source-tree.md line ~601: Agent file size constraints

---

Story Template Version: 2.8
Last Updated: 2026-02-06
