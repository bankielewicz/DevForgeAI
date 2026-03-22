---
id: STORY-383
title: "Mine Dev Tools and Domain Repos for Specialized Patterns"
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
updated: 2026-02-06
format_version: "2.8"
---

# Story: Mine Dev Tools and Domain Repos for Specialized Patterns

## Description

**As a** Framework Owner,
**I want** all 8 specialized Anthropic repos (claude-code-action, claude-code-security-review, claude-plugins-official, claude-constitution, healthcare, life-sciences, original_performance_takehome, and beam) mined for domain-specific and dev-tool prompt engineering patterns with DevForgeAI applicability ratings and agent mapping,
**so that** I have a comprehensive catalog of specialized patterns that can improve domain-specific subagents (security-auditor, deployment-engineer, code-reviewer) and identify new capability opportunities not covered by the foundational course patterns extracted in STORY-380 through STORY-382.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-010" section="problem-statement">
    <quote>"Review Anthropic's official prompt engineering repos to systematically improve DevForgeAI framework's agents, skills, and commands"</quote>
    <line_reference>lines 7-7</line_reference>
    <quantified_impact>Domain-specific patterns for 8+ specialized subagents (security-auditor, deployment-engineer, code-reviewer, etc.)</quantified_impact>
  </origin>

  <decision rationale="split-repos-by-specialization">
    <selected>Mine 8 remaining repos as Feature 4 (specialized/domain repos separate from foundational courses)</selected>
    <rejected alternative="merge-all-12-repos-into-single-story">
      8 specialized repos have fundamentally different content types (GitHub Actions YAML, SKILL.md files, security prompts, constitution text, performance benchmarks) vs. course notebooks — requires domain-aware analysis
    </rejected>
    <trade_off>Separate story allows prioritized analysis (P1 dev tools before P2 domain repos) without blocking foundational course extraction</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="domain-agent-improvement">
    <quote>"Domain-specific patterns for specialized agents (security-auditor, deployment-engineer, etc.)"</quote>
    <source>EPIC-060, Feature 4 description</source>
  </stakeholder>

  <hypothesis id="H2" validation="pattern-count-validation" success_criteria="At least 8 domain-specific patterns extracted across 8 repos with agent mapping to existing DevForgeAI subagents">
    Anthropic's specialized repos contain actionable domain patterns beyond what foundational courses cover, particularly for CI/CD automation, security review, plugin architecture, and healthcare/life-sciences domain prompting
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: All 8 Repos Analyzed with Patterns Extracted

```xml
<acceptance_criteria id="AC1">
  <given>The 8 Anthropic repos exist at tmp/anthropic/ (claude-code-action with GitHub Action source, CLAUDE.md, and .claude/ agents; claude-code-security-review with security prompts in claudecode/prompts.py and .claude/commands/security-review.md; claude-plugins-official with plugin directory containing 12+ external plugins and 8+ official plugins; claude-constitution with 20260120-constitution.md; healthcare with clinical-trial-protocol-skill, prior-auth-review-skill, fhir-developer-skill, and MCP plugins; life-sciences with clinical-trial-protocol-skill, nextflow-development, scientific-problem-selection, instrument-data-to-allotrope skills, and MCP plugins; original_performance_takehome with performance benchmark Python files; beam with Apache Beam fork and CI/CD infrastructure)</given>
  <when>The researcher reads and analyzes each repo's key files (SKILL.md, prompts, CLAUDE.md, README.md, action.yml, plugin.json, agents, commands, references)</when>
  <then>At least 1 pattern is extracted from each of the 8 repos, with no repo skipped or marked "not applicable" without documented justification citing specific files examined</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac1_all_repos_analyzed.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Each Pattern Has DevForgeAI Applicability Rating with Agent Mapping

```xml
<acceptance_criteria id="AC2">
  <given>A set of extracted patterns from all 8 repos</given>
  <when>Each pattern is evaluated against DevForgeAI's architecture (32+ subagents in .claude/agents/, 18 skills in .claude/skills/, operating within Claude Code Terminal constraints)</when>
  <then>Every pattern entry includes an applicability rating of exactly one of: High, Medium, Low, or N/A, with a 1-2 sentence rationale, AND a DevForgeAI agent/skill mapping field identifying which specific subagent(s) or skill(s) the pattern could improve (e.g., "security-auditor", "deployment-engineer", "devforgeai-development")</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac2_applicability_ratings.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Findings Documented in Structured Format Consistent with Features 1-3

