---
id: EPIC-078
title: Operations & Launch (Business Skills Post-MVP Phase 4)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 10
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Operations & Launch (Business Skills Post-MVP Phase 4)

## Business Goal

Guide DevForgeAI users from "business plan complete" to "business launched" through structured operational checklists, tool selection guidance, process design, and scaling readiness assessment. Many aspiring entrepreneurs stall between planning and launching because the operational details feel overwhelming — what tools to use, what processes to set up, what order to do things. This epic converts the abstract "launch a business" into a concrete, adaptive checklist that integrates with the user's existing business plan and legal foundation.

**Integration with DevForgeAI:** For users with active DevForgeAI development projects, the `/ops-plan` command connects business launch operations with the existing `/release` command for code deployment, creating a unified launch experience.

## Success Metrics

- **Metric 1:** MVP launch checklist covers all 5 domains: legal, financial, marketing, technical, operations
- **Metric 2:** Tool selection recommendations include rationale and budget awareness for each recommendation
- **Metric 3:** `/ops-plan` produces a complete launch checklist adapted to user's business model and cognitive profile
- **Metric 4:** All skills < 1,000 lines; all commands < 500 lines
- **Metric 5:** DevForgeAI project integration: `/ops-plan` detects active project and connects deployment to `/release`

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, checklist completeness
- Manual QA via `/ops-plan` workflow
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: MVP Launch Checklist** (3 pts) — Priority: P1
   - Comprehensive launch checklist covering legal, financial, marketing, technical, and operations domains
   - Checklist adapts to business model type (SaaS, marketplace, service, product) from EPIC-073 output
   - Integrates with user profile (EPIC-072) for micro-task chunking and adaptive pacing
   - Output to `devforgeai/specs/business/operations/launch-checklist.md`
   - Maps to: FR-021

2. **Feature 2: Tool Selection Guide** (2 pts) — Priority: P1
   - Guided workflow for selecting business tools: CRM, payment processing, analytics, communication, project management
   - Budget-aware recommendations (free tier, starter, growth)
   - Comparison tables rendered in terminal-compatible ASCII
   - Output to `devforgeai/specs/business/operations/tool-stack.md`
   - Maps to: FR-021

3. **Feature 3: /ops-plan Command & Skill Assembly** (2 pts) — Priority: P1
   - Create `/ops-plan` command invoking `operating-business` skill
   - Assemble full `operating-business` skill with progressive disclosure references
   - Detect active DevForgeAI project and offer `/release` integration
   - Support both standalone and project-anchored modes

4. **Feature 4: Process Design Framework** (2 pts) — Priority: P2
   - Guide users through defining core business processes (customer onboarding, support, fulfillment)
   - Simple process flow documentation adapted to business model
   - Output to `devforgeai/specs/business/operations/core-processes.md`

5. **Feature 5: Scaling Readiness Assessment** (1 pt) — Priority: P2
   - Post-launch assessment: "Is your business ready to scale?"
   - Checklist of scaling prerequisites (infrastructure, processes, team, financial runway)
   - Reference file with guidance on when and how to scale
   - Output to `devforgeai/specs/business/operations/scaling-readiness.md`

### Out of Scope

- ❌ Actual deployment automation (handled by DevForgeAI `/release` command)
- ❌ Specific vendor integrations (Stripe, QuickBooks, etc.) — tool selection is guidance only
- ❌ Industry-specific regulatory compliance (covered in EPIC-076)
- ❌ Team building and HR operations (deferred to EPIC-H)
- ❌ Financial projections and pricing (covered in EPIC-077)
- ❌ Marketing execution (covered in EPIC-075)

## Target Sprints

### Sprint 28: Operations Launch (Consolidated)
**Goal:** Deliver all operations & launch features in a single sprint
**Estimated Points:** 10
**Features:**
- Feature 1: MVP Launch Checklist (STORY-554)
- Feature 2: Tool Selection Guide (STORY-555)
- Feature 3: /ops-plan Command & Skill Assembly (STORY-556) — depends on STORY-554, STORY-555
- Feature 4: Process Design Framework (STORY-557)
- Feature 5: Scaling Readiness Assessment (STORY-558)

**Key Deliverables:**
- `src/claude/skills/operating-business/SKILL.md` + references/
- `src/claude/commands/ops-plan.md`

## User Stories

