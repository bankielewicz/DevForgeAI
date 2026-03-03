---
id: EPIC-007
title: Lean Orchestration Compliance
status: Planning
priority: Medium
business_value: High
created: 2025-11-14
updated: 2025-11-14
timeline: 2-3 sprints (4-6 weeks)
estimated_points: 40
---

# EPIC-007: Lean Orchestration Compliance

## Goal

Restore lean orchestration pattern compliance across all DevForgeAI slash commands by refactoring commands to delegate business logic to skills, ensuring all commands remain within 15K character budget and follow the "commands orchestrate, skills validate" pattern.

## Business Value

**High** - Prevents technical debt accumulation by enforcing architectural pattern compliance. Improves maintainability, reduces token usage by 50%+, and establishes sustainable framework evolution practices.

## Background

**Root Cause:** RCA-009 identified that the /qa command violates lean orchestration pattern by containing business logic (Phases 4 & 5: feedback hooks and story updates) instead of delegating to the devforgeai-qa skill.

**Pattern Violation:**
- Commands should: Parse arguments, load context, set markers, invoke skill, display results (5 responsibilities ONLY)
- Commands should NOT: Contain business logic, complex parsing, template generation, decision-making, error recovery

**Current State:**
- /qa command: 509 lines with Phases 4 & 5 containing 167 lines of business logic
- 2 other commands over 15K budget: /create-ui (19K, 126%), /release (18K, 121%)
- Pattern established in protocol but not fully enforced

**Desired State:**
- All 11 commands <15K character budget
- 100% lean pattern compliance (5 responsibilities, zero violations)
- Skills contain ALL business logic
- Token efficiency improved 50%+ across all commands

## Success Criteria

1. ✅ All commands under 15K character budget (100% compliance)
2. ✅ All commands pass lean orchestration 5-responsibility checklist
3. ✅ Zero business logic in any command (only orchestration code)
4. ✅ Token efficiency improved 50%+ (measured before/after)
5. ✅ Zero functional regressions (all existing tests pass)
6. ✅ Framework documentation updated with pattern

## Features

### Feature 1: Refactor /qa Command (STORY-034)
**Status:** Backlog
**Story Points:** 8
**Description:** Move Phases 4 & 5 from /qa command to devforgeai-qa skill as Phases 6 & 7. Reduce command from 509 to ~340 lines. Create 2 reference files for progressive disclosure.

**Acceptance Criteria:**
- Phase 6 added to skill (feedback hooks)
- Phase 7 added to skill (story updates)
- Command reduced to 3 phases (validate → invoke → display)
- 33% line reduction measured
- Zero functional regressions (75/75 tests pass)

**Dependencies:** RCA-009 analysis complete ✅

**Story:** STORY-034-refactor-qa-command-move-phases-to-skill.story.md

---

### Feature 2: Audit All Commands for Pattern Compliance
**Status:** Backlog
**Story Points:** 3
**Description:** Run `/audit-budget` to identify all over-budget commands. Review all 11 commands against lean-orchestration-pattern.md. Document violations and create refactoring stories for backlog.

**Acceptance Criteria:**
- /audit-budget executed and results documented
- All 11 commands reviewed against 5-responsibility checklist
- Violations documented with severity (critical/high/medium/low)
- Refactoring stories created for each violation

**Story:** STORY-037-audit-commands-pattern-compliance.story.md
- Priority queue established

**Deliverables:**
- devforgeai/qa/command-compliance-audit-YYYY-MM-DD.md
- Backlog stories for violations

---

### Feature 3: Refactor /create-ui Command
**Status:** Not Started
**Story Points:** 13
**Description:** Refactor /create-ui command (currently 19K chars, 126% over budget) to delegate UI generation logic to devforgeai-ui-generator skill. Apply lean pattern.

**Acceptance Criteria:**
- Command reduced to <12K characters (within budget)
- UI generation logic moved to skill
- Command has only 3-5 phases (orchestration only)
- Zero functional regressions
- Token efficiency improved 50%+

**Dependencies:** Feature 2 (audit) provides detailed violation analysis

---

### Feature 4: Refactor /release Command
**Status:** Backlog
**Story Points:** 13
**Description:** Refactor /release command (currently 18K chars, 121% over budget) to delegate deployment logic to devforgeai-release skill. Apply lean pattern.

**Acceptance Criteria:**
- Command reduced to <12K characters (within budget)
- Deployment logic moved to skill
- Command has only 3-5 phases (orchestration only)
- Zero functional regressions (deployment tests pass)
- Token efficiency improved 50%+

**Dependencies:** Feature 2 (audit) provides detailed violation analysis

**Story:** STORY-038-refactor-release-command-lean-orchestration.story.md

---

### Feature 5: Update Framework Documentation
**Status:** Backlog
**Story Points:** 3
**Description:** Update all framework documentation to reflect lean orchestration pattern as standard. Add pattern to command templates, update reference docs, create troubleshooting guide.

**Acceptance Criteria:**
- lean-orchestration-pattern.md includes all 5 refactoring examples
- command-budget-reference.md updated with current metrics
- .claude/memory/commands-reference.md documents pattern for each command
- Command creation template includes lean pattern checklist
- Troubleshooting guide created for pattern violations

**Deliverables:**
- Updated protocol documentation
- Command creation template with lean pattern built-in
- Pattern violation troubleshooting guide

