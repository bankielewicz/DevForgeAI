---
id: EPIC-061
title: "Unified Template Standardization & Enforcement"
status: Planning
start_date: TBD
target_date: TBD
total_points: 30
created: 2026-02-04
updated: 2026-02-04
source_brainstorm: BRAINSTORM-010
source_requirements: devforgeai/specs/requirements/prompt-engineering-improvement-requirements.md
depends_on:
  - EPIC-060
---

# Epic: Unified Template Standardization & Enforcement

## Business Goal

Create canonical templates for agents, skills, and commands based on EPIC-060 research patterns, with automated enforcement via the agent-generator subagent and prompt versioning for tracking changes and enabling rollback. This transforms research findings into actionable, enforceable standards.

## Success Metrics

- **Metric 1:** Canonical agent template created with required/optional sections (validated against 3+ diverse existing agents)
- **Metric 2:** Skill SKILL.md and command template variants created and documented
- **Metric 3:** agent-generator enforces template compliance on all new/updated agents (0% non-compliant creation)
- **Metric 4:** Prompt versioning tracks before/after changes for all modified agents
- **Metric 5:** All templates fit within 15K char command budget constraint

## Scope

### Overview

Design three template variants (agent, skill, command) based on prompt engineering patterns extracted in EPIC-060, update the agent-generator subagent to enforce template compliance at creation time, and implement a prompt versioning system for tracking changes and enabling rollback. This epic produces the tooling and standards needed for EPIC-062's rollout.

### Features

1. **Agent Template Design**
   - Description: Canonical template with required sections (identity, purpose, tools, output format, constraints, examples) and optional sections per category (validator, implementor, analyzer, formatter)
   - User Value: All 32+ agents follow consistent prompt structure proven by Anthropic research
   - Estimated Points: 8 story points
   - **Story:** STORY-386 - Design Canonical Agent Template with Required and Optional Sections

2. **Skill Template Design**
   - Description: SKILL.md variant with phase instruction patterns, progressive disclosure structure, reference file loading patterns based on research findings
   - User Value: New and updated skills are written with proven prompt engineering patterns
   - Estimated Points: 5 story points
   - **Story:** STORY-387 - Design Skill SKILL.md Template with Phase Patterns and Progressive Disclosure

3. **Command Template Design**
   - Description: Command variant respecting 15K char lean orchestration budget with optimal delegation patterns
   - User Value: Commands are efficient orchestrators that maximize quality within token budget
   - Estimated Points: 3 story points
   - **Story:** STORY-388 - Design Command Template Variant with 15K Char Budget Compliance

4. **Agent-Generator Enforcement**
   - Description: Update `agent-generator.md` to validate new/updated agents against canonical template; block non-compliant agents with specific error messages identifying missing/malformed sections
   - User Value: Non-compliant agents are blocked at creation time, preventing quality regression
   - Estimated Points: 8 story points
   - **Story:** STORY-389 - Update Agent-Generator with Template Compliance Enforcement

5. **Prompt Versioning System**
   - Description: Version tracking mechanism for before/after prompt changes per component, enabling rollback within minutes if regression detected
   - User Value: Safe migration with instant rollback capability for any individual component
   - Estimated Points: 6 story points
   - **Story:** STORY-390 - Implement Prompt Versioning System for Template Migration Safety

### Out of Scope

