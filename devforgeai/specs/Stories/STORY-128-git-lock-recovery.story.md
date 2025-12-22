---
id: STORY-128
title: Git Lock File Recovery
type: documentation
status: Backlog
priority: MEDIUM
story-points: 2
epic: EPIC-026
sprint: null
created: 2025-12-20
assignee: null
depends-on: []
---

# STORY-128: Git Lock File Recovery

## User Story

**As a** DevForgeAI developer on WSL2
**I want** documented steps to recover from stale git lock files
**So that** I can quickly resolve "index.lock exists" errors

## Background

During STORY-114 development on WSL2, a stale `.git/index.lock` file blocked git operations. This is a common issue in WSL2 environments due to:
- VS Code Git extension holding locks
- Cross-filesystem access between Windows and WSL
- Previous git commands crashing without cleanup

**Observation from STORY-114:** Lock files are common in WSL2 and recovery is simple but not documented.

## Acceptance Criteria

### AC#1: Lock File Recovery Section in git-workflow-conventions.md
**Given** the git-workflow-conventions.md reference file
**When** I search for "Lock File Recovery"
**Then** a section exists with:
- Diagnosis commands
- Recovery commands
- Safety warnings

### AC#2: Diagnosis Commands Documented
**Given** the Lock File Recovery section
**When** I read the diagnosis steps
**Then** it includes:
```bash
ls -la .git/index.lock  # Check if lock exists
ps aux | grep git       # Check for running git processes
```

### AC#3: Recovery Commands with Safety Warning
**Given** the Lock File Recovery section
**When** I read the recovery steps
**Then** it includes:
```bash
rm -f .git/index.lock
```
**And** a warning: "Only run this if no git processes are running"

### AC#4: WSL2-Specific Guidance
**Given** the Lock File Recovery section
**When** I search for "WSL"
**Then** it documents:
- Common causes in WSL2 (VS Code, cross-filesystem, crashes)
- Prevention tips (close VS Code Git panels, use native paths)

### AC#5: Prevention Tips Documented
**Given** the Lock File Recovery section
**When** I read prevention guidance
**Then** it includes:
- Close VS Code Git panels before terminal git operations
- Use native WSL paths (/mnt/c/) not Windows paths (C:\)
- Avoid running git from both Windows and WSL simultaneously

## Technical Specification

### Files to Modify
| File | Changes |
|------|---------|
| `.claude/skills/devforgeai-development/references/git-workflow-conventions.md` | Add Lock File Recovery section |

### Section Content
```markdown
## Lock File Recovery

### Problem
Git fails with error: "fatal: Unable to create '.git/index.lock': File exists"

### Diagnosis
```bash
# Check if lock file exists
ls -la .git/index.lock

# Check for running git processes
ps aux | grep git

# On Windows (if using PowerShell)
tasklist | findstr git
```

### Recovery
**WARNING:** Only proceed if no git processes are running.

```bash
# Remove stale lock file
rm -f .git/index.lock
```

### WSL2-Specific Notes

**Common Causes:**
- VS Code with Git extension is open and polling for changes
- Cross-filesystem access between Windows (`C:\`) and WSL (`/mnt/c/`)
- Previous git command crashed without cleanup
- File system sync issues between Windows and WSL

**Prevention:**
1. Close VS Code Git panels before running git in terminal
2. Use native WSL paths (`/mnt/c/Projects/`) not Windows paths (`C:\Projects\`)
3. Avoid running git from both Windows CMD and WSL on same repo
4. If using VS Code, disable "Git: Autofetch" setting temporarily

**Alternative Recovery (if rm fails):**
```bash
# Force remove on Windows filesystem
rm -rf .git/index.lock 2>/dev/null || cmd.exe /c "del /f /q .git\\index.lock"
```
```

## Test Strategy

### Test Files Location
`devforgeai/tests/STORY-128/`

### Test Cases
| Test ID | Description | Type |
|---------|-------------|------|
| test-ac1-section-exists.sh | Verify Lock File Recovery section exists | Bash |
| test-ac2-diagnosis-commands.sh | Verify diagnosis commands documented | Bash |
| test-ac3-recovery-warning.sh | Verify recovery includes safety warning | Bash |
| test-ac4-wsl2-guidance.sh | Verify WSL2-specific guidance present | Bash |
| test-ac5-prevention-tips.sh | Verify prevention tips documented | Bash |

## Definition of Done

### Implementation
- [ ] Lock File Recovery section added to git-workflow-conventions.md
- [ ] Diagnosis commands documented
- [ ] Recovery commands with safety warning
- [ ] WSL2-specific causes documented
- [ ] Prevention tips included

### Quality
- [ ] All 5 test cases pass
- [ ] Commands tested on WSL2 environment
- [ ] No broken markdown formatting

### Documentation
- [ ] Section is well-organized with clear headers
- [ ] Examples are copy-paste ready
- [ ] Warnings are prominent

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Lock file guidance causes data loss | Include safety checks - verify no git process running before rm |
| Documentation becomes outdated | Link to official git documentation for authoritative reference |
| Users skip diagnosis and blindly rm | Make warning prominent, add "DANGER" formatting |

## Out of Scope

- Automatic lock file detection and cleanup
- Integration with pre-commit hooks
- Windows-native (non-WSL) documentation
