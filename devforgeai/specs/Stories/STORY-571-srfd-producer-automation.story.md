---
id: STORY-571
title: "SRFD Producer - Automate SRFD Generation in Framework-Analyst and Phase 09"
type: feature
epic: null
sprint: Backlog
status: Backlog
points: 3
depends_on: []
priority: Medium
advisory: false
assigned_to: unassigned
created: 2026-03-03
format_version: "2.9"
---

# STORY-571: SRFD Producer - Automate SRFD Generation in Framework-Analyst and Phase 09

## Description

**As a** DevForgeAI framework maintainer,
**I want** SRFD documents to be automatically generated during Phase 09 feedback using enriched data from framework-analyst Step 8,
**so that** every completed story produces a structured, citable feedback record without manual authoring effort.

This story creates the SRFD format reference file, extends the framework-analyst subagent with a new Step 8 that returns SRFD-enriched data (line numbers, constraint citations, AC scaffolds, epic/sprint context), and extends Phase 09 to write the SRFD markdown file, manage the srfd-index.json, and add `source_srfd` backlinks to recommendation queue entries.

## Acceptance Criteria

### AC#1: SRFD Format Reference File Exists

```xml
<acceptance_criteria id="AC1">
  <given>The devforgeai-feedback skill references directory exists at src/claude/skills/devforgeai-feedback/references/</given>
  <when>STORY-571 implementation is complete</when>
  <then>src/claude/skills/devforgeai-feedback/references/srfd-format.md exists and contains: (a) the canonical SRFD markdown section structure, (b) required vs optional sections table, (c) validation rules, and (d) an empty srfd-index.json template for lazy creation at runtime</then>
  <verification>
    <source_files>
      <file hint="SRFD format specification">src/claude/skills/devforgeai-feedback/references/srfd-format.md</file>
    </source_files>
    <test_file>tests/STORY-571/test_ac1_srfd_format_reference.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Framework-Analyst Step 8 Returns SRFD-Enriched Data

```xml
<acceptance_criteria id="AC2">
  <given>Framework-analyst completes Steps 1-7 and has produced ai-analysis JSON with recommendations</given>
  <when>Step 8 executes</when>
  <then>The returned data includes: (a) affected file paths with line numbers obtained via Read(), (b) constraint citations produced by Read-Quote-Cite-Verify against context files, (c) XML acceptance criteria scaffolded from implementation_code, and (d) epic/sprint values extracted from story YAML frontmatter — all without writing any files (permissionMode: readonly preserved)</then>
  <verification>
    <source_files>
      <file hint="Framework-analyst subagent definition">src/claude/agents/framework-analyst.md</file>
    </source_files>
    <test_file>tests/STORY-571/test_ac2_step8_enriched_data.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Phase 09 Writes SRFD Markdown File

```xml
<acceptance_criteria id="AC3">
  <given>Phase 09 receives SRFD-enriched data from framework-analyst</given>
  <when>The orchestrator executes the SRFD production step</when>
  <then>A file is written to devforgeai/feedback/ai-analysis/{STORY-NNN}/SRFD-{STORY-NNN}-{YYYY-MM-DD}.md matching the format specification in srfd-format.md, with all required sections populated</then>
  <verification>
    <source_files>
      <file hint="Phase 09 feedback workflow">src/claude/skills/implementing-stories/phases/phase-09-feedback.md</file>
      <file hint="SRFD format reference">src/claude/skills/devforgeai-feedback/references/srfd-format.md</file>
    </source_files>
    <test_file>tests/STORY-571/test_ac3_srfd_write.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Phase 09 Creates or Updates srfd-index.json

```xml
<acceptance_criteria id="AC4">
  <given>Phase 09 has written an SRFD markdown file</given>
  <when>The index update step executes</when>
  <then>If devforgeai/feedback/ai-analysis/aggregated/srfd-index.json does not exist, it is created from the empty template in srfd-format.md; the new SRFD entry (id, path, source_story, workflow, generated, recommendation_count, open_count, implemented_count) is appended to the documents array</then>
  <verification>
    <source_files>
      <file hint="Phase 09 feedback workflow">src/claude/skills/implementing-stories/phases/phase-09-feedback.md</file>
    </source_files>
    <test_file>tests/STORY-571/test_ac4_index_management.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Recommendations in Queue Reference Source SRFD