```xml
<acceptance_criteria id="AC3">
  <given>All patterns have been extracted and rated</given>
  <when>The patterns are appended to the shared research document</when>
  <then>Each pattern entry follows the same structure as STORY-380 patterns: pattern name, source repo and specific file reference, description (2-5 sentences), applicability rating with rationale, DevForgeAI recommendation (specific component or category), and agent/skill mapping. A "## Dev Tools and Domain Patterns" section header groups these entries distinctly from Features 1-3</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac3_structured_format.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Source References Include Repo Name and Specific File Path

```xml
<acceptance_criteria id="AC4">
  <given>A pattern extracted from one of the 8 repos</given>
  <when>The pattern is documented in the research artifact</when>
  <then>The source reference includes the repo directory name (e.g., "claude-code-security-review"), the specific file path within the repo (e.g., "claudecode/prompts.py" or "clinical-trial-protocol-skill/SKILL.md"), and sufficient context to locate the pattern in the source material without re-reading the entire repo</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac4_source_references.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: P1 Repos Analyzed Before P2 Repos

```xml
<acceptance_criteria id="AC5">
  <given>The 8 repos have EPIC-060 priority assignments: P1 (claude-code-action, claude-code-security-review, claude-plugins-official, claude-constitution) and P2 (healthcare, life-sciences, original_performance_takehome, beam)</given>
  <when>The research is conducted</when>
  <then>All 4 P1 repos are fully analyzed before any P2 repo analysis begins, and the document reflects this ordering with P1 patterns listed before P2 patterns within the section</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac5_priority_ordering.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Research Output Appended to Shared Document at Correct Location

```xml
<acceptance_criteria id="AC6">
  <given>The research artifact may or may not already exist at devforgeai/specs/research/prompt-engineering-patterns.md (created by STORY-380 if completed first)</given>
  <when>Feature 4 patterns are added</when>
  <then>Patterns are appended to the existing document (not overwriting Features 1-3 content), the document remains at devforgeai/specs/research/prompt-engineering-patterns.md, existing sections are preserved intact, and if the document does not yet exist, it is created with the Feature 4 section and placeholder notes for Features 1-3</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac6_output_location.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#7: Combined Document Remains Under 2,000 Lines

