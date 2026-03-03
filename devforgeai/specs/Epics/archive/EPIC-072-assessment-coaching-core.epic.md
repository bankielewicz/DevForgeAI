---
id: EPIC-072
title: Assessment & Coaching Core (Business Skills MVP Phase 1)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 20
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Assessment & Coaching Core (Business Skills MVP Phase 1)

## Business Goal

Enable DevForgeAI users (solo developers and aspiring entrepreneurs) to receive AI-powered business coaching that adapts to their cognitive style, builds confidence, and tracks progress. This is the **foundation epic** — all subsequent business skills (planning, research, marketing, legal, finance, operations, team) depend on the assessment engine and coaching infrastructure created here.

The system addresses three intertwined barriers: lack of business knowledge (MBA gap), lack of confidence (psychological gap), and executive dysfunction (ADHD/neurodivergent gap). By understanding each user through guided assessment, the AI adapts task granularity, session pacing, celebration intensity, and communication persona to maximize engagement and completion.

## Success Metrics

- **Metric 1:** Assessment skill generates a valid 7-dimension adaptive profile from questionnaire responses
- **Metric 2:** Coaching skill dynamically shifts between coach and consultant personas based on user profile
- **Metric 3:** Emotional state is tracked across sessions and influences subsequent session tone
- **Metric 4:** ASCII progress visualization renders correctly in Claude Code Terminal
- **Metric 5:** All skills < 1,000 lines; all commands < 500 lines; all subagents < 500 lines

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, YAML frontmatter
- Manual QA via `/assess-me` → `/coach-me` → `/my-business` workflow
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: Guided Self-Assessment Skill** (3 pts) — Priority: P1
   - Create `assessing-entrepreneur` skill with 6-dimension questionnaire
   - Create `entrepreneur-assessor` subagent for response normalization
   - Maps to: FR-001

2. **Feature 2: Adaptive Profile Generation** (3 pts) — Priority: P1
   - Add profile synthesis phase to assessment skill (7 calibration dimensions)
   - Create `/assess-me` command invoking the skill
   - Persist profile to `devforgeai/specs/business/user-profile.yaml`
   - Maps to: FR-002

3. **Feature 3: Dynamic Persona Blend Engine** (3 pts) — Priority: P1
   - Create `coaching-entrepreneur` skill with coach/consultant persona spectrum
   - Create `business-coach` subagent for coaching interactions
   - Maps to: FR-003

4. **Feature 4: Emotional State Tracking** (2 pts) — Priority: P2
   - Add cross-session emotional state read/write to coaching skill
   - Self-reported emotional state persisted to session log
   - Next session adapts tone based on previous state
   - Maps to: FR-004

5. **Feature 5: Confidence-Building Patterns** (3 pts) — Priority: P2
   - Create `confidence-patterns.md` reference (imposter syndrome, momentum, affirmation)
   - Update `business-coach` subagent to detect confidence signals and load patterns
   - Maps to: FR-005

6. **Feature 6: Terminal-Compatible Gamification** (3 pts) — Priority: P3
   - Add streak tracking and ASCII progress display to coaching skill
   - Add celebration event patterns as reference file
   - Profile-driven celebration intensity (low → high adaptation)
   - Maps to: FR-006

7. **Feature 7: /my-business Aggregated Dashboard** (3 pts) — Priority: P3
   - Create `/my-business` command reading all business artifacts
   - Create `/coach-me` command invoking coaching skill
   - Single aggregated view: profile, streak, emotional trend, next task
   - Maps to: FR-007

### Out of Scope

- Business plan generation (EPIC-B)
- Market research integration (EPIC-C)
- Marketing, legal, financial, operations, team skills (EPIC-D through EPIC-H)
- GUI/web interface (constraint: terminal-only)
- External tool integrations
- AI-generated legal/financial documents

## Target Sprints

### Sprint 1: Assessment Foundation
**Goal:** Deliver the assessment questionnaire, profile generation, and `/assess-me` command
**Estimated Points:** 6
**Features:**
- Feature 1: Guided Self-Assessment Skill (STORY-A, STORY-B)
- Feature 2: Adaptive Profile Generation (STORY-C, STORY-D)

