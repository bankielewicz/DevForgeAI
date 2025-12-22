---
id: STORY-133
title: Create ideation-result-interpreter Subagent
epic: EPIC-028
sprint: Backlog
status: Backlog
points: 6
depends_on: []  # This story creates the subagent; STORY-131 depends on THIS story
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Create ideation-result-interpreter Subagent

## Description

**As a** framework maintainer,
**I want** to create an ideation-result-interpreter subagent following the dev-result-interpreter pattern,
**so that** the /ideate command can delegate summary presentation and formatting to a specialized subagent, ensuring consistent result interpretation across development and ideation workflows while reducing command complexity.

## Acceptance Criteria

### AC#1: Subagent Structure and Initialization

**Given** the dev-result-interpreter.md file exists as a reference pattern,
**When** ideation-result-interpreter.md is created following the same architectural structure,
**Then** the subagent includes all required sections: Purpose, When Invoked, Workflow, Success Templates, Error Handling, and Related Subagents.

---

### AC#2: Ideation-Specific Output Parsing

**Given** an ideation workflow has completed and generated output (epics, requirements, complexity metrics),
**When** ideation-result-interpreter processes the skill output,
**Then** it correctly extracts and displays: epic count, complexity score, architecture tier, functional requirements summary, NFRs, integration requirements, and provides next-action guidance (greenfield→/create-context, brownfield→/orchestrate).

---

### AC#3: Display Template Generation for Success Cases

**Given** ideation workflow completed successfully with epics generated,
**When** ideation-result-interpreter generates display output,
**Then** the success template displays: ideation summary header with epic count and complexity score, architecture tier classification, requirements breakdown (functional, NFRs, integrations), key design decisions, and recommended next command.

---

### AC#4: Display Template Generation for Warning Cases

**Given** ideation workflow completed with warnings (e.g., low-confidence requirements, missing details),
**When** ideation-result-interpreter processes partial results,
**Then** the warning template displays: completion status, quality warnings with severity levels, incomplete sections highlighted, and resolution path with recommendations.

---

### AC#5: Framework Integration and Tool Restrictions

**Given** the subagent follows DevForgeAI architectural constraints,
**When** ideation-result-interpreter operates within the /ideate command lifecycle,
**Then** the subagent uses ONLY read-only tools (Read, Glob, Grep), respects context file immutability, and returns structured display output (no file creation).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    pattern_to_follow: ".claude/agents/dev-result-interpreter.md"
    templates_source: ".claude/skills/devforgeai-ideation/references/completion-handoff.md"
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    validation_workflow: ".claude/skills/devforgeai-ideation/references/self-validation-workflow.md"

  skill_output_example:
    description: "The ideation skill produces this structured output that the interpreter must parse"
    example: |
      ## Ideation Complete

      **Epics Generated:** 3
      **Complexity Score:** 37/60 (Tier 3 - Complex System)
      **Architecture Tier:** Tier 3

      ### Requirements Summary
      - Functional: 18 requirements
      - Non-Functional: 5 requirements
      - Integration: 3 requirements

      ### Epic Breakdown
      1. EPIC-028: Command Refactoring (6 features, 20-25 points)
      2. EPIC-029: Session Continuity (6 features, 25-30 points)
      3. EPIC-030: Constitutional Compliance (6 features, 15-20 points)

      ### Project Mode
      - Mode: brownfield (6/6 context files exist)
      - Recommended Next Action: /orchestrate or /create-story

  components:
    - type: "Subagent"
      name: "ideation-result-interpreter"
      file_path: ".claude/agents/ideation-result-interpreter.md"
      requirements:
        - id: "SUB-001"
          description: "Parse skill output and extract epic count, complexity score, architecture tier"
          testable: true
          test_requirement: "Test: Given valid skill output, extracts all metadata fields correctly"
          priority: "Critical"
        - id: "SUB-002"
          description: "Generate success display template with ideation summary"
          testable: true
          test_requirement: "Test: Success template includes header, tier, requirements breakdown, next action"
          priority: "Critical"
        - id: "SUB-003"
          description: "Generate warning display template for partial results"
          testable: true
          test_requirement: "Test: Warning template includes status, warnings, incomplete sections, resolution"
          priority: "High"
        - id: "SUB-004"
          description: "Determine greenfield vs brownfield next action"
          testable: true
          test_requirement: "Test: Greenfield recommends /create-context; brownfield recommends /orchestrate"
          priority: "Critical"
        - id: "SUB-005"
          description: "Use only read-only tools (Read, Glob, Grep)"
          testable: true
          test_requirement: "Test: Subagent YAML frontmatter specifies only read-only tools"
          priority: "Critical"
        - id: "SUB-006"
          description: "Handle malformed or missing output fields gracefully"
          testable: true
          test_requirement: "Test: Missing fields display as 'N/A' instead of crashing"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Subagent must follow dev-result-interpreter pattern"
      test_requirement: "Test: Structure matches dev-result-interpreter with ideation-specific adaptations"
    - id: "BR-002"
      rule: "Display output must be presentation-only (no file creation)"
      test_requirement: "Test: Subagent returns formatted string, creates no files"
    - id: "BR-003"
      rule: "Greenfield/brownfield detection based on context file count"
      test_requirement: "Test: 6 context files = brownfield; <6 = greenfield"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Response time for typical ideation output"
      metric: "<500ms for up to 10 epics with 50 requirements"
      test_requirement: "Test: Benchmark with standard output; verify <500ms"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Graceful handling of malformed input"
      metric: "Zero crashes; always returns valid presentation"
      test_requirement: "Test: Feed malformed output; verify fallback message returned"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Subagent size constraint"
      metric: "≤200 lines following lightweight pattern"
      test_requirement: "Test: wc -l ideation-result-interpreter.md returns ≤200"
    - id: "NFR-004"
      category: "Consistency"
      requirement: "Display format matches dev-result-interpreter style"
      metric: "Visual style and markdown structure consistent"
      test_requirement: "Test: Compare output format with dev-result-interpreter"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **Empty or malformed skill output:** If output lacks expected metadata fields (epic count, complexity metrics), display "N/A" with explanatory notes and guidance to re-run ideation.

