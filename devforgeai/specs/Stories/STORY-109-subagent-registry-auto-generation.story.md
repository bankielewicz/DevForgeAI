---
id: STORY-109
title: Subagent Registry Auto-Generation
epic: EPIC-017
sprint: Backlog
status: Backlog
points: 5
depends_on: []
priority: Medium
assigned_to: TBD
created: 2025-12-18
format_version: "2.2"
---

# Story: Subagent Registry Auto-Generation

## Description

**As a** framework maintainer,
**I want** a script that reads `.claude/agents/*.md` frontmatter and generates a CLAUDE.md section with proactive triggers,
**so that** Opus automatically uses the right agent for each task and CLAUDE.md never drifts from actual agents.

This story implements EPIC-017 Feature 2: Script that reads `.claude/agents/*.md` frontmatter and generates CLAUDE.md section with proactive triggers. Single source of truth for subagent discovery.

## Acceptance Criteria

### AC#1: Frontmatter Parsing

**Given** agent files exist in `.claude/agents/`,
**When** the registry generator script runs,
**Then** it extracts: name, description, tools, and proactive_triggers from each agent's YAML frontmatter.

---

### AC#2: CLAUDE.md Section Generation

**Given** agent frontmatter has been parsed,
**When** the registry generator completes,
**Then** it produces a markdown section with:
- Agent name and description table
- Proactive trigger mapping (task patterns → recommended agents)
- Available tools per agent

---

### AC#3: Proactive Triggers Field

**Given** an agent frontmatter file,
**When** I add a `proactive_triggers` field with task patterns,
**Then** the registry includes those patterns for automatic agent selection.

---

### AC#4: Pre-commit Hook Integration

**Given** agent files are modified,
**When** a git commit is attempted,
**Then** the pre-commit hook runs the registry generator to prevent drift.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "SubagentRegistryGenerator"
      file_path: "scripts/generate-subagent-registry.sh"
      interface: "CLI Script"
      lifecycle: "On-demand"
      dependencies:
        - "yq (YAML parser)"
        - "bash 4.0+"
      requirements:
        - id: "SVC-001"
          description: "Parse YAML frontmatter from all .claude/agents/*.md files"
          testable: true
          test_requirement: "Test: Run script with 3 agent files, verify all parsed correctly"
          priority: "Critical"
        - id: "SVC-002"
          description: "Generate markdown table of agents with descriptions"
          testable: true
          test_requirement: "Test: Output contains markdown table with name|description|tools columns"
          priority: "Critical"
        - id: "SVC-003"
          description: "Generate proactive trigger mapping section"
          testable: true
          test_requirement: "Test: Output contains trigger patterns mapped to agent names"
          priority: "High"
        - id: "SVC-004"
          description: "Update CLAUDE.md between marker comments"
          testable: true
          test_requirement: "Test: Content between <!-- BEGIN SUBAGENT REGISTRY --> and <!-- END --> is replaced"
          priority: "Critical"

    - type: "Configuration"
      name: "Agent Frontmatter Schema"
      file_path: ".claude/agents/*.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "code-reviewer"
          required: true
          validation: "Non-empty, alphanumeric with hyphens"
          test_requirement: "Test: Agent without name field causes error"
        - key: "description"
          type: "string"
          example: "Senior code review specialist"
          required: true
          validation: "Non-empty, max 200 characters"
          test_requirement: "Test: Agent without description field causes error"
        - key: "tools"
          type: "array"
          example: "[Read, Grep, Glob]"
          required: false
          default: "[]"
          validation: "Valid tool names from Claude Code"
          test_requirement: "Test: Invalid tool name logged as warning"
        - key: "proactive_triggers"
          type: "array"
          example: "[\"after code implementation\", \"when reviewing changes\"]"
          required: false
          default: "[]"
          validation: "Array of strings describing when to use agent"
          test_requirement: "Test: Proactive triggers appear in output mapping"

    - type: "Configuration"
      name: "Pre-commit Hook"
      file_path: ".git/hooks/pre-commit"
      required_keys:
        - key: "registry_check"
          type: "script_block"
          example: "scripts/generate-subagent-registry.sh --check"
          required: true
          validation: "Exit code 0 if registry up-to-date, 1 if drift detected"
          test_requirement: "Test: Modified agent file without running generator blocks commit"

  business_rules:
    - id: "BR-001"
      rule: "CLAUDE.md registry section must match current agent files"
      trigger: "Pre-commit hook and manual script run"
      validation: "Diff between generated and existing registry section is empty"
      error_handling: "Block commit with message: 'Run scripts/generate-subagent-registry.sh'"
      test_requirement: "Test: Stale registry blocks commit with helpful error"
      priority: "Critical"
    - id: "BR-002"
      rule: "Agent files without valid frontmatter are skipped with warning"
      trigger: "Registry generation"
      validation: "YAML parse attempt, catch exceptions"
      error_handling: "Log warning, continue with other agents"
      test_requirement: "Test: Malformed YAML logs warning, doesn't crash script"
      priority: "High"
    - id: "BR-003"
      rule: "Proactive triggers must be unique across all agents"
      trigger: "Registry generation"
      validation: "Detect duplicate triggers across agent files"
      error_handling: "Log warning listing duplicate triggers and their agents"
      test_requirement: "Test: Two agents with same trigger logs conflict warning"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Registry generation must complete within 5 seconds"
      metric: "< 5 seconds for 50 agent files"
      test_requirement: "Test: Benchmark with 50 test agent files"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Script is idempotent - running twice produces identical output"
      metric: "Diff between two consecutive runs is empty"
      test_requirement: "Test: Run script twice, compare outputs"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Registry generation: < 5 seconds for 50 agent files

