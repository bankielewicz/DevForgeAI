---
id: STORY-439
title: Update Command Routing for Skill Restructure
type: refactor
epic: EPIC-068
sprint: Sprint-3
status: QA Approved
points: 3
depends_on: ["STORY-436", "STORY-437"]
priority: High
advisory: false
assigned_to: Unassigned
created: 2026-02-17
format_version: "2.9"
---

# Story: Update Command Routing for Skill Restructure

## Description

**As a** DevForgeAI framework user,
**I want** the `/create-epic` command to invoke the architecture skill (not orchestration) and the `/ideate` command to output requirements.md (not epic.md),
**so that** commands follow the new clean responsibility chain: `/ideate` → requirements.md → `/create-epic` → epic.md (via architecture skill).

**Business Context:**
After STORY-436 (F5) adds epic creation to architecture skill and STORY-437 (F6) removes it from orchestration skill, the commands must be re-routed to invoke the correct skills. Currently `/create-epic` invokes `devforgeai-orchestration` for epic creation (Phase 4A), but Phase 4A no longer exists. This story updates command routing to invoke `designing-systems` for epic creation and updates `/ideate` to output requirements.md per the F4 schema. Additionally, the `skill-output-schemas.yaml` epic schema moves to architecture skill since architecture now owns epic creation.

## Provenance

