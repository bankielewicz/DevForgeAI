---
id: STORY-404
title: Add AC-Level Chunking to Compliance Verifier
type: refactor
epic: EPIC-063
sprint: Backlog
status: QA Approved
priority: Medium
points: 2
created: 2026-02-08
updated: 2026-02-08
assignee: unassigned
tags: [framework, subagent, token-efficiency, verification, refactor]
source_recommendation: REC-STORY368-001
template_version: "2.8"
---

# STORY-404: Add AC-Level Chunking to Compliance Verifier

## Description

Update the ac-compliance-verifier workflow to verify acceptance criteria in chunks of 3 when a story has 5 or more ACs, reducing peak token usage by approximately 40%.

<!-- provenance>
  <origin document="EPIC-063" section="Feature 6">
    <quote>For large stories (5+ ACs), this consumes excessive tokens because each AC verification requires loading the AC definition, implementation evidence, and test evidence simultaneously</quote>
    <line_reference>lines 380-435</line_reference>
  </origin>
  <decision rationale="Chunking reduces peak token usage without changing report format">
    <selected>Verify ACs in chunks of 3 for stories with 5+ ACs</selected>
    <rejected>Keep single-pass verification for all stories</rejected>
    <trade_off>Token efficiency vs implementation complexity</trade_off>
  </decision>
</provenance -->

## User Story

**As a** DevForgeAI framework operator running /dev workflows on stories with 5 or more acceptance criteria,
**I want** the ac-compliance-verifier to verify ACs in chunks of 3 instead of all at once,
**So that** peak token consumption during fresh-context verification is reduced by approximately 40%, preventing context window exhaustion on large stories.

## Acceptance Criteria

<acceptance_criteria id="AC1" title="Small story single-pass behavior preserved">
  <given>A story file with fewer than 5 acceptance criteria</given>
  <when>The ac-compliance-verifier is invoked via Task() in Phase 4.5 or Phase 5.5</when>
  <then>All ACs are verified in a single pass (existing behavior unchanged), and the verification report matches the current format exactly</then>
  <verification>
    <method>Run verifier on 3-AC story, compare report to expected format</method>
    <expected_result>Report format identical to pre-change behavior</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/ac-compliance-verifier.md" hint="Existing single-pass workflow"/>
    <file path="src/claude/agents/ac-compliance-verifier/references/report-generation.md" hint="Report schema"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC2" title="Chunking activates at 5+ ACs">
  <given>A story file with 5 or more acceptance criteria</given>
  <when>The ac-compliance-verifier is invoked</when>
  <then>The verifier groups ACs into chunks of 3 (e.g., 5 ACs produce chunks [AC1,AC2,AC3] and [AC4,AC5])</then>
  <verification>
    <method>Run verifier on 5-AC story, verify 2 chunks processed</method>
    <expected_result>5 ACs: 2 chunks (3+2), 8 ACs: 3 chunks (3+3+2)</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/ac-compliance-verifier.md" hint="Add chunking logic"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC3" title="Fresh re-read per chunk">
  <given>The verifier is processing a story with 5+ ACs in chunked mode</given>
  <when>Each chunk of ACs is processed</when>
  <then>The story file is re-read fresh from disk using Read() at the start of each chunk's verification pass</then>
  <verification>
    <method>Verify each chunk triggers separate Read() call</method>
    <expected_result>Fresh context per chunk, no stale data</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/ac-compliance-verifier.md" hint="Fresh-context technique"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC4" title="Aggregated report format identical to single-pass">
  <given>The verifier has completed chunked verification across multiple passes</given>
  <when>The final report is assembled by aggregating chunk results</when>
  <then>The output JSON matches the exact schema with correct total_acs, all AC details in document order, and correct overall_status</then>
  <verification>
    <method>Compare aggregated report structure to single-pass report structure</method>
    <expected_result>Schema identical, AC order preserved</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/ac-compliance-verifier/references/report-generation.md" hint="Report schema"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC5" title="Downstream consumers unaffected">
  <given>The aggregated verification report is returned from the ac-compliance-verifier</given>
  <when>Consumed by Phase 4.5/5.5 or QA skill Phase 1</when>
  <then>Downstream consumers process the report without modification and without awareness of chunking</then>
  <verification>
    <method>Run full /dev workflow with 6-AC story, verify no consumer errors</method>
    <expected_result>Workflow completes normally, no chunking-related failures</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/phases/phase-04.5-ac-verification.md" hint="Consumer of report"/>
    <file path="src/claude/skills/devforgeai-qa/SKILL.md" hint="Consumer of report"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC6" title="Token reduction measurable for 5+ AC stories">
  <given>A story with 6 or more acceptance criteria</given>
  <when>The ac-compliance-verifier completes using chunked verification</when>
  <then>Peak per-chunk token usage is lower than full single-pass, and chunking mode is logged in observations_for_persistence</then>
  <verification>
    <method>Check observations_for_persistence for chunk_count and ac_count</method>
    <expected_result>Chunking metadata logged for analysis</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/ac-compliance-verifier.md" hint="observations_for_persistence section"/>
  </source_files>
