---
id: STORY-380
title: "Mine Core Anthropic Courses for Prompt Engineering Patterns"
type: documentation
epic: EPIC-060
sprint: Backlog
status: QA Approved
points: 8
depends_on: []
priority: Medium
advisory: false
assigned_to: null
created: 2026-02-06
updated: 2026-02-10
format_version: "2.8"
---

# Story: Mine Core Anthropic Courses for Prompt Engineering Patterns

## Description

**As a** Framework Owner,
**I want** all 5 Anthropic courses (API fundamentals, prompt engineering interactive tutorial, real-world prompting, prompt evaluations, and tool use) mined for prompt engineering patterns with DevForgeAI applicability ratings,
**so that** I have a comprehensive, research-backed methodology foundation that enables evidence-based improvements across all 32+ subagents, 17 skills, and 39 commands without re-reading source repos in future sessions.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-010" section="problem-statement">
    <quote>"Review Anthropic's official prompt engineering repos to systematically improve DevForgeAI framework's agents, skills, and commands"</quote>
    <line_reference>lines 7-7</line_reference>
    <quantified_impact>Evidence-based improvements across 32+ subagents, 17 skills, and 39 commands</quantified_impact>
  </origin>

  <decision rationale="prioritize-courses-first">
    <selected>Mine 5 courses as Feature 1 (foundational methodology before specialized repos)</selected>
    <rejected alternative="mine-all-12-repos-at-once">
      Scope too broad for single story; progressive extraction maintains quality
    </rejected>
    <trade_off>Sequential extraction takes longer but ensures thorough pattern analysis per source</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="comprehensive-methodology-foundation">
    <quote>"Establishes core prompt engineering methodology from authoritative source material"</quote>
    <source>EPIC-060, Feature 1 description</source>
  </stakeholder>

  <hypothesis id="H1" validation="pattern-count-validation" success_criteria="At least 10 patterns extracted from 5 courses with High/Medium applicability">
    Anthropic's courses contain sufficient actionable patterns to improve DevForgeAI prompt engineering quality
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: All 5 Courses Analyzed with Patterns Extracted

```xml
<acceptance_criteria id="AC1">
  <given>The 5 Anthropic courses exist at tmp/anthropic/courses/ (anthropic_api_fundamentals with 6 notebooks, prompt_engineering_interactive_tutorial with 10+ chapters including appendices, real_world_prompting with 5 notebooks, prompt_evaluations with 9 lessons, and tool_use with 6 notebooks)</given>
  <when>The researcher reads and analyzes each course's notebooks and supporting materials</when>
  <then>At least 1 pattern is extracted from each of the 5 courses, with no course skipped or marked "not applicable" without documented justification</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-380/test_ac1_all_courses_analyzed.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Each Pattern Has DevForgeAI Applicability Rating

```xml
<acceptance_criteria id="AC2">
  <given>A set of extracted patterns from all 5 courses</given>
  <when>Each pattern is evaluated against DevForgeAI's architecture (subagents in .claude/agents/, skills in .claude/skills/, commands in .claude/commands/, operating within Claude Code Terminal constraints)</when>
  <then>Every pattern entry includes an applicability rating of exactly one of: High, Medium, Low, or N/A, with a 1-2 sentence rationale explaining the rating</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-380/test_ac2_applicability_ratings.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Findings Documented in Structured Markdown Format

```xml
<acceptance_criteria id="AC3">
  <given>All patterns have been extracted and rated</given>
  <when>The research document is created</when>
  <then>The output document follows a consistent structure where each pattern entry contains: pattern name, source course and lesson/notebook reference, description (2-5 sentences), applicability rating with rationale, and a DevForgeAI recommendation (specific component or category the pattern could improve)</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-380/test_ac3_structured_format.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Patterns Include Source References

```xml
<acceptance_criteria id="AC4">
  <given>A pattern extracted from a course</given>
  <when>The pattern is documented in the research artifact</when>
  <then>The source reference includes the course name (e.g., "Real World Prompting"), the specific notebook or lesson file name (e.g., "04_call_summarizer.ipynb"), and sufficient context to locate the pattern in the source material without re-reading the entire course</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-380/test_ac4_source_references.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Research Output Stored at Correct Location