```xml
<provenance>
  <origin document="EPIC-068" section="Feature 8">
    <quote>"Change `/create-epic` command from `Skill(command=\"devforgeai-orchestration\")` to invoke architecture skill directly; update `/ideate` command output to produce requirements.md not epic.md; move `skill-output-schemas.yaml` epic schema to architecture skill; update error handling references"</quote>
    <line_reference>lines 157-161</line_reference>
    <quantified_impact>Two command files updated; schema file relocated; command chain becomes: /ideate → requirements.md → /create-epic → epic.md</quantified_impact>
  </origin>

  <decision rationale="clean-command-chain">
    <selected>Route /create-epic to architecture skill; /ideate outputs requirements.md</selected>
    <rejected alternative="keep-orchestration-routing">
      Orchestration's Phase 4A no longer exists (removed in F6); architecture skill now owns epic creation (added in F5)
    </rejected>
    <trade_off>Users expecting /ideate to produce epics directly must now invoke /create-epic separately; cleaner separation of concerns</trade_off>
  </decision>

  <stakeholder role="Framework User" goal="intuitive-command-chain">
    <quote>"Clean command chain: `/ideate` → requirements.md → `/create-epic` → epic.md (via architecture skill)"</quote>
    <source>EPIC-068, Feature 8 User Value</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Uses XML format for machine-parseable verification.

### AC#1: /create-epic Command Routes to Architecture Skill

```xml
<acceptance_criteria id="AC1" implements="ROUTING-001">
  <given>The create-epic.md command currently contains `Skill(command="devforgeai-orchestration")` at line 133 and references orchestration's Phase 4A epic creation workflow</given>
  <when>Command routing is updated to invoke architecture skill</when>
  <then>
    (a) create-epic.md contains `Skill(command="designing-systems")` instead of `devforgeai-orchestration`;
    (b) Context marker `**Mode:** epic-creation` is set to trigger architecture's Phase 6;
    (c) Phase documentation references architecture skill's 8-phase epic creation workflow (not orchestration's Phase 4A);
    (d) Reference file paths point to architecture skill, not orchestration;
    (e) Subagent invocation documentation matches architecture skill's subagent coordination
  </then>
  <verification>
    <source_files>
      <file hint="Create-epic command (src)">src/claude/commands/create-epic.md</file>
    </source_files>
    <test_file>tests/STORY-439/test_ac1_create_epic_routing.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: /ideate Command Output Changed to requirements.md

```xml
<acceptance_criteria id="AC2" implements="OUTPUT-001">
  <given>The ideate.md command currently describes output as "Epic documents, requirements specification, complexity assessment" (line 12) with epic as primary output</given>
  <when>Command output documentation is updated</when>
  <then>
    (a) ideate.md description shows requirements.md as primary output;
    (b) Output section describes YAML-structured requirements.md per F4 schema;
    (c) Completion guidance recommends `/create-epic` as next step for epic generation;
    (d) No references to "epic documents" as direct ideation output;
    (e) References to ideation skill output match STORY-438 (F7) changes
  </then>
  <verification>
    <source_files>
      <file hint="Ideate command (src)">src/claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-439/test_ac2_ideate_output.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: skill-output-schemas.yaml Epic Schema Relocated

```xml
<acceptance_criteria id="AC3" implements="SCHEMA-001">
  <given>The skill-output-schemas.yaml file exists in orchestration skill at `.claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml` and contains the epic output schema</given>
  <when>Epic schema is moved to architecture skill</when>
  <then>
    (a) Epic schema section exists in architecture skill's schema file: `.claude/skills/designing-systems/references/skill-output-schemas.yaml`;
    (b) Orchestration's schema file retains non-epic schemas (story lifecycle, sprint planning);
    (c) create-epic.md Phase 0.5 schema validation references architecture skill path;
    (d) Ideation skill's completion handoff references architecture skill for epic schema validation
  </then>
  <verification>
    <source_files>
      <file hint="Architecture skill schema (src)">src/claude/skills/designing-systems/references/skill-output-schemas.yaml</file>
      <file hint="Orchestration skill schema (src)">src/claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml</file>
    </source_files>
    <test_file>tests/STORY-439/test_ac3_schema_relocation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Error Handling References Updated

```xml
<acceptance_criteria id="AC4" implements="ERROR-001">
  <given>Error handling in create-epic.md references orchestration skill error handling files and Phase 4A error patterns</given>
  <when>Error handling references are updated</when>
  <then>
    (a) Error handling documentation references architecture skill error handling;
    (b) Phase 4A error references removed (Phase 4A no longer exists);
    (c) Schema validation failure messages reference architecture skill;
    (d) Recovery instructions point to architecture skill documentation
  </then>
  <verification>
    <source_files>
      <file hint="Create-epic command (src)">src/claude/commands/create-epic.md</file>
    </source_files>
    <test_file>tests/STORY-439/test_ac4_error_handling.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Dual-Path Sync (src/ and .claude/)

```xml
<acceptance_criteria id="AC5" implements="SYNC-001">
  <given>DevForgeAI uses dual-path architecture with src/ (installer source) and .claude/ (operational) trees</given>
  <when>All changes are applied</when>
  <then>
    (a) src/claude/commands/create-epic.md matches .claude/commands/create-epic.md;
    (b) src/claude/commands/ideate.md matches .claude/commands/ideate.md;
    (c) Schema file changes applied to both src/ and operational paths;
    (d) No path mismatches between source and operational trees
  </then>
  <verification>
    <source_files>
      <file hint="Create-epic command (operational)">./claude/commands/create-epic.md</file>
      <file hint="Ideate command (operational)">./claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-439/test_ac5_dual_path_sync.py</test_file>
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
      name: "create-epic-command-update"
      file_path: "src/claude/commands/create-epic.md"
      requirements:
        - id: "CMD-001"
          description: "Change Skill invocation from devforgeai-orchestration to designing-systems"
          testable: true
          test_requirement: "Test: Grep for 'designing-systems' in Skill() call"
          priority: "Critical"
        - id: "CMD-002"
          description: "Add Mode context marker for epic-creation to trigger architecture Phase 6"
          testable: true
          test_requirement: "Test: Command sets **Mode:** epic-creation context marker"
          priority: "Critical"
        - id: "CMD-003"
          description: "Update Phase 2 documentation to reference architecture skill workflow"
          testable: true
          test_requirement: "Test: No references to orchestration Phase 4A"
          priority: "High"
        - id: "CMD-004"
          description: "Update reference file paths from orchestration to architecture"
          testable: true
          test_requirement: "Test: All skill references point to designing-systems"
          priority: "High"
        - id: "CMD-005"
          description: "Update Phase 0.5 schema validation path to architecture skill"
          testable: true
          test_requirement: "Test: Schema path is designing-systems/references/skill-output-schemas.yaml"
          priority: "High"

    - type: "Configuration"
      name: "ideate-command-update"
      file_path: "src/claude/commands/ideate.md"
      requirements:
        - id: "IDE-001"
          description: "Update description to show requirements.md as primary output"
          testable: true
          test_requirement: "Test: Description mentions requirements.md, not epic.md as primary output"
          priority: "Critical"
        - id: "IDE-002"
          description: "Update Output section to describe YAML requirements format"
          testable: true
          test_requirement: "Test: Output section references F4 schema for requirements.md"
          priority: "High"
        - id: "IDE-003"
          description: "Add next-step recommendation for /create-epic"
          testable: true
          test_requirement: "Test: Completion guidance recommends /create-epic for epic generation"
          priority: "High"
        - id: "IDE-004"
          description: "Remove epic.md as direct output reference"
          testable: true
          test_requirement: "Test: No 'epic documents' as direct ideation output"
          priority: "High"

    - type: "Configuration"
      name: "schema-relocation"
      file_path: "src/claude/skills/designing-systems/references/skill-output-schemas.yaml"
      requirements:
        - id: "SCH-001"
          description: "Copy epic schema section from orchestration to architecture"
          testable: true
          test_requirement: "Test: Epic schema exists in architecture skill schema file"
          priority: "Critical"
        - id: "SCH-002"
          description: "Retain non-epic schemas in orchestration (story lifecycle, sprint planning)"
          testable: true
          test_requirement: "Test: Orchestration schema still contains story and sprint schemas"
          priority: "High"
        - id: "SCH-003"
          description: "Create architecture schema file if it doesn't exist"
          testable: true
          test_requirement: "Test: Architecture skill has skill-output-schemas.yaml file"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      description: "Command chain is now: /ideate → requirements.md → /create-epic → epic.md"
      test_requirement: "Test: /ideate outputs requirements.md; /create-epic outputs epic.md"

    - id: "BR-002"
      description: "Architecture skill owns epic creation; orchestration no longer involved"
      test_requirement: "Test: No /create-epic → orchestration routing"

    - id: "BR-003"
      description: "Dual-path sync: all changes in src/ must be mirrored to .claude/"
      test_requirement: "Test: File diff between src/ and .claude/ paths shows no differences"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Consistency"
      description: "Command routing matches skill responsibility after restructure"
      metric: "Routing correctness"
      target: "100% correct routing (no orchestration for epic creation)"
      measurement: "Manual verification of Skill() calls"

    - id: "NFR-002"
      category: "Usability"
      description: "Clear command chain documented for users"
      metric: "Documentation clarity"
      target: "Next-step recommendations in both commands"
      measurement: "Presence of next-step guidance"
```

## Technical Limitations

1. **Schema file may need creation** — Architecture skill may not have a skill-output-schemas.yaml file yet. If missing, create it with the epic schema section copied from orchestration.

2. **Partial schema retention** — Orchestration's schema file retains non-epic schemas (story lifecycle, sprint planning schemas). Only epic schema moves to architecture.

3. **F7 dependency for ideate output** — The ideate command output change (requirements.md) aligns with STORY-438 (F7) which updates ideation skill output. This story updates the command documentation to match.

4. **Dual-path architecture** — All changes must be applied to both `src/claude/commands/` (source) and `.claude/commands/` (operational) trees.

## Non-Functional Requirements

### Consistency
- Command routing matches skill responsibility boundaries after restructure
- No orphaned routes to removed phases (orchestration Phase 4A)

### Usability
- Clear next-step guidance in both /ideate and /create-epic commands
- Command chain documented: `/ideate` → requirements.md → `/create-epic` → epic.md

### Documentation
- All command documentation reflects new routing
- Schema validation paths reference correct skill locations

## Dependencies

### Prerequisite Stories
- **STORY-436 (F5):** Add Epic Creation Phases to Architecture SKILL.md — architecture must have epic creation capability before /create-epic routes to it
- **STORY-437 (F6):** Remove Phase 4A from Orchestration SKILL.md — orchestration's Phase 4A must be removed (otherwise duplicate epic creation exists)

### Parallel Stories
- **STORY-438 (F7):** Slim Ideation SKILL.md — ideation skill output changes to requirements.md; this story updates /ideate command to match

### Successor Stories
- **Feature 9 (STORY-TBD):** Rename Architecture Skill — after routing is correct, architecture skill may be renamed per ADR-017

## Test Strategy

### Unit Tests
| Test File | Purpose | Coverage Target |
|-----------|---------|-----------------|
| `tests/STORY-439/test_ac1_create_epic_routing.py` | Verify Skill() invokes designing-systems | 95% |
| `tests/STORY-439/test_ac2_ideate_output.py` | Verify requirements.md as primary output | 95% |
| `tests/STORY-439/test_ac3_schema_relocation.py` | Verify epic schema in architecture skill | 95% |
| `tests/STORY-439/test_ac4_error_handling.py` | Verify error references updated | 95% |
| `tests/STORY-439/test_ac5_dual_path_sync.py` | Verify src/ and .claude/ match | 95% |

### Test Patterns
- Grep for skill invocation patterns in command files
- Parse command files for output documentation
- Verify schema file existence and content
- File diff between src/ and operational paths

### Edge Cases
- Schema file may not exist in architecture skill (create if missing)
- Orchestration schema file should retain non-epic schemas (not delete entire file)

## Acceptance Criteria Verification Checklist

### AC#1: /create-epic Command Routes to Architecture Skill
- [x] `Skill(command="designing-systems")` in create-epic.md
- [x] `**Mode:** epic-creation` context marker set
- [x] Phase 2 references architecture skill workflow
- [x] Reference paths point to designing-systems
- [x] Schema validation path updated

### AC#2: /ideate Command Output Changed to requirements.md
- [x] Description shows requirements.md as primary output
- [x] Output section describes YAML requirements format
- [x] Next-step recommends /create-epic
- [x] No "epic documents" as direct output

### AC#3: skill-output-schemas.yaml Epic Schema Relocated
- [x] Epic schema in architecture skill schema file
- [x] Orchestration retains non-epic schemas
- [x] create-epic.md references architecture schema path
- [x] Ideation references architecture for epic schema

### AC#4: Error Handling References Updated
- [x] Error handling references architecture skill
- [x] No Phase 4A error references
- [x] Schema failure messages updated
- [x] Recovery instructions point to architecture docs

### AC#5: Dual-Path Sync
- [x] create-epic.md in sync (src/ and .claude/)
- [x] ideate.md in sync (src/ and .claude/)
- [x] Schema files in sync
- [x] No path mismatches

## Definition of Done

### Implementation Checklist
- [x] All 5 acceptance criteria implemented
- [x] Changes applied to src/ tree (source)
- [x] Changes applied to .claude/ tree (operational)
- [x] All tests pass (21 passed)
- [x] Coverage meets 95% threshold (N/A - documentation/config files, not executable code)

### Quality Checklist
- [x] No new anti-patterns introduced
- [x] Code follows coding-standards.md
- [x] Command routing verified correct

### Testing Checklist
- [x] Unit tests written for all 5 ACs - tests/STORY-439/ (21 tests)
- [x] Edge cases covered (schema creation, partial retention)
- [x] Dual-path sync verified
- [x] Integration tests passed (21/21)

### Documentation Checklist
- [x] Story file complete with all sections
- [x] Technical limitations documented
- [x] Command chain documented

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] All 5 acceptance criteria implemented - Completed: AC#1-5 verified via ac-compliance-verifier
- [x] Changes applied to src/ tree (source) - Completed: create-epic.md, ideate.md, schema files updated
- [x] Changes applied to .claude/ tree (operational) - Completed: All files synced to operational paths
- [x] All tests pass (21 passed) - Completed: pytest tests/STORY-439/ all GREEN
- [x] Coverage meets 95% threshold (N/A - documentation/config files, not executable code) - Completed: Not applicable
- [x] No new anti-patterns introduced - Completed: code-reviewer verified
- [x] Code follows coding-standards.md - Completed: context-validator verified
- [x] Command routing verified correct - Completed: /create-epic → architecture, /ideate → requirements.md
- [x] Unit tests written for all 5 ACs - Completed: 21 tests in tests/STORY-439/
- [x] Edge cases covered (schema creation, partial retention) - Completed: Tests verify both
- [x] Dual-path sync verified - Completed: src/ and .claude/ paths match
- [x] Integration tests passed (21/21) - Completed: integration-tester verified
- [x] Story file complete with all sections - Completed: All sections present
- [x] Technical limitations documented - Completed: Lines 292-298
- [x] Command chain documented - Completed: /ideate → requirements.md → /create-epic → epic.md

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 01 | Complete | Pre-flight validation, git-validator, tech-stack-detector |
| Phase 02 | Complete | Test-first (RED) - 21 tests, 16 failed initially |
| Phase 03 | Complete | Implementation (GREEN) - backend-architect, context-validator |
| Phase 04 | Complete | Refactoring - refactoring-specialist, code-reviewer |
| Phase 4.5 | Complete | AC verification - ac-compliance-verifier (5/5 PASS) |
| Phase 05 | Complete | Integration testing - integration-tester (21/21 PASS) |
| Phase 5.5 | Complete | Post-integration AC verification (5/5 PASS) |
| Phase 06 | Complete | Deferral challenge - No deferrals |
| Phase 07 | Complete | DoD update |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/commands/create-epic.md | Modified | 444 |
| src/claude/commands/ideate.md | Modified | 569 |
| src/claude/skills/designing-systems/references/skill-output-schemas.yaml | Created | 66 |
| src/claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml | Modified | 112 |
| .claude/commands/create-epic.md | Synced | 444 |
| .claude/commands/ideate.md | Synced | 569 |
| .claude/skills/designing-systems/references/skill-output-schemas.yaml | Created | 66 |
| .claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml | Synced | 112 |
| tests/STORY-439/*.py | Created | ~300 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 | devforgeai-story-creation | Story Creation | Initial story created from EPIC-068 Feature 8 | STORY-439-update-command-routing-for-skill-restructure.story.md |
| 2026-02-18 | .claude/qa-result-interpreter | QA Deep | PASSED: 21/21 tests, 2/2 validators, 0 blocking violations | - |

## Notes

### Design Decisions
1. **Schema partial migration** — Only epic schema moves to architecture; orchestration retains story lifecycle and sprint planning schemas since those remain orchestration's responsibility.

2. **Mode context marker** — Adding `**Mode:** epic-creation` context marker ensures architecture skill knows to execute Phase 6 (epic creation) rather than other phases.

3. **Next-step guidance** — Both commands will have explicit next-step recommendations to guide users through the new command chain.

4. **Dual-path sync** — All changes must be applied to both src/ and .claude/ paths to maintain consistency between installer source and operational files.

### Open Questions
None — all technical details verified via file reads during story creation.

### Related ADRs
- ADR-017: Skill Rename Convention (gerund naming)
- EPIC-068: Skill Responsibility Restructure & Rename Migration

### References
- EPIC-068 lines 157-161 (Feature 8 specification)
- EPIC-068 line 287 (F8 dependencies: F5, F6)
- STORY-436 (F5): Add Epic Creation Phases to Architecture SKILL.md
- STORY-437 (F6): Remove Phase 4A from Orchestration SKILL.md
- STORY-438 (F7): Slim Ideation SKILL.md (parallel - ideation output changes)
