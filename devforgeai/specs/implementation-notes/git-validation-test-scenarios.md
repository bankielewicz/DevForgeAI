# Git Validation Test Scenarios

**Implementation:** RCA-006 Recommendations #1 and #2
**Date:** 2025-11-04
**Status:** Ready for Testing

---

## Overview

This document provides test scenarios for validating the Git repository validation implementation in DevForgeAI. The implementation adds pre-flight Git checks to `/dev` command and graceful degradation to `devforgeai-development` skill.

---

## Test Scenario 1: Git Repository (Happy Path)

**Purpose:** Verify normal operation when Git is available

### Setup

```bash
# Create test project with Git
mkdir -p /tmp/test-devforgeai-with-git
cd /tmp/test-devforgeai-with-git

# Initialize Git
git init
git commit --allow-empty -m "Initial commit"

# Create minimal DevForgeAI structure
mkdir -p devforgeai/context .ai_docs/Stories

# Create minimal context files
echo "# Tech Stack" > devforgeai/context/tech-stack.md
echo "# Source Tree" > devforgeai/context/source-tree.md
echo "# Dependencies" > devforgeai/context/dependencies.md
echo "# Coding Standards" > devforgeai/context/coding-standards.md
echo "# Architecture Constraints" > devforgeai/context/architecture-constraints.md
echo "# Anti-Patterns" > devforgeai/context/anti-patterns.md

# Create test story
cat > devforgeai/specs/Stories/STORY-001.story.md <<'EOF'
---
id: STORY-001
title: Test Story
status: Ready for Dev
---

# Test Story

Test story for Git validation.

## Acceptance Criteria

- Given a test scenario
- When executed
- Then should pass
EOF
```

### Test Execution

```bash
# In Claude Code terminal
> /dev STORY-001
```

### Expected Results

✅ **Phase 0: Environment Validation**
- Output: "✓ Git repository detected"
- Output: "✓ Proceeding to argument validation..."
- Displays git status output

✅ **Skill Execution**
- Output: "✓ Git repository detected - full workflow enabled"
- Output: "  - Branch management: Enabled"
- Output: "  - Commit tracking: Enabled"
- Output: "  - Version control: Enabled"

✅ **Phase 5: Git Workflow**
- Executes normal Git commands (git status, git diff, git add, git commit)
- Creates commit with conventional format
- Story file updated with Implementation Notes
- Git commit includes story file

✅ **Completion**
- Story status = "Dev Complete"
- Git commit created successfully
- No errors or warnings about Git

### Validation Checklist

- [ ] Pre-flight check passes
- [ ] Git status displayed in Pre-execution Context
- [ ] Skill detects Git availability
- [ ] Full TDD workflow executes
- [ ] Git commit created
- [ ] Story file included in commit
- [ ] No Git-related errors

---

## Test Scenario 2: Non-Git Directory (Error Path)

**Purpose:** Verify pre-flight check fails gracefully when Git missing

### Setup

```bash
# Create test project WITHOUT Git
mkdir -p /tmp/test-devforgeai-no-git
cd /tmp/test-devforgeai-no-git

# Create minimal DevForgeAI structure (NO git init)
mkdir -p devforgeai/context .ai_docs/Stories

# Create minimal context files (same as Scenario 1)
echo "# Tech Stack" > devforgeai/context/tech-stack.md
echo "# Source Tree" > devforgeai/context/source-tree.md
echo "# Dependencies" > devforgeai/context/dependencies.md
echo "# Coding Standards" > devforgeai/context/coding-standards.md
echo "# Architecture Constraints" > devforgeai/context/architecture-constraints.md
echo "# Anti-Patterns" > devforgeai/context/anti-patterns.md

# Create test story (same as Scenario 1)
cat > devforgeai/specs/Stories/STORY-001.story.md <<'EOF'
---
id: STORY-001
title: Test Story
status: Ready for Dev
---

# Test Story

Test story for Git validation.

## Acceptance Criteria

- Given a test scenario
- When executed
- Then should pass
EOF
```

