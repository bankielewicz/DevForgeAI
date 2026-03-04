---
id: EPIC-074
title: Market Research & Competition (Business Skills MVP Phase 3)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 13
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Market Research & Competition (Business Skills MVP Phase 3)

## Business Goal

Enable DevForgeAI users to validate their business ideas through structured market research and competitive analysis before investing significant time and resources. This epic builds on the assessment engine (EPIC-072) and business planning (EPIC-073) to provide data-driven market intelligence that grounds business plans in reality.

Users currently lack the structured approach to answer critical questions: "Is my market big enough?", "Who are my competitors?", and "What should I ask potential customers?" This epic delivers a guided market research skill that leverages the existing `internet-sleuth` subagent for real-time research and introduces a new `market-analyst` subagent for synthesis and analysis. All outputs adapt to the user's cognitive profile from EPIC-072 (task chunking, pacing, progress visualization).

## Success Metrics

- **Metric 1:** Market sizing skill generates TAM/SAM/SOM estimates with cited data sources
- **Metric 2:** Competitive analysis identifies 3-10 competitors with structured strengths/weaknesses
- **Metric 3:** Customer interview generator produces 10-20 hypothesis-aligned questions
- **Metric 4:** All outputs persist to `devforgeai/specs/business/market-research/` directory
- **Metric 5:** All skills < 1,000 lines; all commands < 500 lines; all subagents < 500 lines

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, YAML frontmatter
- Manual QA via `/market-research` workflow with sample business ideas
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: Market Sizing Guided Workflow** (3 pts) — Priority: P1
   - Create TAM/SAM/SOM estimation workflow in `researching-market` skill
   - Leverage `internet-sleuth` subagent for market data gathering
   - Adapt question depth to user's business knowledge level (from user profile)
   - Output to `devforgeai/specs/business/market-research/market-sizing.md`
   - Maps to: FR-012

2. **Feature 2: Competitive Landscape Analysis** (3 pts) — Priority: P1
   - Add competitive analysis phase to `researching-market` skill
   - Create `market-analyst` subagent for research synthesis and positioning matrix generation
   - Identify 3-10 competitors with strengths, weaknesses, and differentiation opportunities
   - Output to `devforgeai/specs/business/market-research/competitive-analysis.md`
   - Maps to: FR-013

3. **Feature 3: Customer Interview Question Generator** (2 pts) — Priority: P2
   - Add interview question generation phase to `researching-market` skill
   - Generate 10-20 questions organized by hypothesis being tested
   - Include interviewing best practices guidance as reference file
   - Output to `devforgeai/specs/business/market-research/customer-interviews.md`
   - Maps to: FR-014

4. **Feature 4: /market-research Command & Skill Assembly** (3 pts) — Priority: P1
   - Create `/market-research` command invoking `researching-market` skill
   - Assemble full `researching-market` skill with progressive disclosure references
   - Integrate with user profile for adaptive pacing and task chunking
   - Support both standalone and project-anchored modes
   - Maps to: FR-012, FR-013, FR-014 (integration)

5. **Feature 5: Market Research Report Synthesis** (2 pts) — Priority: P2
   - Add report aggregation phase synthesizing market sizing + competitive analysis + customer insights
   - ASCII-rendered summary suitable for terminal display
   - Feed results back into business plan milestones (EPIC-073 integration point)

### Out of Scope

- Business plan generation (EPIC-073)
- Marketing and go-to-market strategy (EPIC-D)
- Financial modeling from market data (EPIC-F)
- GUI/web interface (constraint: terminal-only)
- Real-time market monitoring or alerts
- Paid data source integrations

## Target Sprints

### Sprint 1: Market Research Foundation
**Goal:** Deliver market sizing, competitive analysis, and the `/market-research` command
**Estimated Points:** 9
**Features:**
- Feature 1: Market Sizing Guided Workflow (STORY-535)
- Feature 2: Competitive Landscape Analysis (STORY-536)
- Feature 4: /market-research Command & Skill Assembly (STORY-538)

**Key Deliverables:**
- `src/claude/skills/researching-market/SKILL.md` + references/
- `src/claude/agents/market-analyst.md`
- `src/claude/commands/market-research.md`

### Sprint 2: Customer Discovery & Synthesis
**Goal:** Deliver customer interview generator and research report synthesis
**Estimated Points:** 4
**Features:**
- Feature 3: Customer Interview Question Generator (STORY-537)
- Feature 5: Market Research Report Synthesis (STORY-573)

**Key Deliverables:**
- `src/claude/skills/researching-market/references/customer-interview-guide.md`
- Report synthesis phase in skill
- Integration tests with EPIC-073 business plan

## User Stories