```xml
<acceptance_criteria id="AC5">
  <given>The research artifact is complete</given>
  <when>The document is saved to disk</when>
  <then>It is stored at devforgeai/specs/research/prompt-engineering-patterns.md (per source-tree.md and EPIC-060 specification), and the file is readable via a single Read() call or structured with clear section headers enabling progressive section reads</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-380/test_ac5_output_location.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Research Output Within Size Constraints

```xml
<acceptance_criteria id="AC6">
  <given>The completed research document</given>
  <when>The line count is measured</when>
  <then>The document contains fewer than 2,000 lines total (per EPIC-060 constraint), and each pattern entry is self-contained (understandable without cross-referencing other entries in the document)</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-380/test_ac6_size_constraints.sh</test_file>
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
      name: "Research Output Document"
      file_path: "devforgeai/specs/research/prompt-engineering-patterns.md"
      required_keys:
        - key: "Pattern Catalog Section"
          type: "markdown"
          example: "## Pattern Catalog with structured entries"
          required: true
          validation: "Each entry has: name, source, description, applicability, recommendation"
          test_requirement: "Test: Verify all pattern entries contain 5 required fields"
        - key: "Table of Contents"
          type: "markdown"
          example: "## Table of Contents with navigation links"
          required: true
          validation: "TOC entries match actual section headers"
          test_requirement: "Test: Verify TOC links resolve to valid sections"
        - key: "Executive Summary"
          type: "markdown"
          example: "## Executive Summary with key findings"
          required: true
          validation: "Summary includes total pattern count and rating distribution"
          test_requirement: "Test: Verify summary contains pattern count and rating breakdown"

    - type: "Service"
      name: "CourseAnalysisWorkflow"
      file_path: "N/A - manual research workflow"
      interface: "Research methodology"
      lifecycle: "One-time execution"
      dependencies:
        - "tmp/anthropic/courses/ (5 course directories)"
        - "devforgeai/specs/research/ (output directory)"
      requirements:
        - id: "SVC-001"
          description: "Read and analyze all notebooks in anthropic_api_fundamentals (6 notebooks)"
          testable: true
          test_requirement: "Test: Verify patterns extracted from anthropic_api_fundamentals course"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-002"
          description: "Read and analyze all chapters in prompt_engineering_interactive_tutorial (10+ chapters)"
          testable: true
          test_requirement: "Test: Verify patterns extracted from prompt_engineering_interactive_tutorial"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-003"
          description: "Read and analyze all notebooks in real_world_prompting (5 notebooks)"
          testable: true
          test_requirement: "Test: Verify patterns extracted from real_world_prompting course"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-004"
          description: "Read and analyze all lessons in prompt_evaluations (9 lessons)"
          testable: true
          test_requirement: "Test: Verify patterns extracted from prompt_evaluations course"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-005"
          description: "Read and analyze all notebooks in tool_use (6 notebooks)"
          testable: true
          test_requirement: "Test: Verify patterns extracted from tool_use course"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-006"
          description: "Rate each pattern with exactly one of: High, Medium, Low, N/A applicability"
          testable: true
          test_requirement: "Test: Verify every pattern has valid applicability rating"
          priority: "Critical"
          implements_ac: ["AC2"]
        - id: "SVC-007"
          description: "Document each pattern with structured format: name, source, description, rating, recommendation"
          testable: true
          test_requirement: "Test: Verify pattern entry structure matches required format"
          priority: "Critical"
          implements_ac: ["AC3"]
        - id: "SVC-008"
          description: "Include specific source reference (course name + notebook/lesson filename) for each pattern"
          testable: true
          test_requirement: "Test: Verify all source references contain course name and filename"
          priority: "High"
          implements_ac: ["AC4"]

  business_rules:
    - id: "BR-001"
      rule: "Applicability rating must be exactly one of: High, Medium, Low, N/A"
      trigger: "When assigning applicability to each extracted pattern"
      validation: "Grep for valid rating values; reject any other format"
      error_handling: "Flag pattern for manual review if rating unclear"
      test_requirement: "Test: Verify no patterns have invalid or missing ratings"
      priority: "Critical"

    - id: "BR-002"
      rule: "Duplicate patterns across courses must be consolidated into single entry citing all sources"
      trigger: "When same technique found in multiple courses"
      validation: "No duplicate pattern names in final document"
      error_handling: "Merge entries, cite all courses, note which provides best treatment"
      test_requirement: "Test: Verify no duplicate pattern names in document"
      priority: "High"

    - id: "BR-003"
      rule: "Minimum 10 patterns total across all 5 courses"
      trigger: "After all courses analyzed"
      validation: "Count pattern entries in final document >= 10"
      error_handling: "If fewer than 10, revisit courses for missed patterns"
      test_requirement: "Test: Verify document contains at least 10 pattern entries"
      priority: "High"

    - id: "BR-004"
      rule: "Document must be under 2,000 lines"
      trigger: "Before final save"
      validation: "Line count check on completed document"
      error_handling: "If over limit, consolidate verbose entries or split into summary + detailed sections"
      test_requirement: "Test: Verify document line count < 2000"
      priority: "High"

    - id: "BR-005"
      rule: "Prioritize Anthropic-direct variant over AmazonBedrock/boto3 variant when duplicates exist"
      trigger: "When reading prompt_engineering_interactive_tutorial chapters"
      validation: "Source references point to Anthropic directory (not AmazonBedrock)"
      error_handling: "Replace Bedrock references with Anthropic equivalents"
      test_requirement: "Test: Verify no AmazonBedrock/boto3 source references in final document"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Research document loadable in single Read() call"
      metric: "Document under 2,000 lines (fits in Read() default limit)"
      test_requirement: "Test: Verify Read() returns complete document without truncation"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Document is valid Markdown rendering in GitHub, VS Code, and Claude Code Terminal"
      metric: "Zero Markdown syntax errors; all headers, lists, and code fences properly closed"
      test_requirement: "Test: Verify Markdown syntax validity"
      priority: "High"

    - id: "NFR-003"
      category: "Scalability"
      requirement: "Document structure supports appending patterns from future research stories"
      metric: "Pattern catalog uses consistent entry format parseable by Grep()"
      test_requirement: "Test: Verify Grep(pattern='Applicability:') returns all pattern entries"
      priority: "Medium"

    - id: "NFR-004"
      category: "Security"
      requirement: "No secrets, API keys, or credentials in research document"
      metric: "Zero matches for secret patterns (api_key, password, token, secret)"
      test_requirement: "Test: Verify Grep for secret patterns returns 0 matches"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Claude Code Terminal context window"
    limitation: "Cannot load all 36+ notebooks simultaneously; must use progressive reading"
    decision: "workaround:Read individual notebooks sequentially, extract patterns, summarize per course"
    discovered_phase: "Architecture"
    impact: "Research must be conducted progressively, not in single batch"

  - id: TL-002
    component: "Jupyter notebook rendering"
    limitation: "Read() tool shows raw notebook JSON for .ipynb files; code outputs may not render cleanly"
    decision: "workaround:Focus on markdown cells and code cell source; ignore rendered outputs"
    discovered_phase: "Architecture"
    impact: "Some visual patterns in notebook outputs may be missed"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Document Load Time:**