```xml
<acceptance_criteria id="AC7">
  <given>The research document with Features 1-4 content combined</given>
  <when>The final line count is measured</when>
  <then>The document contains fewer than 2,000 lines total (per EPIC-060 constraint), and if the combined document would exceed the limit, Feature 4 entries are condensed to fit while preserving at least 1 pattern per repo</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac7_size_constraints.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#8: Domain-Specific Agent Mapping Identifies Improvement Targets

```xml
<acceptance_criteria id="AC8">
  <given>All patterns extracted from the 8 repos with applicability ratings of High or Medium</given>
  <when>The agent mapping field is populated</when>
  <then>Each High or Medium pattern maps to at least 1 specific DevForgeAI subagent (from .claude/agents/) or skill (from .claude/skills/), using exact names matching the framework registry, and a summary table at the end of the section lists unique agents/skills with the count of applicable patterns per agent/skill</then>
  <verification>
    <source_files>
      <file hint="Research output document">devforgeai/specs/research/prompt-engineering-patterns.md</file>
      <file hint="Agent registry for name validation">.claude/agents/</file>
    </source_files>
    <test_file>tests/STORY-383/test_ac8_agent_mapping.sh</test_file>
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
      name: "Research Output Document - Dev Tools & Domain Section"
      file_path: "devforgeai/specs/research/prompt-engineering-patterns.md"
      required_keys:
        - key: "Dev Tools and Domain Patterns Section"
          type: "markdown"
          example: "## Dev Tools and Domain Patterns"
          required: true
          validation: "Section header exists and follows Features 1-3 sections"
          test_requirement: "Test: Verify section header exists in document"
        - key: "P1 Subsection"
          type: "markdown"
          example: "### P1: Dev Tool Patterns"
          required: true
          validation: "P1 subsection appears before P2 subsection"
          test_requirement: "Test: Verify P1 subsection precedes P2 subsection"
        - key: "P2 Subsection"
          type: "markdown"
          example: "### P2: Domain-Specific Patterns"
          required: true
          validation: "P2 subsection appears after P1 subsection"
          test_requirement: "Test: Verify P2 subsection exists after P1"
        - key: "Agent Mapping Summary Table"
          type: "markdown"
          example: "| Agent/Skill | Pattern Count | Top Pattern |"
          required: true
          validation: "Table uses exact agent/skill names from framework registry"
          test_requirement: "Test: Verify agent mapping summary table exists with valid agent names"

    - type: "Service"
      name: "DevToolsDomainAnalysisWorkflow"
      file_path: "N/A - manual research workflow"
      interface: "Research methodology"
      lifecycle: "One-time execution"
      dependencies:
        - "tmp/anthropic/claude-code-action/"
        - "tmp/anthropic/claude-code-security-review/"
        - "tmp/anthropic/claude-plugins-official/"
        - "tmp/anthropic/claude-constitution/"
        - "tmp/anthropic/healthcare/"
        - "tmp/anthropic/life-sciences/"
        - "tmp/anthropic/original_performance_takehome/"
        - "tmp/anthropic/beam/"
        - "devforgeai/specs/research/ (output directory)"
      requirements:
        - id: "SVC-001"
          description: "Read and analyze claude-code-action: CLAUDE.md, action.yml, .claude/agents/*.md, .claude/commands/*.md"
          testable: true
          test_requirement: "Test: Verify patterns extracted from claude-code-action repo"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-002"
          description: "Read and analyze claude-code-security-review: claudecode/prompts.py, .claude/commands/security-review.md, evaluation engine"
          testable: true
          test_requirement: "Test: Verify patterns extracted from claude-code-security-review repo"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-003"
          description: "Read and analyze claude-plugins-official: plugin directory, SKILL.md files, plugin.json manifests"
          testable: true
          test_requirement: "Test: Verify patterns extracted from claude-plugins-official repo"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-004"
          description: "Read and analyze claude-constitution: constitution document for constraint and values-alignment patterns"
          testable: true
          test_requirement: "Test: Verify patterns extracted from claude-constitution repo"
          priority: "Critical"
          implements_ac: ["AC1"]
        - id: "SVC-005"
          description: "Read and analyze healthcare: clinical-trial, prior-auth, FHIR skill files and references"
          testable: true
          test_requirement: "Test: Verify patterns extracted from healthcare repo"
          priority: "High"
          implements_ac: ["AC1"]
        - id: "SVC-006"
          description: "Read and analyze life-sciences: nextflow, scientific-problem-selection, instrument-data skill files"
          testable: true
          test_requirement: "Test: Verify patterns extracted from life-sciences repo"
          priority: "High"
          implements_ac: ["AC1"]
        - id: "SVC-007"
          description: "Read and analyze original_performance_takehome: benchmark patterns and test design"
          testable: true
          test_requirement: "Test: Verify patterns extracted from original_performance_takehome repo"
          priority: "High"
          implements_ac: ["AC1"]
        - id: "SVC-008"
          description: "Read and analyze beam: CI/CD workflows and Anthropic-specific fork patterns"
          testable: true
          test_requirement: "Test: Verify patterns extracted from beam repo"
          priority: "High"
          implements_ac: ["AC1"]
        - id: "SVC-009"
          description: "Rate each pattern and map High/Medium patterns to specific DevForgeAI agents/skills"
          testable: true
          test_requirement: "Test: Verify all patterns rated and High/Medium have agent mapping"
          priority: "Critical"
          implements_ac: ["AC2", "AC8"]
        - id: "SVC-010"
          description: "Append section to existing document without overwriting Features 1-3"
          testable: true
          test_requirement: "Test: Verify Features 1-3 content preserved after append"
          priority: "Critical"
          implements_ac: ["AC6"]

  business_rules:
    - id: "BR-001"
      rule: "Applicability rating must be exactly one of: High, Medium, Low, N/A"
      trigger: "When assigning applicability to each extracted pattern"
      validation: "Grep for valid rating values; reject any other format"
      error_handling: "Flag pattern for manual review if rating unclear"
      test_requirement: "Test: Verify no patterns have invalid or missing ratings"
      priority: "Critical"

    - id: "BR-002"
      rule: "P1 repos must be analyzed before P2 repos and listed first in document"
      trigger: "When ordering repo analysis and document sections"
      validation: "P1 subsection line number < P2 subsection line number"
      error_handling: "Reorder sections if misordered"
      test_requirement: "Test: Verify P1 subsection appears before P2 subsection"
      priority: "High"

    - id: "BR-003"
      rule: "Duplicate patterns across repos consolidated citing all sources"
      trigger: "When same technique found in multiple repos"
      validation: "No duplicate pattern names within section"
      error_handling: "Merge entries, cite all repos"
      test_requirement: "Test: Verify no duplicate pattern names within section"
      priority: "High"

    - id: "BR-004"
      rule: "Minimum 8 patterns total across 8 repos"
      trigger: "After all repos analyzed"
      validation: "Count pattern entries >= 8"
      error_handling: "Revisit repos for missed patterns"
      test_requirement: "Test: Verify section contains at least 8 pattern entries"
      priority: "High"

    - id: "BR-005"
      rule: "Agent mapping must use exact names from .claude/agents/ or .claude/skills/ registry"
      trigger: "When mapping patterns to DevForgeAI components"
      validation: "Each mapped name matches registry filename"
      error_handling: "Flag unmatched names for correction"
      test_requirement: "Test: Verify all agent mapping names exist in framework registry"
      priority: "High"

    - id: "BR-006"
      rule: "Combined document must remain under 2,000 lines"
      trigger: "Before final save"
      validation: "Line count check"
      error_handling: "Condense entries if over limit"
      test_requirement: "Test: Verify combined document line count < 2000"
      priority: "High"

    - id: "BR-007"
      rule: "Existing Features 1-3 content must not be modified when appending"
      trigger: "When writing to shared document"
      validation: "Diff check on existing content"
      error_handling: "Restore from git if modified"
      test_requirement: "Test: Verify Features 1-3 content unchanged after append"
      priority: "Critical"

    - id: "BR-008"
      rule: "No PHI or patient data from healthcare/life-sciences repos"
      trigger: "When extracting patterns from healthcare and life-sciences repos"
      validation: "Grep for PHI patterns returns 0 matches"
      error_handling: "Redact any PHI found in pattern descriptions"
      test_requirement: "Test: Verify zero PHI pattern matches in document"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Combined research document loadable in single Read() call"
      metric: "Document under 2,000 lines total"
      test_requirement: "Test: Verify Read() returns complete document without truncation"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Document is valid Markdown rendering"
      metric: "Zero Markdown syntax errors; all headers, lists, tables, and code fences properly closed"
      test_requirement: "Test: Verify Markdown syntax validity"
      priority: "High"

    - id: "NFR-003"
      category: "Scalability"
      requirement: "Consistent entry format enables Grep() parsing across all features"
      metric: "Grep(pattern='Applicability:') returns entries from all feature sections"
      test_requirement: "Test: Verify Grep returns entries from Feature 4"
      priority: "Medium"

    - id: "NFR-004"
      category: "Security"
      requirement: "No secrets, API keys, credentials, or patient data in document"
      metric: "Zero matches for secret and PHI patterns"
      test_requirement: "Test: Verify Grep for secret and PHI patterns returns 0 matches"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Claude Code Terminal context window"
    limitation: "Cannot load all 8 repos simultaneously; beam is extremely large"
    decision: "workaround:Read key files per repo (SKILL.md, prompts.py, CLAUDE.md, README.md, action.yml)"
    discovered_phase: "Architecture"
    impact: "May miss patterns in deeply nested files; mitigated by targeting high-value files"

  - id: TL-002
    component: "beam repo size"
    limitation: "Full Apache Beam fork with thousands of files; exhaustive analysis impractical"
    decision: "workaround:Focus on Anthropic-specific files (.github/workflows/, CLAUDE.md, README.md) not upstream Beam code"
    discovered_phase: "Architecture"
    impact: "Patterns from beam limited to Anthropic's CI/CD and fork management practices"

  - id: TL-003
    component: "Shared document concurrent access"
    limitation: "STORY-380, 381, 382 may modify the shared research document"
    decision: "workaround:Append with clear section boundaries; verify structure before writing"
    discovered_phase: "Architecture"
    impact: "Must verify document structure before appending; rollback if corrupted"

  - id: TL-004
    component: "Healthcare/life-sciences PHI concerns"
    limitation: "Repos may contain sample patient data or clinical trial examples"
    decision: "workaround:Extract prompt engineering patterns only; never copy patient data or identifiers"
    discovered_phase: "Architecture"
    impact: "Some pattern examples may be redacted or generalized"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Document Load Time:**