- Applying templates to existing agents (EPIC-062)
- Research and pattern extraction (EPIC-060)
- Automated prompt optimization (Won't Have per BRAINSTORM-010)
- External evaluation tools
- Changes to lean orchestration protocol itself

## Target Sprints

**Estimated Duration:** 2 sprints / 6 weeks

**Sprint Breakdown:**
- **Sprint 1:** F1: Agent Template + F2: Skill Template + F3: Command Template — 16 story points
  - Goal: Design all 3 template variants from EPIC-060 research findings
- **Sprint 2:** F4: Agent-Generator Enforcement + F5: Prompt Versioning — 14 story points
  - Goal: Build enforcement mechanism and version tracking system

## Dependencies

### External Dependencies

- None required (all work within Claude Code Terminal)

### Internal Dependencies

- **Dependency 1:** EPIC-060 must complete first (research patterns feed template design)
- **Note:** Some overlap possible — EPIC-061 Sprint 1 can start during EPIC-060 Sprint 3 if research artifact is substantially complete

### Blocking Issues

- None identified, assuming EPIC-060 completes successfully

## Stakeholders

- **Product Owner:** Framework Owner — Approves template design, validates enforcement rules
- **Orchestrator:** Opus — Executes template creation and enforcement implementation
- **Affected:** All subagent authors, skill developers, command maintainers

## Requirements

### Functional Requirements

#### User Stories

**User Story 7:**
```
As a Framework Owner,
I want a unified agent template with required/optional sections,
So that all agents follow consistent prompt structure.
```

**Acceptance Criteria:**
- [ ] Template defines required sections (identity, purpose, tools, output format, constraints)
- [ ] Template defines optional sections per agent category (validator, implementor, analyzer, formatter)
- [ ] Template validated against 3+ diverse existing agents (e.g., test-automator, code-reviewer, security-auditor)
- [ ] Template fits within 500-line subagent size limit

**User Story 8:**
```
As a Skill Developer,
I want a skill SKILL.md template variant with phase instruction patterns,
So that new skills are written with proven patterns.
```

**Acceptance Criteria:**
- [ ] Skill template includes phase numbering convention
- [ ] Progressive disclosure structure defined (main file vs references/)
- [ ] Reference file loading patterns documented
- [ ] Template fits within 1000-line skill size limit

**User Story 9:**
```
As a Framework Owner,
I want a command template variant respecting 15K char budget,
So that commands are efficient orchestrators.
```

**Acceptance Criteria:**
- [ ] Command template fits within 500-line / 15K char limit
- [ ] Delegation patterns to skills documented
- [ ] Error handling patterns included
- [ ] Character budget allocation guidance provided

**User Story 10:**
```
As Opus,
I want agent-generator to enforce template compliance,
So that non-compliant agents are blocked.
```

**Acceptance Criteria:**
- [ ] agent-generator validates against canonical template on create/update
- [ ] Non-compliant agents blocked with specific error messages
- [ ] Required section validation (missing section = block)
- [ ] Optional section validation (missing optional = warning, not block)
- [ ] No --skip-validation flag unless emergency (logged as deviation)

**User Story 11:**
```
As a Framework Owner,
I want prompt versioning tracking before/after changes,
So that I can rollback if quality decreases.
```

**Acceptance Criteria:**
- [ ] Version tracking mechanism implemented (git-based or file-based)
- [ ] Before/after state captured for each modified component
- [ ] Rollback possible within minutes for any individual component
- [ ] Version history accessible for audit

### Non-Functional Requirements (NFRs)

#### Performance
- Agent template processing must not increase agent response time noticeably
- Template validation in agent-generator completes within normal invocation time

#### Stability
- Zero breaking changes to existing command interface
- Templates are additive — existing agents continue to work without modification
- Enforcement applies only to new/updated agents (not retroactively to existing)

### Data Requirements

#### Entities

**Entity: Agent Template**
- **Location:** `.claude/skills/devforgeai-subagent-creation/assets/templates/` or `.claude/agents/` (TBD)
- **Attributes:** Required sections, optional sections, validation rules, category extensions
- **Relationships:** Enforced by agent-generator; applied to all 32+ agents in EPIC-062

**Entity: Prompt Version Record**
- **Location:** Git history + optional version section in each file
- **Attributes:** Component ID, before hash, after hash, change date, change reason
- **Relationships:** One per migrated component

### Integration Requirements

#### Internal Systems

**Integration 1: agent-generator subagent**
- **Purpose:** Enforce template compliance at agent creation time
- **Direction:** Two-way (generator reads template, validates against it)
- **Impact:** agent-generator.md must be updated with validation logic

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate**
- **Score:** 31/60 points (inherited from overall initiative)
- **Rationale:** Template design is conceptually straightforward; enforcement and versioning add moderate complexity

### Recommended Architecture Pattern
Uses existing DevForgeAI framework patterns:
- Templates as Markdown files (per tech-stack.md)
- Enforcement via subagent system prompt (existing pattern)
- Versioning via git history (existing capability)

### Technology Constraints
- All templates as Markdown files (per tech-stack.md)
- Agent template must fit within 500-line subagent limit (per source-tree.md)
- Skill template must fit within 1000-line skill limit (per source-tree.md)
- Command template must fit within 500-line / 15K char limit (per source-tree.md)
- No new dependencies required

## Risks & Constraints

### Technical Risks

**Risk 1: Template Too Rigid**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Category flexibility with optional sections; pilot validation in EPIC-062 before mass rollout

**Risk 2: Token Budget Exceeded**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Measure during template design; char limits per section; progressive disclosure for verbose sections

### Business Risks

**Risk 1: Template Revision Creates Inconsistency**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** EPIC-062 handles migration of all existing agents to new template; prompt versioning tracks changes

### Constraints

**Constraint 1: 15K Character Budget**
- **Impact:** Command template must be highly efficient
- **Mitigation:** Lean orchestration pattern delegation; progressive disclosure

**Constraint 2: Backward Compatibility**
- **Impact:** Templates cannot break existing agent/skill/command functionality
- **Mitigation:** Templates are additive; enforcement only for new/updated components

## Assumptions

1. **A2:** A single unified template can accommodate all agent categories with optional sections (validated during template design against 3+ diverse agents)
2. Research artifact from EPIC-060 provides sufficient patterns for template design

## Template Design Decisions (from Ideation)

- **Standardization Level:** Full standardization — single canonical template with required sections, optional sections, and validation rules enforced by agent-generator
- **Enforcement Mechanism:** agent-generator validates at creation time; non-compliant agents are blocked
- **No --skip-validation flag** unless emergency (must be logged as deviation)

## Next Steps

### Immediate Actions
1. **Wait for EPIC-060:** Research patterns must be available before template design begins
2. **Story Creation:** Run `/create-story` to decompose features into implementable stories
3. **Template Design:** Begin with agent template (highest impact, most components)

### Pre-Development Checklist
- [ ] EPIC-060 research artifact complete and reviewed
- [ ] Sprint 1 stories created
- [ ] Sprint plan approved
- [ ] 3+ diverse existing agents selected for template validation

## Notes

- Template design should start from the most impactful patterns identified in EPIC-060
- Agent-generator is updated last in EPIC-062 Wave 3 (it enforces the template, so update it after template is proven)
- Wait — agent-generator enforcement is in THIS epic (EPIC-061 F4). The EPIC-062 note about "update last" refers to migrating agent-generator's own prompt to the new template, which is separate from adding enforcement logic.

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2026-02-06