**Key Deliverables:**
- `src/claude/skills/assessing-entrepreneur/SKILL.md` + references/
- `src/claude/agents/entrepreneur-assessor.md`
- `src/claude/commands/assess-me.md`
- `devforgeai/specs/business/user-profile.yaml` schema

### Sprint 2: Coaching Engine
**Goal:** Deliver coaching skill, persona blend, emotional tracking, and confidence patterns
**Estimated Points:** 8
**Features:**
- Feature 3: Dynamic Persona Blend Engine (STORY-E, STORY-F)
- Feature 4: Emotional State Tracking (STORY-G)
- Feature 5: Confidence-Building Patterns (STORY-H, STORY-I)

**Key Deliverables:**
- `src/claude/skills/coaching-entrepreneur/SKILL.md` + references/
- `src/claude/agents/business-coach.md`
- Coaching session state persistence

### Sprint 3: Dashboard & Gamification
**Goal:** Deliver gamification, dashboard, and final commands
**Estimated Points:** 6
**Features:**
- Feature 6: Terminal-Compatible Gamification (STORY-J, STORY-K)
- Feature 7: /my-business Dashboard (STORY-L, STORY-M)

**Key Deliverables:**
- `src/claude/commands/coach-me.md`
- `src/claude/commands/my-business.md`
- ASCII progress visualization patterns

## User Stories

1. **STORY-465:** Guided Self-Assessment Skill (3 pts, High) — Feature 1
2. **STORY-466:** Adaptive Profile Generation (3 pts, High) — Feature 2
3. **STORY-467:** Dynamic Persona Blend Engine (3 pts, High) — Feature 3
4. **STORY-468:** Emotional State Tracking (2 pts, Medium) — Feature 4
5. **STORY-469:** Confidence-Building Patterns (3 pts, Medium) — Feature 5
6. **STORY-470:** Terminal-Compatible Gamification (3 pts, Low) — Feature 6
7. **STORY-471:** /my-business Aggregated Dashboard (3 pts, Low) — Feature 7

**Total: 20 points across 7 stories**

### Dependency Chain
```
STORY-465 → STORY-466 → STORY-467 → STORY-468 → STORY-469
                              └──→ STORY-470 → STORY-471
```

### Sprint Allocation
- **Sprint 1** (6 pts): STORY-465, STORY-466
- **Sprint 2** (8 pts): STORY-467, STORY-468, STORY-469
- **Sprint 3** (6 pts): STORY-470, STORY-471

## Technical Considerations

### Architecture Impact
- **2 new skills** in `src/claude/skills/` (assessing-entrepreneur, coaching-entrepreneur)
- **2 new subagents** in `src/claude/agents/` (entrepreneur-assessor, business-coach)
- **3 new commands** in `src/claude/commands/` (assess-me, coach-me, my-business)
- **New data directory:** `devforgeai/specs/business/` for user profiles and coaching state
- **Progressive disclosure:** Both skills require `references/` directories for deep documentation

### Technology Decisions
- **Data format:** YAML for user profiles and coaching state (framework standard)
- **UX:** ASCII-only terminal rendering (no Unicode outside ASCII-safe range)
- **Skill naming:** Gerund-object convention per ADR-017 (assessing-entrepreneur, coaching-entrepreneur)
- **Profile ownership:** Assessment skill is sole writer; coaching skill reads only

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Subagents: < 500 lines, cannot invoke skills or commands
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Safety Requirements
- Never diagnose ADHD, anxiety, depression, or any mental health condition
- All health-related content includes disclaimer
- Emotional tracking is self-reported only (no AI inference of mental state)
- User can override any adaptation setting

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete
  - **Impact if missing:** Skills cannot validate against framework constraints

### External Dependencies
- None (framework operates entirely within Claude Code Terminal)

### Epic Dependencies
- **This epic blocks:** EPIC-B (Business Planning), EPIC-C (Market Research), and all subsequent business skill epics
- **This epic depends on:** Nothing (foundation epic)

## Risks & Mitigation