- Combined research document loads via single `Read()` call: target 800-1,800 lines total
- Each section independently readable via `Read()` with `offset` and `limit` parameters
- No computation or API calls required to consume output — pure Markdown text

### Security

- No secrets, API keys, or credentials in research document
- No patient health information (PHI), clinical trial identifiers, or FHIR resources with patient data
- All code examples wrapped in fenced blocks with "Example (from source):" labels
- Source paths reference only local `tmp/anthropic/` directories
- Zero matches for: `api_key`, `password`, `token`, `secret`, `patient_id`, `SSN`, `MRN`

### Reliability

- Valid Markdown rendering in GitHub, VS Code, and Claude Code Terminal
- All internal cross-references use relative anchors within same document
- Document survives context window clears
- Append operation preserves existing Features 1-3 content

### Scalability

- Supports appending patterns from Features 5-6 without restructuring
- Consistent entry format enables Grep() parsing across all features
- Agent mapping summary table enables quick lookup of improvement targets

---

## Edge Cases & Error Handling

1. **Shared document not yet created by STORY-380:** Create document with Feature 4 section and placeholder notes for Features 1-3.

2. **Duplicate skill across healthcare and life-sciences repos:** clinical-trial-protocol-skill appears in both. Consolidate into single entry citing both repos.