### Test Execution

```bash
# In Claude Code terminal
> /dev STORY-001
```

### Expected Results

❌ **Phase 0: Environment Validation HALTS**

Output displays error box:
```
┌─────────────────────────────────────────────────────────────────┐
│ ❌ ERROR: Git Repository Required                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ The /dev command requires a Git repository for version         │
│ control, but the current directory is not Git-initialized.     │
│                                                                 │
│ CURRENT DIRECTORY:                                              │
│   /tmp/test-devforgeai-no-git                                  │
│                                                                 │
│ Git Status: NOT INITIALIZED                                     │
│                                                                 │
│ RESOLUTION:                                                     │
│                                                                 │
│ Option 1: Initialize Git (Recommended)                         │
│   git init                                                      │
│   git add .                                                     │
│   git commit -m "Initial commit"                               │
│                                                                 │
│ Option 2: Use manual development workflows                     │
│   DevForgeAI requires Git for:                                 │
│   - /dev (TDD development)                                     │
│   - /qa (quality validation)                                   │
│   - /release (deployment)                                      │
│   - /orchestrate (full lifecycle)                              │
│                                                                 │
│   Git-independent commands:                                    │
│   - /ideate (requirements gathering)                           │
│   - /create-context (architecture setup)                       │
│   - /create-story (story generation)                           │
│                                                                 │
│ For more information:                                           │
│   See CLAUDE.md section "Prerequisites > Git Repository"       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

✅ **Command Halts**
- Does NOT proceed to Phase 0a (Argument Validation)
- Does NOT execute any Bash git commands
- Does NOT invoke devforgeai-development skill
- NO cryptic Git errors displayed

### Validation Checklist

- [ ] Pre-flight check detects Git missing
- [ ] Clear error message displayed
- [ ] Resolution steps provided
- [ ] Command halts before Bash execution
- [ ] No cryptic errors (fatal: not a git repository)
- [ ] User understands next actions

### Recovery Test

After seeing error, user initializes Git:

```bash
git init
git add .
git commit -m "Initial commit"

# Retry command
> /dev STORY-001
```

Expected: Now passes and executes normally (same as Scenario 1)

---

## Test Scenario 3: Skill File-Based Fallback (Advanced)

**Purpose:** Verify skill graceful degradation when Git unavailable but skill invoked directly

### Setup

```bash
# Same as Scenario 2 (no Git)
mkdir -p /tmp/test-skill-fallback
cd /tmp/test-skill-fallback

# Create minimal structure
mkdir -p devforgeai/context .ai_docs/Stories

# Create context files and story (same as above)
```

### Test Execution

```bash
# Manually load story
@devforgeai/specs/Stories/STORY-001.story.md

# Directly invoke skill (bypassing /dev command pre-flight check)
Skill(command="devforgeai-development")
```

### Expected Results

⚠️ **Phase 0: Git Availability Detection**

Output:
```
⚠ Git not available - using file-based workflow
  - Branch management: Disabled
  - Commit tracking: Disabled (manual file organization)
  - Version control: Disabled (changes tracked in story file)

Note: Initialize Git to enable full DevForgeAI features:
      git init && git add . && git commit -m 'Initial commit'
```

✅ **TDD Phases Execute Normally**
- Phase 1-4 (Red/Green/Refactor/Integration) work identically
- All tests execute
- Code implementation proceeds
- NO Git commands attempted

✅ **Phase 5: File-Based Change Tracking**

Instead of Git workflow, executes:
1. Creates `devforgeai/stories/STORY-001/changes/` directory
2. Generates `implementation-{timestamp}.md` manifest
3. Updates story file with file-based tracking reference
4. Displays completion summary with Git migration instructions

Output:
```
┌─────────────────────────────────────────────────────────────────┐
│ ✅ Development Complete (File-Based Workflow)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Story: STORY-001 - Test Story                                  │
│ Status: Dev Complete                                            │
│                                                                 │
│ Tests: X/Y passing                                              │
│ Coverage: Z%                                                    │
│                                                                 │
│ Changes tracked in:                                             │
│   devforgeai/stories/STORY-001/changes/implementation-...     │
│                                                                 │
│ Git Integration: Not Available                                  │
│                                                                 │
│ To enable Git workflow:                                         │
│   git init                                                      │
│   git add .                                                     │
│   git commit -m 'Initial commit'                               │
│   Then re-run: /dev STORY-001                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