**Story:** STORY-039-update-framework-documentation-lean-orchestration.story.md

---

### Feature 6: Refactor /create-context Command Budget Compliance
**Status:** Backlog
**Story Points:** 3
**Description:** Refactor /create-context command (currently 16.2K chars, 108% over budget) by extracting pattern documentation to references and condensing Phase N inline documentation. Target: ≤14K characters (93% of budget).

**Acceptance Criteria:**
- Character count reduced to ≤14,000 (from 16,210)
- Phase N pattern docs externalized to `devforgeai/protocols/hook-integration-pattern.md`
- All workflow steps preserved (functionality unchanged)
- Budget audit passes (✅ COMPLIANT status)
- Zero functional regressions

**Dependencies:**
- STORY-030 complete (pattern file already created) ✅

**Story:** STORY-049-refactor-create-context-budget-compliance.story.md

---

## Timeline

**Duration:** 2-3 sprints (4-6 weeks)

**Sprint 1:**
- Feature 1: Refactor /qa command (STORY-034) - 8 points
- Feature 2: Audit all commands - 3 points
- Total: 11 points

**Sprint 2:**
- Feature 3: Refactor /create-ui - 13 points
- Total: 13 points

**Sprint 3:**
- Feature 4: Refactor /release - 13 points
- Feature 5: Update framework docs - 3 points
- Total: 16 points

**Total:** 40 story points across 3 sprints

## Stakeholders

- **Framework Maintainers** - Responsible for architecture compliance, refactoring implementation
- **AI Development Team** - Provides guidance on Claude Code Terminal patterns, validates approach

## Technical Assessment

### Complexity Score: 5.6/10 (Medium-High)

**Feature Complexity Breakdown:**
- Feature 1 (/qa refactor): 5/10 - Well-defined, proven pattern
- Feature 2 (audit): 2/10 - Simple discovery work
- Feature 3 (/create-ui): 7/10 - Large command, complex UI logic
- Feature 4 (/release): 7/10 - Large command, deployment complexity
- Feature 5 (documentation): 3/10 - Straightforward updates

### Key Risks

1. **Functional Regressions** (Medium Risk)
   - **Impact:** Broken commands affect all users
   - **Mitigation:**
     - Backup all commands before refactoring
     - Run existing test suites (75 tests for /qa)
     - Measure before/after behavior
   - **Owner:** Framework Maintainers

2. **Pattern Misapplication** (Low Risk)
   - **Impact:** Refactoring doesn't achieve compliance
   - **Mitigation:**
     - Follow proven examples (/qa, /dev, /create-sprint)
     - Reference lean-orchestration-pattern.md
     - Manual checklist validation per command
   - **Owner:** Framework Maintainers

3. **Token Budget Regression** (Low Risk)
   - **Impact:** Refactoring increases token usage instead of decreasing
   - **Mitigation:**
     - Measure baseline token usage before refactoring
     - Target 50%+ efficiency improvement
     - Performance tests before/after
   - **Owner:** AI Development Team

### Prerequisites

- ✅ RCA-009 analysis complete
- ✅ lean-orchestration-pattern.md protocol exists
- ✅ Refactoring examples exist (/dev, /qa, /create-sprint, /create-epic, /orchestrate)

### Dependencies

- None (independent epic, no external blockers)

## Metrics

**Baseline (before epic):**
- Commands over budget: 3 (/qa 509 lines, /create-ui 19K chars, /release 18K chars)
- Pattern compliance: ~55% (6/11 commands compliant)
- Avg token usage: ~8K per command

**Target (after epic):**
- Commands over budget: 0 (100% compliance)
- Pattern compliance: 100% (11/11 commands compliant)
- Avg token usage: ~4K per command (50% reduction)
- Character budget: All commands 6K-12K range

## Status History

- **2025-11-14:** Epic created (EPIC-007) - Status: Planning - Context gathered from RCA-009 analysis
- **2025-11-14:** Feature decomposition complete - 5 features identified (40 story points total)
- **2025-11-14:** Technical assessment complete - Complexity 5.6/10, 3 risks identified with mitigations
- **2025-11-14:** Epic approved for Sprint-3 planning

## Notes

**Why This Epic Matters:**

From RCA-009:
> "Commands orchestrate. Skills validate. Subagents specialize."
>
> **Root Cause:** Phases 4 & 5 are in the command instead of the skill, violating lean orchestration.

**Pattern Benefits:**
- ✅ Maintainability: Commands become simpler (3-5 phases vs 6+ phases)
- ✅ Token Efficiency: 50%+ reduction in main conversation tokens
- ✅ Scalability: Skills designed for complex workflows, commands are not
- ✅ Testability: Skills tested independently, commands tested for orchestration only
- ✅ Reusability: Skills invoked by multiple commands, logic stays DRY

**Evidence-Based Approach:**
- Pattern proven in 5 command refactorings (average 37% line reduction, 62% token savings)
- Skills already have execution model, commands do not
- Progressive disclosure keeps entry points lean
- Subagent isolation prevents main conversation bloat

**Related Work:**
- RCA-009: Root cause analysis (Phase 5 not executed autonomously)
- STORY-024: Wire hooks into /qa (added Phase 4 originally, triggered violation)
- lean-orchestration-pattern.md: Protocol defining pattern (v1.2, 2025-11-06)
- command-budget-reference.md: Budget tracking and compliance monitoring