3. **beam repo too large for meaningful analysis:** Focus on Anthropic-specific additions only (.github/workflows/, CLAUDE.md). Document N/A if no applicable patterns found.

4. **original_performance_takehome contains only code, no prompts:** Extract patterns from code structure (test design, problem decomposition). Rate N/A if no applicable patterns.

5. **claude-constitution contains values, not prompts:** Extract constraint-definition and values-alignment patterns relevant to DevForgeAI's context files.

6. **Combined document exceeds 2,000 lines after append:** Condense entries by reducing descriptions to 1-2 sentences. Last resort: create separate sub-document.

7. **Healthcare/life-sciences repos contain patient data:** Never extract PHI. Use only structural patterns (prompt organization, domain context provision, validation structure).

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-380:** Mine Core Anthropic Courses for Prompt Engineering Patterns
  - **Why:** Shares output file devforgeai/specs/research/prompt-engineering-patterns.md; creates initial document structure
  - **Status:** Backlog
  - **Note:** Soft dependency — STORY-383 can create the document if STORY-380 has not yet run

- [ ] **STORY-381:** Extract Prompt Engineering Patterns from Interactive Tutorial
  - **Why:** Shares output file; adds tutorial section
  - **Status:** Backlog
  - **Note:** Soft dependency — section headers prevent conflicts

- [ ] **STORY-382:** Analyze Cookbook and Quickstart Repos for Implementation Patterns
  - **Why:** Shares output file; adds cookbook/quickstart section
  - **Status:** Backlog
  - **Note:** Soft dependency — section headers prevent conflicts

### External Dependencies

- [x] **12 Anthropic repos cloned:** Available at `tmp/anthropic/` (CONFIRMED in EPIC-060)

### Technology Dependencies

None — uses only Read(), Glob(), Grep() tools and Write()/Edit() for output.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for validation checks

**Test Scenarios:**
1. **Happy Path:** All 8 repos analyzed, 8+ patterns extracted, document under 2,000 lines
2. **Edge Cases:**
   - Combined document at 1,999 lines (just under limit)
   - Duplicate pattern across healthcare/life-sciences consolidated
   - beam repo yields only N/A patterns
3. **Error Cases:**
   - Missing repo directory (Read() fails)
   - Pattern without applicability rating
   - Agent mapping name not in registry
   - PHI detected in extracted content

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **End-to-End Research Flow:** Run research workflow, verify output document structure
2. **Grep Parseability:** Verify patterns findable via Grep() queries
3. **Cross-Section Integrity:** Verify existing Features 1-3 sections not corrupted
4. **Agent Mapping Validation:** Verify all mapped names resolve to real agents/skills

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: All 8 Repos Analyzed