- Research document loads via single `Read()` call: target 800-1,500 lines
- Each section independently readable via `Read()` with `offset` and `limit` parameters
- No computation or API calls required to consume output — pure Markdown text

### Security

- No secrets, API keys, or credentials in research document
- No executable code blocks that could be mistakenly run — all code examples wrapped in fenced blocks with "Example (from source):" labels
- Source material paths reference only local `tmp/anthropic/courses/` directory

### Reliability

- Valid Markdown rendering in GitHub, VS Code, and Claude Code Terminal Read() output
- All internal cross-references use relative anchors resolving within same document
- Document survives context window clears — fresh session can Read() and apply patterns immediately

### Scalability

- Structure supports appending patterns from future research stories without restructuring
- Consistent entry format enables Grep() parsing (e.g., `Grep(pattern="Applicability: High")`)
- Table of contents at document top enables quick navigation

---

## Edge Cases & Error Handling

1. **Course content too large to process in single context window:** Some courses contain 10+ notebooks with extensive examples. Use progressive reading — process individual notebooks, extract patterns, summarize, then move to next. Prioritize Anthropic-direct variant over AmazonBedrock variant when duplicates exist.

2. **Duplicate or overlapping patterns across courses:** Same technique (e.g., chain-of-thought) may appear in multiple courses. Create single consolidated pattern entry citing all source courses, noting which provides most detailed treatment.

