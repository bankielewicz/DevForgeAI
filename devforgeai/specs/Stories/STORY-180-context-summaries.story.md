---
id: STORY-180
title: Pass Context File Summaries to Subagents
type: refactor
epic: EPIC-033
priority: MEDIUM
points: 2
status: Backlog
created: 2025-12-31
source: STORY-156 QA framework enhancement analysis
---

# STORY-180: Pass Context File Summaries to Subagents

## User Story

**As a** DevForgeAI framework user,
**I want** subagent prompts to include context file summaries,
**So that** subagents don't redundantly load 6 context files (~3-4K tokens).

## Background

Anti-pattern-scanner and other subagents re-read context files that the parent skill already loaded.

## Acceptance Criteria

### AC-1: Context Summary Format Defined
**Then** concise summary format documented (key constraints only)

### AC-2: Anti-Pattern Scanner Accepts Summary
**Given** anti-pattern-scanner.md
**Then** accepts "Context Summary" in prompt

### AC-3: Subagent Documentation Updated
**Then** "IF context_files_in_prompt: Use provided summaries" documented

### AC-4: QA Skill Passes Summaries
**Given** deep validation
**Then** context summaries passed to validators

### AC-5: Token Reduction Measurable
**Then** target: -3K tokens per subagent call

## Technical Specification

### Files to Modify
- `.claude/agents/anti-pattern-scanner.md`
- `.claude/skills/devforgeai-qa/references/parallel-validation.md`

### Summary Format
```markdown
**Context Summary (do not re-read files):**
- tech-stack.md: Framework-agnostic, Markdown-based, no external deps
- anti-patterns.md: No Bash for file ops, no monolithic components
- architecture-constraints.md: Three-layer, single responsibility
```

## Definition of Done

- [ ] Context summary format defined
- [ ] Anti-pattern-scanner accepts summaries
- [ ] Subagent documentation updated
- [ ] QA skill passes summaries
- [ ] Token reduction measured

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 2 hours

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-156 QA framework enhancement |
