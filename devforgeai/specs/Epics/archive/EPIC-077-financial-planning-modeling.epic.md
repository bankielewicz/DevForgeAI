---
id: EPIC-077
title: Financial Planning & Modeling (Business Skills Post-MVP Phase 3)
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

# Epic: Financial Planning & Modeling (Business Skills Post-MVP Phase 3)

## Business Goal

Enable DevForgeAI users to create financial projections, pricing strategies, and funding plans for their business. Many first-time entrepreneurs avoid financial planning because it feels overwhelming or requires spreadsheet skills they lack. This epic provides guided, adaptive financial modeling through terminal-compatible tables and clear explanations, making financial planning accessible to non-finance backgrounds.

The `financial-modeler` subagent handles complex calculations and projection generation, while the `managing-finances` skill guides users through structured financial decisions adapted to their cognitive profile from EPIC-072.

**Safety constraint:** All financial outputs include "not financial advice" disclaimers (NFR-S003). Professional referral triggers for complex tax, investment, and accounting decisions.

## Success Metrics

- **Metric 1:** Pricing strategy framework produces guided recommendation based on cost structure, market data, and business model
- **Metric 2:** Revenue projection generates 12-month forecast with assumptions clearly stated
- **Metric 3:** Break-even analysis calculates units/revenue needed with terminal table output
- **Metric 4:** Every financial output file contains "not financial advice" disclaimer header
- **Metric 5:** All skills < 1,000 lines; all commands < 500 lines; all subagents < 500 lines

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, disclaimer presence
- Manual QA via `/financial-model` workflow with sample business scenarios
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: Startup Financial Model Generator** (3 pts) — Priority: P1
   - Create financial projection workflow in `managing-finances` skill
   - Simple revenue projection model (12-month, assumptions-based)
   - Cost structure analysis (fixed vs variable costs)
   - Terminal table output format for projections
   - Output to `devforgeai/specs/business/financial/projections.md`
   - Maps to: FR-019

2. **Feature 2: Pricing Strategy Framework** (3 pts) — Priority: P1
   - Add pricing workflow to `managing-finances` skill
   - Guided pricing strategy selection (cost-plus, value-based, competitive)
   - Integration with market research data from EPIC-074 for competitive pricing context
   - Output to `devforgeai/specs/business/financial/pricing-model.md`
   - Maps to: FR-019

3. **Feature 3: Break-Even Analysis** (2 pts) — Priority: P1
   - Add break-even calculation phase to `managing-finances` skill
   - Calculate units/revenue needed to cover costs
   - ASCII chart visualization of break-even point
   - Output appended to `devforgeai/specs/business/financial/projections.md`
   - Maps to: FR-019

4. **Feature 4: /financial-model Command & Skill Assembly** (1 pt) — Priority: P1
   - Create `/financial-model` command invoking `managing-finances` skill
   - Create `financial-modeler` subagent for calculation and projection generation
   - Integrate with user profile for adaptive pacing
   - Support both standalone and project-anchored modes

5. **Feature 5: Funding Options Guide** (1 pt) — Priority: P3
   - Decision tree based on business stage, capital needs, and founder preferences
   - Covers: bootstrapping, grants, angel investors, venture capital, loans
   - Pros/cons for each funding type with clear guidance on when each is appropriate
   - Output to `devforgeai/specs/business/financial/funding-strategy.md`
   - Maps to: FR-020

### Out of Scope

- Actual accounting or bookkeeping
- Tax preparation or tax advice
- Integration with financial software (QuickBooks, Xero)
- Investment portfolio management
- Detailed cash flow forecasting beyond 12 months
- Payroll calculations (deferred to EPIC-H team building)

## Target Sprints

### Sprint 1: Financial Modeling Core
**Goal:** Deliver financial projections, pricing strategy, break-even analysis, and `/financial-model` command
**Estimated Points:** 9
**Features:**
- Feature 1: Startup Financial Model Generator (STORY-A, STORY-B)
- Feature 2: Pricing Strategy Framework (STORY-C)
- Feature 3: Break-Even Analysis (STORY-D)
- Feature 4: /financial-model Command & Skill Assembly (STORY-E)

**Key Deliverables:**
- `src/claude/skills/managing-finances/SKILL.md` + references/
- `src/claude/agents/financial-modeler.md`
- `src/claude/commands/financial-model.md`

### Sprint 2: Funding Guide
**Goal:** Deliver funding options decision tree
**Estimated Points:** 1
**Features:**
- Feature 5: Funding Options Guide (STORY-F)

**Key Deliverables:**
- `src/claude/skills/managing-finances/references/funding-options-guide.md`

## User Stories

