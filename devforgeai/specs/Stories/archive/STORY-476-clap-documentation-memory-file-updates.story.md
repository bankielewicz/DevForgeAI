---
id: STORY-476
title: CLAP Documentation and Memory File Updates
type: documentation
epic: EPIC-081
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-473", "STORY-474", "STORY-475"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: CLAP Documentation and Memory File Updates

## Description

**As a** DevForgeAI framework developer,
**I want** the alignment-auditor subagent, /audit-alignment command, and designing-systems Phase 5.5 documented in the memory reference files and CLAUDE.md subagent registry,
**so that** CLAP components are discoverable through standard lookup mechanisms and new sessions can find, invoke, and understand these artifacts without prior context.

## Provenance

```xml
<provenance>
  <origin document="ENH-CLAP-001" section="solution-overview">
    <quote>"Memory file updates — commands-reference, subagents-reference, and skills-reference updated so /audit-alignment, alignment-auditor, and Phase 5.5 are discoverable"</quote>
    <line_reference>requirements spec FR-007, lines 400-416</line_reference>
    <quantified_impact>3 memory files + CLAUDE.md registry updated for full CLAP discoverability</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: commands-reference.md Updated with /audit-alignment

```xml
<acceptance_criteria id="AC1">
  <given>The file .claude/memory/commands-reference.md exists with a Framework Maintenance section</given>
  <when>STORY-476 edits are applied</when>
  <then>Framework Maintenance section contains /audit-alignment entry with purpose, invokes (alignment-auditor), workflow overview, example usage (2+ examples), output format, and related commands. Command counts updated (+1) in all locations (quick_index, overview, command_overview)</then>
  <verification>
    <source_files>
      <file hint="Commands reference">.claude/memory/commands-reference.md</file>
    </source_files>
    <test_file>tests/STORY-476/test_ac1_commands_reference.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: subagents-reference.md Updated with alignment-auditor

```xml
<acceptance_criteria id="AC2">
  <given>The file .claude/memory/subagents-reference.md exists with a subagents catalog</given>
  <when>STORY-476 edits are applied</when>
  <then>Available Subagents table contains alignment-auditor row in alphabetical order (between agent-generator and anti-pattern-scanner) with name, purpose, model (haiku), tools. Proactive trigger mapping entry added. Subagent counts updated (+1) in all locations</then>
  <verification>
    <source_files>
      <file hint="Subagents reference">.claude/memory/subagents-reference.md</file>
    </source_files>
    <test_file>tests/STORY-476/test_ac2_subagents_reference.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: skills-reference.md Updated with Phase 5.5

```xml
<acceptance_criteria id="AC3">
  <given>The file .claude/memory/skills-reference.md has a designing-systems entry</given>
  <when>STORY-476 edits are applied</when>
  <then>designing-systems phase count updated to reflect Phase 5.5, Phase 5.5 listed between Phase 5 and Phase 6 with description, reference files list includes prompt-alignment-workflow.md, subagent integration section mentions alignment-auditor for Phase 5.5</then>
  <verification>
    <source_files>
      <file hint="Skills reference">.claude/memory/skills-reference.md</file>
    </source_files>
    <test_file>tests/STORY-476/test_ac3_skills_reference.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: CLAUDE.md Subagent Registry Updated

