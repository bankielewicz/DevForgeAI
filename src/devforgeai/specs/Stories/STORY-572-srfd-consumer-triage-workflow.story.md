---
id: STORY-572
title: "SRFD Consumer - Enhance Triage Workflow to Read SRFD Documents"
type: feature
epic: null
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-571"]
priority: Medium
advisory: false
assigned_to: unassigned
created: 2026-03-03
format_version: "2.9"
---

# STORY-572: SRFD Consumer - Enhance Triage Workflow to Read SRFD Documents

## Description

**As a** DevForgeAI orchestrator creating stories from triage recommendations,
**I want** Phase 4 of the triage-workflow to read SRFD documents and extract rich context for each selected recommendation,
**so that** stories created from recommendations include pre-built AC scaffolds, implementation guidance, decision trails, and dependency info instead of minimal context markers.

The triage-workflow currently passes minimal context markers (Feature Description, Implementation Approach, Affected Files, Source, Priority) to `/create-story` in Phase 4. This story enhances Phase 4 to look up the `source_srfd` field on each selected recommendation, read the SRFD document, extract the specific `### REC-{id}` section, and pass enriched context including batch context markers, AC scaffolds, implementation guidance, decision trail, and dependency info. When `source_srfd` is missing or the SRFD file doesn't exist, the workflow falls back to the current minimal context behavior.

## Acceptance Criteria

### AC#1: SRFD Document Lookup and REC Section Extraction

```xml
<acceptance_criteria id="AC1">
  <given>A selected recommendation has a source_srfd field pointing to an existing SRFD file</given>
  <when>Phase 4 processes that recommendation for story creation</when>
  <then>The workflow reads the SRFD file, extracts the specific REC section matching the recommendation ID (e.g., ### REC-010-003), and passes the extracted content as enriched context to /create-story</then>
  <verification>
    <source_files>
      <file hint="Triage workflow reference">src/claude/skills/devforgeai-feedback/references/triage-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-572/test_ac1_srfd_lookup.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Enriched Context Markers Passed to /create-story

```xml
<acceptance_criteria id="AC2">
  <given>The SRFD REC section has been successfully extracted</given>
  <when>The enriched context is assembled for /create-story</when>
  <then>The context includes all of: (a) batch context markers from the Batch Context Markers subsection, (b) pre-built AC scaffold from the Acceptance Criteria Scaffold subsection, (c) implementation guidance from the Implementation Guidance subsection, (d) decision trail from the Decision Trail subsection, and (e) dependency info from the Classification table Depends On field</then>
  <verification>
    <source_files>
      <file hint="Triage workflow reference">src/claude/skills/devforgeai-feedback/references/triage-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-572/test_ac2_enriched_context.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Graceful Fallback When source_srfd Is Missing

```xml
<acceptance_criteria id="AC3">
  <given>A selected recommendation has no source_srfd field (field missing or null)</given>
  <when>Phase 4 processes that recommendation</when>
  <then>Story creation proceeds with current minimal context markers (Feature Description, Implementation Approach, Affected Files, Source, Priority) and no error is raised</then>
  <verification>
    <source_files>
      <file hint="Triage workflow reference">src/claude/skills/devforgeai-feedback/references/triage-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-572/test_ac3_fallback_missing_field.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Graceful Fallback When SRFD File Does Not Exist

```xml
<acceptance_criteria id="AC4">
  <given>A selected recommendation has a source_srfd field pointing to a non-existent file</given>
  <when>Phase 4 attempts to read the SRFD file</when>
  <then>Story creation falls back to minimal context markers, a warning is displayed indicating the SRFD file was not found, and processing continues without interruption</then>
  <verification>
    <source_files>
      <file hint="Triage workflow reference">src/claude/skills/devforgeai-feedback/references/triage-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-572/test_ac4_fallback_missing_file.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

