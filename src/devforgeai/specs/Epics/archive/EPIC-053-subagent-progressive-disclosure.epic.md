---
id: EPIC-053
title: Subagent Progressive Disclosure Refactoring
status: Planning
start_date: 2026-01-29
target_date: 2026-02-28
total_points: 13
completed_points: 0
created: 2026-01-29
owner: DevForgeAI Team
tech_lead: Claude
team: DevForgeAI
priority: P1 - High
source_research: RESEARCH-006
source_adr: ADR-012
context_files:
  - devforgeai/specs/context/tech-stack.md
  - devforgeai/specs/context/source-tree.md
  - devforgeai/specs/context/architecture-constraints.md
  - devforgeai/specs/context/anti-patterns.md
  - devforgeai/specs/context/dependencies.md
  - devforgeai/specs/context/coding-standards.md
---

# Epic: Subagent Progressive Disclosure Refactoring

## Business Goal

Bring the 4 most oversized subagents (>1000 lines) into constitutional compliance with the 500-line maximum defined in tech-stack.md by implementing progressive disclosure patterns.

**Problem Statement (RESEARCH-006):**
- 26 of 32 subagents (81%) exceed the constitutional 500-line maximum
- Top 4 violators are 233-474% over the limit
- Current state causes excessive token consumption per subagent invocation
- Constitutional debt accumulating without enforcement

**Value Statement:** Achieve 60-80% token reduction per subagent invocation for CRITICAL subagents, establish the reference loading pattern for future refactoring of remaining 22 subagents.

## Success Metrics

- **Metric 1:** All 4 CRITICAL subagents reduced to ≤300 lines (core files)
- **Metric 2:** Token consumption per invocation reduced by 60%+ (measured)
- **Metric 3:** Zero regression in subagent behavior (all existing tests pass)
- **Metric 4:** Reference loading pattern documented and validated

**Measurement Plan:**
- Baseline: Current line counts (2370, 1860, 1761, 1165)
- Target: All core files ≤300 lines
- Test: Before/after token consumption comparison
- Review: After each story completion

## Scope

### In Scope

#### Feature 0: Constitutional Update (PREREQUISITE)
- **Points:** 1
- **ADR:** ADR-012
- **Problem:** source-tree.md line 582 prohibits subagent subdirectories
- **Solution:** Update source-tree.md to allow `references/` subdirectories for subagents >500 lines
- **Business Value:** Enables progressive disclosure pattern for subagents

#### Feature 1: Refactor agent-generator.md (CRITICAL)
- **Points:** 3
- **Lines:** 2,370 → ≤300 (core) + references/
- **Problem:** 474% over maximum, largest subagent
- **Solution:** Extract to core + 8-10 reference files
- **Business Value:** Highest token savings impact

#### Feature 2: Refactor session-miner.md (CRITICAL)
- **Points:** 3
- **Lines:** 1,860 → ≤300 (core) + references/
- **Problem:** 372% over maximum
- **Solution:** Extract workflow-specific documentation to references
- **Business Value:** Second highest impact

#### Feature 3: Refactor test-automator.md (CRITICAL)
- **Points:** 3
- **Lines:** 1,761 → ≤300 (core) + references/
- **Problem:** 352% over maximum, frequently invoked
- **Solution:** Extract framework patterns, remediation mode, exception coverage to references
- **Business Value:** High invocation frequency = high cumulative savings

#### Feature 4: Refactor ac-compliance-verifier.md (CRITICAL)
- **Points:** 2
- **Lines:** 1,165 → ≤300 (core) + references/
- **Problem:** 233% over maximum
- **Solution:** Extract verification workflows to references
- **Business Value:** Completes CRITICAL tier refactoring

#### Feature 5: Enforcement Mechanism
- **Points:** 1
- **Problem:** No automated enforcement of subagent size limits
- **Solution:** Add pre-commit warning for >500 lines, CI failure for >600 lines
- **Business Value:** Prevents future constitutional violations

### Out of Scope

- Refactoring remaining 22 HIGH-priority subagents (500-1000 lines) - future EPIC-xxx
- Changing subagent behavior or functionality
- Updating the 500-line constitutional limit
- Converting subagents to skills

## Technical Specification

### Reference Loading Pattern (per ADR-012)

**Directory Structure:**
```
src/claude/agents/
├── {subagent}.md                    # Core (≤300 lines)
└── {subagent}/
    └── references/
        ├── {topic-1}.md
        ├── {topic-2}.md
        └── ...
```

**Core File Structure:**
```markdown
---
name: {subagent}
description: {description}
tools: {tools}
model: {model}
---

# {Subagent Name}

## Purpose
{10-20 lines}

## When Invoked
{20-30 lines}

## Workflow
{50-100 lines - condensed, with reference pointers}

## Success Criteria
{15-20 lines}

## Error Handling
{20-30 lines}

## Reference Loading
{10-20 lines - pointers to references/}

## Observation Capture (MANDATORY)
{50 lines}

## References
{5-10 lines}
```

**Reference Loading Syntax:**
```markdown
## Remediation Mode

For QA-Dev integration remediation workflow:
Read(file_path=".claude/agents/test-automator/references/remediation-mode.md")

Execute the remediation workflow as documented.
```