```xml
<acceptance_criteria id="AC5">
  <given>Phase 09 produces recommendations for the feedback queue</given>
  <when>Each recommendation object is added to recommendations-queue.json</when>
  <then>It includes a source_srfd field containing the relative path to the SRFD markdown file (e.g., "STORY-NNN/SRFD-STORY-NNN-YYYY-MM-DD.md")</then>
  <verification>
    <source_files>
      <file hint="Phase 09 feedback workflow">src/claude/skills/implementing-stories/phases/phase-09-feedback.md</file>
    </source_files>
    <test_file>tests/STORY-571/test_ac5_queue_backlink.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

| File | Action | Purpose |
|------|--------|---------|
| `src/claude/skills/devforgeai-feedback/references/srfd-format.md` | Create | SRFD format specification with section structure, validation rules, and empty index template |
| `src/claude/agents/framework-analyst.md` | Modify | Add Step 8: return SRFD-enriched data (line numbers, citations, AC scaffolds, epic/sprint) |
| `src/claude/skills/implementing-stories/phases/phase-09-feedback.md` | Modify | Add SRFD write orchestration, index management, queue backlink insertion |

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "srfd-format.md"
      file_path: "src/claude/skills/devforgeai-feedback/references/srfd-format.md"
      required_keys:
        - key: "SRFD Section Structure"
          type: "string"
          required: true
          description: "Canonical SRFD markdown template with YAML frontmatter, Session Summary, Constraint Analysis, Recommendations (7 subsections each), Cross-Recommendation Dependencies, Patterns Observed, Anti-Patterns Detected"
          test_requirement: "Test: Verify all required sections listed in Required vs Optional table are present in section structure"
        - key: "Required vs Optional Sections Table"
          type: "string"
          required: true
          description: "Table listing each SRFD section with Required/Optional status and notes"
          test_requirement: "Test: Verify table contains entries for all SRFD sections"
        - key: "Validation Rules"
          type: "string"
          required: true
          description: "Rules for no-placeholder, citation compliance, AC XML format, verbatim code, batch markers"
          test_requirement: "Test: Verify 5 validation rules documented"
        - key: "Empty srfd-index.json Template"
          type: "string"
          required: true
          description: "JSON template with version, description, and empty documents array"
          test_requirement: "Test: Verify template is valid JSON with documents array"

    - type: "Service"
      name: "framework-analyst Step 8"
      file_path: "src/claude/agents/framework-analyst.md"
      interface: "readonly (no Write/Edit tools)"
      lifecycle: "Invoked per story during Phase 09"
      dependencies:
        - "ai-analysis JSON (from Steps 1-7)"
        - "Story file YAML frontmatter"
        - "6 constitutional context files"
      requirements:
        - id: "SVC-001"
          description: "Read affected files and extract line numbers for each recommendation"
          testable: true
          test_requirement: "Test: Step 8 output contains affected_files with non-null line numbers for existing files"
          priority: "High"
        - id: "SVC-002"
          description: "Read context files and produce constraint citations via Read-Quote-Cite-Verify"
          testable: true
          test_requirement: "Test: Each citation has file path, line range, and 2+ line verbatim quote"
          priority: "High"
        - id: "SVC-003"
          description: "Scaffold XML acceptance criteria from implementation_code field"
          testable: true
          test_requirement: "Test: At least 2 XML AC blocks per recommendation with given/when/then"
          priority: "High"
        - id: "SVC-004"
          description: "Extract epic and sprint from story YAML frontmatter"
          testable: true
          test_requirement: "Test: epic_association and sprint_context populated from story file"
          priority: "Medium"

    - type: "Service"
      name: "Phase 09 SRFD Orchestration"
      file_path: "src/claude/skills/implementing-stories/phases/phase-09-feedback.md"
      interface: "Write access for SRFD files"
      lifecycle: "Invoked per story after framework-analyst returns"
      dependencies:
        - "framework-analyst Step 8 enriched data"
        - "srfd-format.md (format reference)"
      requirements:
        - id: "SVC-005"
          description: "Write SRFD markdown conforming to srfd-format.md specification"
          testable: true
          test_requirement: "Test: Written SRFD has all required sections per format spec"
          priority: "Critical"
        - id: "SVC-006"
          description: "Create srfd-index.json from template if not exists; append entry if exists"
          testable: true
          test_requirement: "Test: Index created on first run; entry appended on subsequent runs"
          priority: "High"
        - id: "SVC-007"
          description: "Add source_srfd field to each recommendation in recommendations-queue.json"
          testable: true
          test_requirement: "Test: All recommendations for the story have source_srfd pointing to SRFD file"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Framework-analyst must not write files (permissionMode: readonly)"
      trigger: "Step 8 execution"
      validation: "No Write() or Edit() calls in Step 8"
      error_handling: "Violation detected by Phase 09 validation gate"
      test_requirement: "Test: Verify framework-analyst.md tools list does not include Write or Edit"
      priority: "Critical"
    - id: "BR-002"
      rule: "SRFD files must be written only under devforgeai/feedback/ai-analysis/"
      trigger: "Phase 09 SRFD write step"
      validation: "Path starts with devforgeai/feedback/ai-analysis/"
      error_handling: "HALT if path traversal detected"
      test_requirement: "Test: SRFD write path validated before Write() call"
      priority: "High"
    - id: "BR-003"
      rule: "Duplicate SRFD for same story+date overwrites existing and updates (not duplicates) index entry"
      trigger: "Phase 09 re-run on same day"
      validation: "Check for existing entry with matching story_id + date"
      error_handling: "Overwrite file, update existing index entry"
      test_requirement: "Test: Re-run produces one index entry, not two"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Step 8 completes within 30 seconds for stories with up to 20 affected files"
      metric: "< 30s wall-clock time"
      test_requirement: "Test: Time Step 8 execution with 20-file story"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Malformed srfd-index.json triggers backup and recreate, not crash"
      metric: "Zero unhandled exceptions from corrupt index"
      test_requirement: "Test: Corrupt index file backed up and fresh index created"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "framework-analyst"
    limitation: "Read-Quote-Cite-Verify performs up to 6 Read() calls per story (one per context file), adding token overhead"
    decision: "workaround:Only read context files relevant to recommendation categories (architecture, security, tooling)"
    discovered_phase: "Architecture"
    impact: "Token usage may increase by up to 3K tokens per Phase 09 invocation"
  - id: TL-002
    component: "srfd-index.json"
    limitation: "Flat JSON array does not support efficient lookup for large numbers of SRFDs"
    decision: "pending"
    discovered_phase: "Architecture"
    impact: "Performance may degrade with 1000+ SRFD entries; consider restructuring to keyed object in future"
```

