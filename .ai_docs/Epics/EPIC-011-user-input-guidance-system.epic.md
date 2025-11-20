---
epic_id: EPIC-011
title: User Input Guidance System
status: Planning
created: 2025-01-20
priority: High
complexity: 18
estimated_sprints: 1
stakeholders:
  - DevForgeAI Users
  - Framework Maintainers
tags:
  - documentation
  - user-experience
  - framework-cohesion
  - quality-improvement
---

# EPIC-011: User Input Guidance System

## Executive Summary

Create a cohesive user input guidance system for the DevForgeAI framework to improve requirement quality, reduce iteration cycles, and ensure framework-wide consistency in how users communicate their needs.

## Business Problem

**Current State:**
- 40% of user stories are incomplete due to ambiguous feature descriptions
- Average 2.5 subagent re-invocations per story creation
- Token waste: ~10K per story from iteration cycles
- Users frustrated by "too many questions" without understanding it's intentional
- No unified guidance on how to provide effective input to DevForgeAI commands

**Impact:**
- Slower story creation (15-20 minutes vs potential 10-12 minutes)
- Lower quality specifications leading to implementation issues
- Token inefficiency (115K vs potential 105K per story)
- Poor user onboarding experience

## Business Goals

1. **Reduce incomplete stories by 67%** (40% → 13%)
2. **Improve token efficiency by 9%** (10K savings per story)
3. **Reduce iteration cycles by 52%** (2.5 → 1.2 subagent re-invocations)
4. **Improve user experience** (faster story creation, clearer expectations)
5. **Ensure framework cohesion** (all skills reference same guidance)

## Success Criteria

1. ✅ effective-prompting-guide.md created in src/ and linked from src/CLAUDE.md
2. ✅ user-input-guidance.md created in src/ and integrated in 5 skills
3. ✅ claude-code-terminal-expert enhanced with prompting guidance section
4. ✅ 10 test stories show 85%+ single-pass success rate (up from 40%)
5. ✅ Token usage reduced by 9% (measured on 10 test stories)
6. ✅ User feedback indicates clearer understanding of "Ask, Don't Assume" principle
7. ✅ All source files in src/ tree, operational files synced to .claude/

## Features

### Feature 1: User-Facing Prompting Guide
**Description:** Comprehensive guide teaching users how to provide clear, complete input to DevForgeAI commands

**Deliverables:**
- `src/claude/memory/effective-prompting-guide.md` (~3,500 lines)
- Command-specific guidance (/ideate, /create-story, /create-context, etc.)
- 20-30 before/after examples
- Quick reference checklists
- Common pitfalls documentation

**Value:** Users learn effective communication patterns upfront, reducing frustration and iteration cycles

**Dependencies:** None (standalone document)

**Estimated Points:** 8

---

### Feature 2: Framework-Internal Guidance Reference
**Description:** Internal reference for Claude executing skills, providing patterns for eliciting complete requirements

**Deliverables:**
- `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` (~2,500 lines)
- Functional requirement expansion patterns
- NFR quantification techniques
- Edge case discovery methods
- 20-30 AskUserQuestion templates

**Value:** Skills formulate better questions, anticipate gaps, reduce subagent re-invocations

**Dependencies:** None (standalone document)

**Estimated Points:** 8

---

### Feature 3: claude-code-terminal-expert Enhancement
**Description:** Add prompting guidance section to claude-code-terminal-expert for framework cohesion

**Deliverables:**
- Update `src/claude/skills/claude-code-terminal-expert/SKILL.md`
- New section on "How DevForgeAI Skills Work with User Input"
- Cross-references to both guidance documents
- Quick examples of DevForgeAI communication patterns
- Explanation of "Ask, Don't Assume" principle

**Value:** Ensures all framework components reference same authoritative guidance source

**Dependencies:** Features 1 & 2 (references them)

**Estimated Points:** 3

---

### Feature 4: devforgeai-ideation Integration
**Description:** Integrate user-input-guidance.md into ideation skill Phase 1

**Deliverables:**
- Update `src/claude/skills/devforgeai-ideation/SKILL.md`
- Phase 1 Step 0: Load guidance before discovery
- Use patterns throughout Phase 1-2 for better questions

**Value:** Entry point skill benefits immediately from guidance

**Dependencies:** Feature 2

**Estimated Points:** 3

---

### Feature 5: devforgeai-story-creation Integration
**Description:** Integrate user-input-guidance.md into story creation skill Phase 1

**Deliverables:**
- Update `src/claude/skills/devforgeai-story-creation/SKILL.md`
- Phase 1 Step 0: Load guidance before feature capture
- Use patterns before invoking requirements-analyst subagent

**Value:** Highest-impact integration (story creation has most iteration cycles)

**Dependencies:** Feature 2

