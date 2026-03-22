---
id: STORY-573
title: Market Research Report Synthesis
type: feature
epic: EPIC-074
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-535", "STORY-536", "STORY-537"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-03-04
format_version: "2.9"
---

# Story: Market Research Report Synthesis

## Description

**As a** solo founder conducting market research,
**I want** a synthesized report that aggregates market sizing, competitive analysis, and customer interview insights into a single terminal-rendered summary,
**so that** I can evaluate the full market picture in one view and feed validated findings into my business plan milestones.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-011" section="business-skills-framework">
    <quote>"Enable DevForgeAI users to validate their business ideas through structured market research and competitive analysis"</quote>
    <line_reference>EPIC-074, lines 22-24</line_reference>
    <quantified_impact>Synthesizes 3 separate research outputs into one actionable view, reducing context-switching overhead for solo founders</quantified_impact>
  </origin>

  <decision rationale="aggregation-over-dashboard">
    <selected>Single synthesized markdown report combining all research outputs</selected>
    <rejected alternative="interactive-dashboard">Terminal-only constraint eliminates interactive dashboards</rejected>
    <trade_off>Static report requires manual regeneration when source data changes</trade_off>
  </decision>

  <stakeholder role="Solo Founder" goal="market-validation">
    <quote>"I want a synthesized research report so that I can see the full market picture in one view"</quote>
    <source>EPIC-074, User Stories section</source>
  </stakeholder>

  <hypothesis id="H1" validation="user-testing" success_criteria="Founder can make go/no-go decision from single report">
    A single synthesized report reduces research-to-decision time compared to reviewing 3 separate documents
  </hypothesis>
</provenance>
```

## Acceptance Criteria

### AC#1: Report Aggregation From Three Source Files

```xml
<acceptance_criteria id="AC1" implements="SVC-001,SVC-002">
  <given>market-sizing.md, competitive-analysis.md, and customer-interviews.md exist in devforgeai/specs/business/market-research/</given>
  <when>The synthesis phase is invoked by the researching-market skill</when>
  <then>The market-analyst subagent reads all three files and produces synthesized-report.md in devforgeai/specs/business/market-research/ containing sections for Market Size Summary, Competitive Landscape Summary, Customer Insights Summary, and Combined Strategic Assessment</then>
  <verification>
    <source_files>
      <file hint="Synthesis phase implementation">src/claude/skills/researching-market/references/report-synthesis.md</file>
      <file hint="Market analyst subagent">src/claude/agents/market-analyst.md</file>
    </source_files>
    <test_file>tests/STORY-573/test_ac1_report_aggregation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: ASCII-Rendered Terminal Output

```xml
<acceptance_criteria id="AC2" implements="SVC-003">
  <given>The synthesized report has been generated</given>
  <when>The synthesis phase completes</when>
  <then>An ASCII-rendered summary is displayed to the terminal using box-drawing characters, section headers, and bullet lists that render correctly in 80-column terminals with no Unicode dependencies beyond ASCII</then>
  <verification>
    <source_files>
      <file hint="Terminal rendering logic">src/claude/skills/researching-market/references/report-synthesis.md</file>
    </source_files>
    <test_file>tests/STORY-573/test_ac2_ascii_rendering.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Partial Input Handling

```xml
<acceptance_criteria id="AC3" implements="SVC-004">
  <given>Only 1 or 2 of the 3 source files exist (e.g., customer-interviews.md is missing)</given>
  <when>The synthesis phase is invoked</when>
  <then>The report is generated from available sources, each missing source is noted with a "[Not Available]" marker in its summary section, and a warning is displayed to the terminal listing which inputs were absent</then>
  <verification>
    <source_files>
      <file hint="Partial input handling">src/claude/skills/researching-market/references/report-synthesis.md</file>
    </source_files>
    <test_file>tests/STORY-573/test_ac3_partial_input.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: EPIC-073 Integration Point

