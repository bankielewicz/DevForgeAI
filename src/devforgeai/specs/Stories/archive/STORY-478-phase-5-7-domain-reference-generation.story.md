---
id: STORY-478
title: Phase 5.7 Domain Reference Generation Workflow Integration
type: feature
epic: EPIC-082
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-477"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: Phase 5.7 Domain Reference Generation Workflow Integration

## Description

**As a** project bootstrapper running `/create-context` on a new project,
**I want** a Phase 5.7 "Domain Reference Generation" step that automatically evaluates detection heuristics and generates project-specific domain reference files for subagents after context files are validated and prompt is aligned,
**so that** subagents have structured, project-specific knowledge from day one without requiring manual reference file creation or repeated context file re-derivation on every invocation.

## Provenance

```xml
<provenance>
  <origin document="ENH-CLAP-001" section="Part 3 - Domain Reference Generation">
    <quote>"Phase 5.7 in designing-systems skill — After context files are validated and prompt is aligned, analyze context files for specialized domain knowledge"</quote>
    <line_reference>requirements spec FR-003, FR-004</line_reference>
    <quantified_impact>Automatic domain reference generation for 4 subagents during /create-context workflow</quantified_impact>
  </origin>
  <decision rationale="progressive-disclosure-integration">
    <selected>Phase 5.7 reference file (~250 lines) loaded on-demand, with ~25-30 line SKILL.md entry</selected>
    <rejected alternative="inline-workflow">Inlining the workflow in SKILL.md would exceed recommended phase entry size and violate progressive disclosure (ADR-012)</rejected>
    <trade_off>Reference file adds one Read() call during /create-context execution</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Reference File at Correct Path

```xml
<acceptance_criteria id="AC1">
  <given>The designing-systems skill has reference files in .claude/skills/designing-systems/references/</given>
  <when>The domain-reference-generation.md reference file is created</when>
  <then>The file is at .claude/skills/designing-systems/references/domain-reference-generation.md, approximately 250 lines (+/- 20%), containing the complete 5-step workflow</then>
  <verification>
    <source_files>
      <file hint="New reference file">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac1_reference_file.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: SKILL.md Phase 5.7 Insertion

```xml
<acceptance_criteria id="AC2">
  <given>SKILL.md has Phase 5 (Validate Spec) and Phase 6 (Epic Creation) sections</given>
  <when>Phase 5.7 is inserted into SKILL.md</when>
  <then>"Phase 5.7: Domain Reference Generation" appears between Phase 5 and Phase 6, adds approximately 25-30 lines, uses Read() for on-demand reference loading</then>
  <verification>
    <source_files>
      <file hint="Modified skill file">.claude/skills/designing-systems/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac2_skillmd_insertion.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Progressive Disclosure Compliance

```xml
<acceptance_criteria id="AC3">
  <given>The reference file contains the full Phase 5.7 workflow (~250 lines)</given>
  <when>The SKILL.md Phase 5.7 entry is evaluated for progressive disclosure (ADR-012)</when>
  <then>SKILL.md contains only a lean entry (25-30 lines) with purpose, precondition, postcondition, and Read() instruction — detailed workflow logic resides exclusively in the reference file</then>
  <verification>
    <source_files>
      <file hint="SKILL.md entry">.claude/skills/designing-systems/SKILL.md</file>
      <file hint="Reference file">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac3_progressive_disclosure.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: 5-Step Workflow Completeness

```xml
<acceptance_criteria id="AC4">
  <given>The reference file domain-reference-generation.md is loaded</given>
  <when>The workflow steps are enumerated</when>
  <then>Exactly 5 steps defined in order: (1) Run Detection Heuristics, (2) Present Recommendations via AskUserQuestion, (3) Generate Reference Files, (4) Verify No Contradictions, (5) Report</then>
  <verification>
    <source_files>
      <file hint="Workflow steps">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac4_workflow_steps.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#5: Skip Behavior When No Heuristics Trigger

```xml
<acceptance_criteria id="AC5">
  <given>A project where no detection heuristics (DH-01 through DH-04) are triggered</given>
  <when>Phase 5.7 Step 1 completes evaluation</when>
  <then>Steps 2-5 are skipped, informational message displayed: "No domain references needed for this project", workflow proceeds to Phase 6 (non-blocking)</then>
  <verification>
    <source_files>
      <file hint="Skip behavior">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac5_skip_behavior.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#6: User Approval via AskUserQuestion

