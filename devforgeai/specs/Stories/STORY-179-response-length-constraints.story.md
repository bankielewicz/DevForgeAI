---
id: STORY-179
title: Add Response Length Constraints to Subagent Prompts
type: refactor
epic: EPIC-033
priority: MEDIUM
points: 2
status: Backlog
created: 2025-12-31
source: STORY-156 framework enhancement analysis
---

# STORY-179: Add Response Length Constraints to Subagent Prompts

## User Story

**As a** DevForgeAI framework user,
**I want** subagent prompts to include response length constraints,
**So that** context window consumption is reduced by ~40%.

## Background

Subagents return verbose responses (~13K tokens for parallel validators) when only actionable findings are needed.

## Acceptance Criteria

### AC-1: All Subagent Prompts Include Response Constraints
**Given** Task prompts in phase files
**Then** all include "Response Constraints" section

### AC-2: Maximum Word Limit Specified
**Then** 500 words maximum recommended

### AC-3: Bullet Point Format Mandated
**Then** "Use bullet points, not paragraphs" instruction added

### AC-4: Actionable Findings Only
**Then** "Only include actionable findings" instruction added

### AC-5: Token Reduction Measurable
**Then** target: -40% token reduction

## Technical Specification

### Files to Modify
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md`
- `.claude/skills/devforgeai-development/phases/phase-03-implementation.md`
- `.claude/skills/devforgeai-development/phases/phase-04-refactoring.md`
- `.claude/skills/devforgeai-development/phases/phase-05-integration.md`

### Constraint Template
```markdown
**Response Constraints:**
- Limit response to 500 words maximum
- Use bullet points, not paragraphs
- Only include actionable findings
- No code snippets unless essential
```

## Definition of Done

- [ ] Response constraints added to phase-02-test-first.md
- [ ] Response constraints added to phase-03-implementation.md
- [ ] Response constraints added to phase-04-refactoring.md
- [ ] Response constraints added to phase-05-integration.md
- [ ] Consistent format across all phase files

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 1 hour

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-156 framework enhancement |
