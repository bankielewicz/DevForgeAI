---
id: EPIC-073
title: Business Planning & Viability (Business Skills MVP Phase 2)
status: Planning
start_date: TBD
target_date: TBD
total_points: 16
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Business Planning & Viability (Business Skills MVP Phase 2)

## Business Goal

Enable users to create structured, milestone-based business plans through guided AI workflows. The planning skill reads the user's adaptive profile (from EPIC-072) to calibrate question depth, task granularity, and session pacing. Plans use milestones instead of calendar deadlines to reduce anxiety and support neurodivergent users. The skill operates in dual mode: project-anchored (analyzes an existing DevForgeAI codebase for business potential) and standalone (pure business idea without code).

This epic delivers the core deliverable users expect — a business plan — making DevForgeAI's business skills tangible and immediately useful.

## Success Metrics

- **Metric 1:** Lean Canvas generated with all 9 blocks populated from guided workflow
- **Metric 2:** Milestone-based plan with 10 adaptive milestones, each with micro-tasks and validation gates
- **Metric 3:** Business model correctly detected and model-specific guidance provided
- **Metric 4:** Dual-mode operates correctly (with and without DevForgeAI project)
- **Metric 5:** Plan iteration works across multiple sessions (data persists)

**Measurement Plan:**
- Structural validation tests in `tests/` verify skill file sizes, sections, frontmatter
- Manual QA via `/business-plan` in both standalone and project-anchored modes
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: Lean Canvas Guided Workflow** (5 pts) — Priority: P1
   - Create `planning-business` skill with Lean Canvas phase (9 blocks)
   - Adaptive question depth based on user profile from EPIC-072
   - Output to `devforgeai/specs/business/business-plan/lean-canvas.md`
   - Iteration support (refine over multiple sessions)
   - Maps to: FR-008

2. **Feature 2: Milestone-Based Plan Generator** (5 pts) — Priority: P1
   - Add milestone generation phase to `planning-business` skill
   - 10 milestones from Problem Validated to Launch Ready
   - Each milestone: definition, soft timeframe, micro-tasks, validation gate, celebration
   - Guard rails: 7-day min, 180-day soft max with recalibration trigger
   - Output to `devforgeai/specs/business/business-plan/milestones.yaml`
   - Maps to: FR-009

3. **Feature 3: Business Model Pattern Matching** (3 pts) — Priority: P2
   - Add business model detection phase (SaaS, marketplace, service, product)
   - Model-specific guidance and frameworks loaded from references/
   - Viability scoring rubric with clear pass/fail criteria
   - Maps to: FR-010

4. **Feature 4: Dual-Mode & /business-plan Command** (3 pts) — Priority: P1
   - Create `/business-plan` command invoking `planning-business` skill
   - Project-anchored mode: detects DevForgeAI project, analyzes codebase context
   - Standalone mode: works with business idea description only
   - Both modes produce same output format
   - Maps to: FR-011

### Out of Scope

- Market research and competitive analysis (EPIC-C)
- Marketing strategy (EPIC-D)
- Legal, financial, operations, team skills (EPIC-E through EPIC-H)
- Financial projections and pricing models (EPIC-F)
- GUI/web interface

## Target Sprints

### Sprint 1: Planning Foundation
**Goal:** Deliver Lean Canvas workflow and /business-plan command
**Estimated Points:** 8
**Features:**
- Feature 1: Lean Canvas Guided Workflow
- Feature 4: Dual-Mode & /business-plan Command

**Key Deliverables:**
- `src/claude/skills/planning-business/SKILL.md` + references/
- `src/claude/commands/business-plan.md`
- Lean Canvas output template

### Sprint 2: Milestones & Models
**Goal:** Deliver milestone generator and business model pattern matching
**Estimated Points:** 8
**Features:**
- Feature 2: Milestone-Based Plan Generator
- Feature 3: Business Model Pattern Matching

**Key Deliverables:**
- Milestone generation phase added to planning skill
- Business model references/ files
- Viability scoring rubric

## User Stories