3. **Patterns not applicable to Claude Code Terminal context:** API-level concerns (streaming config, vision processing, Bedrock integration) get "N/A" rating with brief explanation, preserving knowledge for potential future use.

4. **Notebooks primarily contain code with minimal explanatory text:** Extract underlying prompt engineering principle from code patterns rather than documenting syntax.

5. **Course content references deprecated API features:** Evaluate for current relevance. Note deprecation in applicability rating rationale.

---

## Dependencies

### Prerequisite Stories

None — this is the first research story in EPIC-060.

### External Dependencies

- [x] **12 Anthropic repos cloned:** Available at `tmp/anthropic/` (CONFIRMED in EPIC-060)

### Technology Dependencies

None — uses only Read(), Glob(), Grep() tools and Write() for output.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for validation checks

**Test Scenarios:**
1. **Happy Path:** All 5 courses analyzed, 10+ patterns extracted, document under 2,000 lines
2. **Edge Cases:**
   - Document at 1,999 lines (just under limit)
   - Duplicate pattern name detected
   - Pattern with N/A rating has justification
3. **Error Cases:**
   - Missing course directory (Read() fails)
   - Pattern without applicability rating
   - Document exceeds 2,000 lines

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **End-to-End Research Flow:** Run research workflow, verify output document structure
2. **Grep Parseability:** Verify patterns findable via Grep() queries

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: All 5 Courses Analyzed

- [x] anthropic_api_fundamentals notebooks read and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [x] prompt_engineering_interactive_tutorial chapters read and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [x] real_world_prompting notebooks read and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [x] prompt_evaluations lessons read and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [x] tool_use notebooks read and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md

### AC#2: Applicability Ratings

- [x] Every pattern has exactly one rating (High/Medium/Low/N/A) - **Phase:** 2 - **Evidence:** Grep validation
- [x] Each rating includes 1-2 sentence rationale - **Phase:** 2 - **Evidence:** Pattern entry structure

### AC#3: Structured Format

- [x] Each pattern has: name, source, description, rating, recommendation - **Phase:** 2 - **Evidence:** Document structure validation
- [x] Descriptions are 2-5 sentences (30-150 words) - **Phase:** 2 - **Evidence:** Word count per entry

### AC#4: Source References

- [x] Each pattern cites course name - **Phase:** 2 - **Evidence:** Grep for course directory names
- [x] Each pattern cites specific notebook/lesson filename - **Phase:** 2 - **Evidence:** Grep for .ipynb/.md filenames

### AC#5: Output Location

- [x] File exists at devforgeai/specs/research/prompt-engineering-patterns.md - **Phase:** 5 - **Evidence:** Glob/Read verification

### AC#6: Size Constraints

- [x] Document under 2,000 lines - **Phase:** 5 - **Evidence:** wc -l output (418 lines)
- [x] Pattern entries are self-contained - **Phase:** 2 - **Evidence:** Manual review

---

