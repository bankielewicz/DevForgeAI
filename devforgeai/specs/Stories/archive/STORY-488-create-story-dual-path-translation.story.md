---
id: STORY-488
title: Create-Story Skill Dual-Path Translation Rule
type: feature
epic: null
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-487"]
priority: High
advisory: false
source_gap: null
source_story: null
source_rca: "RCA-039"
source_recommendation: "REC-3"
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: Create-Story Skill Dual-Path Translation Rule

## Description

**As a** developer running `/create-story`,
**I want** the story creation skill to automatically translate `.claude/` paths to `src/claude/` in technical specifications and add `dual_path_sync` blocks and DoD items,
**so that** newly created stories always reference the source-of-truth development path and include dual-path sync requirements, preventing the constitutional violation documented in RCA-039.

## Provenance

```xml
<provenance>
  <origin document="RCA-039" section="REC-3">
    <quote>"The story creation skill generates .claude/ paths in technical specifications because it reads source-tree.md's directory listings directly."</quote>
    <line_reference>RCA-039 lines 195-243</line_reference>
    <quantified_impact>Defense-in-depth: prevents issue at generation point (REC-1/2 catches at validation point)</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: .claude/ Paths Auto-Translated to src/claude/

```xml
<acceptance_criteria id="AC1">
  <given>a feature description requiring creation of .claude/agents/new-agent.md</given>
  <when>/create-story generates the technical specification</when>
  <then>the file_path value is "src/claude/agents/new-agent.md" (not ".claude/agents/new-agent.md")</then>
  <verification>
    <source_files>
      <file hint="tech spec creation reference">src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md</file>
    </source_files>
    <test_file>tests/STORY-488/test_ac1_path_translation.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: dual_path_sync Block Auto-Generated

```xml
<acceptance_criteria id="AC2">
  <given>a story being created that modifies files in .claude/ directories</given>
  <when>/create-story generates the technical specification</when>
  <then>a dual_path_sync YAML block is included with source_paths (src/claude/...), operational_paths (.claude/...), and test_against: "src/"</then>
  <verification>
    <source_files>
      <file hint="tech spec creation reference">src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md</file>
    </source_files>
    <test_file>tests/STORY-488/test_ac2_sync_block.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Dual-Path Sync DoD Section Auto-Added

```xml
<acceptance_criteria id="AC3">
  <given>a story being created that modifies files in .claude/ directories</given>
  <when>/create-story generates the Definition of Done</when>
  <then>a "### Dual-Path Sync" subsection is included with checkboxes: "Files created/modified in src/claude/", "Files synced to .claude/", "Tests run against src/ tree"</then>
  <verification>
    <source_files>
      <file hint="tech spec creation reference">src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md</file>
    </source_files>
    <test_file>tests/STORY-488/test_ac3_dod_section.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: Exempt Paths Not Translated

