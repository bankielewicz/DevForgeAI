---
id: STORY-121
title: Story-Scoped Pre-Commit Validation
epic: EPIC-024
sprint: Sprint-8
status: Backlog
points: 5
depends_on: []
priority: High
assigned_to: TBD
created: 2025-12-20
format_version: "2.2"
---

# Story: Story-Scoped Pre-Commit Validation

## Description

**As a** developer,
**I want** pre-commit validation scoped to only my current story via environment variable,
**So that** other stories with validation errors don't block my commits.

This story implements EPIC-024 Feature 2: Add environment variable `DEVFORGEAI_STORY` to scope pre-commit validation to specific story, preventing blocks from unrelated story validation errors.

## Acceptance Criteria

### AC#1: DEVFORGEAI_STORY Environment Variable Scopes Validation

**Given** a developer sets `DEVFORGEAI_STORY=STORY-114`,
**When** they run `git commit`,
**Then** pre-commit hook validates only `STORY-114` file (not all staged story files).

---

### AC#2: Backward Compatibility When Env Var Unset

**Given** `DEVFORGEAI_STORY` is NOT set,
**When** developer runs `git commit`,
**Then** pre-commit hook validates ALL staged `.story.md` files (original behavior).

---

### AC#3: Clear Console Message Shows Scoping Status

**Given** a developer commits with or without `DEVFORGEAI_STORY`,
**When** pre-commit hook runs,
**Then** console shows "Scoped to: STORY-114" if scoped, or no scoping message if unscoped.

---

### AC#4: Pre-Commit Hook Template Updated

**Given** `.git/hooks/pre-commit` needs scoping support,
**When** developer installs/reinstalls hooks via `install_hooks.sh`,
**Then** hook template includes DEVFORGEAI_STORY filtering logic.

---

### AC#5: User Documentation Explains Scoped Commits

**Given** documentation for scoped commits doesn't exist,
**When** developer searches for guidance,
**Then** `devforgeai/docs/STORY-SCOPED-COMMITS.md` explains when/how to use scoping.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Git Hook"
      name: ".git/hooks/pre-commit"
      file_path: ".git/hooks/pre-commit"
      current_lines: "44-58"
      modification: "Add DEVFORGEAI_STORY env var filtering"
      implementation: |
        if [ -n "$DEVFORGEAI_STORY" ]; then
            # Scoped validation - only validate specific story
            STORY_FILES=$(git diff --cached --name-only --diff-filter=d | grep "${DEVFORGEAI_STORY}" | grep -v '^tests/' || true)
            echo "  Scoped to: $DEVFORGEAI_STORY"
        else
            # Default behavior - validate all staged story files
            STORY_FILES=$(git diff --cached --name-only --diff-filter=d | grep '\.story\.md$' | grep -v '^tests/' || true)
        fi

    - type: "Shell Script Template"
      name: "install_hooks.sh"
      file_path: "src/claude/scripts/install_hooks.sh"
      modification: "Update hook template to include scoping logic"
      lines_affected: "Template section for pre-commit hook"
      test_requirement: "Test: Installed hook contains scoping logic"

    - type: "Documentation"
      name: "STORY-SCOPED-COMMITS.md"
      file_path: "devforgeai/docs/STORY-SCOPED-COMMITS.md"
      purpose: "User guide for scoped commits"
      required_sections:
        - section: "Overview"
          description: "What scoped commits are, when to use"
        - section: "Basic Usage"
          description: "Syntax: DEVFORGEAI_STORY=STORY-120 git commit"
        - section: "Examples"
          description: "Walkthrough scenarios (single story, multiple uncommitted stories)"
        - section: "Troubleshooting"
          description: "Common issues and solutions"

  data_models:
    - name: "Environment Variable"
      variable: "DEVFORGEAI_STORY"
      type: "string (shell env var)"
      format: "STORY-NNN (3-digit number)"
      example: "STORY-114"
      validation: "Must match STORY-\\d{3} format or be unset"
      scope: "Session-local (per git commit command)"
      required: false (defaults to unscoped if unset)

  validation_logic:
    scoped_mode:
      trigger: "[ -n \"$DEVFORGEAI_STORY\" ]"
      action: "grep \"${DEVFORGEAI_STORY}\" from staged files"
      output: "Only files matching story ID"
      message: "Scoped to: STORY-XXX"
    unscoped_mode:
      trigger: "DEVFORGEAI_STORY is unset"
      action: "grep '\\.story\\.md$' from staged files"
      output: "All .story.md files"
      message: "(no message)"

  behavior:
    precedence: "env var DEVFORGEAI_STORY > default behavior"
    effect_scope: "Single git commit command only"
    persistence: "Variable does NOT persist to next command (session-local)"
    validation_target: "Only affects which files dod_validator checks"
```

## Non-Functional Requirements

| Requirement | Target | Justification |
|-------------|--------|---------------|
| Pre-commit overhead | <500ms additional | Minimal impact on commit speed |
| Backward compatibility | 100% when env var unset | No breaking changes to existing workflows |
| Validation accuracy | 100% for correct story ID | Must not accidentally validate wrong story |

## Test Strategy

### Unit Tests
- **Test 1:** Hook filters correctly when DEVFORGEAI_STORY set
- **Test 2:** Hook validates all stories when DEVFORGEAI_STORY unset
- **Test 3:** Hook message shows "Scoped to: STORY-120" when set
- **Test 4:** Hook message absent when unset

### Integration Tests
- **Test 5:** Developer can commit STORY-114 with scoping while STORY-115 has errors (both uncommitted)
- **Test 6:** Without scoping, STORY-115 errors block STORY-114 commit
- **Test 7:** Multiple stories staged, scoping validates only target story
- **Test 8:** Explicit story ID (STORY-120) scopes correctly

### Edge Cases
- **Test 9:** Invalid STORY-XXX format in env var (e.g., STORY-120-extra) gracefully handled
- **Test 10:** Empty DEVFORGEAI_STORY (unset) defaults to unscoped
- **Test 11:** Case sensitivity: STORY-120 vs story-120 vs Story-120

## Definition of Done

### Implementation
- [ ] `.git/hooks/pre-commit` lines 44-58 modified with scoping logic
- [ ] `src/claude/scripts/install_hooks.sh` hook template updated
- [ ] `devforgeai/docs/STORY-SCOPED-COMMITS.md` created with complete guidance
- [ ] Logic validates DEVFORGEAI_STORY format (STORY-\\d{3} only)

### Quality
- [ ] All unit tests passing (4 tests)
- [ ] All integration tests passing (4 tests)
- [ ] All edge cases handled (3 tests)
- [ ] No security vulnerabilities (env var injection proof)
- [ ] Hook performance <500ms overhead verified

### Testing
- [ ] Manual test: DEVFORGEAI_STORY=STORY-120 git commit validates only STORY-120
- [ ] Manual test: git commit without env var validates all stories (backward compatible)
- [ ] Manual test: Invalid STORY-ID format handled gracefully
- [ ] Manual test: Reinstall hooks via install_hooks.sh includes scoping logic

### Documentation
- [ ] STORY-SCOPED-COMMITS.md complete with examples
- [ ] Hook comments explain scoping logic
- [ ] install_hooks.sh comments updated
- [ ] README references scoped commits feature

### Release
- [ ] All tests passing
- [ ] Code reviewed for security (env var sanitization)
- [ ] Backward compatibility verified
- [ ] Ready for QA validation