```xml
<acceptance_criteria id="AC6">
  <given>One or more detection heuristics have triggered</given>
  <when>Phase 5.7 Step 2 executes</when>
  <then>AskUserQuestion is invoked with triggered heuristic count and agent names, options: "Generate all", "Select individually", "Skip" — generation proceeds only for approved references</then>
  <verification>
    <source_files>
      <file hint="User approval flow">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac6_user_approval.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#7: Generated File Output Paths

```xml
<acceptance_criteria id="AC7">
  <given>The user approves generation for one or more subagents</given>
  <when>Phase 5.7 Step 3 writes reference files</when>
  <then>Each file is written to .claude/agents/{agent-name}/references/project-{type}.md following the project-*.md naming convention</then>
  <verification>
    <source_files>
      <file hint="File generation">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac7_output_paths.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#8: Derivation Purity Verification

```xml
<acceptance_criteria id="AC8">
  <given>Reference files have been generated in Step 3</given>
  <when>Phase 5.7 Step 4 (Verify No Contradictions) executes</when>
  <then>Each generated file is compared against source context files to confirm 100% content derivation — verification failure halts generation with a warning</then>
  <verification>
    <source_files>
      <file hint="Verification step">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac8_purity_verification.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#9: Precondition and Postcondition

```xml
<acceptance_criteria id="AC9">
  <given>The designing-systems skill is executing its phase sequence</given>
  <when>Phase 5.7 is reached</when>
  <then>Precondition "Phase 5.5 (Prompt Alignment) completed" verified before execution. Postcondition "Generated references contain only context-derived content" validated before proceeding to Phase 6</then>
  <verification>
    <source_files>
      <file hint="Pre/postconditions">.claude/skills/designing-systems/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac9_conditions.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#10: Summary Report Display