```xml
<acceptance_criteria id="AC4">
  <given>a story being created that modifies devforgeai/specs/adrs/ADR-021.md or CLAUDE.md or tests/ files</given>
  <when>/create-story generates the technical specification</when>
  <then>these paths are NOT prefixed with "src/" and no dual_path_sync block is added for them</then>
  <verification>
    <source_files>
      <file hint="tech spec creation reference">src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md</file>
    </source_files>
    <test_file>tests/STORY-488/test_ac4_exempt_paths.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree."
    source_paths:
      - "src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
    operational_paths:
      - ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "dual-path-translation-rule"
      file_path: "src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
      required_keys:
        - key: "Dual-Path Translation Rule section"
          type: "string"
          required: true
          validation: "Section exists with .claude/ → src/claude/ translation logic, exempt_prefixes list, and dual_path_sync template"
          test_requirement: "Test: Grep for 'Dual-Path Translation Rule' in file"

  business_rules:
    - id: "BR-001"
      rule: "Translation only applies when source-tree.md has Dual-Location Architecture section"
      trigger: "During file_path generation"
      validation: "Check source-tree.md before translating"
      error_handling: "Skip translation for greenfield projects"
      test_requirement: "Test: No translation when section missing"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Translation is idempotent — already-translated paths not double-prefixed"
      metric: "src/claude/ paths remain unchanged"
      test_requirement: "Test: Path already starting with src/claude/ not modified"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Reliability
- Idempotent translation (already src/ paths not double-prefixed)
- Greenfield projects without Dual-Location section skip translation

## Dependencies

### Prerequisite Stories
- [ ] **STORY-487:** Dual-Path Validation Function — validation must exist before generation fix
  - **Status:** Backlog

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Feature creating .claude/agents/x.md → generates src/claude/agents/x.md + dual_path_sync + DoD
2. **Edge Cases:** ADR path not translated; CLAUDE.md not translated; already src/ path not double-prefixed
3. **Error Cases:** No Dual-Location section → no translation

## Acceptance Criteria Verification Checklist

- [x] Path translation .claude/ → src/claude/ - **Phase:** 2
- [x] dual_path_sync block generated - **Phase:** 2
- [x] DoD section added - **Phase:** 2
- [x] Exempt paths not translated - **Phase:** 2

**Checklist Progress:** 4/4 items complete (100%)

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT -->

## Definition of Done

### Implementation
- [x] Dual-Path Translation Rule section added to technical-specification-creation.md
- [x] .claude/ → src/claude/ translation logic implemented
- [x] dual_path_sync YAML block template included
- [x] Dual-Path Sync DoD subsection template included
- [x] Exempt paths list documented (devforgeai/specs/*, CLAUDE.md, README.md, tests/*)

### Dual-Path Sync
- [x] File modified in src/claude/ (source of truth)
- [x] File synced to .claude/ (operational)
- [x] Tests run against src/ tree

### Quality
- [x] All 4 acceptance criteria have passing tests

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack detected |
| 02 Red | ✅ Complete | 16 tests generated, all failing (RED confirmed) |
| 03 Green | ✅ Complete | Dual-Path Translation Rule section added, 16/16 tests passing |
| 04 Refactor | ✅ Complete | refactoring-specialist + code-reviewer approved |
| 4.5 AC Verify | ✅ Complete | 4/4 ACs PASS with HIGH confidence |
| 05 Integration | ✅ Complete | File integrity verified, src/operational sync confirmed |
| 5.5 AC Verify | ✅ Complete | 4/4 ACs PASS post-integration |
| 06 Deferral | ✅ Complete | No deferrals |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md | Modified | +82 lines (Dual-Path Translation Rule section) |
| .claude/skills/devforgeai-story-creation/references/technical-specification-creation.md | Synced | Operational copy updated |
| tests/STORY-488/test_ac1_path_translation.sh | Created | 48 lines |
| tests/STORY-488/test_ac2_sync_block.sh | Created | 52 lines |
| tests/STORY-488/test_ac3_dod_section.sh | Created | 52 lines |
| tests/STORY-488/test_ac4_exempt_paths.sh | Created | 56 lines |
| tests/STORY-488/run_all_tests.sh | Created | Runner script |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] Dual-Path Translation Rule section added to technical-specification-creation.md - Completed: Added comprehensive section with path translation logic, exempt paths, dual_path_sync template, and DoD subsection
- [x] .claude/ → src/claude/ translation logic implemented - Completed: Pseudocode with idempotency guard and pre-condition check for Dual-Location Architecture
- [x] dual_path_sync YAML block template included - Completed: Template with source_paths, operational_paths, test_against keys
- [x] Dual-Path Sync DoD subsection template included - Completed: Markdown template with 3 checkboxes for src/claude/, .claude/ sync, and src/ testing
- [x] Exempt paths list documented (devforgeai/specs/*, CLAUDE.md, README.md, tests/*) - Completed: YAML exempt_prefixes list with 6 entries
- [x] File modified in src/claude/ (source of truth) - Completed: src/ tree is source of truth
- [x] File synced to .claude/ (operational) - Completed: cp command synced to operational
- [x] Tests run against src/ tree - Completed: All 16 tests target src/ tree
- [x] All 4 acceptance criteria have passing tests - Completed: 16/16 tests passing

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | /create-stories-from-rca | Created | Story created from RCA-039 REC-3 | STORY-488.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 16/16 tests, 0 violations, 3/3 validators | STORY-488-qa-report.md |

## Notes

**Design Decisions:**
- Depends on STORY-487 so validation exists as safety net even if generation fix has edge cases
- Exempt paths list matches validate_dual_path() exemptions for consistency

**References:**
- [RCA-039](devforgeai/RCA/RCA-039-dual-path-architecture-validation-gap.md) (REC-3)
- [source-tree.md §Dual-Location Architecture](devforgeai/specs/context/source-tree.md)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
