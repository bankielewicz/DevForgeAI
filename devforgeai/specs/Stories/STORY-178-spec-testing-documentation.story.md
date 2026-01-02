---
id: STORY-178
title: Document Specification File Testing Pattern in Test-Automator
type: documentation
epic: EPIC-033
priority: MEDIUM
points: 1
status: Backlog
created: 2025-12-31
source: STORY-156 framework enhancement analysis
---

# STORY-178: Document Specification File Testing Pattern in Test-Automator

## User Story

**As a** DevForgeAI developer,
**I want** guidance on testing Markdown specification files,
**So that** tests validate structure rather than brittle narrative text.

## Acceptance Criteria

### AC-1: Specification File Testing Section Added
**Given** test-automator.md
**Then** includes "Specification File Testing" section

### AC-2: Structural Testing Guidance
**Then** guidance for testing section headers, phase markers documented

### AC-3: Tool Invocation Testing Guidance
**Then** guidance for testing AskUserQuestion, Read, Write references documented

### AC-4: Anti-Pattern Documented
**Then** "Avoid testing for specific comment text" documented

### AC-5: Example Patterns Provided
**Then** example test patterns for Markdown commands included

## Technical Specification

### Files to Modify
- `.claude/agents/test-automator.md`

### Content to Add
```markdown
### Specification File Testing (Markdown Commands/Skills)

For Markdown specification files, generate tests that validate:
1. **Structural elements** (section headers, phase markers)
2. **Tool invocations** (AskUserQuestion, Read, Write)
3. **Data contracts** (input/output schemas)

**Avoid:**
- Testing for specific comment text (changes during refactoring)
- Testing for narrative phrases (not structural)
```

## Definition of Done

- [ ] "Specification File Testing" section added
- [ ] Structural testing guidance documented
- [ ] Tool invocation testing guidance documented
- [ ] Anti-pattern documented
- [ ] Example patterns provided

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 15 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-156 framework enhancement |
