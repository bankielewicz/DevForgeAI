---
id: EPIC-033
title: Framework Enhancement Triage Q4 2025
business-value: Consolidate and implement accumulated framework improvement recommendations from AI analysis
status: Planning
priority: High
complexity-score: 25
architecture-tier: Tier 2
created: 2025-12-31
estimated-points: 35-55
target-sprints: 2-3
epic: EPIC-033
---

# Framework Enhancement Triage Q4 2025

## Business Goal

Implement accumulated framework improvement recommendations from AI architectural analysis captured during STORY-144 through STORY-158 development cycles, providing:
- **Framework Stability:** Eliminate false positives and workflow interruptions
- **Developer Experience:** Reduce friction points in /dev and /qa workflows
- **Scalability:** Support STORY-1000+ and standardize observation capture
- **Token Efficiency:** Reduce context window consumption through adaptive validation

**Success Metrics:**
- Anti-pattern scanner false positive rate: <5% (down from ~20%)
- Plan mode interruptions during workflow: 0 (down from 2-3 per session)
- Observation capture rate: 100% (up from 10%)
- QA validation token usage for documentation stories: -40%

## Problem Statement

During Q4 2025 development cycles, AI architectural analysis captured 35 framework improvement recommendations across 12 stories. 22 of these remain unimplemented, creating:
1. False positive violations blocking valid workflows
2. Plan mode interruptions during subagent execution
3. Missing observation data for AI analysis phase
4. Token waste from uniform validation on documentation stories

## User Personas

1. **Framework User:** Uses DevForgeAI for software development, expects smooth workflow execution
2. **Framework Maintainer:** Maintains DevForgeAI framework, needs accurate violation detection

## Features

### Feature 1: Subagent Execution Isolation (HIGH)
**Description:** Prevent subagents from triggering plan mode during workflow execution
**User Stories:**
1. Add plan file creation constraints to backend-architect.md
2. Add execution-mode frontmatter to execution commands (/qa, /dev, /release)
3. Implement auto-exit plan mode for immediate commands

**Estimated Effort:** Medium (3-5 story points)

### Feature 2: Anti-Pattern Scanner Accuracy (HIGH)
**Description:** Eliminate false positives for Markdown specification files
**User Stories:**
1. Add Slash Command exclusions (.claude/commands/*.md)
2. Add pre-report verification against source-tree.md
3. Add special handling for Markdown specification files

**Estimated Effort:** Low (2-3 story points)

### Feature 3: QA Workflow Intelligence (MEDIUM)
**Description:** Adaptive validation based on story type
**User Stories:**
1. Implement story type detection in /qa skill Phase 0
2. Add adaptive parallel validation (skip irrelevant validators)
3. Add regression vs pre-existing classification
4. Reduce validator token overhead with response constraints

**Estimated Effort:** Medium (5-8 story points)

### Feature 4: Phase State Enhancements (MEDIUM)
**Description:** Improve phase state tracking and observation capture
**User Stories:**
1. Extend STORY_ID_PATTERN to support STORY-1000+
2. Add observation capture command (phase-observe)
3. Add phase timing metrics
4. Add workflow state recovery command

**Estimated Effort:** Medium (5-8 story points)

### Feature 5: Developer Experience (LOW)
**Description:** Documentation and automation improvements
**User Stories:**
1. Auto-regenerate subagent registry in pre-commit hook
2. Add .gitattributes for CRLF line ending normalization
3. Document Markdown specification testing pattern
4. Document cross-reference format standard
5. Consolidate marker operations reference file

**Estimated Effort:** Low (3-5 story points)

### Feature 6: DoD Validation Improvements (MEDIUM)
**Description:** Enhance DoD validation accuracy
**User Stories:**
1. Add prefix normalization to DoD text matching
2. Add story status atomic update protocol
3. Implement Phase 09 hooks CLI --type flag

**Estimated Effort:** Low (2-3 story points)

## Dependencies

- EPIC-031: Phase Execution Enforcement (completed STORY-148, STORY-149)
- EPIC-032: RCA-to-Story Automation (in progress)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Changes break existing workflows | Medium | High | Comprehensive test coverage before deployment |
| Token optimization reduces validation quality | Low | Medium | A/B testing with deep mode fallback |
| STORY-1000+ migration breaks state files | Low | High | Backward compatible regex, migration script |

## Acceptance Criteria (Epic Level)

- [ ] All 22 stories created and associated with EPIC-033
- [ ] Anti-pattern scanner false positive rate measured <5%
- [ ] Plan mode interruptions during workflow: 0
- [ ] Documentation stories use adaptive validation
- [ ] STORY-1000+ pattern supported in phase_state.py

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Initial epic created from recommendations-triage analysis |
