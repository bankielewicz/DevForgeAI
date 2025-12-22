---
id: STORY-129
title: CLI Command Availability Check
type: feature
status: Backlog
priority: MEDIUM
story-points: 2
epic: EPIC-026
sprint: null
created: 2025-12-20
assignee: null
depends-on: []
---

# STORY-129: CLI Command Availability Check

## User Story

**As a** DevForgeAI developer
**I want** graceful fallback when devforgeai CLI is not installed
**So that** preflight validation doesn't fail with cryptic errors

## Background

During STORY-114 development, `devforgeai check-hooks` returned "Unknown command" because the CLI is not fully implemented. This creates confusion when documentation references commands that don't exist or aren't installed.

**Observation from STORY-114:** CLI commands are referenced in documentation but may not be available, causing unexpected failures.

## Acceptance Criteria

### AC#1: Preflight Step 0.0.5 Checks CLI Availability
**Given** the preflight-validation.md reference file
**When** I search for "CLI Availability"
**Then** a new Step 0.0.5 exists that checks if `devforgeai` command is available

### AC#2: Warning Displayed If CLI Not Installed
**Given** the devforgeai CLI is not installed
**When** preflight runs
**Then** a warning (not error) is displayed:
```
WARN: devforgeai CLI not installed
  - Hook checks will be skipped
  - Manual validation required
```

### AC#3: CLI Version Displayed If Available
**Given** the devforgeai CLI is installed
**When** preflight runs
**Then** it displays:
```
✓ devforgeai CLI: {version}
```

### AC#4: Downstream Steps Skip CLI Calls Gracefully
**Given** CLI_AVAILABLE is false
**When** a step would call `devforgeai check-hooks` or similar
**Then** it skips with message: "Skipping: CLI-based hook checks (CLI not available)"
**And** does not fail the preflight

### AC#5: Fallback Validation Documented
**Given** CLI is not available
**When** developer needs to validate manually
**Then** preflight-validation.md documents:
- What CLI validations are skipped
- How to perform manual validation
- What risks exist without CLI validation

## Technical Specification

### Files to Modify
| File | Changes |
|------|---------|
| `.claude/skills/devforgeai-development/references/preflight-validation.md` | Add Step 0.0.5 CLI Availability Check |

### New Preflight Step (Step 0.0.5)
```markdown
## Step 0.0.5: CLI Availability Check

**Purpose:** Verify devforgeai CLI is installed before attempting CLI-based validations.

**Token Cost:** ~100 tokens

**Implementation:**
```bash
if ! command -v devforgeai &> /dev/null; then
    echo "WARN: devforgeai CLI not installed"
    echo "  - Hook checks will be skipped"
    echo "  - Manual validation required"
    CLI_AVAILABLE=false
else
    CLI_AVAILABLE=true
    DEVFORGEAI_VERSION=$(devforgeai --version 2>/dev/null || echo "unknown")
    echo "✓ devforgeai CLI: $DEVFORGEAI_VERSION"
fi
```

**Downstream Impact:**
When `CLI_AVAILABLE=false`:
- Skip: `devforgeai check-hooks`
- Skip: `devforgeai validate-dod`
- Skip: `devforgeai validate-context`

**Fallback:** Use grep-based validation patterns documented in each step.

**Success:** `CLI_AVAILABLE` variable set for downstream steps.
**Failure:** N/A - this step always succeeds (warning only).
```

### CLI-Dependent Steps to Update
| Step | CLI Command | Fallback |
|------|-------------|----------|
| Step N.N | `devforgeai check-hooks` | Grep hooks.yaml for operation |
| Step N.N | `devforgeai validate-dod` | Grep story file for DoD checkboxes |
| Step N.N | `devforgeai validate-context` | Check 6 context files exist |

### Fallback Validation Patterns (Claude Code Terminal Tools)
```markdown
## Manual Validation When CLI Not Available

### Hook Eligibility (replaces devforgeai check-hooks)
Grep(pattern="operation: dev", path="src/devforgeai/config/hooks.yaml", output_mode="count")
If count > 0: Hooks enabled for dev operation

### DoD Validation (replaces devforgeai validate-dod)
Grep(pattern="^\\s*-\\s*\\[[ x]\\]", path="$STORY_FILE", output_mode="count")
Count represents number of DoD checkbox items

### Context Validation (replaces devforgeai validate-context)
For each context file, verify exists:
- Read(file_path="devforgeai/specs/context/tech-stack.md")
- Read(file_path="devforgeai/specs/context/source-tree.md")
- Read(file_path="devforgeai/specs/context/dependencies.md")
- Read(file_path="devforgeai/specs/context/coding-standards.md")
- Read(file_path="devforgeai/specs/context/architecture-constraints.md")
- Read(file_path="devforgeai/specs/context/anti-patterns.md")

If ANY Read fails: Context incomplete - run /create-context
```

## Test Strategy

### Test Files Location
`devforgeai/tests/STORY-129/`

### Test Cases
| Test ID | Description | Type |
|---------|-------------|------|
| test-ac1-step-exists.sh | Verify Step 0.0.5 exists in preflight-validation.md | Bash |
| test-ac2-warning-format.sh | Verify warning message format when CLI missing | Bash |
| test-ac3-version-display.sh | Verify version displayed when CLI available | Bash |
| test-ac4-skip-gracefully.sh | Verify downstream steps skip without failing | Bash |
| test-ac5-fallback-docs.sh | Verify fallback validation documented | Bash |

## Definition of Done

### Implementation
- [ ] Step 0.0.5 added to preflight-validation.md
- [ ] CLI availability check uses `command -v`
- [ ] Warning message format matches AC#2
- [ ] CLI_AVAILABLE variable set for downstream use
- [ ] Downstream steps check CLI_AVAILABLE before CLI calls
- [ ] Fallback validation patterns documented

### Quality
- [ ] All 5 test cases pass
- [ ] Tested with CLI installed and uninstalled
- [ ] No preflight failures due to missing CLI

### Documentation
- [ ] Step 0.0.5 documented with token cost
- [ ] Fallback validation patterns included
- [ ] Risks of skipped validations documented

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| CLI fallback misses validations | Document which validations are CLI-only and their risks |
| Grep-based fallback produces false positives | Test fallback patterns against real story files |
| CLI version check fails silently | Use `2>/dev/null` with fallback to "unknown" |

## Out of Scope

- Automatic CLI installation
- Feature parity between CLI and grep-based validation
- CLI command implementation (separate story)