| File | Action | Purpose |
|------|--------|---------|
| `src/claude/skills/devforgeai-feedback/references/triage-workflow.md` | Modify | Enhance Phase 4 with SRFD lookup, extraction, enriched context passing, and fallback logic |

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "Triage Workflow Phase 4 Enhancement"
      file_path: "src/claude/skills/devforgeai-feedback/references/triage-workflow.md"
      interface: "Read-only SRFD access"
      lifecycle: "Invoked per recommendation during /recommendations-triage"
      dependencies:
        - "recommendations-queue.json (source_srfd field)"
        - "SRFD files (devforgeai/feedback/ai-analysis/*/SRFD-*.md)"
        - "srfd-format.md (section structure reference)"
      requirements:
        - id: "SVC-001"
          description: "Look up source_srfd field on each selected recommendation"
          testable: true
          test_requirement: "Test: source_srfd field read from recommendation object"
          priority: "High"
        - id: "SVC-002"
          description: "Read SRFD file and extract REC section matching recommendation ID"
          testable: true
          test_requirement: "Test: REC section extracted by matching ### REC-{id} header"
          priority: "High"
        - id: "SVC-003"
          description: "Parse REC section into enriched context fields (batch markers, AC scaffold, implementation guidance, decision trail, dependencies)"
          testable: true
          test_requirement: "Test: All 5 enriched context fields extracted from REC section"
          priority: "High"
        - id: "SVC-004"
          description: "Pass enriched context to /create-story invocation"
          testable: true
          test_requirement: "Test: /create-story receives batch_mode markers and AC scaffold"
          priority: "High"
        - id: "SVC-005"
          description: "Fall back to minimal context when source_srfd missing or file not found"
          testable: true
          test_requirement: "Test: Fallback produces identical output to current Phase 4 behavior"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Each recommendation processed independently — one SRFD failure does not affect others in batch"
      trigger: "Multi-recommendation triage session"
      validation: "Process continues after SRFD read failure"
      error_handling: "Log warning, fall back to minimal context, continue to next recommendation"
      test_requirement: "Test: Batch of 3 recs where middle one has missing SRFD — first and third get enriched context"
      priority: "High"
    - id: "BR-002"
      rule: "Existing Phase 4 behavior must not regress when source_srfd field is absent"
      trigger: "Processing recommendations created before SRFD pipeline"
      validation: "Minimal context path unchanged"
      error_handling: "No error — absence of source_srfd is the normal pre-SRFD state"
      test_requirement: "Test: Recommendation without source_srfd produces identical story creation context as current behavior"
      priority: "Critical"
    - id: "BR-003"
      rule: "REC section matching uses exact recommendation ID match against ### REC-{id} headers"
      trigger: "SRFD section extraction"
      validation: "No fuzzy matching — exact string match only"
      error_handling: "If no matching section found, fall back to minimal context with warning"
      test_requirement: "Test: REC-010-003 matches ### REC-010-003 but not ### REC-010-004"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "SRFD read and section extraction completes in under 500ms per recommendation"
      metric: "< 500ms per recommendation"
      test_requirement: "Test: Time extraction for a 500-line SRFD document"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Zero regression to existing triage workflow when source_srfd absent"
      metric: "100% backward compatibility"
      test_requirement: "Test: Run triage with pre-SRFD recommendations, verify identical behavior"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "triage-workflow"
    limitation: "REC section extraction relies on markdown header pattern matching — SRFD format changes could break extraction"
    decision: "workaround:Reference srfd-format.md for canonical section headers; format changes require coordinated update"
    discovered_phase: "Architecture"
    impact: "If SRFD format changes without updating extraction logic, fallback to minimal context activates"
