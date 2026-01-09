---
id: STORY-196
title: Add Pattern Matching for Pipes and Redirects
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Dev Complete
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
- [x] **STORY-195:** Add Common Command Composition Patterns (QA Approved)
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
- [x] Sed extraction logic added - **Phase:** 3 - **Evidence:** pre-tool-use.sh lines 126-173
- [x] Test: Pipe extraction works - **Phase:** 5 - **Evidence:** test-rec-02.sh tests 1-3

### AC#2: Pipe Command Auto-Approval
- [x] Test: `git status | head` auto-approves - **Phase:** 5 - **Evidence:** test-rec-02.sh test 1

### AC#3: Redirect Command Auto-Approval
- [x] Test: `pytest > output.txt` auto-approves - **Phase:** 5 - **Evidence:** test-rec-02.sh test 5

### AC#4: Stderr Redirect Handling
- [x] Test: `cmd 2>&1` extracts base correctly - **Phase:** 5 - **Evidence:** test-rec-02.sh test 6

---

**Checklist Progress:** 5/5 items complete (100%)

---

## Definition of Done

### Implementation
- [x] BASE_CMD extraction logic added to pattern matching loop
- [x] Sed commands strip |, >, 2>&1 correctly
- [x] Log message updated: "MATCHED safe pattern (with pipe/redirect)"
- [x] Existing pattern matching preserved for non-pipe commands

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Edge cases covered (multiple pipes, mixed redirects)
- [x] Security validated (dangerous commands still blocked)

### Testing
- [x] Unit tests for extraction logic
- [x] Integration tests with sample commands

### Documentation
- [x] Inline comments explaining extraction logic

---

## Implementation Notes

- [x] BASE_CMD extraction logic added to pattern matching loop - Completed: Phase 03, lines 126-173 in pre-tool-use.sh
- [x] Sed commands strip |, >, 2>&1 correctly - Completed: Phase 03, lines 148-159 extract_base_command()
- [x] Log message updated: "MATCHED safe pattern (with pipe/redirect)" - Completed: Phase 03, lines 182-188
- [x] Existing pattern matching preserved for non-pipe commands - Completed: Phase 03, lines 176-223
- [x] All 4 acceptance criteria have passing tests - Completed: Phase 05, test-rec-02.sh 23 tests
- [x] Edge cases covered (multiple pipes, mixed redirects) - Completed: Phase 05, tests 2,7,10,11
- [x] Security validated (dangerous commands still blocked) - Completed: Phase 05, tests 12-20
- [x] Unit tests for extraction logic - Completed: Phase 02, test-rec-02.sh categories 1-3
- [x] Integration tests with sample commands - Completed: Phase 05, test-rec-02.sh all categories
- [x] Inline comments explaining extraction logic - Completed: Phase 03, lines 124-125, 145-146, 166-167

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-09

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-015 REC-2 | STORY-196-pipe-redirect-pattern-matching.story.md |
| 2026-01-09 | claude/opus | Dev Complete | TDD validation of pre-existing implementation | pre-tool-use.sh, test-rec-02.sh |

## Notes

**Source RCA:** RCA-015, REC-2 (HIGH priority)
**Expected Impact:** Additional 5-10% friction reduction

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
