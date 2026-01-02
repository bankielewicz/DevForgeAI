---
id: STORY-176
title: Add Slash Command Exclusions to Anti-Pattern Scanner
type: bugfix
epic: EPIC-033
priority: HIGH
points: 2
status: Backlog
created: 2025-12-31
source: STORY-155, STORY-153 framework enhancement analysis
---

# STORY-176: Add Slash Command Exclusions to Anti-Pattern Scanner

## User Story

**As a** DevForgeAI framework maintainer,
**I want** the anti-pattern-scanner to exclude Markdown specification files from inappropriate violation categories,
**So that** valid Slash Command files don't trigger false positive violations.

## Acceptance Criteria

### AC#1: Exclusions Section Added
**Given** anti-pattern-scanner.md
**Then** includes `## Exclusions` section with file pattern rules

### AC#2: Command Files Excluded from Structure Validation
**Given** files matching `.claude/commands/*.md`
**When** Phase 3 runs
**Then** files skipped with log message

### AC#3: Skill Files Excluded from Code Smell Detection
**Given** files matching `.claude/skills/**/*.md`
**When** Phase 5 runs
**Then** files skipped

### AC#4: Pre-Report Verification
**Given** structure violation about to be reported
**Then** verify path exists in source-tree.md before flagging

### AC#5: Skip Security Scanning on Code Examples
**Given** Markdown with fenced code blocks
**When** Phase 6 runs
**Then** code examples not scanned for vulnerabilities

### AC#6: Zero False Positives
**Given** valid Slash Command files
**When** full scan runs
**Then** zero CRITICAL/HIGH/MEDIUM violations

## Technical Specification

### Files to Modify
- `.claude/agents/anti-pattern-scanner.md`

### Exclusion Patterns
```yaml
exclusion_patterns:
  - pattern: ".claude/commands/*.md"
    excludes_from: [Phase 3, Phase 6 code examples]
  - pattern: ".claude/skills/**/*.md"
    excludes_from: [Phase 5, Phase 6 code examples]
  - pattern: ".claude/agents/*.md"
    excludes_from: [Phase 5]
```

## Definition of Done

- [ ] `## Exclusions` section added
- [ ] File pattern rules documented
- [ ] `## Pre-Report Verification` section added
- [ ] Phase 3 skips `.claude/commands/*.md`
- [ ] Phase 5 skips `.claude/skills/**/*.md`
- [ ] Phase 6 skips fenced code blocks
- [ ] Zero false positives verified

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 30 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-155/153 framework enhancement |
