---
id: EPIC-028
title: /ideate Command Refactoring & Lean Orchestration
business-value: Reduce token consumption by 64% (554→200 lines) and eliminate duplicate user prompts
status: Planning
priority: High
complexity-score: 37
architecture-tier: Tier 3
created: 2025-12-22
estimated-points: 20-25
target-sprints: 2-3
source-brainstorm: BRAINSTORM-001
---

# EPIC-028: /ideate Command Refactoring & Lean Orchestration

## Business Goal

Refactor the `/ideate` command from 554 lines to ~200 lines by following the proven `/dev` pattern (174 lines). Eliminate redundant user interactions by delegating summary, verification, and next-action logic to the skill, improving user experience and reducing token consumption.

**Success Metrics:**
- Command reduced from 554 lines to ≤200 lines (64% reduction)
- Zero duplicate questions (D1-D5 eliminated)
- Token consumption per ideation session reduced by 30-40%
- User reports "no repetitive questions" in feedback

## Features

### Feature 1: Delegate Artifact Verification to Skill
**Description:** Remove Phase 3 artifact verification from command (lines 239-289), as skill already validates in Phase 6.4

**User Stories (high-level):**
1. As a framework maintainer, I want artifact verification logic in ONE place (skill) so I don't maintain duplicate code
2. As a user, I want consistent validation behavior regardless of how ideation completes
3. As a developer, I want the command to trust skill's self-validation

**Implementation:**
- Remove command Phase 3 (artifact verification)
- Rely on skill Phase 6.4 (self-validation-workflow.md)
- If skill reports validation failure, command HALTs with error message

**Estimated Effort:** Small (5 points)

---

### Feature 2: Delegate Summary Presentation to Skill
**Description:** Remove Phase 4 summary presentation from command (lines 293-331), as skill already presents in Phase 6.5

**User Stories (high-level):**
1. As a user, I want to see the summary ONCE at the end of ideation, not twice
2. As a framework maintainer, I want summary templates in ONE place (completion-handoff.md)
3. As a developer, I want command to display skill's formatted output

**Implementation:**
- Remove command Phase 4 (quick summary)
- Create ideation-result-interpreter subagent (similar to dev-result-interpreter)
- Result interpreter reads skill output and formats display
- Command invokes result interpreter in new Phase 3

**Estimated Effort:** Medium (8 points)

---

### Feature 3: Delegate Next Action Determination to Skill
**Description:** Remove Phase 5 next action questions from command (lines 350-437), as skill already asks in Phase 6.6

**User Stories (high-level):**
1. As a user, I want to answer "What's next?" ONCE, not twice
2. As a framework maintainer, I want next-action logic in skill (context-aware decision)
3. As a developer, I want command to respect skill's handoff instructions

**Implementation:**
- Remove command Phase 5 (verify next steps communicated)
- Skill Phase 6.6 already asks user for next action
- Command displays brief confirmation only

**Estimated Effort:** Small (3 points)

---

### Feature 4: Create ideation-result-interpreter Subagent
**Description:** New subagent following dev-result-interpreter pattern (adapted for ideation outputs)

**User Stories (high-level):**
1. As a framework maintainer, I want consistent result interpretation across /dev and /ideate
2. As a user, I want clear, structured display of ideation results
3. As a developer extending framework, I want a reusable pattern for result interpretation

**Implementation:**
- Create `.claude/agents/ideation-result-interpreter.md`
- Follow dev-result-interpreter structure but adapt templates for:
  - Epic count, complexity score, architecture tier
  - Requirements summary (functional, NFRs, integrations)
  - Next action (greenfield→/create-context, brownfield→/orchestrate)
- Read-only tools: Read, Glob, Grep

**Estimated Effort:** Medium (6 points)

---

### Feature 5: Smart Greenfield/Brownfield Detection
**Description:** Check for context files existence to determine if project is greenfield or brownfield

**User Stories (high-level):**
1. As a user in brownfield mode, I want ideation to skip architecture handoff automatically
2. As a user in greenfield mode, I want clear next step to create context files
3. As a framework maintainer, I want smart detection to reduce user friction

**Implementation:**
- In command Phase 1 (after argument validation):
  - Check: `Glob(pattern="devforgeai/specs/context/*.md")`
  - If 6 context files exist: brownfield mode (skip architecture, suggest /orchestrate)
  - If <6 context files: greenfield mode (suggest /create-context)
