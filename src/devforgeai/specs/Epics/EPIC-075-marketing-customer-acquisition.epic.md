---
id: EPIC-075
title: Marketing & Customer Acquisition (Business Skills Post-MVP Phase 1)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 11
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Marketing & Customer Acquisition (Business Skills Post-MVP Phase 1)

## Business Goal

Enable DevForgeAI users to create actionable go-to-market strategies and customer acquisition plans. After validating their business idea (EPIC-072/073) and researching their market (EPIC-074), users need a clear path to reach their first customers. This epic bridges the gap between "I know my market" and "I know how to reach customers."

The system guides users through positioning, messaging, channel selection, and go-to-market planning — all adapted to their cognitive style from the assessment engine (EPIC-072). For ADHD users, marketing planning is chunked into micro-tasks with clear next actions rather than overwhelming strategy documents.

## Success Metrics

- **Metric 1:** Go-to-market strategy skill generates channel-prioritized plan with budget awareness
- **Metric 2:** Positioning framework produces differentiated messaging for 3-5 audience segments
- **Metric 3:** All outputs persist to `devforgeai/specs/business/marketing/` directory
- **Metric 4:** All skills < 1,000 lines; all commands < 500 lines

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, YAML frontmatter
- Manual QA via `/marketing-plan` workflow with sample business scenarios
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: Go-to-Market Strategy Builder** (3 pts) — Priority: P1
   - Create go-to-market workflow in `marketing-business` skill
   - Channel selection matrix based on business model, budget, and target audience
   - Prioritized action items for first 30 days post-launch
   - Output to `devforgeai/specs/business/marketing/go-to-market.md`
   - Maps to: FR-015

2. **Feature 2: Positioning & Messaging Framework** (3 pts) — Priority: P1
   - Add positioning workflow to `marketing-business` skill
   - Generate positioning statement using standard framework (category, differentiation, audience)
   - Create 3-5 key messages for different audience segments
   - Output to `devforgeai/specs/business/marketing/positioning.md`
   - Maps to: FR-016

3. **Feature 3: /marketing-plan Command & Skill Assembly** (2 pts) — Priority: P1
   - Create `/marketing-plan` command invoking `marketing-business` skill
   - Assemble full `marketing-business` skill with progressive disclosure references
   - Integrate with user profile for adaptive pacing
   - Support both standalone and project-anchored modes

4. **Feature 4: Customer Discovery Workflow** (2 pts) — Priority: P2
   - Add customer discovery phase leveraging interview questions from EPIC-074
   - Guide users through outreach planning and feedback synthesis
   - Track discovery progress as milestone in business plan

5. **Feature 5: Content & Channel Strategy Outline** (1 pt) — Priority: P3
   - Generate content strategy skeleton (topics, frequency, channels)
   - Social media presence guide (which platforms, basic posting cadence)
   - Lightweight reference file, not a full content management system

### Out of Scope

- Automated social media posting or scheduling
- Email marketing template generation
- Paid advertising campaign management
- SEO/SEM technical implementation
- GUI/web interface (constraint: terminal-only)
- Content creation (only strategy and planning)

## Target Sprints

### Sprint 1: Marketing Strategy Foundation
**Goal:** Deliver go-to-market strategy, positioning framework, and `/marketing-plan` command
**Estimated Points:** 8
**Features:**
- Feature 1: Go-to-Market Strategy Builder (STORY-A, STORY-B)
- Feature 2: Positioning & Messaging Framework (STORY-C, STORY-D)
- Feature 3: /marketing-plan Command & Skill Assembly (STORY-E)

**Key Deliverables:**
- `src/claude/skills/marketing-business/SKILL.md` + references/
- `src/claude/commands/marketing-plan.md`

### Sprint 2: Customer Discovery & Content
**Goal:** Deliver customer discovery workflow and content strategy outline
**Estimated Points:** 3
**Features:**
- Feature 4: Customer Discovery Workflow (STORY-F)
- Feature 5: Content & Channel Strategy Outline (STORY-G)

**Key Deliverables:**
- `src/claude/skills/marketing-business/references/customer-discovery-workflow.md`
- `src/claude/skills/marketing-business/references/channel-selection-matrix.md`
- Integration with EPIC-074 customer interview outputs

## User Stories

