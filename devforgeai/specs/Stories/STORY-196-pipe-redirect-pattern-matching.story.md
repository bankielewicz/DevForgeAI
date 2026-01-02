---
id: STORY-196
title: Add Pattern Matching for Pipes and Redirects
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
points: 1
depends_on: ["STORY-195"]
priority: High
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-015
source_recommendation: REC-2
format_version: "2.5"
---

# Story: Add Pattern Matching for Pipes and Redirects

## Description

**As a** DevForgeAI framework developer,
**I want** the pre-tool-use.sh hook to recognize safe commands even when followed by pipes or redirects,
**so that** commands like `git status | head` auto-approve without manual intervention.

**Context from RCA-015:**
Commands with pipes (`|`), output redirection (`>`), and process substitution require approval even when the base command is safe. Modifying pattern matching to extract the base command before pipes/redirects will provide an additional 5-10% friction reduction.

## Acceptance Criteria

### AC#1: Base Command Extraction

**Given** a command containing pipe (`|`) or redirect (`>`)
**When** the pre-tool-use hook evaluates the command
**Then** the base command (before pipe/redirect) is extracted for pattern matching

---

### AC#2: Pipe Command Auto-Approval

**Given** a command like `git status | head -10`
**When** the base command `git status` matches a safe pattern
**Then** the entire command is auto-approved

---

### AC#3: Redirect Command Auto-Approval

**Given** a command like `python3 -m pytest > output.txt`
**When** the base command `python3 -m pytest` matches a safe pattern
**Then** the entire command is auto-approved

---

### AC#4: Stderr Redirect Handling

**Given** a command with `2>&1` (stderr redirect)
**When** the base command matches a safe pattern
**Then** the entire command is auto-approved

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "pre-tool-use.sh"
      file_path: ".claude/hooks/pre-tool-use.sh"
      requirements:
        - id: "CFG-001"
          description: "Modify pattern matching loop to extract base command"
          testable: true
          test_requirement: "Test: echo 'git status | head' | extract_base returns 'git status'"
          priority: "Critical"
        - id: "CFG-002"
          description: "Use sed to strip pipes, redirects, and stderr"
          testable: true
          test_requirement: "Test: BASE_CMD extraction handles |, >, 2>&1"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Base command determines safety, not piped commands"
      trigger: "Pattern evaluation with pipes/redirects"
      validation: "Only first command segment evaluated for safety"
      error_handling: "If base command unsafe, entire chain requires approval"
      test_requirement: "Test: 'rm -rf | cat' still requires approval"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Sed extraction adds < 10ms overhead"
      metric: "< 10ms additional latency per command"
      test_requirement: "Test: Time BASE_CMD extraction on 100 commands"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Base command extraction: < 10ms overhead
- Total hook evaluation: < 110ms with extraction

### Security
- Extraction must not bypass dangerous command detection
- Pipes to dangerous commands still blocked (e.g., `safe | rm -rf`)

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-195:** Add Common Command Composition Patterns
  - **Why:** Establishes baseline patterns before adding extraction logic
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests
1. Test BASE_CMD extraction for pipes: `git status | head` → `git status`
2. Test BASE_CMD extraction for redirects: `pytest > out.txt` → `pytest`
3. Test BASE_CMD extraction for stderr: `cmd 2>&1` → `cmd`
4. Test multi-pipe: `git log | grep fix | head` → `git log`

### Integration Tests
1. Verify piped commands auto-approve when base is safe
2. Verify piped commands block when base is unsafe

---

## Acceptance Criteria Verification Checklist

### AC#1: Base Command Extraction
- [ ] Sed extraction logic added - **Phase:** 3 - **Evidence:** pre-tool-use.sh diff
- [ ] Test: Pipe extraction works - **Phase:** 5 - **Evidence:** test file

### AC#2: Pipe Command Auto-Approval
- [ ] Test: `git status | head` auto-approves - **Phase:** 5 - **Evidence:** test file

### AC#3: Redirect Command Auto-Approval
- [ ] Test: `pytest > output.txt` auto-approves - **Phase:** 5 - **Evidence:** test file

### AC#4: Stderr Redirect Handling
- [ ] Test: `cmd 2>&1` extracts base correctly - **Phase:** 5 - **Evidence:** test file

---

**Checklist Progress:** 0/5 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] BASE_CMD extraction logic added to pattern matching loop
- [ ] Sed commands strip |, >, 2>&1 correctly
- [ ] Log message updated: "MATCHED safe pattern (with pipe/redirect)"
- [ ] Existing pattern matching preserved for non-pipe commands

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (multiple pipes, mixed redirects)
- [ ] Security validated (dangerous commands still blocked)

### Testing
- [ ] Unit tests for extraction logic
- [ ] Integration tests with sample commands

### Documentation
- [ ] Inline comments explaining extraction logic

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-015 REC-2 | STORY-196-pipe-redirect-pattern-matching.story.md |

## Notes

**Source RCA:** RCA-015, REC-2 (HIGH priority)
**Expected Impact:** Additional 5-10% friction reduction

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