## Non-Functional Requirements

### Performance
- Step 8 completes in < 30 seconds for stories touching up to 20 files
- Phase 09 SRFD write + index update completes in < 5 seconds
- Read-Quote-Cite-Verify performs at most 6 Read() calls per story

### Security
- Framework-analyst remains permissionMode: readonly — zero Write/Edit calls in Step 8
- SRFD files written only under `devforgeai/feedback/ai-analysis/` — path traversal forbidden
- No secrets, credentials, or environment variable values appear in SRFD content

### Scalability
- srfd-index.json supports up to 10,000 entries without restructuring
- SRFD generation adds < 2 seconds overhead to Phase 09 per story
- No in-memory caching of index between stories — each Phase 09 invocation reads fresh from disk

### Reliability
- Malformed srfd-index.json triggers backup + recreate (no data loss, no crash)
- Read() failure on any single file does not abort Step 8 or Phase 09 — graceful degradation with null markers
- Phase 09 validates SRFD content against srfd-format.md structure before writing

### Observability
- Phase 09 logs: "SRFD generated: {path}" on success
- Phase 09 logs: "srfd-index.json created from template" on first run
- Step 8 logs count of recommendations enriched and any Read() failures

## Dependencies

### Prerequisite Stories
- None

### External Dependencies
- None

### Technology Dependencies
- None (all changes are markdown prompt files)

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Framework-analyst produces enriched data → Phase 09 writes SRFD → index created → queue updated
2. **Edge Cases:**
   - Story without epic/sprint frontmatter fields
   - Malformed srfd-index.json recovery
   - Read() failure on referenced file
   - Same-day SRFD re-run (overwrite, not duplicate)
3. **Error Cases:**
   - Missing required keys in Step 8 enriched data
   - Path traversal attempt in SRFD write path
   - Empty recommendations array (no SRFD generated)

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Flow:** `/dev STORY-XXX` → Phase 09 → SRFD generated + index updated + queue backlinked
2. **Format Compliance:** Generated SRFD passes all validation rules from srfd-format.md

### E2E Tests (If Applicable)

Not applicable — framework prompt files, not compiled code.

## Acceptance Criteria Verification Checklist

### AC#1: SRFD Format Reference File Exists
- [ ] srfd-format.md created at src/claude/skills/devforgeai-feedback/references/ - **Phase:** 3 - **Evidence:** File exists with all sections
- [ ] Contains SRFD section structure template - **Phase:** 3 - **Evidence:** Grep for required headers
- [ ] Contains required vs optional sections table - **Phase:** 3 - **Evidence:** Table present
- [ ] Contains empty srfd-index.json template - **Phase:** 3 - **Evidence:** Valid JSON block

