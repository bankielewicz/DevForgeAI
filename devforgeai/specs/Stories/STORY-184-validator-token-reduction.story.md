---
id: STORY-184
title: Reduce Validator Token Overhead with Response Constraints
type: refactor
epic: EPIC-033
priority: MEDIUM
points: 1
status: Backlog
created: 2025-12-31
source: STORY-153 framework enhancement analysis
---

# STORY-184: Reduce Validator Token Overhead with Response Constraints

## User Story

**As a** DevForgeAI user,
**I want** parallel validator prompts to include response constraints,
**So that** token usage is reduced from ~13K to <6K total.

## Acceptance Criteria

### AC-1: Test-Automator Prompt Has Constraints
**Then** response constraints added to test-automator prompt

### AC-2: Code-Reviewer Prompt Has Constraints
**Then** response constraints added to code-reviewer prompt

### AC-3: Security-Auditor Prompt Has Constraints
**Then** response constraints added to security-auditor prompt

### AC-4: Response Format Defined
**Then** format: Status, Coverage%, Key findings (max 3), Blocking issues

### AC-5: Exclusions Documented
**Then** "Do NOT include: full analysis, code snippets, detailed recommendations"

## Technical Specification

### Files to Modify
- `.claude/skills/devforgeai-qa/references/parallel-validation.md`

### Constraint Template
```markdown
**Response Constraints:**
Return ONLY:
1. Status: PASS/FAIL
2. Coverage %: {number}
3. Key findings (max 3 bullets)
4. Blocking issues (if any)

Do NOT include: full analysis, code snippets, detailed recommendations.
```

## Definition of Done

- [ ] Constraints added to test-automator prompt
- [ ] Constraints added to code-reviewer prompt
- [ ] Constraints added to security-auditor prompt
- [ ] Response format documented
- [ ] Token reduction measured (<2K per validator)

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 20 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-153 framework enhancement |