- [ ] claude-code-action analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] claude-code-security-review analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] claude-plugins-official analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] claude-constitution analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] healthcare analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] life-sciences analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] original_performance_takehome analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md
- [ ] beam analyzed and patterns extracted - **Phase:** 2 - **Evidence:** devforgeai/specs/research/prompt-engineering-patterns.md

### AC#2: Applicability Ratings with Agent Mapping

- [ ] Every pattern has exactly one rating (High/Medium/Low/N/A) - **Phase:** 2 - **Evidence:** Grep validation
- [ ] Each rating includes 1-2 sentence rationale - **Phase:** 2 - **Evidence:** Pattern entry structure
- [ ] High/Medium patterns have agent/skill mapping - **Phase:** 2 - **Evidence:** Mapping field validation

### AC#3: Structured Format

- [ ] Each pattern has: name, source, description, rating, recommendation, mapping - **Phase:** 2 - **Evidence:** Structure validation
- [ ] Section header is "## Dev Tools and Domain Patterns" - **Phase:** 2 - **Evidence:** Header check

### AC#4: Source References

- [ ] Each pattern cites repo directory name - **Phase:** 2 - **Evidence:** Grep for repo names
- [ ] Each pattern cites specific file path within repo - **Phase:** 2 - **Evidence:** Grep for file paths

### AC#5: Priority Ordering

- [ ] P1 repos listed before P2 repos in document - **Phase:** 5 - **Evidence:** Line number comparison

### AC#6: Output Location

- [ ] Section appended to devforgeai/specs/research/prompt-engineering-patterns.md - **Phase:** 5 - **Evidence:** Glob/Read verification
- [ ] Existing sections preserved intact - **Phase:** 5 - **Evidence:** Diff check

### AC#7: Size Constraints

- [ ] Combined document under 2,000 lines - **Phase:** 5 - **Evidence:** wc -l output

### AC#8: Agent Mapping Summary

- [ ] Summary table lists agents/skills with pattern counts - **Phase:** 2 - **Evidence:** Table validation
- [ ] All mapped names match framework registry - **Phase:** 2 - **Evidence:** Registry cross-check

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [x] All 8 Anthropic repos analyzed (4 P1 + 4 P2)
- [x] At least 8 unique patterns extracted across repos (14 patterns D1-D14)
- [x] Each pattern has complete entry (name, source, description, rating, recommendation, agent mapping)
- [x] P1 repos analyzed and documented before P2 repos
- [x] Section appended to devforgeai/specs/research/prompt-engineering-patterns.md
- [x] Agent mapping summary table created (17 agents/skills listed)
- [x] Duplicate patterns consolidated with multi-repo citations
- [x] No PHI or patient data in document

### Quality
- [x] All 8 acceptance criteria have passing tests (67/67 assertions)
- [x] Combined document under 2,000 lines (1,607 lines)
- [x] All applicability ratings valid (High/Medium/Low/N/A)
- [x] All agent mapping names match framework registry
- [x] No vague descriptions without specific metrics
- [x] No secrets, credentials, or PHI in document
- [x] Valid Markdown syntax throughout
- [x] Existing Features 1-3 sections not corrupted

### Testing
- [x] Shell tests validate document structure
- [x] Grep tests validate pattern entry format
- [x] Line count validation passes
- [x] Source reference validation passes
- [x] Rating value validation passes
- [x] Agent mapping name validation passes
- [x] PHI detection passes (zero matches)
- [x] Priority ordering validation passes

### Documentation
- [x] Research section is self-contained and readable in fresh session
- [x] Each pattern entry understandable without cross-references
- [x] Agent mapping summary provides actionable improvement targets

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-10
**Branch:** main

