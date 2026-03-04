---
id: EPIC-079
title: Team Building & HR (Business Skills Post-MVP Phase 5)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 7
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Team Building & HR (Business Skills Post-MVP Phase 5)

## Business Goal

Guide solo entrepreneurs through the transition from solopreneur to employer — deciding when to hire, who to hire first, whether to use contractors or employees, and how to evaluate co-founder compatibility. Many first-time founders either hire too early (burning runway) or too late (burning out). This epic provides structured decision frameworks that help users make informed people decisions at the right time, based on their financial capacity (EPIC-077) and operational maturity (EPIC-078).

## Success Metrics

- **Metric 1:** First hire decision framework produces a recommendation with rationale based on business stage and financial inputs
- **Metric 2:** Co-founder compatibility assessment covers complementary skills, values alignment, conflict resolution, and equity expectations
- **Metric 3:** Contractor vs employee decision tree accounts for legal, financial, and operational factors
- **Metric 4:** All skills < 1,000 lines; all commands < 500 lines

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, decision tree completeness
- Manual QA via `/build-team` workflow
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: First Hire Decision Framework** (3 pts) — Priority: P2
   - Guided workflow: "When should I make my first hire?"
   - Decision factors: revenue threshold, time spent on non-core tasks, growth trajectory, financial runway
   - Produces role recommendation with job description outline
   - Integrates with financial data from EPIC-077 for affordability assessment
   - Output to `devforgeai/specs/business/team/first-hire-plan.md`
   - Maps to: FR-022

2. **Feature 2: Co-Founder Compatibility Assessment** (2 pts) — Priority: P2
   - Structured questionnaire evaluating complementary skills, values, vision, work style, conflict resolution, equity expectations
   - Generates compatibility report with strengths and risk areas
   - Output to `devforgeai/specs/business/team/cofounder-assessment.md`
   - Maps to: FR-022

3. **Feature 3: /build-team Command & Skill Assembly** (1 pt) — Priority: P2
   - Create `/build-team` command invoking `building-team` skill
   - Assemble full `building-team` skill with progressive disclosure references
   - Integrate with user profile for adaptive pacing
   - Support both standalone and project-anchored modes

4. **Feature 4: Contractor vs Employee Decision Tree** (1 pt) — Priority: P2
   - Decision framework: legal classification factors, cost comparison, management overhead, IP considerations
   - Includes "consult a professional" triggers for complex situations
   - Reference file with guidance on contractor agreements and onboarding
   - Output to `devforgeai/specs/business/team/workforce-strategy.md`
   - Maps to: FR-022

### Out of Scope

- ❌ Actual job posting or recruiting automation
- ❌ Payroll setup or HR software implementation
- ❌ Employment law advice (liability — general guidance with disclaimers only)
- ❌ Performance management systems
- ❌ Benefits and compensation administration
- ❌ International hiring and remote team management

## Target Sprints

### Sprint 1: Team Foundations
**Goal:** Deliver first hire framework, co-founder assessment, and `/build-team` command
**Estimated Points:** 6
**Features:**
- Feature 1: First Hire Decision Framework (STORY-562)
- Feature 2: Co-Founder Compatibility Assessment (STORY-563)
- Feature 3: /build-team Command & Skill Assembly (STORY-564)

**Key Deliverables:**
- `src/claude/skills/building-team/SKILL.md` + references/
- `src/claude/commands/build-team.md`

### Sprint 2: Workforce Strategy
**Goal:** Deliver contractor vs employee guidance
**Estimated Points:** 1
**Features:**
- Feature 4: Contractor vs Employee Decision Tree (STORY-565)

**Key Deliverables:**
- `src/claude/skills/building-team/references/contractor-vs-employee.md`

## User Stories