```

## Non-Functional Requirements

### Performance
- SRFD file read and REC section extraction: < 500ms per recommendation
- Total Phase 4 overhead for enriched context (batch of 10): < 5 seconds additional
- No more than 2 Read() calls per recommendation (1 for SRFD, 1 for fallback verification)

### Security
- SRFD file reads use native Read() tool only (no Bash file operations)
- File paths from source_srfd validated to exist within project root (no path traversal)

### Scalability
- Supports batch sizes up to 20 recommendations per triage session
- SRFD documents up to 500 lines parsed without timeout

### Reliability
- Fallback to minimal context on any SRFD-related failure with zero impact on existing workflow
- No regression when source_srfd is absent — current minimal context path unchanged

### Observability
- Display warning when SRFD file not found: "⚠️ SRFD not found: {path}. Using minimal context."
- Display info when enriched context loaded: "✓ SRFD context loaded for {rec_id}"
- Log extraction failures for debugging

## Dependencies

### Prerequisite Stories
- [ ] **STORY-571:** SRFD Producer - Automate SRFD Generation in Framework-Analyst and Phase 09
  - **Why:** Produces the SRFD files and srfd-index.json that this story consumes; creates srfd-format.md reference
  - **Status:** Backlog

### External Dependencies
- None

### Technology Dependencies
- None (all changes are markdown prompt files)

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Recommendation with valid source_srfd → SRFD read → REC extracted → enriched context passed to /create-story
2. **Edge Cases:**
   - source_srfd field missing (null/absent) → minimal context fallback
   - SRFD file does not exist → warning + minimal context fallback
   - REC section not found in SRFD → warning + minimal context fallback
   - Malformed SRFD → warning + minimal context fallback
   - Batch with mixed SRFD availability → independent processing
3. **Error Cases:**
   - Path traversal attempt in source_srfd → rejected
   - Empty SRFD file → fallback

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Flow:** `/recommendations-triage` → select recommendation with source_srfd → /create-story receives enriched context
2. **Backward Compatibility:** Run triage with pre-SRFD recommendations → identical to current behavior

## Acceptance Criteria Verification Checklist

### AC#1: SRFD Document Lookup and REC Section Extraction
- [ ] Phase 4 reads source_srfd from recommendation - **Phase:** 3 - **Evidence:** Read() call in Phase 4
- [ ] SRFD file content loaded via Read() - **Phase:** 3 - **Evidence:** Read() with source_srfd path
- [ ] REC section extracted by exact ID match - **Phase:** 3 - **Evidence:** Grep for ### REC-{id}
- [ ] Extracted content structured for downstream use - **Phase:** 3 - **Evidence:** Variables populated

### AC#2: Enriched Context Markers Passed to /create-story
- [ ] Batch context markers extracted from SRFD - **Phase:** 3 - **Evidence:** YAML block parsed
- [ ] AC scaffold passed to /create-story - **Phase:** 3 - **Evidence:** XML blocks in context
- [ ] Implementation guidance included - **Phase:** 3 - **Evidence:** File:line table in context
- [ ] Decision trail included - **Phase:** 3 - **Evidence:** Alternatives table in context
- [ ] Dependency info included - **Phase:** 3 - **Evidence:** Depends On field in context

### AC#3: Graceful Fallback When source_srfd Is Missing
- [ ] Missing field detected without error - **Phase:** 3 - **Evidence:** Conditional check
- [ ] Minimal context markers used as fallback - **Phase:** 3 - **Evidence:** Current Phase 4 path

### AC#4: Graceful Fallback When SRFD File Does Not Exist
- [ ] Read() failure caught gracefully - **Phase:** 3 - **Evidence:** Try/catch or existence check
- [ ] Warning displayed to user - **Phase:** 3 - **Evidence:** Display statement
- [ ] Processing continues - **Phase:** 3 - **Evidence:** Next recommendation processed

---

**Checklist Progress:** 0/12 items complete (0%)

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
- [ ] triage-workflow.md Phase 4 enhanced with SRFD lookup logic
- [ ] REC section extraction implemented with exact ID matching
- [ ] Enriched context assembly for /create-story (batch markers, AC scaffold, implementation guidance, decision trail, dependencies)
- [ ] Graceful fallback to minimal context when source_srfd missing or file not found

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (missing field, missing file, missing section, malformed SRFD, mixed batch)
- [ ] Zero regression to existing Phase 4 behavior verified
- [ ] Warning messages displayed for fallback scenarios

### Testing
- [ ] Verification that enriched context includes all 5 fields from REC section
- [ ] Verification that fallback produces identical output to current behavior
- [ ] Verification that batch processing handles mixed SRFD availability independently

### Documentation
- [ ] Phase 4 enhancement documented inline in triage-workflow.md
- [ ] Fallback behavior documented with warning message format

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from SRFD pipeline Layer 3 plan | STORY-572.story.md |

## Notes

**Dual-Path Architecture Constraint (CRITICAL — read before implementing):**

This project uses a dual-path architecture (source-tree.md, lines 14-15):
> "Do not modify operational files. Only modify src/, tests/ files."

- **What the `/dev` workflow modifies:** Only `src/claude/skills/devforgeai-feedback/references/triage-workflow.md`
- **What the triage workflow reads at runtime (NOT touched by `/dev`):** SRFD files in `devforgeai/feedback/ai-analysis/`, `source_srfd` field from `recommendations-queue.json`
- **TDD tests verify:** That `triage-workflow.md` (in `src/`) contains correct SRFD lookup instructions, REC section extraction logic, enriched context assembly, and graceful fallback behavior. Tests do NOT read from or assert against files in `devforgeai/feedback/`.
- **Runtime reads** from `devforgeai/feedback/` occur when `/recommendations-triage` executes in deployed projects. This story's ACs only **read** from operational paths (no writes), which is constitutionally compliant, but TDD tests still verify the `src/` prompt file content, not runtime behavior.

**Design Decisions:**
- Enriched context fields are all optional — missing subsections in the REC section are simply omitted, not passed as empty strings.
- REC section matching uses exact string match (not fuzzy) to avoid false positives.
- Each recommendation processed independently in batch — one SRFD failure doesn't cascade.

**Source Plan:** `/home/bryan/.claude/plans/effervescent-leaping-quiche.md` — Layer 3 SRFD Automation, Story 2

**Related Work:**
- STORY-571 (SRFD Producer) is the prerequisite — produces the SRFD files this story consumes
- SRFD format specification reference: `src/claude/skills/devforgeai-feedback/references/srfd-format.md` (created by STORY-571)

**References:**
- Current triage workflow: `src/claude/skills/devforgeai-feedback/references/triage-workflow.md`
- SRFD STORY-010 instance (reference): `tmp/DevForgeAI-CLI/devforgeai/feedback/ai-analysis/STORY-010/SRFD-STORY-010-2026-03-02.md`

---

Story Template Version: 2.9
Last Updated: 2026-03-03
