---
id: STORY-181
title: Add .gitattributes for Line Ending Normalization
type: bugfix
epic: EPIC-033
priority: MEDIUM
points: 1
status: Backlog
created: 2025-12-31
source: STORY-155 framework enhancement analysis
---

# STORY-181: Add .gitattributes for Line Ending Normalization

## User Story

**As a** DevForgeAI developer,
**I want** shell scripts to have normalized line endings,
**So that** test files generated on Windows execute without errors.

## Background

Test files with CRLF line endings cause: "syntax error near unexpected token"

## Acceptance Criteria

### AC-1: .gitattributes Created
**Given** project root
**Then** .gitattributes file exists

### AC-2: Shell Files Configured for LF
**Then** `*.sh text eol=lf` in .gitattributes

### AC-3: Test Shell Files Configured
**Then** `tests/**/*.sh text eol=lf` in .gitattributes

### AC-4: Existing Files Normalized
**Then** existing CRLF files normalized on next commit

### AC-5: Test-Automator Updated (Optional)
**Then** post-generation normalization step added

## Technical Specification

### Files to Create/Modify
- `.gitattributes` (create)
- `.claude/agents/test-automator.md` (optional)

### .gitattributes Content
```
*.sh text eol=lf
tests/**/*.sh text eol=lf
```

### Optional Normalization Step
```markdown
# Use native Edit tool for line ending normalization (per tech-stack.md lines 206-210)
Edit(file_path="${TEST_FILE}", old_string="\r\n", new_string="\n", replace_all=true)
```
**Note:** Native tools are required per tech-stack.md - Bash should NOT be used for file operations.

## Definition of Done

- [ ] .gitattributes created at project root
- [ ] *.sh configured for LF
- [ ] tests/**/*.sh configured for LF
- [ ] Existing files normalized

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 15 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-155 framework enhancement |