1. **As a** growing entrepreneur, **I want** guidance on when and who to hire first **so that** I build the right team at the right time
2. **As a** founder considering a co-founder, **I want** a compatibility assessment **so that** I evaluate partnership fit before committing
3. **As a** user, **I want** one command (`/build-team`) **so that** I can access all team-building guidance
4. **As a** user deciding between contractors and employees, **I want** a decision framework **so that** I choose the right workforce model

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/` (building-team)
- **1 new command** in `src/claude/commands/` (build-team)
- **No new subagents** — leverages existing `business-coach` for adaptive guidance
- **Progressive disclosure:** Skill requires `references/` directory

### Technology Decisions
- **Data format:** Markdown for team guidance outputs
- **Skill naming:** Gerund-object convention per ADR-017 (building-team)
- **Profile integration:** Reads user profile from EPIC-072 for adaptive pacing (read-only)
- **Financial integration:** Reads financial data from EPIC-077 for hire affordability (read-only)
- **Operations integration:** Reads operational context from EPIC-078 for role prioritization (read-only)

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Safety Requirements
- Employment law guidance includes "consult a professional" disclaimer
- Co-founder equity discussions include "consult a lawyer" triggers
- Contractor classification guidance warns about misclassification risks
- No jurisdiction-specific employment law (general US guidance with "verify locally" warnings)

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete

- [ ] **EPIC-077 (Financial Planning & Modeling)** — Financial capacity for hiring decisions
  - **Status:** Planning
  - **Impact if delayed:** First hire framework works without financial integration; uses user-provided estimates

- [ ] **EPIC-078 (Operations & Launch)** — Operational context for role prioritization
  - **Status:** Planning
  - **Impact if delayed:** Works without operations context; uses general prioritization

- [ ] **EPIC-072 (Assessment & Coaching Core)** — User profile for adaptive pacing
  - **Status:** Planning
  - **Impact if delayed:** Works without adaptation; uses default settings

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** EPIC-077 (Financial Planning), EPIC-078 (Operations & Launch)
- **This epic blocks:** None (final epic in business skills chain)

## Risks & Mitigation

### Risk 1: Users treat hiring guidance as employment law advice
- **Probability:** Medium
- **Impact:** High — liability and user harm
- **Mitigation:** Prominent disclaimers; "consult an employment lawyer" triggers at every legal threshold; never use prescriptive language
- **Contingency:** Add per-session disclaimer acknowledgment

### Risk 2: Co-founder assessment creates false confidence
- **Probability:** Medium
- **Impact:** Medium — bad partnership decisions
- **Mitigation:** Frame as "conversation starter, not verdict"; include "discuss with a business advisor" recommendation; emphasize iterative evaluation
- **Contingency:** Add prominent caveat that no assessment replaces extended real-world collaboration

### Risk 3: Contractor vs employee misclassification guidance
- **Probability:** Low
- **Impact:** High — legal consequences for users
- **Mitigation:** Education-only framing; IRS guidelines reference (general); mandatory "consult a tax professional" trigger
- **Contingency:** Limit to general awareness; redirect all classification decisions to professionals

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo entrepreneurs growing beyond solopreneur stage
- Founders considering co-founder partnerships

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `building-team/SKILL.md` | Skill | `src/claude/skills/building-team/` | F1, F2, F4 |
| `building-team/references/` | References | `src/claude/skills/building-team/references/` | F1, F2, F4 |
| `build-team.md` | Command | `src/claude/commands/build-team.md` | F3 |

**Total: 3 framework deliverables** (1 skill + 1 command + 1 reference directory)

### Reference Files (Progressive Disclosure)

| Reference File | Purpose | Feature |
|----------------|---------|---------|
| `first-hire-framework.md` | When/who to hire decision tree | F1 |
| `co-founder-assessment.md` | Partnership compatibility questionnaire | F2 |
| `contractor-vs-employee.md` | Workforce model decision tree | F4 |
| `culture-definition-guide.md` | Company culture and values definition | F1 |

## Feature Dependency Chain

```
Feature 3 (/build-team Command + Skill Assembly)
  ├── Feature 1 (First Hire Decision Framework)
  │     └── Feature 4 (Contractor vs Employee)
  └── Feature 2 (Co-Founder Compatibility Assessment)
```

## Complexity Assessment

**Score: 3.5 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 3/10 | 3 deliverables (simplest pattern) |
| State management | 3/10 | Reads profile + financial data; writes team artifacts |
| Scope clarity | 8/10 | Well-defined: hire + co-founder + workforce |
| Framework integration | 4/10 | Standard skill/command pattern |
| Testing strategy | 4/10 | Markdown structural tests + decision tree validation |
| Safety sensitivity | 5/10 | Employment law disclaimers needed but lower risk than legal/financial |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Team Foundations (6 pts)
Sprint 2: Workforce Strategy (1 pt)
================================
Total Duration: 1-2 sprints
Total Points: 7
Stories: 5
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/build-team` generates first hire recommendation and co-founder assessment
- [ ] **Sprint 2 Complete:** Contractor vs employee framework available
- [ ] **Epic Complete:** Full team-building workflow functional with adaptive pacing

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 6 | 4 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 1 | 1 | 0 | 0 | 0 |
| **Total** | **0%** | **7** | **5** | **0** | **0** | **0** |

## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-562 | Feature 1 | First Hire Decision Framework | 3 | Backlog |
| STORY-563 | Feature 2 | Co-Founder Compatibility Assessment | 2 | Backlog |
| STORY-564 | Feature 3 | /build-team Command & Skill Assembly | 1 | Backlog |
| STORY-565 | Feature 4 | Contractor vs Employee Decision Tree | 1 | Backlog |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