---

### Reliability

**Error Handling:**
- Malformed YAML: Skip file with warning, continue processing
- Missing required fields: Log error, exclude from registry

**Idempotency:**
- Multiple runs produce identical output

---

## Dependencies

### Prerequisite Stories

None - this is a foundation story.

### Technology Dependencies

- [ ] **yq** v4.0+
  - **Purpose:** YAML parsing in shell scripts
  - **Approved:** Pending
  - **Added to dependencies.md:** Pending

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for parsing logic

**Test Scenarios:**
1. **Happy Path:** 3 well-formed agents generate correct registry
2. **Edge Cases:**
   - Agent with no proactive_triggers
   - Agent with empty tools array
   - Agent with very long description (truncate?)
3. **Error Cases:**
   - Invalid YAML syntax
   - Missing required fields
   - Duplicate trigger patterns

---

## Acceptance Criteria Verification Checklist

### AC#1: Frontmatter Parsing

- [ ] Extract name field from frontmatter - **Phase:** 3 - **Evidence:** TBD
- [ ] Extract description field from frontmatter - **Phase:** 3 - **Evidence:** TBD
- [ ] Extract tools array from frontmatter - **Phase:** 3 - **Evidence:** TBD
- [ ] Extract proactive_triggers array from frontmatter - **Phase:** 3 - **Evidence:** TBD

### AC#2: CLAUDE.md Section Generation

- [ ] Generate agent table with columns - **Phase:** 3 - **Evidence:** TBD
- [ ] Generate proactive trigger mapping - **Phase:** 3 - **Evidence:** TBD
- [ ] Output valid markdown format - **Phase:** 3 - **Evidence:** TBD

### AC#3: Proactive Triggers Field

- [ ] New frontmatter field documented - **Phase:** 2 - **Evidence:** TBD
- [ ] Triggers appear in registry output - **Phase:** 3 - **Evidence:** TBD
- [ ] Triggers mapped to correct agent - **Phase:** 3 - **Evidence:** TBD

### AC#4: Pre-commit Hook Integration

- [ ] Hook script created - **Phase:** 3 - **Evidence:** TBD
- [ ] Hook detects registry drift - **Phase:** 3 - **Evidence:** TBD
- [ ] Hook blocks commit on drift - **Phase:** 3 - **Evidence:** TBD

---

**Checklist Progress:** 0/13 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] `scripts/generate-subagent-registry.sh` created
- [ ] Agent frontmatter schema documented with proactive_triggers field
- [ ] CLAUDE.md marker comments added for registry section
- [ ] Pre-commit hook configured

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (malformed YAML, missing fields, duplicates)
- [ ] Idempotency verified
- [ ] Code coverage >95% for parsing logic

### Testing
- [ ] Unit tests for YAML parsing
- [ ] Unit tests for markdown generation
- [ ] Integration test for end-to-end registry flow
- [ ] Pre-commit hook test

### Documentation
- [ ] Agent frontmatter schema documented
- [ ] proactive_triggers field usage guide
- [ ] Pre-commit hook setup instructions

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Using shell script + yq for portability (no Python dependency)
- Marker comments in CLAUDE.md allow targeted updates without affecting other content
- Proactive triggers are suggestions, not mandatory agent selection

**References:**
- EPIC-017: Parallel Task Orchestration for DevForgeAI
- Research: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-18