**Estimated Points:** 3

---

### Feature 6: Additional Skill Integrations
**Description:** Integrate guidance into devforgeai-architecture, devforgeai-ui-generator, devforgeai-orchestration

**Deliverables:**
- Update `src/claude/skills/devforgeai-architecture/SKILL.md`: Phase 1 (Context Discovery)
- Update `src/claude/skills/devforgeai-ui-generator/SKILL.md`: Phase 2 (Story Analysis)
- Update `src/claude/skills/devforgeai-orchestration/SKILL.md`: Phase 4A (Epic), Phase 3 (Sprint)

**Value:** Framework-wide consistency, all user-input skills follow same patterns

**Dependencies:** Feature 2

**Estimated Points:** 5

---

### Feature 7: Documentation Updates
**Description:** Update framework documentation to reference new guidance system

**Deliverables:**
- Update `src/CLAUDE.md`: Add "Learning DevForgeAI" section
- Update `src/claude/memory/commands-reference.md`: Add cross-refs for each command
- Update `src/claude/memory/skills-reference.md`: Add cross-refs for each skill

**Value:** Discoverability - users and framework both know guidance exists

**Dependencies:** Features 1, 2, 3

**Estimated Points:** 3

---

### Feature 8: Validation & Testing Suite
**Description:** Test on real stories, measure impact, document success metrics

**Deliverables:**
- `tests/user-input-guidance/test-story-creation-with-guidance.sh`
- `tests/user-input-guidance/test-story-creation-without-guidance.sh`
- `tests/user-input-guidance/validate-token-savings.py`
- `tests/user-input-guidance/measure-success-rate.py`
- 10 test fixtures in `tests/user-input-guidance/fixtures/`
- Impact report: `.devforgeai/specs/enhancements/USER-INPUT-GUIDANCE-IMPACT-REPORT.md`

**Value:** Validates hypothesis, provides evidence for future improvements

**Dependencies:** Features 1-7 (tests complete system)

**Estimated Points:** 5

---

### Feature 9: Operational Sync
**Description:** Sync source files to operational folders for runtime use

**Deliverables:**
- Copy `src/claude/memory/effective-prompting-guide.md` → `.claude/memory/`
- Copy `src/claude/skills/*/` updates → `.claude/skills/*/`
- Copy `src/CLAUDE.md` → `CLAUDE.md`
- Validation script: `tests/user-input-guidance/validate-sync.sh`

**Value:** Ensures operational folders match source distribution

**Dependencies:** Features 1-7

**Estimated Points:** 2

---

## Epic Roadmap

### Sprint 1: Complete Implementation (Total: 40 points)
- Week 1: Features 1-3 (Documents creation, 19 points)
- Week 2: Features 4-9 (Integration, testing, sync, 21 points)

**Total Estimated Effort:** 1 sprint (40 story points)

## Source Tree Structure

### Source Files (src/)
```
src/
├── CLAUDE.md (updated)
├── claude/
│   ├── memory/
│   │   ├── effective-prompting-guide.md (NEW)
│   │   ├── commands-reference.md (updated)
│   │   └── skills-reference.md (updated)
│   └── skills/
│       ├── claude-code-terminal-expert/
│       │   └── SKILL.md (updated)
│       ├── devforgeai-ideation/
│       │   ├── SKILL.md (updated)
│       │   └── references/
│       │       └── user-input-guidance.md (NEW)
│       ├── devforgeai-story-creation/
│       │   └── SKILL.md (updated)
│       ├── devforgeai-architecture/
│       │   └── SKILL.md (updated)
│       ├── devforgeai-ui-generator/
│       │   └── SKILL.md (updated)
│       └── devforgeai-orchestration/
│           └── SKILL.md (updated)
└── devforgeai/
    └── specs/enhancements/
        └── USER-INPUT-GUIDANCE-IMPACT-REPORT.md (NEW)
```

### Test Files (tests/)
```
tests/
└── user-input-guidance/
    ├── test-story-creation-with-guidance.sh
    ├── test-story-creation-without-guidance.sh
    ├── test-ideation-with-guidance.sh
    ├── validate-token-savings.py
    ├── measure-success-rate.py
    ├── validate-sync.sh
    ├── fixtures/
    │   ├── feature-001-login.txt
    │   ├── feature-002-dashboard.txt
    │   └── [8 more test fixtures]
    ├── baseline/ (results without guidance)
    └── enhanced/ (results with guidance)
```

### Operational Files (.claude/ - synced from src/)
```
.claude/
├── memory/
│   └── effective-prompting-guide.md (synced)
└── skills/
    └── [updated skills] (synced)

CLAUDE.md (synced)
```

## Technical Considerations

### Architecture Pattern
**Tier 1: Monolithic/Simple** - Documentation enhancement with skill integration