- Pass mode to skill via context marker
- Skill adjusts Phase 6.6 next action accordingly

**Estimated Effort:** Small (3 points)

---

### Feature 6: Display-Only Architecture Handoff
**Description:** Remove auto-invocation of architecture skill (W3 violation), show display-only next steps

**User Stories (high-level):**
1. As a user, I want control over when architecture skill runs (avoid token overflow)
2. As a framework maintainer, I want commands to orchestrate, not auto-execute chains
3. As a developer, I want clear separation: command ends, user decides next action

**Implementation:**
- Remove auto-architecture invocation from command Phase 5
- Skill Phase 6.6 presents next action: "Run `/create-context [project-name]`"
- Command displays skill's recommendation, does not auto-invoke

**Estimated Effort:** Small (2 points)

---

## Requirements Summary

### Functional Requirements
- Command delegates verification, summary, next-action to skill
- Result interpreter formats skill output for display
- Smart detection identifies greenfield vs brownfield
- No auto-invocation of downstream skills

### Data Model
**Entities:**
- Command file (ideate.md): Orchestrator, ~200 lines
- Skill file (SKILL.md): Implementation, unchanged
- Result interpreter subagent: New, read-only
- Context files: Used for brownfield detection

**Relationships:**
- Command → Skill (invokes)
- Command → Result Interpreter (formats output)
- Skill → Context files (checks existence)

### Integration Points
1. **Skill invocation:** Skill(command="devforgeai-ideation")
2. **Result interpretation:** Task(subagent_type="ideation-result-interpreter")
3. **Context file detection:** Glob for 6 context files

### Non-Functional Requirements

**Token Efficiency:**
- 64% line reduction (554→200) = fewer tokens loaded per invocation
- Eliminate duplicate questions = 30-40% token savings

**Maintainability:**
- Single source of truth for verification, summary, next-action
- Consistent pattern with /dev command

**User Experience:**
- Zero duplicate questions
- Clear next steps
- No unexpected auto-invocations

## Architecture Considerations

**Complexity Tier:** Tier 3 (Complex System)

**Recommended Architecture:**
- **Pattern:** Lean Orchestration (command delegates to skill, skill implements)
- **Layers:** Command (orchestration), Skill (workflow), Result Interpreter (display), Reference Files (deep knowledge)
- **Data Flow:** Command → Skill (work) → Result Interpreter (format) → User (display)

**Technology Recommendations:**
- Markdown for command/skill files (existing)
- YAML frontmatter for epic metadata (existing)
- Bash for file checks (context detection only, not creation)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Breaking existing /ideate users | MEDIUM | User approved breaking changes; clear migration guide in PR |
| Result interpreter pattern doesn't fit ideation | LOW | Adapt dev-result-interpreter template with ideation-specific sections |
| Brownfield detection false positives | LOW | Check for exactly 6 context files with specific names |
| Users expect auto-architecture like before | LOW | Explain in Phase 6.6 why manual invocation prevents token overflow |

## Dependencies

**Prerequisites:**
- None (this is the foundational epic)

**Dependents:**
- EPIC-029 (Session Continuity) depends on refactored command structure
- EPIC-030 (Constitutional Compliance) can run in parallel

## Next Steps

1. **Implementation:** Start with Feature 2 (result interpreter) as it's independent
2. **Then:** Features 1, 3, 6 (remove duplicates) - sequential, dependent on each other
3. **Then:** Feature 5 (brownfield detection) - integrates with refactored structure
4. **Testing:** Validate all 6 features with greenfield and brownfield test scenarios
5. **Documentation:** Update /ideate command docs, add migration guide

---

**Created from:** BRAINSTORM-001 (HIGH confidence)

## Stories

| Story ID | Feature | Title | Status | Points |
|----------|---------|-------|--------|--------|
| STORY-130 | F1 | Delegate Artifact Verification to Skill | Backlog | 5 |
| STORY-131 | F2 | Delegate Summary Presentation to Skill | Backlog | 8 |
| STORY-132 | F3 | Delegate Next Action Determination to Skill | Backlog | 3 |
| STORY-133 | F4 | Create ideation-result-interpreter Subagent | Backlog | 6 |
| STORY-134 | F5 | Smart Greenfield/Brownfield Detection | Backlog | 3 |
| STORY-135 | F6 | Display-Only Architecture Handoff | Backlog | 2 |

**Total Points:** 27