✅ **Artifacts Created**
- `devforgeai/stories/STORY-001/changes/implementation-{timestamp}.md` exists
- Contains file lists, test results, acceptance criteria status
- Story file updated with "File-Based" workflow history entry
- Story status = "Dev Complete"

### Validation Checklist

- [ ] Skill detects Git unavailable
- [ ] Warning message displayed
- [ ] TDD phases execute without Git commands
- [ ] File-based tracking artifacts created
- [ ] Change manifest contains all required sections
- [ ] Story file updated correctly
- [ ] Clear migration instructions provided
- [ ] No Git-related errors

---

## Test Scenario 4: Git Initialization During Session

**Purpose:** Verify transition from file-based to Git-based workflow

### Setup

```bash
# Start without Git
mkdir -p /tmp/test-git-transition
cd /tmp/test-git-transition

# Create structure
mkdir -p devforgeai/context .ai_docs/Stories

# Create files (same as above)
```

### Test Execution - Part 1 (No Git)

```bash
# First attempt without Git
> /dev STORY-001

# Expected: Error message with instructions
# User sees resolution steps
```

### Test Execution - Part 2 (Initialize Git)

```bash
# User initializes Git
git init
git add .
git commit -m "Initial commit"

# Retry command
> /dev STORY-001

# Expected: Now executes with full Git workflow
```

### Expected Results

✅ **Transition Successful**
- First attempt: Pre-flight check fails
- After git init: Pre-flight check passes
- Second attempt: Full Git workflow available
- All Git features enabled

### Validation Checklist

- [ ] Pre-flight check detects state change
- [ ] Git-based workflow activates after initialization
- [ ] No residual file-based artifacts
- [ ] Git commit created properly
- [ ] Story tracked in version control

---

## Validation Summary

### Test Coverage

| Scenario | Purpose | Git Status | Expected Outcome |
|----------|---------|------------|------------------|
| 1 | Happy path | Available | Full Git workflow |
| 2 | Error handling | Missing | Clear error, no cryptic messages |
| 3 | Fallback | Missing | File-based tracking works |
| 4 | State transition | Added mid-session | Workflow adapts correctly |

### Success Criteria

All scenarios must pass:
- [ ] Scenario 1: Git workflow executes normally
- [ ] Scenario 2: Pre-flight check fails gracefully
- [ ] Scenario 3: File-based fallback creates artifacts
- [ ] Scenario 4: Git initialization enables full workflow

### Framework Principles Validation

- [ ] **Ask, Don't Assume:** Error messages guide users clearly
- [ ] **Evidence-Based:** Uses proven `git rev-parse` pattern
- [ ] **Token Efficient:** Native tools used throughout
- [ ] **Non-Aspirational:** No hypothetical features
- [ ] **Graceful Degradation:** File-based fallback works
- [ ] **No Breaking Changes:** Existing Git workflows unaffected

---

## Notes for Testing

**Environment Requirements:**
- Claude Code terminal access
- Ability to create test directories
- Git installed (for Scenario 1 and 4)
- Ability to run `/dev` command

**Time Estimate:**
- Scenario 1: ~5 minutes
- Scenario 2: ~3 minutes
- Scenario 3: ~10 minutes (skill direct invocation)
- Scenario 4: ~5 minutes
- **Total: ~25 minutes**

**Cleanup:**
```bash
rm -rf /tmp/test-devforgeai-with-git
rm -rf /tmp/test-devforgeai-no-git
rm -rf /tmp/test-skill-fallback
rm -rf /tmp/test-git-transition
```

---

**Status:** Test scenarios documented and ready for execution