1. **STORY-539:** Go-to-Market Strategy Builder (3 pts, High) — **As an** entrepreneur, **I want** a go-to-market strategy **so that** I know how to reach my first customers
2. **STORY-540:** Positioning & Messaging Framework (3 pts, High) — **As a** user, **I want** help crafting positioning and messaging **so that** my marketing is consistent and compelling
3. **STORY-541:** /marketing-plan Command & Skill Assembly (2 pts, High) — **As a** user, **I want** one command (`/marketing-plan`) **so that** I can run the full marketing planning workflow
4. **STORY-542:** Customer Discovery Workflow (2 pts, Medium) — **As a** user who completed customer interviews, **I want** guidance synthesizing feedback **so that** I can refine my approach
5. **STORY-543:** Content & Channel Strategy Outline (1 pt, Low) — **As a** solo entrepreneur, **I want** a simple content strategy outline **so that** I know what to post and where

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/` (marketing-business)
- **1 new command** in `src/claude/commands/` (marketing-plan)
- **No new subagents** — leverages existing `business-coach` for adaptive guidance
- **Progressive disclosure:** Skill requires `references/` directory for deep documentation

### Technology Decisions
- **Data format:** Markdown for marketing outputs
- **Skill naming:** Gerund-object convention per ADR-017 (marketing-business)
- **Profile integration:** Reads user profile from EPIC-072 for adaptive pacing (read-only)
- **Market data integration:** Reads competitive analysis from EPIC-074 to inform positioning

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Safety Requirements
- Marketing guidance is educational, not a substitute for professional marketing consultation
- Channel recommendations include budget impact warnings
- No promises of specific customer acquisition numbers

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete

- [ ] **EPIC-074 (Market Research & Competition)** — Competitive analysis for positioning
  - **Status:** Planning
  - **Impact if delayed:** Marketing skill works but positioning lacks competitive data

- [ ] **EPIC-072 (Assessment & Coaching Core)** — User profile for adaptive pacing
  - **Status:** Planning
  - **Impact if delayed:** Works without adaptation; uses default settings

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** EPIC-074 (needs market research for informed positioning)
- **This epic blocks:** None directly (EPIC-F Financial uses market data from EPIC-074, not this epic)

## Risks & Mitigation

### Risk 1: Marketing guidance too generic without market research data
- **Probability:** Medium
- **Impact:** Medium — users get boilerplate instead of tailored strategy
- **Mitigation:** Require EPIC-074 outputs as input; fallback to guided questions if missing
- **Contingency:** Clearly label outputs as "template" vs "data-informed"

### Risk 2: marketing-business skill exceeds 1,000-line limit
- **Probability:** Medium
- **Impact:** High — violates framework constraints
- **Mitigation:** Go-to-market framework, positioning strategy, channel matrix, customer discovery in separate reference files
- **Contingency:** Extract additional phases into reference files

### Risk 3: Scope creep into content creation
- **Probability:** High
- **Impact:** Medium — delays and scope bloat
- **Mitigation:** Explicit out-of-scope: content creation, social media posting, email templates
- **Contingency:** Defer content creation to a future epic or ADR

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo developers ready to market their product
- Aspiring entrepreneurs building pre-launch marketing plans

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `marketing-business/SKILL.md` | Skill | `src/claude/skills/marketing-business/` | F1, F2, F4, F5 |
| `marketing-business/references/` | References | `src/claude/skills/marketing-business/references/` | F1, F2, F4, F5 |
| `marketing-plan.md` | Command | `src/claude/commands/marketing-plan.md` | F3 |

**Total: 3 framework deliverables** (1 skill + 1 command + 1 reference directory)

### Reference Files (Progressive Disclosure)

| Reference File | Purpose | Feature |
|----------------|---------|---------|
| `go-to-market-framework.md` | GTM strategy builder with channel prioritization | F1 |
| `positioning-strategy.md` | Positioning statement and messaging framework | F2 |
| `channel-selection-matrix.md` | Channel evaluation criteria and budget mapping | F1 |
| `customer-discovery-workflow.md` | Outreach planning and feedback synthesis | F4 |

## Feature Dependency Chain

```
Feature 3 (/marketing-plan Command + Skill Assembly)
  ├── Feature 1 (Go-to-Market Strategy)
  │     └── Feature 4 (Customer Discovery)
  ├── Feature 2 (Positioning & Messaging)
  │     └── Feature 5 (Content Strategy Outline)
  └── Feature 4 (Customer Discovery)
```

## Complexity Assessment

**Score: 4.5 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 3/10 | 3 deliverables (simpler than EPIC-072/074) |
| State management | 4/10 | Reads profile + market research; writes marketing artifacts |
| Scope clarity | 7/10 | Well-defined: GTM + positioning + customer discovery |
| Framework integration | 5/10 | Reads from EPIC-072 and EPIC-074 outputs |
| Testing strategy | 5/10 | Markdown structural tests via pytest |
| Domain complexity | 5/10 | Marketing frameworks well-established |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Marketing Strategy Foundation (8 pts)
Sprint 2: Customer Discovery & Content (3 pts)
================================
Total Duration: 2 sprints
Total Points: 11
Stories: 7
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/marketing-plan` generates GTM strategy and positioning
- [ ] **Sprint 2 Complete:** Customer discovery workflow and content outline available
- [ ] **Epic Complete:** Full marketing planning workflow functional

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 8 | 5 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 3 | 2 | 0 | 0 | 0 |
| **Total** | **0%** | **11** | **7** | **0** | **0** | **0** |

## Revisitation Trigger

After this epic is implemented and QA-approved, trigger revisitation:
```
/brainstorm --resume BRAINSTORM-011

"EPIC-D (Marketing) is complete. These skills exist: assessing-entrepreneur, coaching-entrepreneur,
planning-business, researching-market, marketing-business. How does marketing integrate with the
assessment engine from EPIC-A? Should coaching sessions now include marketing accountability?"
```

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