- [x] All 8 Anthropic repos analyzed (4 P1 + 4 P2) - Completed: claude-code-action, claude-code-security-review, claude-plugins-official, claude-constitution (P1); healthcare, life-sciences, original_performance_takehome, beam (P2)
- [x] At least 8 unique patterns extracted across repos (14 patterns D1-D14) - Completed: Extracted 14 patterns (D1-D14), 6 more than minimum requirement
- [x] Each pattern has complete entry (name, source, description, rating, recommendation, agent mapping) - Completed: All 14 patterns have 6 required fields
- [x] P1 repos analyzed and documented before P2 repos - Completed: P1 section at line 1290, P2 section at line 1408
- [x] Section appended to devforgeai/specs/research/prompt-engineering-patterns.md - Completed: Dev Tools and Domain Patterns section at lines 1280-1584
- [x] Agent mapping summary table created (17 agents/skills listed) - Completed: Table at lines 1560-1581 with pattern counts per agent
- [x] Duplicate patterns consolidated with multi-repo citations - Completed: D8 cites both healthcare and life-sciences
- [x] No PHI or patient data in document - Completed: Zero PHI patterns detected in security scan
- [x] All 8 acceptance criteria have passing tests (67/67 assertions) - Completed: 8 test scripts with 100% pass rate
- [x] Combined document under 2,000 lines (1,607 lines) - Completed: 393 lines below limit
- [x] All applicability ratings valid (High/Medium/Low/N/A) - Completed: 8 High, 4 Medium, 2 Low
- [x] All agent mapping names match framework registry - Completed: 17 agents/skills verified against .claude/agents/ and .claude/skills/
- [x] No vague descriptions without specific metrics - Completed: All descriptions cite specific files and line numbers
- [x] No secrets, credentials, or PHI in document - Completed: Security scan passed
- [x] Valid Markdown syntax throughout - Completed: All code fences paired
- [x] Existing Features 1-3 sections not corrupted - Completed: Content at lines 1-1279 preserved
- [x] Shell tests validate document structure - Completed: test_ac3_structured_format.sh (9/9 pass)
- [x] Grep tests validate pattern entry format - Completed: Pattern fields validated via Grep
- [x] Line count validation passes - Completed: test_ac7_size_constraints.sh (7/7 pass)
- [x] Source reference validation passes - Completed: test_ac4_source_references.sh (15/15 pass)
- [x] Rating value validation passes - Completed: test_ac2_applicability_ratings.sh (8/8 pass)
- [x] Agent mapping name validation passes - Completed: test_ac8_agent_mapping.sh (7/7 pass)
- [x] PHI detection passes (zero matches) - Completed: Zero PHI patterns in Dev Tools section
- [x] Priority ordering validation passes - Completed: test_ac5_priority_ordering.sh (8/8 pass)
- [x] Research section is self-contained and readable in fresh session - Completed: Section includes all context and can be read independently
- [x] Each pattern entry understandable without cross-references - Completed: Each pattern has complete source, description, and recommendation
- [x] Agent mapping summary provides actionable improvement targets - Completed: Table identifies anti-pattern-scanner and code-reviewer as highest-priority targets

### TDD Workflow Summary

**Key Patterns Identified:**
- D2: Phased Security Audit with Confidence Scoring (applicable to security-auditor)
- D6: Principal Hierarchy for Trust Delegation (applicable to all subagents)
- D8: Waypoint-Based Workflow Architecture (applicable to devforgeai-development)
- D12: Anti-Cheating Guardrails for AI Agents (applicable to test-automator)

**No Deferrals:** All DoD items completed.

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-06 | claude/story-requirements-analyst | Created | Story created from EPIC-060 Feature 4 | STORY-383-mine-dev-tools-domain-patterns.story.md |
| 2026-02-10 | .claude/qa-result-interpreter | QA Deep | PASSED: 67/67 tests, 0 violations, documentation quality validated | devforgeai/qa/reports/STORY-383/ |

## Notes

**Design Decisions:**
- Story type = "documentation" (skips integration testing phase in TDD workflow)
- 8 points reflects analyzing 8 repos with diverse content types (GitHub Actions, security prompts, plugins, constitution, healthcare SKILL.md, performance benchmarks)
- P1/P2 ordering follows EPIC-060 priority assignments
- Minimum 8 patterns (1 per repo minimum) — some repos may yield N/A only
- Agent mapping field is new addition vs. STORY-380-382 pattern — identifies concrete improvement targets

**Open Questions:**
- None — scope is well-defined by EPIC-060 Feature 4 and BRAINSTORM-010

**Related ADRs:**
- None required — research-only story, no architecture changes

**References:**
- EPIC-060: Prompt Engineering Research & Knowledge Capture
- BRAINSTORM-010: Prompt Engineering Improvement from Anthropic Repos
- STORY-380: Mine Core Anthropic Courses (shares output document)
- STORY-381: Extract Tutorial Prompt Patterns (shares output document)
- STORY-382: Analyze Cookbook and Quickstart Patterns (shares output document)

---

Story Template Version: 2.8
Last Updated: 2026-02-06