1. **As a** user ready to launch, **I want** a comprehensive checklist **so that** I don't miss critical launch steps
2. **As a** user choosing business tools, **I want** budget-aware recommendations **so that** I pick the right tools for my stage
3. **As a** user, **I want** one command (`/ops-plan`) **so that** I can access all operations guidance
4. **As a** user defining how my business works, **I want** process design guidance **so that** I have documented workflows
5. **As a** user post-launch, **I want** to assess my scaling readiness **so that** I know when to grow

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/` (operating-business)
- **1 new command** in `src/claude/commands/` (ops-plan)
- **No new subagents** — leverages existing `business-coach` for adaptive guidance
- **Progressive disclosure:** Skill requires `references/` directory
- **Integration point:** DevForgeAI `/release` command connection for project-anchored mode

### Technology Decisions
- **Data format:** Markdown for operations guidance outputs
- **Skill naming:** Gerund-object convention per ADR-017 (operating-business)
- **Profile integration:** Reads user profile from EPIC-072 for adaptive pacing (read-only)
- **Business plan integration:** Reads business model from EPIC-073 for checklist adaptation (read-only)
- **Legal integration:** Reads business structure from EPIC-076 for compliance checklist items (read-only)

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Performance Requirements
- Launch checklist generation: < 30 seconds
- Tool selection workflow: adaptive micro-sessions (5-15 min per EPIC-072 profile)
- ASCII table rendering: terminal-compatible, no GUI dependencies

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete

- [ ] **EPIC-073 (Business Planning & Viability)** — Business model context for checklist adaptation
  - **Status:** Planning
  - **Impact if delayed:** Launch checklist works generically; lacks model-specific recommendations

- [ ] **EPIC-076 (Legal & Compliance)** — Legal foundation items for compliance checklist
  - **Status:** Planning
  - **Impact if delayed:** Legal checklist items use generic defaults; no structure-specific guidance

- [ ] **EPIC-072 (Assessment & Coaching Core)** — User profile for adaptive pacing
  - **Status:** Planning
  - **Impact if delayed:** Works without adaptation; uses default settings

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** EPIC-073 (Business Planning), EPIC-076 (Legal & Compliance)
- **This epic blocks:** EPIC-H/EPIC-079 (Team Building — needs operations context)

## Risks & Mitigation

### Risk 1: Tool recommendations become outdated
- **Probability:** High
- **Impact:** Medium — recommendations lose credibility
- **Mitigation:** Recommend tool categories and selection criteria rather than specific products; include "verify current pricing" disclaimer
- **Contingency:** Reference files are easily updatable; version date in each recommendation

### Risk 2: Checklist overwhelms ADHD users despite chunking
- **Probability:** Medium
- **Impact:** High — defeats the purpose of the framework
- **Mitigation:** Micro-task adaptation from EPIC-072 profile; show only next 3 items; celebrate each completion
- **Contingency:** Add "launch essentials only" mode showing minimum viable launch steps

### Risk 3: `/release` integration creates coupling
- **Probability:** Low
- **Impact:** Medium — operational complexity
- **Mitigation:** Integration is optional; detected via project presence, not required
- **Contingency:** Standalone mode works independently; `/release` connection is additive only

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo developers ready to launch their product as a business
- Aspiring entrepreneurs moving from planning to execution

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `operating-business/SKILL.md` | Skill | `src/claude/skills/operating-business/` | F1, F2, F4, F5 |
| `operating-business/references/` | References | `src/claude/skills/operating-business/references/` | F1, F2, F4, F5 |
| `ops-plan.md` | Command | `src/claude/commands/ops-plan.md` | F3 |

**Total: 3 framework deliverables** (1 skill + 1 command + 1 reference directory)

### Reference Files (Progressive Disclosure)

| Reference File | Purpose | Feature |
|----------------|---------|---------|
| `mvp-launch-checklist.md` | Comprehensive launch checklist by domain | F1 |
| `tool-selection-guide.md` | Budget-aware tool recommendations by category | F2 |
| `process-design-framework.md` | Core business process templates | F4 |
| `scaling-readiness-assessment.md` | Post-launch scaling criteria and checklist | F5 |

## Feature Dependency Chain

```
Feature 3 (/ops-plan Command + Skill Assembly)
  ├── Feature 1 (MVP Launch Checklist)
  │     └── Feature 4 (Process Design Framework)
  └── Feature 2 (Tool Selection Guide)
        └── Feature 5 (Scaling Readiness Assessment)
```

## Complexity Assessment

**Score: 4.5 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 3/10 | 3 deliverables (standard skill/command pattern) |
| State management | 4/10 | Reads profile + business plan + legal artifacts; writes operations artifacts |
| Scope clarity | 8/10 | Well-defined: checklist + tools + process + scale |
| Framework integration | 5/10 | Standard pattern + optional /release integration |
| Testing strategy | 5/10 | Markdown structural tests + checklist completeness validation |
| Cross-epic integration | 5/10 | Reads from 3 other epics (072, 073, 076) |

## Timeline

```
Epic Timeline:
================================
Sprint 28: Operations Launch (10 pts)
================================
Total Duration: 1 sprint
Total Points: 10
Stories: 5
```

### Key Milestones
- [ ] **Sprint 28 Complete:** All operations & launch features delivered (checklist, tools, command, processes, scaling)
- [ ] **Epic Complete:** Full operations workflow functional with adaptive pacing

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 28 | Active | 10 | 5 | 0 | 0 | 0 |
| **Total** | **0%** | **10** | **5** | **0** | **0** | **0** |

## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-554 | Feature 1 | MVP Launch Checklist | 3 | Backlog |
| STORY-555 | Feature 2 | Tool Selection Guide | 2 | Backlog |
| STORY-556 | Feature 3 | /ops-plan Command & Skill Assembly | 2 | Backlog |
| STORY-557 | Feature 4 | Process Design Framework | 2 | Backlog |
| STORY-558 | Feature 5 | Scaling Readiness Assessment | 1 | Backlog |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