**Checklist Progress:** 13/13 items complete (100%)

---

## Definition of Done

### Implementation
- [x] All 5 Anthropic courses read and analyzed - Completed: 24 patterns extracted from all 5 courses (anthropic_api_fundamentals, prompt_engineering_interactive_tutorial, real_world_prompting, prompt_evaluations, tool_use)
- [x] At least 10 patterns extracted across courses - Completed: 24 patterns total (12 High, 8 Medium, 3 Low, 1 N/A applicability)
- [x] Each pattern has complete entry (name, source, description, rating, recommendation) - Completed: All 24 patterns have 5 required fields verified by ac-compliance-verifier
- [x] Research document written to devforgeai/specs/research/prompt-engineering-patterns.md - Completed: 418-line structured Markdown document
- [x] Document includes Table of Contents and Executive Summary - Completed: TOC with navigation, Executive Summary with pattern count and rating distribution
- [x] Duplicate patterns consolidated with multi-course citations - Completed: Patterns 21-24 are cross-course consolidated patterns

### Quality
- [x] All 6 acceptance criteria have passing tests - Completed: 6 test scripts, 38/38 assertions GREEN
- [x] Document under 2,000 lines - Completed: 418 lines (21% of limit)
- [x] All applicability ratings are valid (High/Medium/Low/N/A) - Completed: All 24 ratings validated
- [x] No vague descriptions without specific metrics - Completed: Each description 2-5 sentences with specific details
- [x] No secrets or credentials in document - Completed: test_ac5 validates zero secret patterns
- [x] Valid Markdown syntax throughout - Completed: All fences closed, headers valid

### Testing
- [x] Shell tests validate document structure - Completed: test_ac3_structured_format.sh (9 assertions)
- [x] Grep tests validate pattern entry format - Completed: test_ac2_applicability_ratings.sh (5 assertions)
- [x] Line count validation passes - Completed: test_ac6_size_constraints.sh (5 assertions)
- [x] Source reference validation passes - Completed: test_ac4_source_references.sh (5 assertions)
- [x] Rating value validation passes - Completed: test_ac2_applicability_ratings.sh (5 assertions)

### Documentation
- [x] Research document is self-contained and readable in fresh session - Completed: 418 lines, single Read() call, no external dependencies
- [x] Executive summary provides quick orientation - Completed: Lines 25-40 with pattern count, rating distribution, key findings
- [x] Each pattern entry understandable without cross-references - Completed: Self-contained entries with all 5 fields

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-10
**Branch:** main

- [x] All 5 Anthropic courses read and analyzed - Completed: 24 patterns extracted from all 5 courses (anthropic_api_fundamentals, prompt_engineering_interactive_tutorial, real_world_prompting, prompt_evaluations, tool_use)
- [x] At least 10 patterns extracted across courses - Completed: 24 patterns total (12 High, 8 Medium, 3 Low, 1 N/A applicability)
- [x] Each pattern has complete entry (name, source, description, rating, recommendation) - Completed: All 24 patterns have 5 required fields verified by ac-compliance-verifier
- [x] Research document written to devforgeai/specs/research/prompt-engineering-patterns.md - Completed: 418-line structured Markdown document
- [x] Document includes Table of Contents and Executive Summary - Completed: TOC with navigation, Executive Summary with pattern count and rating distribution
- [x] Duplicate patterns consolidated with multi-course citations - Completed: Patterns 21-24 are cross-course consolidated patterns
- [x] All 6 acceptance criteria have passing tests - Completed: 6 test scripts, 38/38 assertions GREEN
- [x] Document under 2,000 lines - Completed: 418 lines (21% of limit)
- [x] All applicability ratings are valid (High/Medium/Low/N/A) - Completed: All 24 ratings validated
- [x] No vague descriptions without specific metrics - Completed: Each description 2-5 sentences with specific details
- [x] No secrets or credentials in document - Completed: test_ac5 validates zero secret patterns
- [x] Valid Markdown syntax throughout - Completed: All fences closed, headers valid
- [x] Shell tests validate document structure - Completed: test_ac3_structured_format.sh (9 assertions)
- [x] Grep tests validate pattern entry format - Completed: test_ac2_applicability_ratings.sh (5 assertions)
- [x] Line count validation passes - Completed: test_ac6_size_constraints.sh (5 assertions)
- [x] Source reference validation passes - Completed: test_ac4_source_references.sh (5 assertions)
- [x] Rating value validation passes - Completed: test_ac2_applicability_ratings.sh (5 assertions)
- [x] Research document is self-contained and readable in fresh session - Completed: 418 lines, single Read() call, no external dependencies
- [x] Executive summary provides quick orientation - Completed: Lines 25-40 with pattern count, rating distribution, key findings
- [x] Each pattern entry understandable without cross-references - Completed: Self-contained entries with all 5 fields

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 6 shell test scripts covering all 6 acceptance criteria
- 38 total test assertions following PASS/FAIL pattern
- Test files: tests/STORY-380/test_ac{1-6}_*.sh