### Files to Create/Modify

| File | Action | Story |
|------|--------|-------|
| devforgeai/specs/context/source-tree.md | MODIFY | STORY-330 |
| src/claude/agents/agent-generator.md | REFACTOR | STORY-331 |
| src/claude/agents/agent-generator/references/*.md | CREATE | STORY-331 |
| src/claude/agents/session-miner.md | REFACTOR | STORY-332 |
| src/claude/agents/session-miner/references/*.md | CREATE | STORY-332 |
| src/claude/agents/test-automator.md | REFACTOR | STORY-333 |
| src/claude/agents/test-automator/references/*.md | CREATE | STORY-333 |
| src/claude/agents/ac-compliance-verifier.md | REFACTOR | STORY-334 |
| src/claude/agents/ac-compliance-verifier/references/*.md | CREATE | STORY-334 |
| .claude/hooks/pre-commit-subagent-size.sh | CREATE | STORY-335 |

## Target Sprints

### Sprint 1: Foundation + First Refactoring
**Goal:** Enable progressive disclosure pattern, refactor largest subagent
**Estimated Points:** 7
**Features:**
- Feature 0: Constitutional Update (1 pt)
- Feature 1: Refactor agent-generator.md (3 pts)
- Feature 3: Refactor test-automator.md (3 pts)

**Key Deliverables:**
- source-tree.md updated per ADR-012
- agent-generator.md compliant (2370 → ≤300 lines)
- test-automator.md compliant (1761 → ≤300 lines)
- Reference loading pattern validated

### Sprint 2: Complete CRITICAL Tier + Enforcement
**Goal:** Finish remaining CRITICAL subagents, add enforcement
**Estimated Points:** 6
**Features:**
- Feature 2: Refactor session-miner.md (3 pts)
- Feature 4: Refactor ac-compliance-verifier.md (2 pts)
- Feature 5: Enforcement Mechanism (1 pt)

**Key Deliverables:**
- All 4 CRITICAL subagents compliant
- Pre-commit hook warns on >500 lines
- CI blocks on >600 lines
- Pattern documented for EPIC-xxx

## User Stories

### Sprint 1 Stories (7 points)
| ID | Title | Type | Points | Depends On | Status |
|----|-------|------|--------|------------|--------|
| STORY-330 | Update source-tree.md for Subagent References | refactor | 1 | ADR-012 | Backlog |
| STORY-331 | Refactor agent-generator.md with Progressive Disclosure | refactor | 3 | STORY-330 | Backlog |
| STORY-333 | Refactor test-automator.md with Progressive Disclosure | refactor | 3 | STORY-330 | Backlog |

### Sprint 2 Stories (6 points)
| ID | Title | Type | Points | Depends On | Status |
|----|-------|------|--------|------------|--------|
| STORY-332 | Refactor session-miner.md with Progressive Disclosure | refactor | 3 | STORY-330 | Backlog |
| STORY-334 | Refactor ac-compliance-verifier.md with Progressive Disclosure | refactor | 2 | STORY-330 | Backlog |
| STORY-335 | Add Subagent Size Enforcement Mechanism | feature | 1 | STORY-331 | Backlog |

## Dependencies

### Internal Dependencies
- **ADR-012:** Must be approved before STORY-330 can proceed
- **STORY-330:** All refactoring stories depend on constitutional update

### External Dependencies
- None

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Reference loading breaks subagent behavior | Medium | High | Thorough testing, behavior comparison before/after |
| Token savings less than expected | Low | Medium | Measure baseline, adjust if needed |
| Pattern doesn't scale to remaining 22 | Low | Medium | Validate pattern with 4 before EPIC-xxx |

## Acceptance Criteria

### Epic-Level AC
1. All 4 CRITICAL subagents have core files ≤300 lines
2. All extracted references are in `{subagent}/references/` directories
3. All subagent tests pass (no behavior regression)
4. Token consumption reduced by ≥60% (measured)
5. Pre-commit hook warns on >500 line subagents
6. CI fails on >600 line subagents
7. Pattern documented for EPIC-xxx continuation

## Related Work

| ID | Type | Relationship |
|----|------|--------------|
| RESEARCH-006 | Research | Source analysis and findings |
| ADR-012 | ADR | Architectural decision enabling this work |
| EPIC-xxx | Epic | Follow-up for remaining 22 HIGH subagents (to be created) |

## Change Log

| Date | Change |
|------|--------|
| 2026-01-29 | Epic created from RESEARCH-006 and ADR-012 |
| 2026-01-29 | STORY-330 created (Update source-tree.md for Subagent References) |
| 2026-01-29 | STORY-331 created (Refactor agent-generator.md with Progressive Disclosure) |
| 2026-01-29 | STORY-332 created (Refactor session-miner.md with Progressive Disclosure) |
| 2026-01-29 | STORY-333 created (Refactor test-automator.md with Progressive Disclosure) |
| 2026-01-30 | STORY-334 created (Refactor ac-compliance-verifier.md with Progressive Disclosure) |
| 2026-01-30 | STORY-335 created (Add Subagent Size Enforcement Mechanism) |