2. **Greenfield vs. Brownfield detection failure:** If context file detection is ambiguous (partial files: 3-5 of 6), display both /create-context and /orchestrate options with conditions.

3. **Extremely complex or minimal results:** If complexity score is very high (>50) or very low (<5), include sensitivity-appropriate warnings.

4. **Architecture tier ambiguity:** If conflicting tier recommendations, display both options and recommend /create-context for clarification.

5. **No NFRs or integration requirements:** Flag as "Not Addressed" with guidance to re-run /ideate with emphasis on performance/security requirements.

## UI Specification

**Not applicable** - This story creates a subagent (Markdown documentation) with no visual UI components.

## Definition of Done

### Implementation Checklist
- [ ] ideation-result-interpreter.md created in .claude/agents/
- [ ] YAML frontmatter with name, description, tools (Read, Glob, Grep), model
- [ ] Purpose section describing when invoked
- [ ] Workflow section with parsing and template generation steps
- [ ] Success template for complete ideation results
- [ ] Warning template for partial results
- [ ] Greenfield/brownfield next-action logic
- [ ] Error handling for malformed input

### Testing Checklist
- [ ] Test: Parses valid skill output correctly
- [ ] Test: Handles malformed output gracefully
- [ ] Test: Success template formats correctly
- [ ] Test: Warning template formats correctly
- [ ] Test: Greenfield detection works (<6 context files)
- [ ] Test: Brownfield detection works (6 context files)
- [ ] Test: Execution time <500ms

### Documentation Checklist
- [ ] Subagent registered in CLAUDE.md subagent registry
- [ ] EPIC-028 updated with story reference

### Quality Checklist
- [ ] Subagent under 200 lines
- [ ] Read-only tools only
- [ ] Follows dev-result-interpreter pattern
- [ ] Story marked as "Dev Complete" upon implementation

## AC Verification Checklist

### AC#1: Structure
- [ ] File created at .claude/agents/ideation-result-interpreter.md
- [ ] YAML frontmatter present
- [ ] All required sections included
- [ ] Follows dev-result-interpreter pattern

### AC#2: Output Parsing
- [ ] Epic count extracted
- [ ] Complexity score extracted
- [ ] Architecture tier extracted
- [ ] Requirements summary generated
- [ ] Next-action guidance provided

### AC#3: Success Templates
- [ ] Header with epic count and complexity
- [ ] Architecture tier displayed
- [ ] Requirements breakdown shown
- [ ] Next command recommended

### AC#4: Warning Templates
- [ ] Completion status shown
- [ ] Warnings with severity levels
- [ ] Incomplete sections highlighted
- [ ] Resolution path provided

### AC#5: Tool Restrictions
- [ ] Only Read, Glob, Grep in tools list
- [ ] No Write, Edit, Bash
- [ ] No file creation in logic