```xml
<acceptance_criteria id="AC4">
  <given>CLAUDE.md contains a subagent registry block (BEGIN/END SUBAGENT REGISTRY comments)</given>
  <when>STORY-476 updates are applied</when>
  <then>Registry table contains alignment-auditor row in alphabetical order with Description and Tools ([Read, Glob, Grep]). Proactive Trigger Mapping table contains alignment-auditor entry. Registry update mechanism documented (auto-generation script or manual edit)</then>
  <verification>
    <source_files>
      <file hint="CLAUDE.md registry">CLAUDE.md</file>
    </source_files>
    <test_file>tests/STORY-476/test_ac4_claudemd_registry.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree. Memory files are modified in src/claude/memory/ and synced to .claude/memory/ operational folders. CLAUDE.md at project root is single-path (no src/ equivalent for root CLAUDE.md edits)."
    source_paths:
      - "src/claude/memory/commands-reference.md"
      - "src/claude/memory/subagents-reference.md"
      - "src/claude/memory/skills-reference.md"
    operational_paths:
      - ".claude/memory/commands-reference.md"
      - ".claude/memory/subagents-reference.md"
      - ".claude/memory/skills-reference.md"
    single_path:
      - "CLAUDE.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "commands-reference-update"
      file_path: "src/claude/memory/commands-reference.md"
      required_keys:
        - key: "/audit-alignment entry"
          type: "string"
          required: true
          validation: "Entry present in Framework Maintenance section"
          test_requirement: "Test: Grep for '/audit-alignment' in commands-reference.md"
        - key: "command_count"
          type: "integer"
          required: true
          validation: "Count incremented by 1 in all locations"
          test_requirement: "Test: Verify command count consistency across 3 locations"

    - type: "Configuration"
      name: "subagents-reference-update"
      file_path: "src/claude/memory/subagents-reference.md"
      required_keys:
        - key: "alignment-auditor entry"
          type: "string"
          required: true
          validation: "Entry in alphabetical order with model: haiku"
          test_requirement: "Test: Grep for 'alignment-auditor' in catalog table"
        - key: "subagent_count"
          type: "integer"
          required: true
          validation: "Count incremented by 1 in all locations"
          test_requirement: "Test: Verify subagent count consistency"

    - type: "Configuration"
      name: "skills-reference-update"
      file_path: "src/claude/memory/skills-reference.md"
      required_keys:
        - key: "Phase 5.5 entry"
          type: "string"
          required: true
          validation: "Phase 5.5 listed in designing-systems entry"
          test_requirement: "Test: Grep for 'Phase 5.5' in designing-systems section"

    - type: "Configuration"
      name: "claudemd-registry-update"
      file_path: "CLAUDE.md"
      required_keys:
        - key: "alignment-auditor registry entry"
          type: "string"
          required: true
          validation: "Entry in registry between agent-generator and anti-pattern-scanner"
          test_requirement: "Test: Grep for 'alignment-auditor' in SUBAGENT REGISTRY block"

  business_rules:
    - id: "BR-001"
      rule: "All count references must be updated atomically (no partial count updates)"
      trigger: "When adding entries to reference files"
      validation: "Grep for old count returns 0 matches in count-specific locations"
      error_handling: "Verify all count locations before marking complete"
      test_requirement: "Test: Old count value absent from all count locations"
      priority: "High"
    - id: "BR-002"
      rule: "All prerequisite artifacts must exist before documentation references them"
      trigger: "Before starting implementation"
      validation: "STORY-473, STORY-474, STORY-475 in Dev Complete or later status"
      error_handling: "HALT if prerequisites not complete"
      test_requirement: "Test: Verify referenced files exist on disk"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "All 4 files remain valid markdown after edits"
      metric: "0 broken tables or formatting"
      test_requirement: "Test: Markdown lint on all 4 files post-edit"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- All 4 file edits: < 30 minutes total
- No file exceeds 200KB after edits
- Grep searches for "alignment-auditor" return within 2 seconds

### Security
- No secrets or credentials in documentation
- Documentation-only changes (no executable code)

### Reliability
- All 4 files valid markdown after edits
- Pre-commit validation passes on first attempt
- Independent file edits (one failure doesn't block others)

### Scalability
- Patterns consistent with existing conventions for future additions
- Count update locations documented for future reference

## Dependencies

### Prerequisite Stories
- [ ] **STORY-473:** alignment-auditor Subagent — documented in subagents-reference and CLAUDE.md
  - **Status:** Backlog
- [ ] **STORY-474:** /audit-alignment Command — documented in commands-reference
  - **Status:** Backlog
- [ ] **STORY-475:** Phase 5.5 Integration — documented in skills-reference
  - **Status:** Backlog

### Technology Dependencies
- None

## Test Strategy

### Unit Tests
**Coverage Target:** N/A (documentation story)

**Test Scenarios:**
1. **Happy Path:** All 4 files updated, counts correct, entries in alphabetical order
2. **Edge Cases:**
   - Auto-generation script vs manual edit for CLAUDE.md registry
   - Prerequisite artifacts don't exist yet
   - Count arithmetic across multiple sections
   - Alphabetical insertion position verification

## Acceptance Criteria Verification Checklist

### AC#1: commands-reference.md
- [x] /audit-alignment entry in Framework Maintenance - **Phase:** 3
- [x] Command count updated in all 3 locations - **Phase:** 3

### AC#2: subagents-reference.md
- [x] alignment-auditor in catalog (alphabetical) - **Phase:** 3
- [x] Proactive trigger mapping entry added - **Phase:** 3
- [x] Subagent count updated in all locations - **Phase:** 3

### AC#3: skills-reference.md
- [x] Phase 5.5 in designing-systems entry - **Phase:** 3
- [x] prompt-alignment-workflow.md in references list - **Phase:** 3

### AC#4: CLAUDE.md Registry
- [x] alignment-auditor in Subagent Registry table - **Phase:** 3
- [x] alignment-auditor in Proactive Trigger Mapping - **Phase:** 3

**Checklist Progress:** 9/9 items complete (100%)

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Definition of Done

### Implementation
- [x] commands-reference.md updated with /audit-alignment entry and count
- [x] subagents-reference.md updated with alignment-auditor entry and count
- [x] skills-reference.md updated with Phase 5.5 and reference file
- [x] CLAUDE.md subagent registry updated with alignment-auditor
- [x] All counts consistent across multiple locations per file

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] All referenced artifacts verified to exist on disk
- [x] No broken markdown formatting

### Testing
- [x] Grep tests for new entries pass
- [x] Count consistency tests pass
- [x] Alphabetical ordering verified

### Dual-Path Sync
- [x] Memory files modified in src/claude/memory/ (source of truth)
- [x] Memory files synced to .claude/memory/ (operational)
- [x] CLAUDE.md edited at project root (single-path, no src/ equivalent)
- [x] Tests run against src/ tree

### Documentation
- [x] Registry update mechanism documented in Implementation Notes

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | Complete | 25 failing tests across 4 AC test files |
| Green | Complete | All 4 files edited, 25/25 tests pass |
| Refactor | Complete | Minor formatting fix, code review passed |
| Integration | Complete | Cross-file consistency verified |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/memory/commands-reference.md | Modified | +35 (audit-alignment entry, count updates) |
| src/claude/memory/subagents-reference.md | Modified | +12 (alignment-auditor entry, triggers, count) |
| src/claude/memory/skills-reference.md | Modified | +5 (Phase 5.5, reference file, alignment note) |
| CLAUDE.md | Modified | +4 (registry row, 3 trigger entries) |
| tests/STORY-476/test_ac1_commands_reference.sh | Created | 72 |
| tests/STORY-476/test_ac2_subagents_reference.sh | Created | 62 |
| tests/STORY-476/test_ac3_skills_reference.sh | Created | 50 |
| tests/STORY-476/test_ac4_claudemd_registry.sh | Created | 45 |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] commands-reference.md updated with /audit-alignment entry and count - Completed: Added full /audit-alignment command section with purpose, workflow, examples, output, related commands. Updated counts 39→40 in quick_index, overview, command_overview. Framework Maintenance category updated 8→9 commands.
- [x] subagents-reference.md updated with alignment-auditor entry and count - Completed: Added alignment-auditor row to catalog table between agent-generator and anti-pattern-scanner. Added Proactive Trigger Mapping section with 3 triggers. Updated counts 39→40 in 3 locations.
- [x] skills-reference.md updated with Phase 5.5 and reference file - Completed: Added Phase 5.5 to designing-systems workflow list. Added prompt-alignment-workflow.md to reference files. Added alignment-auditor note in key features.
- [x] CLAUDE.md subagent registry updated with alignment-auditor - Completed: Added alignment-auditor row between agent-generator and anti-pattern-scanner with description and tools [Read, Glob, Grep]. Added 3 proactive trigger entries.
- [x] All counts consistent across multiple locations per file - Completed: Verified 40 count appears in all expected locations.
- [x] All 4 acceptance criteria have passing tests - Completed: 25/25 assertions pass across 4 test files.
- [x] All referenced artifacts verified to exist on disk - Completed: alignment-auditor.md exists in .claude/agents/.
- [x] No broken markdown formatting - Completed: All tables valid, no broken formatting.
- [x] Grep tests for new entries pass - Completed: All grep-based tests pass.
- [x] Count consistency tests pass - Completed: 40 count verified in all locations.
- [x] Alphabetical ordering verified - Completed: alignment-auditor between agent-generator and anti-pattern-scanner in all files.
- [x] Memory files modified in src/claude/memory/ (source of truth) - Completed: All edits in src/ tree.
- [x] Memory files synced to .claude/memory/ (operational) - Completed: cp sync performed.
- [x] CLAUDE.md edited at project root (single-path, no src/ equivalent) - Completed: Direct edit to CLAUDE.md.
- [x] Tests run against src/ tree - Completed: All tests target src/claude/memory/.
- [x] Registry update mechanism documented in Implementation Notes - Completed: CLAUDE.md registry uses manual edit (comment says auto-generated but hybrid approach used). Registry rows added manually between BEGIN/END SUBAGENT REGISTRY markers.

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from EPIC-081 Feature 5 (batch 5/5) | STORY-476.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 25/25 tests, 0 violations, documentation story | - |

## Notes

**Design Decisions:**
- All 4 files updated as a single story because they are all documentation for the same deliverables
- Count updates must be atomic across all locations per file to prevent inconsistency
- CLAUDE.md registry mechanism to be determined during implementation

**Edge Cases Documented:**
1. Auto-generation vs manual edit for CLAUDE.md registry
2. Prerequisite artifacts may not exist yet
3. Count arithmetic across multiple sections
4. Alphabetical insertion position
5. Phase 5.5 fractional numbering convention

**References:**
- [Requirements Specification](devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md) (FR-007)
- [EPIC-081](devforgeai/specs/Epics/EPIC-081-configuration-layer-alignment-protocol.epic.md)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