**Phase 03 (Green): Implementation**
- Mined all 5 Anthropic courses for prompt engineering patterns
- Created research document with 24 structured pattern entries
- All 38 test assertions passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Reviewed by refactoring-specialist and code-reviewer subagents
- Document structure clean, no refactoring needed

**Phase 05 (Integration): Full Validation**
- Full test suite executed: 38/38 assertions GREEN
- AC compliance verified by ac-compliance-verifier (all 6 ACs PASS)

**Phase 06 (Deferral Challenge): DoD Validation**
- All 20 DoD items implemented (100%)
- Zero deferrals — no deferral challenge needed

### Files Created/Modified

**Created:**
- devforgeai/specs/research/prompt-engineering-patterns.md (418 lines, 24 patterns)
- tests/STORY-380/test_ac1_all_courses_analyzed.sh (8 assertions)
- tests/STORY-380/test_ac2_applicability_ratings.sh (5 assertions)
- tests/STORY-380/test_ac3_structured_format.sh (9 assertions)
- tests/STORY-380/test_ac4_source_references.sh (5 assertions)
- tests/STORY-380/test_ac5_output_location.sh (6 assertions)
- tests/STORY-380/test_ac6_size_constraints.sh (5 assertions)

**Modified:**
- devforgeai/specs/Stories/STORY-380-mine-core-anthropic-courses.story.md

### Test Results

- **Total tests:** 6 scripts, 38 assertions
- **Pass rate:** 100%
- **Execution time:** <5 seconds total

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-06 | claude/story-requirements-analyst | Created | Story created from EPIC-060 Feature 1 | STORY-380-mine-core-anthropic-courses.story.md |
| 2026-02-10 | .claude/opus | DoD Update (Phase 07) | Development complete, all 20 DoD items verified, 38/38 tests passing | STORY-380-mine-core-anthropic-courses.story.md, devforgeai/specs/research/prompt-engineering-patterns.md |
| 2026-02-10 | claude/qa-result-interpreter | QA Light | PASSED: 38/38 tests, 0 violations, 100% traceability | - |
| 2026-02-10 | .claude/qa-result-interpreter | QA Deep | PASSED: 38/38 tests, 0 violations, 97% quality score, 1/1 validators | - |

## Notes

**Design Decisions:**
- Research story type = "documentation" (skips integration testing phase in TDD workflow)
- Minimum 10 patterns (not 30+) because 30+ is the target across all 12 repos, not a single story
- Progressive reading approach due to context window constraints

**Open Questions:**
- None — scope is well-defined by EPIC-060 Feature 1 and BRAINSTORM-010

**Related ADRs:**
- None required — research-only story, no architecture changes

**References:**
- EPIC-060: Prompt Engineering Research & Knowledge Capture
- BRAINSTORM-010: Prompt Engineering Improvement from Anthropic Repos

---

Story Template Version: 2.8
Last Updated: 2026-02-10