```xml
<acceptance_criteria id="AC4" implements="SVC-002">
  <given>A synthesized report has been generated</given>
  <when>The report file is written</when>
  <then>The file includes a Business Plan Integration section containing key findings formatted as actionable milestones (market validation status, competitive positioning, customer pain points) that the EPIC-073 business plan workflow can parse</then>
  <verification>
    <source_files>
      <file hint="Report template with integration section">src/claude/skills/researching-market/references/report-synthesis.md</file>
    </source_files>
    <test_file>tests/STORY-573/test_ac4_business_plan_integration.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Idempotent Regeneration

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>A synthesized-report.md already exists from a previous run</given>
  <when>The synthesis phase is invoked again</when>
  <then>The existing report is overwritten with a freshly generated version and the terminal output includes a "[Regenerated]" indicator with timestamp</then>
  <verification>
    <source_files>
      <file hint="Overwrite logic">src/claude/skills/researching-market/references/report-synthesis.md</file>
    </source_files>
    <test_file>tests/STORY-573/test_ac5_idempotent_regeneration.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

- `hint="Synthesis phase implementation"` — The report-synthesis.md reference file containing the synthesis workflow
- `hint="Market analyst subagent"` — The market-analyst subagent that performs data extraction and synthesis
- `hint="Terminal rendering logic"` — ASCII rendering functions within the synthesis reference

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "ReportSynthesisPhase"
      file_path: "src/claude/skills/researching-market/references/report-synthesis.md"
      interface: "Skill Reference File"
      lifecycle: "Stateless"
      dependencies:
        - "market-analyst subagent"
        - "market-sizing.md output"
        - "competitive-analysis.md output"
        - "customer-interviews.md output"
      requirements:
        - id: "SVC-001"
          description: "Read and parse 3 source markdown files, extracting key findings from each"
          testable: true
          test_requirement: "Test: Given 3 populated source files, synthesizer extracts at least 1 finding per source"
          priority: "Critical"
        - id: "SVC-002"
          description: "Generate synthesized-report.md with 4 mandatory sections: Market Size Summary, Competitive Landscape Summary, Customer Insights Summary, Business Plan Integration"
          testable: true
          test_requirement: "Test: Output file contains all 4 required ## headers"
          priority: "Critical"
        - id: "SVC-003"
          description: "Render ASCII terminal summary within 80-column width"
          testable: true
          test_requirement: "Test: All output lines are <= 80 characters when terminal width is 80"
          priority: "High"
        - id: "SVC-004"
          description: "Handle missing or empty source files without crashing"
          testable: true
          test_requirement: "Test: With 0, 1, 2, or 3 source files present (including empty files), synthesis completes without unhandled exception"
          priority: "High"
        - id: "SVC-005"
          description: "Overwrite existing report on regeneration with timestamp indicator"
          testable: true
          test_requirement: "Test: When synthesized-report.md exists, re-invocation overwrites it and terminal shows [Regenerated] with ISO 8601 timestamp"
          priority: "Medium"

    - type: "Configuration"
      name: "SynthesisConfig"
      file_path: "src/claude/skills/researching-market/references/report-synthesis.md"
      required_keys:
        - key: "source_directory"
          type: "string"
          example: "devforgeai/specs/business/market-research/"
          required: true
          default: "devforgeai/specs/business/market-research/"
          validation: "Must be valid directory path"
          test_requirement: "Test: Default path resolves to expected directory"
        - key: "output_filename"
          type: "string"
          example: "synthesized-report.md"
          required: true
          default: "synthesized-report.md"
          validation: "Must end in .md"
          test_requirement: "Test: Output filename matches expected pattern"
        - key: "terminal_width"
          type: "int"
          example: "80"
          required: false
          default: "80"
          validation: "Must be >= 40"
          test_requirement: "Test: Terminal width defaults to 80 when not specified"

  business_rules:
    - id: "BR-001"
      rule: "Synthesis requires at least 1 of 3 source files to produce a report"
      trigger: "When synthesis phase is invoked"
      validation: "Check existence of market-sizing.md, competitive-analysis.md, customer-interviews.md"
      error_handling: "If all 3 missing, exit with error message and no output file created"
      test_requirement: "Test: With 0 source files, synthesis exits with descriptive error and no report file"
      priority: "Critical"
    - id: "BR-002"
      rule: "Empty source files (0 bytes) are treated as missing"
      trigger: "When reading source files"
      validation: "Check file size > 0 bytes"
      error_handling: "Show [Empty Input — No Data] in corresponding section"
      test_requirement: "Test: Empty file produces [Empty Input — No Data] marker in report"
      priority: "High"
    - id: "BR-003"
      rule: "Report writes must be atomic (temp file then rename)"
      trigger: "When writing synthesized-report.md"
      validation: "Write to temp file first, rename on success"
      error_handling: "If write fails, temp file remains, no partial report"
      test_requirement: "Test: Interrupted write produces no partial synthesized-report.md"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Synthesis completion time under 3 seconds"
      metric: "< 3 seconds for 3 source files totaling up to 50 KB"
      test_requirement: "Test: Synthesis of 3 × 50 KB files completes in < 3 seconds"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Terminal rendering time under 500ms"
      metric: "< 500ms after report generation"
      test_requirement: "Test: ASCII output renders in < 500ms"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Zero unhandled exceptions on any input combination"
      metric: "0 unhandled exceptions across all test permutations"
      test_requirement: "Test: All permutations of 0-3 files (present/empty/malformed) complete without crash"
      priority: "Critical"
    - id: "NFR-004"
      category: "Scalability"
      requirement: "Handle individual input files up to 100 KB"
      metric: "No degradation with files up to 100 KB each"
      test_requirement: "Test: 100 KB source file processes without timeout or memory error"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "market-analyst subagent"
    limitation: "Subagent synthesis quality depends on source file structure consistency; unstructured markdown may produce lower-quality summaries"
    decision: "workaround:best-effort extraction with [Partial Parse] warnings"
    discovered_phase: "Architecture"
    impact: "Some source files may not be fully represented in synthesized report"
  - id: TL-002
    component: "Terminal rendering"
    limitation: "ASCII box-drawing characters may not render correctly in all terminal emulators"
    decision: "workaround:use only standard ASCII characters (+-|) for maximum compatibility"
    discovered_phase: "Architecture"
    impact: "Visual aesthetics may vary across terminal environments"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Synthesis phase:** < 3 seconds (p95) for 3 source files up to 50 KB each
- **Terminal rendering:** < 500ms (p95) after report generation

**Throughput:**
- Single invocation at a time (CLI workflow, no concurrent users)

**Performance Test:**
- Synthesis of 3 × 50 KB files completes in < 3 seconds
- Memory usage < 25 MB during synthesis phase

---

### Security

**Authentication:**
- None (local file operations only)

**Authorization:**
- None (framework-internal skill)

**Data Protection:**
- Sensitive fields: None (market research data is user-generated)
- No external network calls during synthesis
- No secrets or credentials referenced in output

**Security Testing:**
- [ ] No hardcoded secrets in output
- [ ] No external network calls
- [ ] Read-only access to source files

**Rate Limiting:**
- Not applicable (CLI tool)

---

### Scalability

**Horizontal Scaling:**
- Stateless design: Yes
- Load balancing: Not Required

**Database:**
- Not applicable (file-based)

**Caching:**
- Cache strategy: None (stateless execution)

---

### Reliability

**Error Handling:**
- All file I/O errors caught and reported as user-facing messages
- Atomic file writes: write to temporary file then rename
- Exit code 0 on success (even with partial inputs), exit code 1 only when zero inputs available

**Retry Logic:**
- Retry transient failures: No
- Stateless execution; user re-invokes manually if needed

**Monitoring:**
- Terminal output confirms success/failure
- Report includes generation timestamp

---

### Observability

**Logging:**
- Log level: INFO
- Terminal output shows which source files were found/missing
- Include generation timestamp in report YAML header

**Metrics:**
- Source files found count (0-3)
- Sections generated count
- Regeneration indicator (first run vs overwrite)

**Tracing:**
- Distributed tracing: No
- Terminal output provides sequential phase visibility

---

## Dependencies

### Prerequisite Stories

Stories that must complete BEFORE this story can start:

- [ ] **STORY-535:** Market Sizing Guided Workflow
  - **Why:** Produces market-sizing.md source file for synthesis
  - **Status:** Backlog

- [ ] **STORY-536:** Competitive Landscape Analysis
  - **Why:** Produces competitive-analysis.md source file for synthesis
  - **Status:** Backlog

- [ ] **STORY-537:** Customer Interview Question Generator
  - **Why:** Produces customer-interviews.md source file for synthesis
  - **Status:** Backlog

### External Dependencies

None — framework operates entirely within Claude Code Terminal.

### Technology Dependencies

No new packages required. Uses existing:
- market-analyst subagent (created in STORY-536)
- researching-market skill (created in STORY-538)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** All 3 source files present → synthesized-report.md generated with 4 sections
2. **Edge Cases:**
   - Only 1 source file present → report generated with 2 "[Not Available]" sections
   - Only 2 source files present → report generated with 1 "[Not Available]" section
   - All 3 source files missing → error message, no report generated
   - Empty source file (0 bytes) → treated as missing with "[Empty Input]" marker
   - Malformed markdown source → best-effort extraction with "[Partial Parse]" warning
3. **Error Cases:**
   - Source directory does not exist → clear error message
   - Write permission denied → clear error message
   - Existing report overwrite → "[Regenerated]" indicator shown

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Synthesis Flow:** Run full researching-market skill with synthesis phase, verify output file
2. **market-analyst Subagent Integration:** Verify subagent correctly extracts findings from source files

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Report Aggregation From Three Source Files

- [ ] Read 3 source files from devforgeai/specs/business/market-research/ - **Phase:** 2 - **Evidence:** test_ac1_report_aggregation.py
- [ ] Invoke market-analyst subagent for synthesis - **Phase:** 2 - **Evidence:** test_ac1_report_aggregation.py
- [ ] Generate synthesized-report.md with 4 required sections - **Phase:** 3 - **Evidence:** test_ac1_report_aggregation.py
- [ ] Verify file written to correct directory - **Phase:** 3 - **Evidence:** test_ac1_report_aggregation.py

### AC#2: ASCII-Rendered Terminal Output

- [ ] ASCII box rendering with standard characters - **Phase:** 2 - **Evidence:** test_ac2_ascii_rendering.py
- [ ] 80-column width compliance - **Phase:** 3 - **Evidence:** test_ac2_ascii_rendering.py
- [ ] Section headers and bullet lists render correctly - **Phase:** 3 - **Evidence:** test_ac2_ascii_rendering.py

### AC#3: Partial Input Handling

- [ ] 1 of 3 files present → report with 2 "[Not Available]" markers - **Phase:** 2 - **Evidence:** test_ac3_partial_input.py
- [ ] 2 of 3 files present → report with 1 "[Not Available]" marker - **Phase:** 2 - **Evidence:** test_ac3_partial_input.py
- [ ] 0 files present → error message, no report - **Phase:** 2 - **Evidence:** test_ac3_partial_input.py
- [ ] Empty file treated as missing - **Phase:** 3 - **Evidence:** test_ac3_partial_input.py

### AC#4: EPIC-073 Integration Point

- [ ] Business Plan Integration section present in output - **Phase:** 2 - **Evidence:** test_ac4_business_plan_integration.py
- [ ] Actionable milestones formatted for parsing - **Phase:** 3 - **Evidence:** test_ac4_business_plan_integration.py

### AC#5: Idempotent Regeneration

- [ ] Existing report overwritten on re-invocation - **Phase:** 2 - **Evidence:** test_ac5_idempotent_regeneration.py
- [ ] "[Regenerated]" indicator with timestamp shown - **Phase:** 3 - **Evidence:** test_ac5_idempotent_regeneration.py

---

**Checklist Progress:** 0/15 items complete (0%)

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

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Report synthesis reference file created at src/claude/skills/researching-market/references/report-synthesis.md
- [ ] Synthesis phase integrated into researching-market skill SKILL.md
- [ ] ASCII terminal rendering implemented with 80-column width compliance
- [ ] Partial input handling with "[Not Available]" and "[Empty Input]" markers
- [ ] Business Plan Integration section with parseable milestone format
- [ ] Atomic file write (temp file → rename) for synthesized-report.md
- [ ] Idempotent regeneration with "[Regenerated]" indicator

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (0/1/2/3 source files, empty files, malformed markdown)
- [ ] Data validation enforced (source file existence, output section verification)
- [ ] NFRs met (< 3s synthesis, < 500ms rendering, zero unhandled exceptions)
- [ ] Code coverage > 95% for synthesis logic

### Testing
- [ ] Unit tests for report aggregation (AC1)
- [ ] Unit tests for ASCII rendering (AC2)
- [ ] Unit tests for partial input handling (AC3)
- [ ] Unit tests for business plan integration section (AC4)
- [ ] Unit tests for idempotent regeneration (AC5)
- [ ] Integration tests for end-to-end synthesis flow

### Documentation
- [ ] Report synthesis reference file includes usage instructions
- [ ] SKILL.md updated with synthesis phase documentation
- [ ] Edge case behavior documented in reference file

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
| 2026-03-04 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-074 Feature 5 | STORY-573-market-research-report-synthesis.story.md |

## Notes

**Design Decisions:**
- Single markdown file output rather than multi-file report for simplicity and terminal-friendliness
- ASCII-only rendering (no Unicode box-drawing) for maximum terminal compatibility
- Best-effort extraction for malformed inputs rather than hard failure
- Atomic writes via temp-file-then-rename pattern for reliability

**Open Questions:**
- [ ] Exact format of "actionable milestones" for EPIC-073 integration — **Owner:** DevForgeAI — **Due:** Sprint 2

**Related ADRs:**
- ADR-017: Skill Naming Convention (gerund-object)

**References:**
- EPIC-074: Market Research & Competition
- STORY-535: Market Sizing Guided Workflow
- STORY-536: Competitive Landscape Analysis
- STORY-537: Customer Interview Question Generator
- STORY-538: /market-research Command & Skill Assembly

---

Story Template Version: 2.9
Last Updated: 2026-03-04