</acceptance_criteria>

## Technical Specification

### Component Overview

| Component | Type | Description |
|-----------|------|-------------|
| ac-compliance-verifier.md | Subagent | Add chunking logic for 5+ AC stories |

### Technical Details

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Subagent
      name: ac-compliance-verifier
      file_path: src/claude/agents/ac-compliance-verifier.md
      description: Add AC-level chunking for stories with 5+ ACs
      dependencies:
        - src/claude/agents/ac-compliance-verifier/references/report-generation.md
        - src/claude/agents/ac-compliance-verifier/references/verification-workflow.md
        - src/claude/agents/ac-compliance-verifier/references/xml-parsing-protocol.md
      test_requirement: 5+ AC stories processed in chunks of 3, report format unchanged

  business_rules:
    - rule: Chunking threshold
      description: If AC count >= 5, chunk into groups of 3; else single-pass
      test_requirement: 4 ACs -> single pass, 5 ACs -> 2 chunks

    - rule: Fresh context per chunk
      description: Re-read story file at start of each chunk
      test_requirement: Each chunk triggers separate Read() call

    - rule: Report format invariant
      description: Aggregated report identical to single-pass format
      test_requirement: Schema comparison passes

  non_functional_requirements:
    - category: Performance
      requirement: Reduced peak token usage
      metric: ~40% reduction for 5+ AC stories
      test_requirement: Measure per-chunk vs full-pass tokens

    - category: Reliability
      requirement: Deterministic aggregation
      metric: Same inputs always produce same output
      test_requirement: Multiple runs produce identical reports
```

### Chunking Algorithm

```
1. Count ACs: Grep for <acceptance_criteria id= patterns
2. If count < 5: Single-pass (existing behavior)
3. If count >= 5: Chunk into groups of 3
4. For each chunk:
   a. Read story file fresh
   b. Verify only ACs in current chunk
   c. Store chunk results