**Source vs Operational:**
- Primary development in `src/` tree
- Sync to `.claude/` and `.devforgeai/` for runtime
- Tests validate both source and operational versions

### Integration Strategy
**Progressive Disclosure Pattern:**
- Guidance loaded on-demand by skills (token efficient)
- Only loaded when skill needs requirement elicitation
- ~2-3K token cost per load (net savings 7-8K from avoiding iterations)

### Cross-Reference Architecture
```
src/claude/memory/effective-prompting-guide.md ←→ src/claude/skills/.../user-input-guidance.md
         ↓                                                  ↓
   src/CLAUDE.md, docs                     5 skills (ideation, story, arch, ui, orch)
         ↓                                                  ↓
   src/claude/skills/claude-code-terminal-expert ──────────┘
   (authoritative knowledge base)
```

## Risks & Mitigations

### Risk 1: Source/operational sync issues
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:** Automated sync validation script, CI/CD checks

### Risk 2: Guidance not used by skills
**Likelihood:** Low
**Impact:** High
**Mitigation:** Mandatory Step 0 in Phase 1 of affected skills (automatic load)

### Risk 3: Guidance becomes outdated
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:** Version guidance documents, review quarterly, update examples

### Risk 4: Token overhead negates savings
**Likelihood:** Low
**Impact:** Medium
**Mitigation:** Progressive disclosure (load once per session), measure actual impact

## Non-Functional Requirements

### Performance
- Guidance load time: <500ms (Read tool)
- Net token savings: 9% per story (10K tokens)
- No impact on command execution time

### Maintainability
- Single source of truth in src/ (no duplication)
- Cross-references for cohesion
- Markdown format (easy to update)
- Automated sync to operational folders

### Usability
- Clear examples (20-30 before/after)
- Scannable format (checklists, quick reference)
- Progressive disclosure (users read as needed)

### Quality
- 85%+ single-pass success rate (validation target)
- <15% incomplete stories (quality target)
- Framework cohesion (all skills aligned)

## Dependencies

**Prerequisites:**
- DevForgeAI framework operational (existing)
- 5 skills to integrate with (existing in src/)
- claude-code-terminal-expert skill (existing in src/)
- Source tree structure established (existing)

**External Dependencies:**
- None (internal framework enhancement)

## Related Epics

- EPIC-001: DevForgeAI Core Framework (parent)
- EPIC-006: Story Creation Skill (Feature 5 integrates)
- EPIC-002: Ideation Skill (Feature 4 integrates)
- EPIC-010: src/ Migration (ensures proper source tree)

## Notes

This epic emerged from analysis rejecting "devforgeai-prompt-engineering" skill concept. The hybrid guidance approach (user-facing + framework-internal) proved superior to single-purpose skill that would violate framework principles.

**Key Insight:** DevForgeAI succeeds through expansion (clarifying questions), not compression (keyword translation). This epic reinforces that philosophy through cohesive guidance.

**Source Tree Alignment:** All deliverables target `src/` tree with sync to operational folders, following DevForgeAI installer pattern.

## Stories

1. **STORY-052:** User-Facing Prompting Guide Documentation (8 pts) - Backlog
2. **STORY-053:** Framework-Internal Guidance Reference (8 pts) - Backlog
3. **STORY-054:** claude-code-terminal-expert Prompting Guidance Enhancement (3 pts) - Backlog
4. **STORY-055:** devforgeai-ideation Skill Integration with User Input Guidance (3 pts) - Backlog
5. **STORY-056:** devforgeai-story-creation Skill Integration with User Input Guidance (3 pts) - Backlog
6. **STORY-057:** Additional Skill Integrations (architecture, ui-generator, orchestration) (5 pts) - Backlog
7. **STORY-058:** Documentation Updates with User Input Guidance Cross-References (3 pts) - Backlog
8. **STORY-059:** User Input Guidance Validation & Testing Suite (5 pts) - Backlog
9. **STORY-060:** Operational Sync for User Input Guidance System (2 pts) - Backlog

**Total:** 9 stories, 40 story points

---

## Acceptance Criteria

- [ ] All 9 features implemented and tested
- [ ] 10 validation stories show 85%+ single-pass success
- [ ] Token savings measured at 9%+ improvement
- [ ] All cross-references verified working
- [ ] Impact report documents success metrics
- [ ] User feedback collected and positive
- [ ] Framework cohesion validated (all skills use same terminology)
- [ ] Source files in src/ tree, operational files synced
- [ ] All tests passing in tests/user-input-guidance/

---

**Epic Status:** Planning → Ready for Sprint Planning
**Next Action:** Run `/create-sprint` to plan Sprint implementation
**Stories Created:** 2025-01-20 (9 stories: STORY-052 through STORY-060)