1. **STORY-531:** Lean Canvas Guided Workflow (5 pts, High) — Feature 1
2. **STORY-532:** Milestone-Based Plan Generator (5 pts, High) — Feature 2
3. **STORY-533:** Business Model Pattern Matching (3 pts, Medium) — Feature 3
4. **STORY-534:** Dual-Mode /business-plan Command (3 pts, High) — Feature 4

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/planning-business/`
- **1 new command** in `src/claude/commands/business-plan.md`
- **No new subagents** (uses existing `business-coach` from EPIC-072 for adaptive tone)
- **New data files:** `devforgeai/specs/business/business-plan/` directory

### Skill Structure (Progressive Disclosure)
```
src/claude/skills/planning-business/
├── SKILL.md                              (< 1000 lines, core phases)
└── references/
    ├── lean-canvas-workflow.md            (9-block guided workflow)
    ├── milestone-generator.md            (milestone creation logic)
    ├── business-model-patterns.md        (SaaS, marketplace, service, product)
    ├── viability-scoring.md              (scoring rubric)
    └── plan-iteration-workflow.md        (cross-session refinement)
```

### Constraints
- Reads user profile from `devforgeai/specs/business/user-profile.yaml` (created by EPIC-072)
- Planning skill reads profile but does NOT write to it (assessment skill = sole writer)
- All output to `devforgeai/specs/business/business-plan/`
- Markdown only, < 1,000 lines, progressive disclosure required
- Development in `src/` tree; tests in `tests/`

### Safety Requirements
- Viability scoring is guidance, not financial advice — disclaimer required
- Business model recommendations include "consult a professional" when appropriate

## Dependencies

### Internal Dependencies
- [x] **EPIC-072 (Assessment & Coaching Core)** — MUST complete first
  - **Reason:** Planning skill reads user adaptive profile for question depth and pacing
  - **Impact if delayed:** Planning skill operates without adaptation (degraded experience)

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** EPIC-072
- **This epic blocks:** EPIC-C (Market Research), EPIC-E (Legal), EPIC-F (Financial)

## Risks & Mitigation

### Risk 1: Lean Canvas workflow exceeds SKILL.md line limit
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** 9 canvas blocks documented in `references/lean-canvas-workflow.md`, not in SKILL.md
- **Contingency:** Split into multiple reference files per canvas block group

### Risk 2: Milestone generation produces generic plans
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Milestones adapt based on business model type and user profile
- **Contingency:** Add industry-specific milestone templates in references/

### Risk 3: Dual-mode detection fails for edge cases
- **Probability:** Low
- **Impact:** Low
- **Mitigation:** Clear mode detection: check for `devforgeai/specs/context/` files → project-anchored; else standalone
- **Contingency:** User selects mode via AskUserQuestion

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `planning-business/SKILL.md` | Skill | `src/claude/skills/planning-business/` | F1, F2, F3 |
| `planning-business/references/` | References | `src/claude/skills/planning-business/references/` | F1, F2, F3 |
| `business-plan.md` | Command | `src/claude/commands/business-plan.md` | F4 |

**Total: 3 framework deliverables** (1 skill + 1 reference directory + 1 command)

## Feature Dependency Chain

```
Feature 4 (Dual-Mode + /business-plan command)
  └── Feature 1 (Lean Canvas Workflow)
        ├── Feature 2 (Milestone Generator)
        └── Feature 3 (Business Model Matching)
```

## Complexity Assessment

**Score: 5.0 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 3/10 | 1 skill + 1 command + references — lean |
| Content depth | 7/10 | Lean Canvas (9 blocks) + 10 milestones + 4 model types |
| State management | 4/10 | Reads profile (read-only), writes plan (sole owner) |
| Framework integration | 5/10 | Standard skill pattern, reads existing profile |
| Dual-mode logic | 6/10 | Project detection + standalone fallback |
| Testing | 5/10 | Structural tests for Markdown artifacts |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Planning Foundation (8 pts)
  - Lean Canvas + /business-plan command
Sprint 2: Milestones & Models (8 pts)
  - Milestone generator + business model matching
================================
Total Duration: 2 sprints
Total Points: 16
Stories: ~6-8
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/business-plan` generates Lean Canvas in both modes
- [ ] **Sprint 2 Complete:** Milestone-based plan with model-specific guidance
- [ ] **Epic Complete:** Full planning workflow integrated with assessment profile

## Progress Tracking

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 8 | 3-4 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 8 | 3-4 | 0 | 0 | 0 |
| **Total** | **0%** | **16** | **6-8** | **0** | **0** | **0** |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md` (FR-008 to FR-011)
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`
- **Depends on:** `devforgeai/specs/Epics/EPIC-072-assessment-coaching-core.epic.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