5. Aggregate: Merge all chunk results into single report
```

### Test Scenarios

| AC Count | Chunks | Chunk Sizes |
|----------|--------|-------------|
| 3 | 1 | [3] (single pass) |
| 5 | 2 | [3, 2] |
| 6 | 2 | [3, 3] |
| 8 | 3 | [3, 3, 2] |
| 20 | 7 | [3, 3, 3, 3, 3, 3, 2] |

### Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `src/claude/agents/ac-compliance-verifier.md` | Edit | Add chunking logic after AC count detection |

## Edge Cases

1. **Exactly 5 ACs (threshold boundary):** Chunking activates at exactly 5 ACs (2 chunks: 3+2).

2. **Single AC story:** Works in single-pass mode without chunking interference.

3. **BLOCKED status in one chunk:** Correctly carries BLOCKED status into aggregated report.

4. **Mixed FAIL and PASS across chunks:** Aggregated overall_status is PARTIAL if any chunk has FAIL.

5. **Story file changes between chunk reads:** Each chunk verifies against version it reads.

6. **20 ACs (maximum):** 7 chunks handled within 300-second timeout.

7. **Anti-pattern violations in chunked mode:** Merged into aggregated report without duplication.

## Non-Functional Requirements

| Category | Requirement | Metric |
|----------|-------------|--------|
| Performance | Token reduction | ~40% for 5+ AC stories |
| Performance | Single-pass no regression | Identical latency for <5 ACs |
| Reliability | Deterministic aggregation | Same inputs → same output |
| Scalability | Handle 1-20 ACs | Maximum 7 chunks for 20 ACs |

## Definition of Done

### Implementation
- [x] AC count detection step added after XML parsing
- [x] Chunking decision logic: <5 ACs → single pass, >=5 ACs → chunks of 3
- [x] Chunk processing loop with fresh Read() per chunk
- [x] Result aggregation matching report-generation.md schema
- [x] Chunking metadata logged in observations_for_persistence

### Quality
- [x] Single-pass behavior unchanged for <5 AC stories
- [x] Aggregated report format identical to single-pass
- [x] AC order preserved (document order)
- [x] All chunk results correctly merged

### Testing
- [x] 3-AC story: single pass, report unchanged
- [x] 5-AC story: 2 chunks (3+2)
- [x] 6-AC story: 2 chunks (3+3)
- [x] 8-AC story: 3 chunks (3+3+2)
- [x] Downstream consumers work without modification
- [x] observations_for_persistence contains chunking metadata

### Documentation
- [x] Chunking behavior documented in ac-compliance-verifier.md

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-09
**Branch:** main

- [x] AC count detection step added after XML parsing - Completed: Step 0 Threshold Detection (lines 92-116)
- [x] Chunking decision logic: <5 ACs → single pass, >=5 ACs → chunks of 3 - Completed: Step 0 (lines 100-115)
- [x] Chunk processing loop with fresh Read() per chunk - Completed: Step 0.2 Fresh Re-Read (lines 138-157)
- [x] Result aggregation matching report-generation.md schema - Completed: Step 0.3 Report Aggregation (lines 158-183)
- [x] Chunking metadata logged in observations_for_persistence - Completed: Step 0.5 (lines 194-217)
- [x] Single-pass behavior unchanged for <5 AC stories - Completed: Tested via AC#1 suite (4/4 assertions)
- [x] Aggregated report format identical to single-pass - Completed: Tested via AC#4 suite (6/6 assertions)
- [x] AC order preserved (document order) - Completed: Line 169 sort by ac_id
- [x] All chunk results correctly merged - Completed: Step 0.3 aggregation logic
- [x] 3-AC story: single pass, report unchanged - Completed: Tested via AC#1 suite
- [x] 5-AC story: 2 chunks (3+2) - Completed: Tested via AC#2 suite (6/6 assertions)
- [x] 6-AC story: 2 chunks (3+3) - Completed: Tested via AC#2 suite
- [x] 8-AC story: 3 chunks (3+3+2) - Completed: Tested via AC#2 suite
- [x] Downstream consumers work without modification - Completed: Tested via AC#5 suite (4/4 assertions)
- [x] observations_for_persistence contains chunking metadata - Completed: Tested via AC#6 suite (5/5 assertions)
- [x] Chunking behavior documented in ac-compliance-verifier.md - Completed: Version 2.1, updated 2026-02-09

### TDD Workflow Summary

Added AC-Level Chunking Workflow section to ac-compliance-verifier.md (src/claude/agents/).
The chunking logic is inserted as Steps 0.0-0.5 before the existing Core Verification Workflow,
preserving backward compatibility for all stories with <5 ACs.

**Files Modified:**
- `src/claude/agents/ac-compliance-verifier.md` - Added ~130 lines of chunking workflow

**Tests:**
- 6 test suites, 29 assertions, all passing
- Tests in `tests/STORY-404/`

## Notes

- **Source Recommendation:** REC-STORY368-001 from STORY-368 Phase 09 framework-analyst analysis
- **Root Cause:** Single-pass verification consumes excessive tokens for large stories
- **Impact:** ~40% peak token reduction for 5+ AC stories

## Key References

| Reference | Path | Relevance |
|-----------|------|-----------|
| AC Compliance Verifier | `src/claude/agents/ac-compliance-verifier.md` | Target file |
| Report Generation | `src/claude/agents/ac-compliance-verifier/references/report-generation.md` | Report schema |
| XML Parsing Protocol | `src/claude/agents/ac-compliance-verifier/references/xml-parsing-protocol.md` | AC parsing |

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/opus | Story Creation | Initial story created from EPIC-063 Feature 6 | STORY-404-add-ac-level-chunking.story.md |
| 2026-02-09 | claude/opus | TDD Implementation | Added AC-Level Chunking workflow, all 6 ACs verified | src/claude/agents/ac-compliance-verifier.md, tests/STORY-404/ |
| 2026-02-09 | .claude/qa-result-interpreter | QA Deep | PASSED: 29/29 tests, 0 violations, 2/2 validators | - |