### Risk 1: Coaching skill exceeds 1,000-line limit
- **Probability:** High
- **Impact:** High — violates framework constraints
- **Mitigation:** Pre-plan references/ structure; persona blend, confidence patterns, and ASCII UX in separate reference files
- **Contingency:** Extract into additional reference files during refactoring phase

### Risk 2: YAML profile data coordination between skills
- **Probability:** Medium
- **Impact:** High — silent data loss
- **Mitigation:** Assessment skill is sole profile writer; coaching skill reads only; separate coaching state file
- **Contingency:** Add schema validation in profile read/write operations

### Risk 3: Emotional tracking scope creep
- **Probability:** High
- **Impact:** Medium — delays development
- **Mitigation:** Scope explicitly as self-reported state only; defer AI inference to future ADR
- **Contingency:** Drop emotional tracking to post-MVP if it blocks sprint 2

### Risk 4: /my-business command exceeds 500 lines
- **Probability:** Medium
- **Impact:** Medium — violates command size limit
- **Mitigation:** Keep as thin reader/renderer; extract complex aggregation to skill if needed
- **Contingency:** Create `summarizing-business` skill to back the command

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo developers wanting to turn projects into businesses
- Aspiring entrepreneurs needing structured guidance and confidence building

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `assessing-entrepreneur/SKILL.md` | Skill | `src/claude/skills/assessing-entrepreneur/` | F1, F2 |
| `assessing-entrepreneur/references/` | References | `src/claude/skills/assessing-entrepreneur/references/` | F1, F2 |
| `entrepreneur-assessor.md` | Subagent | `src/claude/agents/entrepreneur-assessor.md` | F1 |
| `assess-me.md` | Command | `src/claude/commands/assess-me.md` | F2 |
| `coaching-entrepreneur/SKILL.md` | Skill | `src/claude/skills/coaching-entrepreneur/` | F3, F4, F6 |
| `coaching-entrepreneur/references/` | References | `src/claude/skills/coaching-entrepreneur/references/` | F4, F5, F6 |
| `business-coach.md` | Subagent | `src/claude/agents/business-coach.md` | F3, F5 |
| `coach-me.md` | Command | `src/claude/commands/coach-me.md` | F7 |
| `my-business.md` | Command | `src/claude/commands/my-business.md` | F7 |

**Total: 9 framework deliverables** (2 skills + 2 subagents + 3 commands + 2 reference directories)

## Feature Dependency Chain

```
Feature 1 (Assessment Skill + Subagent)
  └── Feature 2 (Profile Generation + /assess-me)
        └── Feature 3 (Coaching Skill + Business-Coach Subagent)
                ├── Feature 4 (Emotional State Tracking)
                │     └── Feature 5 (Confidence Patterns)
                └── Feature 6 (Gamification)
                      └── Feature 7 (/my-business + /coach-me)
```

## Complexity Assessment

**Score: 6.5 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 6/10 | 9 deliverables across 4 types |
| State management | 7/10 | YAML profile shared between skills |
| Scope clarity | 7/10 | Emotional tracking scope defined (self-reported only) |
| Framework integration | 6/10 | New business/ directory in specs tree |
| Testing strategy | 6/10 | Markdown structural tests via pytest |
| ASCII UX | 5/10 | Terminal rendering well-understood |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Assessment Foundation (6 pts)
Sprint 2: Coaching Engine (8 pts)
Sprint 3: Dashboard & Gamification (6 pts)
================================
Total Duration: 3 sprints
Total Points: 20
Stories: 13
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/assess-me` generates valid adaptive profile
- [ ] **Sprint 2 Complete:** `/coach-me` delivers persona-adaptive coaching session
- [ ] **Sprint 3 Complete:** `/my-business` shows aggregated dashboard
- [ ] **Epic Complete:** Full assessment → coaching → dashboard workflow functional

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 6 | 4 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 8 | 5 | 0 | 0 | 0 |
| Sprint 3 | Not Started | 6 | 4 | 0 | 0 | 0 |
| **Total** | **0%** | **20** | **13** | **0** | **0** | **0** |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