1. **As an** entrepreneur, **I want** help creating revenue projections **so that** I understand my financial viability
2. **As a** user, **I want** guided pricing strategy selection **so that** I price my product appropriately
3. **As a** user, **I want** a break-even analysis **so that** I know how much I need to sell to cover costs
4. **As a** user, **I want** one command (`/financial-model`) **so that** I can run the full financial planning workflow
5. **As a** user needing capital, **I want** to understand funding options **so that** I can choose the right path

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/` (managing-finances)
- **1 new subagent** in `src/claude/agents/` (financial-modeler)
- **1 new command** in `src/claude/commands/` (financial-model)
- **Progressive disclosure:** Skill requires `references/` directory

### Technology Decisions
- **Data format:** Markdown with ASCII tables for financial outputs
- **Calculations:** `financial-modeler` subagent handles projections (no external libraries)
- **Skill naming:** Gerund-object convention per ADR-017 (managing-finances)
- **Market data integration:** Reads competitive pricing from EPIC-074 market research outputs

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Subagents: < 500 lines, cannot invoke skills or commands
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Safety Requirements (CRITICAL)
- **NFR-S003:** All financial guidance includes "not financial advice" disclaimer
- Revenue projections clearly label assumptions and uncertainty ranges
- Never implies AI can replace licensed financial advisors or accountants
- Professional referral triggers for tax planning, investment decisions, complex funding rounds

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete

- [ ] **EPIC-073 (Business Planning & Viability)** — Business model for financial context
  - **Status:** Planning
  - **Impact if delayed:** Financial skill works but lacks business model context for tailored projections

- [ ] **EPIC-074 (Market Research & Competition)** — Market data for competitive pricing
  - **Status:** Planning
  - **Impact if delayed:** Pricing strategy works without competitive data; relies on user inputs only

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** EPIC-073 (business model) + EPIC-074 (market data)
- **This epic blocks:** EPIC-H (Team Building — needs financial capacity data)

## Risks & Mitigation

### Risk 1: Users treat AI financial projections as reliable forecasts
- **Probability:** High
- **Impact:** Critical — poor business decisions based on AI estimates
- **Mitigation:** Prominent disclaimers; always show assumptions; label as "directional estimates"; include confidence ranges
- **Contingency:** Add per-output "assumptions review" step requiring user acknowledgment

### Risk 2: Financial calculations produce incorrect results
- **Probability:** Medium
- **Impact:** High — incorrect break-even or projections
- **Mitigation:** Simple arithmetic models only; show calculation steps; test with known scenarios
- **Contingency:** Include "verify with an accountant" recommendation alongside all calculations

### Risk 3: managing-finances skill exceeds 1,000-line limit
- **Probability:** Medium
- **Impact:** High — violates framework constraints
- **Mitigation:** Financial model, pricing framework, break-even analysis, funding guide in separate reference files
- **Contingency:** Extract additional phases into reference files

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo developers needing basic financial projections for their product
- Aspiring entrepreneurs building investor-ready financial plans

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `managing-finances/SKILL.md` | Skill | `src/claude/skills/managing-finances/` | F1, F2, F3, F5 |
| `managing-finances/references/` | References | `src/claude/skills/managing-finances/references/` | F1, F2, F3, F5 |
| `financial-modeler.md` | Subagent | `src/claude/agents/financial-modeler.md` | F4 |
| `financial-model.md` | Command | `src/claude/commands/financial-model.md` | F4 |

**Total: 4 framework deliverables** (1 skill + 1 subagent + 1 command + 1 reference directory)

### Reference Files (Progressive Disclosure)

| Reference File | Purpose | Feature |
|----------------|---------|---------|
| `startup-financial-model.md` | Revenue projection methodology and templates | F1 |
| `pricing-strategy-framework.md` | Cost-plus, value-based, competitive pricing guides | F2 |
| `break-even-analysis.md` | Break-even calculation methodology and ASCII charts | F3 |
| `funding-options-guide.md` | Bootstrap, grants, angels, VC decision tree | F5 |

## Feature Dependency Chain

```
Feature 4 (/financial-model Command + financial-modeler Subagent)
  ├── Feature 1 (Financial Model Generator)
  │     └── Feature 3 (Break-Even Analysis)
  ├── Feature 2 (Pricing Strategy)
  └── Feature 5 (Funding Options Guide)
```

## Complexity Assessment

**Score: 5.0 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 4/10 | 4 deliverables across 3 types |
| State management | 4/10 | Reads profile + market data; writes financial artifacts |
| Scope clarity | 7/10 | Well-defined: projections + pricing + break-even + funding |
| Framework integration | 5/10 | New subagent (financial-modeler); reads EPIC-074 outputs |
| Testing strategy | 5/10 | Structural tests + calculation verification |
| Safety sensitivity | 6/10 | Financial disclaimer enforcement required |

## Revisitation Trigger

After this epic is implemented and QA-approved:
```
/brainstorm --resume BRAINSTORM-011

"EPIC-F (Financial Planning) is complete. Financial modeling and pricing are now available.
Has the user's confidence changed? Update coaching approach. Does the business plan
milestone tracker need financial gates added?"
```

## Timeline

```
Epic Timeline:
================================
Sprint 1: Financial Modeling Core (9 pts)
Sprint 2: Funding Guide (1 pt)
================================
Total Duration: 1-2 sprints
Total Points: 10
Stories: 6
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/financial-model` generates projections, pricing, and break-even
- [ ] **Sprint 2 Complete:** Funding options guide available
- [ ] **Epic Complete:** Full financial planning workflow functional with disclaimers

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 9 | 5 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 1 | 1 | 0 | 0 | 0 |
| **Total** | **0%** | **10** | **6** | **0** | **0** | **0** |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