1. **As an** entrepreneur, **I want** help estimating my market size **so that** I understand the revenue opportunity
2. **As a** user, **I want** to understand my competitive landscape **so that** I can differentiate my business
3. **As a** user preparing for customer discovery, **I want** AI-generated interview questions **so that** I can validate my assumptions with real customers
4. **As a** user, **I want** one command (`/market-research`) **so that** I can run the full research workflow
5. **As a** user, **I want** a synthesized research report **so that** I can see the full market picture in one view

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/` (researching-market)
- **1 new subagent** in `src/claude/agents/` (market-analyst)
- **1 new command** in `src/claude/commands/` (market-research)
- **Leverages existing:** `internet-sleuth` subagent for web research
- **Progressive disclosure:** Skill requires `references/` directory for deep documentation

### Technology Decisions
- **Data format:** Markdown for research outputs (human-readable, version-controlled)
- **Research engine:** `internet-sleuth` subagent (existing) + `market-analyst` subagent (new, synthesis layer)
- **Skill naming:** Gerund-object convention per ADR-017 (researching-market)
- **Profile integration:** Reads user profile from EPIC-072 for adaptive pacing (read-only)

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Subagents: < 500 lines, cannot invoke skills or commands
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Safety Requirements
- Market sizing estimates include uncertainty ranges and methodology disclaimers
- Competitive analysis avoids defamatory language about competitors
- All financial projections include "not financial advice" disclaimer
- Research data sources are cited where available

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete
  - **Impact if missing:** Skills cannot validate against framework constraints

- [ ] **EPIC-072 (Assessment & Coaching Core)** — User profile for adaptive pacing
  - **Status:** Planning
  - **Impact if delayed:** Market research skill works but without adaptive pacing; can use default settings

- [ ] **EPIC-073 (Business Planning & Viability)** — Business model context for targeted research
  - **Status:** Planning
  - **Impact if delayed:** Market research works standalone but lacks business model context for focused queries

### External Dependencies
- None (framework operates entirely within Claude Code Terminal)

### Epic Dependencies
- **This epic depends on:** EPIC-073 (needs business model context)
- **This epic blocks:** EPIC-D (Marketing — needs market research), EPIC-F (Financial — needs market data)

## Risks & Mitigation

### Risk 1: internet-sleuth subagent rate limiting or unavailability
- **Probability:** Medium
- **Impact:** High — core research capability degraded
- **Mitigation:** Design skill to work with partial data; include manual input fallback where user provides their own research
- **Contingency:** Skill generates research framework and questions for user to fill manually

### Risk 2: Market sizing produces low-quality estimates without real data
- **Probability:** High
- **Impact:** Medium — estimates may be unreliable
- **Mitigation:** Use Fermi estimation methodology with clear assumptions; always show methodology alongside numbers
- **Contingency:** Label estimates as "directional" and focus on relative comparisons

### Risk 3: researching-market skill exceeds 1,000-line limit
- **Probability:** Medium
- **Impact:** High — violates framework constraints
- **Mitigation:** Pre-plan references/ structure; market sizing workflow, competitive analysis framework, interview guide in separate reference files
- **Contingency:** Extract additional phases into reference files during refactoring

### Risk 4: Overlap with internet-sleuth capabilities
- **Probability:** Low
- **Impact:** Medium — confusion about which tool to use
- **Mitigation:** Clear separation: `internet-sleuth` is the research engine (raw data); `market-analyst` is the synthesis layer (structured analysis)
- **Contingency:** Document usage guidance in skill references

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo developers wanting to validate business potential of their projects
- Aspiring entrepreneurs needing structured market validation before investing time

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `researching-market/SKILL.md` | Skill | `src/claude/skills/researching-market/` | F1, F2, F3, F5 |
| `researching-market/references/` | References | `src/claude/skills/researching-market/references/` | F1, F2, F3, F5 |
| `market-analyst.md` | Subagent | `src/claude/agents/market-analyst.md` | F2 |
| `market-research.md` | Command | `src/claude/commands/market-research.md` | F4 |

**Total: 4 framework deliverables** (1 skill + 1 subagent + 1 command + 1 reference directory)

### Reference Files (Progressive Disclosure)

| Reference File | Purpose | Feature |
|----------------|---------|---------|
| `market-sizing-methodology.md` | TAM/SAM/SOM estimation guide with Fermi methodology | F1 |
| `competitive-analysis-framework.md` | Competitor identification, positioning matrix, SWOT | F2 |
| `trend-analysis-patterns.md` | Industry trend detection and validation patterns | F2, F5 |
| `customer-interview-guide.md` | Interview question generation, best practices | F3 |

## Feature Dependency Chain

```
Feature 4 (/market-research Command + Skill Assembly)
  ├── Feature 1 (Market Sizing Workflow)
  │     └── Feature 5 (Report Synthesis)
  ├── Feature 2 (Competitive Analysis + market-analyst Subagent)
  │     └── Feature 5 (Report Synthesis)
  └── Feature 3 (Customer Interview Generator)
        └── Feature 5 (Report Synthesis)
```

## Complexity Assessment

**Score: 5.5 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 4/10 | 4 deliverables across 3 types (simpler than EPIC-072) |
| State management | 5/10 | Reads user profile; writes research artifacts |
| Scope clarity | 7/10 | Well-defined: market sizing + competitive + interviews |
| Framework integration | 6/10 | Leverages existing internet-sleuth; adds market-analyst |
| Testing strategy | 5/10 | Markdown structural tests via pytest |
| External data dependency | 7/10 | Relies on web research quality from internet-sleuth |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Market Research Foundation (9 pts)
Sprint 2: Customer Discovery & Synthesis (4 pts)
================================
Total Duration: 2 sprints
Total Points: 13
Stories: 7
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/market-research` generates market sizing and competitive analysis
- [ ] **Sprint 2 Complete:** Customer interview questions generated; synthesized report available
- [ ] **Epic Complete:** Full market research workflow functional with adaptive pacing

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 9 | 5 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 4 | 2 | 0 | 0 | 0 |
| **Total** | **0%** | **13** | **7** | **0** | **0** | **0** |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