### AC#2: Framework-Analyst Step 8 Returns SRFD-Enriched Data
- [ ] Step 8 added to framework-analyst.md after Step 7 - **Phase:** 3 - **Evidence:** Step 8 header present
- [ ] Reads affected files for line numbers - **Phase:** 3 - **Evidence:** Read() calls in Step 8
- [ ] Produces constraint citations via Read-Quote-Cite-Verify - **Phase:** 3 - **Evidence:** Citation format documented
- [ ] Scaffolds XML ACs from implementation_code - **Phase:** 3 - **Evidence:** XML template in Step 8
- [ ] Extracts epic/sprint from story frontmatter - **Phase:** 3 - **Evidence:** YAML parsing in Step 8
- [ ] No Write/Edit calls (readonly preserved) - **Phase:** 3 - **Evidence:** Tools list unchanged

### AC#3: Phase 09 Writes SRFD Markdown File
- [ ] SRFD write step added to phase-09-feedback.md - **Phase:** 3 - **Evidence:** Write() call with SRFD path
- [ ] SRFD conforms to srfd-format.md specification - **Phase:** 3 - **Evidence:** All required sections present

### AC#4: Phase 09 Creates or Updates srfd-index.json
- [ ] Index creation from template on first run - **Phase:** 3 - **Evidence:** Conditional create logic
- [ ] Index entry appended on subsequent runs - **Phase:** 3 - **Evidence:** Append logic documented
- [ ] Duplicate entry handling on same-day re-run - **Phase:** 3 - **Evidence:** Update-not-duplicate logic

### AC#5: Recommendations in Queue Reference Source SRFD
- [ ] source_srfd field added to recommendation objects - **Phase:** 3 - **Evidence:** Field assignment in Phase 09

---

**Checklist Progress:** 0/16 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** unassigned
**Implemented:** N/A

## Definition of Done

### Implementation
- [ ] srfd-format.md created at src/claude/skills/devforgeai-feedback/references/srfd-format.md
- [ ] framework-analyst.md updated with Step 8 (SRFD-enriched data return)
- [ ] phase-09-feedback.md updated with SRFD write, index management, and queue backlink steps

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (no epic/sprint, malformed index, Read failure, same-day re-run)
- [ ] Framework-analyst permissionMode: readonly verified unchanged
- [ ] SRFD format matches specification in srfd-format.md

### Testing
- [ ] Verification that srfd-format.md contains all required sections
- [ ] Verification that Step 8 output schema includes all required keys
- [ ] Verification that Phase 09 writes valid SRFD file
- [ ] Verification that index is created/updated correctly
- [ ] Verification that queue entries have source_srfd field

### Documentation
- [ ] srfd-format.md serves as self-documenting specification
- [ ] Step 8 documented in framework-analyst.md with input/output contract
- [ ] Phase 09 SRFD steps documented with error handling

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| `src/claude/skills/devforgeai-feedback/references/srfd-format.md` | Create | ~200 |
| `src/claude/agents/framework-analyst.md` | Modify | +50 |
| `src/claude/skills/implementing-stories/phases/phase-09-feedback.md` | Modify | +80 |

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from SRFD pipeline Layer 3 plan | STORY-571.story.md |

## Notes

**Design Decisions:**
- Phase 09 orchestrator performs all SRFD writes, keeping framework-analyst readonly. This follows the existing pattern where Phase 09 already handles ai-analysis JSON storage.
- srfd-index.json is lazily created from a template embedded in srfd-format.md rather than shipped as a seed file via the installer.
- SRFD format reference file lives at `src/claude/skills/devforgeai-feedback/references/srfd-format.md` (not `devforgeai/specs/`) so it deploys to all projects via the installer.

**Source Plan:** `/home/bryan/.claude/plans/effervescent-leaping-quiche.md` — Layer 3 SRFD Automation

**Related Work:**
- Layer 1-2 (SRFD format spec + first instance) completed in prior session
- STORY-546 (SRFD Consumer) is the companion story for triage-workflow enhancement

**References:**
- SRFD Format Specification (Layer 1): `devforgeai/specs/SRFD-FORMAT-SPECIFICATION.md` (reference instance in tmp/DevForgeAI-CLI)
- SRFD STORY-010 instance (Layer 2): `devforgeai/feedback/ai-analysis/STORY-010/SRFD-STORY-010-2026-03-02.md` (reference instance in tmp/DevForgeAI-CLI)

---

Story Template Version: 2.9
Last Updated: 2026-03-03