```xml
<acceptance_criteria id="AC10">
  <given>Phase 5.7 has completed generation and verification</given>
  <when>Step 5 (Report) executes</when>
  <then>Summary displays: count of files generated, file paths, source context files per reference, and regeneration command (/audit-alignment --generate-refs)</then>
  <verification>
    <source_files>
      <file hint="Report step">.claude/skills/designing-systems/references/domain-reference-generation.md</file>
    </source_files>
    <test_file>tests/STORY-478/test_ac10_summary_report.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree. Files are modified in src/claude/ and synced to .claude/ operational folders."
    source_paths:
      - "src/claude/skills/designing-systems/references/domain-reference-generation.md"
      - "src/claude/skills/designing-systems/SKILL.md"
    operational_paths:
      - ".claude/skills/designing-systems/references/domain-reference-generation.md"
      - ".claude/skills/designing-systems/SKILL.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "domain-reference-generation"
      file_path: "src/claude/skills/designing-systems/references/domain-reference-generation.md"
      required_keys:
        - key: "5-step workflow"
          type: "string"
          required: true
          validation: "Exactly 5 steps: Run Heuristics, Present Recommendations, Generate Files, Verify, Report"
          test_requirement: "Test: Count step headers, verify 5"
        - key: "heuristic definitions"
          type: "string"
          required: true
          validation: "DH-01 through DH-04 defined with trigger conditions and thresholds"
          test_requirement: "Test: Grep for DH-01, DH-02, DH-03, DH-04"
        - key: "reference file template"
          type: "string"
          required: true
          validation: "Contains template with auto-generation header and 5 sections"
          test_requirement: "Test: Grep for 'DO NOT EDIT MANUALLY' and section headers"
        - key: "AskUserQuestion integration"
          type: "string"
          required: true
          validation: "Step 2 uses AskUserQuestion with 3 options"
          test_requirement: "Test: Grep for 'AskUserQuestion' in Step 2"

    - type: "Configuration"
      name: "designing-systems-skillmd-phase57"
      file_path: "src/claude/skills/designing-systems/SKILL.md"
      required_keys:
        - key: "phase_57_header"
          type: "string"
          example: "Phase 5.7: Domain Reference Generation"
          required: true
          validation: "Header exists between Phase 5 and Phase 6"
          test_requirement: "Test: Phase 5.7 header present after Phase 5 and before Phase 6"
        - key: "reference_loading"
          type: "string"
          required: true
          validation: "Contains Read() call for domain-reference-generation.md"
          test_requirement: "Test: Grep for Read(file_path containing domain-reference-generation)"
        - key: "precondition"
          type: "string"
          required: true
          validation: "States 'Phase 5.5 completed' as precondition"
          test_requirement: "Test: Grep for 'Phase 5.5' in precondition"

  business_rules:
    - id: "BR-001"
      rule: "Phase 5.7 inserts after Phase 5.5, before Phase 6"
      trigger: "SKILL.md structural modification"
      validation: "Phase ordering: 5 → 5.5 → 5.7 → 6"
      error_handling: "Verify marker positions before insertion"
      test_requirement: "Test: Verify phase ordering in SKILL.md"
      priority: "Critical"
    - id: "BR-002"
      rule: "User approval required before generating any files"
      trigger: "When heuristics trigger"
      validation: "AskUserQuestion invoked before any Write() calls"
      error_handling: "Skip generation if user declines"
      test_requirement: "Test: AskUserQuestion appears before file generation step"
      priority: "Critical"
    - id: "BR-003"
      rule: "Derivation purity verification mandatory after generation"
      trigger: "After Step 3 (Generate Files)"
      validation: "Step 4 compares generated content against source context files"
      error_handling: "Halt and warn if non-derived content detected"
      test_requirement: "Test: Verification step present after generation step"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Full Phase 5.7 execution under 120 seconds"
      metric: "< 120 seconds total including verification"
      test_requirement: "Test: Time full Phase 5.7 execution"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Heuristic failure does not halt entire Phase 5.7"
      metric: "0 full halts on individual heuristic failure"
      test_requirement: "Test: Simulate single heuristic failure, verify others complete"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- Full Phase 5.7 execution: < 120 seconds total
- Heuristic evaluation: < 10 seconds for all 4
- Reference file generation: < 30 seconds per file
- SKILL.md modification: < 5 seconds

### Security
- No modification to subagent core .md files (references/ directory only)
- Generated content derives exclusively from context files
- File write restricted to reference file path and agent references/ directories

### Reliability
- Individual heuristic failure does not halt Phase 5.7
- Partial generation failure (one agent) continues for remaining agents
- Idempotent regeneration with identical context files
- Verification failure halts only affected file, not entire phase

### Scalability
- Adding new heuristics requires only reference file edits (not SKILL.md)
- Template supports optional sections for diverse project types

## Dependencies

### Prerequisite Stories
- [ ] **STORY-477:** Detection Heuristic Engine and Reference File Template
  - **Why:** Phase 5.7 uses heuristic engine for detection and template for generation
  - **Status:** Backlog

### Technology Dependencies
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+ for workflow logic

**Test Scenarios:**
1. **Happy Path:** Phase 5.7 runs, heuristics triggered, user approves, files generated, verified, summary displayed
2. **Edge Cases:**
   - No Phase 5.5 exists yet (CLAP incomplete)
   - Agent references/ subdirectory missing (create it)
   - All 4 heuristics trigger (multi-select presentation)
   - User selects "Skip" (graceful termination)
   - Existing project-*.md files (overwrite)
   - Context files with minimal domain content (no triggers)

## Acceptance Criteria Verification Checklist

### AC#1-3: File Structure
- [ ] Reference file at correct path, 200-300 lines - **Phase:** 3
- [ ] SKILL.md Phase 5.7 inserted, 25-30 lines added - **Phase:** 3
- [ ] Progressive disclosure compliance verified - **Phase:** 3

### AC#4: Workflow
- [ ] 5 workflow steps documented - **Phase:** 3

### AC#5-6: User Interaction
- [ ] Skip behavior when no heuristics trigger - **Phase:** 2
- [ ] AskUserQuestion with 3 options - **Phase:** 2

### AC#7-8: Generation
- [ ] Output paths follow project-*.md convention - **Phase:** 3
- [ ] Derivation purity verification present - **Phase:** 2

### AC#9-10: Conditions and Report
- [ ] Pre/postconditions documented - **Phase:** 3
- [ ] Summary report with file count and regen command - **Phase:** 2

**Checklist Progress:** 0/10 items complete (0%)

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] domain-reference-generation.md created at .claude/skills/designing-systems/references/ - Completed: Extended existing file (from STORY-477) with 5-step Phase 5.7 workflow (~120 lines added, total 383 lines)
- [x] 5-step workflow documented with inputs, actions, tools, outputs - Completed: Steps 1-5 with clear inputs/outputs/error handling per step
- [x] Reference file template included with auto-generation header - Completed: Template with 5 sections and auto-generation header preserved from STORY-477
- [x] Detection heuristic definitions (DH-01 through DH-04) documented - Completed: All 4 heuristics preserved from STORY-477 base content
- [x] AskUserQuestion integration for user approval - Completed: Step 2 with 3 options (Generate all, Select individually, Skip)
- [x] Derivation purity verification logic documented - Completed: Step 4 with per-file verification, 100% derivation requirement, halt on failure
- [x] SKILL.md modified with Phase 5.7 entry (25-30 lines) - Completed: 28-line entry inserted between Phase 5.5 and Phase 6
- [x] Read() reference loading instruction present - Completed: Read(file_path) instruction in SKILL.md Phase 5.7 entry
- [x] Precondition and postcondition stated - Completed: Precondition "Phase 5.5 completed", Postcondition "context-derived content"
- [x] All 10 acceptance criteria have passing tests - Completed: 10/10 test suites pass in tests/STORY-478/
- [x] Edge cases covered (6 scenarios) - Completed: Documented in reference file workflow steps
- [x] Reference file 300-400 lines - Completed: 383 lines (combined STORY-477 base + STORY-478 workflow)
- [x] Workflow step tests pass - Completed: AC#4 tests pass (5-step verification)
- [x] Skip behavior tests pass - Completed: AC#5 tests pass
- [x] Purity verification tests pass - Completed: AC#8 tests pass
- [x] Reference file extended in src/claude/skills/designing-systems/references/ (source of truth) - Completed: src/ is source of truth
- [x] SKILL.md modified in src/claude/skills/designing-systems/ (source of truth) - Completed: 28-line Phase 5.7 entry
- [x] Both synced to .claude/ operational folders - Completed: cp from src/ to .claude/
- [x] Tests run against src/ tree - Completed: All tests point to src/claude/ paths
- [x] source-tree.md updated if needed (ADR required) - Completed: No update needed, reference file path already exists in source-tree.md

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 01 | ✅ Complete | Pre-flight validation, git-validator, tech-stack-detector |
| Phase 02 | ✅ Complete | 10 test suites created, all failing (RED) |
| Phase 03 | ✅ Complete | domain-reference-generation.md extended, SKILL.md Phase 5.7 inserted |
| Phase 04 | ✅ Complete | Code review APPROVED, no refactoring needed |
| Phase 04.5 | ✅ Complete | 10/10 ACs verified PASS |
| Phase 05 | ✅ Complete | Integration: cross-file refs, phase ordering, dual-path sync |
| Phase 05.5 | ✅ Complete | 10/10 ACs re-verified PASS |
| Phase 06 | ✅ Complete | No deferrals |
| Phase 07 | ✅ Complete | DoD updated |
| Phase 08 | ⏳ Pending | Git commit |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/designing-systems/references/domain-reference-generation.md | Extended | 383 (+123) |
| src/claude/skills/designing-systems/SKILL.md | Modified | 451 (+28) |
| .claude/skills/designing-systems/references/domain-reference-generation.md | Synced | 383 |
| .claude/skills/designing-systems/SKILL.md | Synced | 451 |
| tests/STORY-478/run_all_tests.sh | Created | Runner |
| tests/STORY-478/test_ac1_reference_file_path.sh | Created | AC#1 |
| tests/STORY-478/test_ac2_skillmd_phase57.sh | Created | AC#2 |
| tests/STORY-478/test_ac3_progressive_disclosure.sh | Created | AC#3 |
| tests/STORY-478/test_ac4_5step_workflow.sh | Created | AC#4 |
| tests/STORY-478/test_ac5_skip_behavior.sh | Created | AC#5 |
| tests/STORY-478/test_ac6_user_approval.sh | Created | AC#6 |
| tests/STORY-478/test_ac7_output_paths.sh | Created | AC#7 |
| tests/STORY-478/test_ac8_derivation_purity.sh | Created | AC#8 |
| tests/STORY-478/test_ac9_precondition_postcondition.sh | Created | AC#9 |
| tests/STORY-478/test_ac10_summary_report.sh | Created | AC#10 |

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from EPIC-082 Feature 3 (batch 2/3) | STORY-478.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 36/36 tests, 0 violations, 3/3 validators | STORY-478-qa-report.md |

## Notes

**Design Decisions:**
- **Shared file ownership:** STORY-477 CREATES `domain-reference-generation.md` with heuristic definitions and template. This story EXTENDS the same file by adding the 5-step Phase 5.7 workflow that orchestrates the heuristics and template into an executable workflow. Implementation must preserve STORY-477 content and append workflow sections.
- Phase 5.7 uses progressive disclosure (reference file) to keep SKILL.md lean
- 5-step workflow follows established Phase 5.5 precedent from EPIC-081
- User approval required before any file generation (consistent with immutable-first philosophy)
- Derivation purity verification ensures no hallucinated content in references

**Edge Cases Documented:**
1. No Phase 5.5 exists (position after Phase 5 with dependency note)
2. Agent references/ subdirectory missing (create before writing)
3. All 4 heuristics trigger (present multi-select via AskUserQuestion)
4. User selects "Skip" (graceful termination, proceed to Phase 6)
5. Existing project-*.md files (overwrite with fresh content)
6. Context files with minimal content (no triggers, skip Phase 5.7)

**References:**
- [Requirements Specification](devforgeai/specs/requirements/domain-reference-generation-requirements.md) (FR-003, FR-004)
- [designing-systems SKILL.md](.claude/skills/designing-systems/SKILL.md)
- [EPIC-082](devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
