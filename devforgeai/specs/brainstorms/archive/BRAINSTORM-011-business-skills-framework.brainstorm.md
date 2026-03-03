---
# DevForgeAI Brainstorm Session
id: BRAINSTORM-011
title: "Business Skills Framework for DevForgeAI"
status: Complete
created: 2026-02-21
facilitator: DevForgeAI
session_duration: "45 minutes"
question_count: 10

# Core Outputs (AI-Consumable for /ideate)
problem_statement: "Developers and aspiring entrepreneurs build projects but never turn them into businesses due to intertwined barriers: lack of business knowledge (MBA gap), lack of confidence (psychological gap), and executive dysfunction (ADHD/neurodivergent gap)."
target_outcome: "An AI-powered business coaching framework integrated into DevForgeAI that adapts to each user's cognitive style, builds confidence, and guides them from project/idea to viable business through milestone-based plans."
recommended_approach: "9 new skills (MBA-style domains) + 10 slash commands + 4 subagents, rolled out via iterative agile epics (A-H + R revisitation), with an adaptive assessment engine as the foundation."
confidence_level: "High"

# Stakeholder Summary
primary_stakeholder: "Solo developers and aspiring entrepreneurs"
user_personas:
  - "Solo Developer: Has a project, wants to turn it into a business, struggles with overwhelm and imposter syndrome"
  - "Aspiring Entrepreneur: Has a business idea, no technical product yet, doesn't know where to start"

# Constraint Summary
budget_range: "Framework development only (no external costs)"
timeline: "Iterative — 9 epics delivered sequentially via agile"
hard_constraints:
  - "Claude Code Terminal only (no GUI/web components)"
  - "Markdown documentation only (no executable code in skills)"
  - "Skills must follow gerund naming, <1000 lines, progressive disclosure"
  - "Development in src/ tree, tests in tests/, operational .claude/ only after QA"
  - "All skills must read 6 context files before processing"

# Hypothesis Summary
critical_assumptions:
  - "H1: ADHD-adapted micro-tasks increase session completion rates"
  - "H2: Confidence coaching improves business plan quality"
  - "H3: Milestone-based planning outperforms calendar-based for neurodivergent users"
  - "H4: Adaptive blend persona (coach/consultant) outperforms fixed personas"
  - "H5: Terminal-only UX is sufficient for gamification and progress tracking"

# Prioritization Summary
must_have_capabilities:
  - "User assessment engine (ADHD, confidence, work style detection)"
  - "Adaptive coaching with confidence building"
  - "Business plan generation with milestone-based tracking"
  - "Market research and competitive analysis"
  - "Terminal-compatible progress visualization"
  - "Micro-task chunking for executive dysfunction support"
nice_to_have:
  - "Legal template library with disclaimers"
  - "Financial model generator with terminal tables"
  - "Team building and HR guidance"
  - "Gamification with streaks and achievement tracking"
---

# Business Skills Framework for DevForgeAI

## Executive Summary

DevForgeAI currently excels at spec-driven software development but stops short of helping users turn their projects into businesses. This brainstorm session identified a critical gap: developers and aspiring entrepreneurs face **three intertwined barriers** — lack of business knowledge, lack of confidence, and executive dysfunction (ADHD/neurodivergent challenges). These barriers compound each other: ADHD makes the overwhelming number of business steps worse, which erodes confidence, which increases avoidance.

The proposed solution is a full suite of 9 AI-powered business skills integrated into the DevForgeAI framework, each with corresponding slash commands and subagents. The AI operates as an **adaptive blend** — dynamically shifting between empathetic coach and professional consultant based on user needs detected through a combination of self-reporting and guided assessment. Skills work in **both modes**: standalone (pure business coaching without a code project) and project-anchored (connected to a DevForgeAI development project).

The framework rolls out via **9 iterative agile epics** (A through H, plus R for revisitation), with a dedicated revisitation loop that re-evaluates the brainstorm after each epic's completion to ensure integration quality. All development follows the dual-path architecture: code in `src/`, tests in `tests/`, operational `.claude/` updated only after QA approval.

---

## 1. Stakeholder Analysis

### 1.1 Stakeholder Map

| Category | Stakeholder | Role | Influence |
|----------|-------------|------|-----------|
| Primary | Solo developer/creator | End user — turns project into business | HIGH |
| Primary | Aspiring entrepreneur (non-technical) | End user — structures business idea | HIGH |
| Secondary | DevForgeAI framework | Platform for skill integration | HIGH |
| Tertiary | Professional advisors (lawyers, accountants) | External — receives prepared clients | LOW |

### 1.2 Stakeholder Goals & Concerns

**Primary Stakeholders:**

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| Solo developer | Turn project into revenue, gain business confidence | Overwhelm, imposter syndrome, ADHD, time management |
| Aspiring entrepreneur | Validate idea, create actionable plan, launch | Don't know where to start, self-doubt, analysis paralysis |

**Secondary Stakeholders:**

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| DevForgeAI framework | Extensible, constraint-compliant skill integration | No code in skills, progressive disclosure, size limits |

### 1.3 Identified Conflicts

| Stakeholders | Conflict | Resolution Approach |
|--------------|----------|---------------------|
| Developer vs Entrepreneur | Different starting points (have code vs have idea) | Dual-mode: project-anchored vs standalone |
| Speed vs Thoroughness | ADHD users need quick wins; business planning needs depth | Micro-task chunking with progressive depth |
| Coach vs Consultant | Some users want encouragement, others want deliverables | Adaptive blend persona that detects and shifts |

---

## 2. Problem Analysis

### 2.1 Problem Statement

> Creators and developers experience parallel barriers — they lack business knowledge (MBA gap), lack confidence (psychological gap), and struggle with executive function (ADHD/neurodivergent gap). These barriers are deeply intertwined: ADHD makes the overwhelming number of business steps worse, which erodes confidence, which increases avoidance. No existing AI framework addresses all three simultaneously with adaptive coaching.

### 2.2 Root Cause Analysis (5 Whys)

| Level | Question | Answer |
|-------|----------|--------|
| 1 | Why don't developers turn projects into businesses? | They don't know the business steps required |
| 2 | Why don't they learn the business steps? | The information is overwhelming and scattered |
| 3 | Why is it overwhelming? | There are too many steps with no clear prioritization for their specific situation |
| 4 | Why can't they prioritize? | Executive dysfunction (ADHD), self-doubt, and analysis paralysis prevent action |
| 5 | Why does self-doubt persist? | No feedback loop confirming they're making progress; no one adapted guidance to their cognitive style |

**Root Cause:** Lack of adaptive, personalized business guidance that accounts for neurodivergent cognitive styles and builds confidence through progressive, visible milestones.

### 2.3 Current State Assessment

**Process Type:** None — No integrated business guidance exists in DevForgeAI

| Metric | Current Value | Target Value |
|--------|---------------|--------------|
| Business skills available | 0 skills | 9 skills |
| Commands for business guidance | 0 commands | 10 commands |
| ADHD adaptation | None | Full adaptive system |
| Confidence coaching | None | Integrated into every session |

**Bottlenecks:**
1. No assessment mechanism to understand user's cognitive style
2. No business domain knowledge encoded in framework
3. No progress tracking or gamification for motivation

### 2.4 Pain Point Inventory

| Pain Point | Business Impact | Severity |
|------------|-----------------|----------|
| No business guidance after building a project | Lost entrepreneurial potential | CRITICAL |
| No ADHD/neurodivergent accommodation | Users abandon before starting | CRITICAL |
| No confidence building mechanism | Users with good ideas never execute | HIGH |
| No milestone-based planning | Calendar deadlines create anxiety, not action | HIGH |
| No market research integration | Users build without market validation | MEDIUM |

### 2.5 Failed Solution History

| Previous Attempt | What Happened | Lessons Learned |
|------------------|---------------|-----------------|
| Generic business courses | Too broad, not personalized, no accountability | Must adapt to individual |
| Self-help books | Inspiration fades without structured follow-through | Need ongoing coaching, not one-shot |
| Traditional business consultants | Expensive, don't understand neurodivergent needs | AI can be available 24/7 and adapt |

---

## 3. Opportunity Canvas

### 3.1 Blue-Sky Vision

**Ideal Future State:**
A developer finishes building their app in DevForgeAI and types `/my-business`. The AI says: "Based on your project, here's what I see as a business opportunity. Let's explore it together." Over the next weeks, through adaptive micro-sessions that match their cognitive style, they go from idea to launched business — with the AI celebrating every milestone, adapting to their energy levels, and building their confidence at every step.

**Key Outcomes:**
- Users who would never start a business actually launch one
- ADHD/neurodivergent users complete business plans at rates comparable to neurotypical users
- Confidence measurably increases across coaching sessions
- Framework becomes a complete idea-to-business pipeline

### 3.2 Technology Opportunities

| Technology | Application | Fit |
|-----------|------------|-----|
| AI coaching (Claude) | Adaptive persona, business analysis, market research | Perfect — already the platform |
| Progressive disclosure | Load deep frameworks only when needed | Required by architecture |
| ASCII visualization | Terminal-compatible progress bars, celebrations | Constraint-compliant |
| YAML persistence | User profiles, milestone tracking, streak data | Framework standard |

### 3.3 Identified Opportunities

| Opportunity | Description | Potential Impact |
|-------------|-------------|------------------|
| Assessment engine | Understand each user's cognitive style and adapt all guidance | Foundation for everything else |
| Adaptive coaching | Dynamic coach/consultant persona that shifts per user needs | Addresses confidence + knowledge gaps |
| Milestone planning | Non-calendar business plans that progress by completion | ADHD-friendly, reduces anxiety |
| Market research integration | Leverage existing internet-sleuth for business analysis | Validates ideas before users invest time |
| Gamification | Streaks, progress bars, celebrations in terminal | Dopamine-friendly motivation |
| Dual-mode operation | Works with or without a code project | Doubles the addressable user base |

### 3.4 Adjacent Opportunities

| Related Problem | Connection | Synergy |
|-----------------|------------|---------|
| DevForgeAI project deployment | `/release` already exists | Connect business launch to code deployment |
| Feedback system | Coaching session feedback | Use existing feedback infrastructure |
| Brainstorm revisitation | Re-evaluate after each epic | Built-in framework evolution |

---

## 4. Constraint Matrix

### 4.1 Budget Constraints

| Aspect | Constraint | Flexibility |
|--------|------------|-------------|
| Initial investment | Framework development time only | Flexible |
| Ongoing costs | Zero (no external services) | Fixed |
| ROI expectation | Value to users, not revenue | N/A |

### 4.2 Timeline Constraints

| Milestone | Target | Flexibility |
|-----------|--------|-------------|
| EPIC-A (Foundation) | First epic | Fixed (must be first) |
| EPIC-B (Business Plan) | After EPIC-A | Depends on EPIC-A |
| EPIC-C (Market Research) | After EPIC-B | Depends on EPIC-B |
| EPIC-D through H | Sequential post-MVP | Negotiable order (some parallel possible) |

### 4.3 Resource Constraints

| Resource | Available | Gap |
|----------|-----------|-----|
| AI platform | Claude Code Terminal | None |
| Business knowledge | Encoded in skill references | Must be authored |
| ADHD/neurodivergent expertise | Research-based patterns | Must be encoded in references |

### 4.4 Technical Constraints

- [x] Must operate within Claude Code Terminal (no GUI)
- [x] Must use Markdown documentation only (no executable code in skills)
- [x] Must follow gerund naming for skills
- [x] Must keep SKILL.md under 1,000 lines (target 500-800)
- [x] Must use progressive disclosure (references/ for deep docs)
- [x] Must develop in src/ tree, test in tests/
- [x] Must read 6 context files before processing

### 4.5 Organizational Constraints

- [x] Skills follow DevForgeAI architecture-constraints.md
- [x] No circular dependencies between skills
- [x] Subagents cannot invoke skills or commands
- [x] All user decisions require AskUserQuestion (never assume)

---

## 5. Hypothesis Register

### 5.1 Critical Hypotheses

| ID | Hypothesis | Success Criteria | Validation Method | Risk if Wrong |
|----|------------|------------------|-------------------|---------------|
| H1 | IF we break business tasks into 5-15 min micro-chunks, THEN ADHD users will complete more sessions | 50%+ session completion rate | Track completion % with/without adaptation | Users abandon framework |
| H2 | IF we integrate confidence coaching into business planning, THEN plan quality improves | Plans score higher on viability rubric | Compare coached vs uncoached sessions | Coaching is wasted effort |
| H3 | IF we use milestone-based plans instead of calendar-based, THEN neurodivergent users complete more milestones | 40%+ milestone completion rate | User satisfaction + completion tracking | Plans feel arbitrary |
| H4 | IF we use adaptive blend persona (coach↔consultant), THEN user satisfaction exceeds fixed personas | >4/5 satisfaction rating | User preference surveys across sessions | Wrong persona alienates |
| H5 | IF we use terminal-only ASCII UX for gamification, THEN engagement is sufficient | Session return rate >60% | User engagement metrics | Need GUI component |

### 5.2 Validation Priority

**Must Validate First:**
1. H1 (micro-tasks): Foundation for ADHD adaptation — if this fails, redesign required
2. H3 (milestones): Core plan structure depends on this

**Can Validate During Development:**
- H2 (coaching quality)
- H4 (persona blend)
- H5 (terminal UX)

---

## 6. Prioritized Opportunities

### 6.1 MoSCoW Classification

**Must Have (Critical — MVP):**
- User assessment engine (cognitive style, confidence, work patterns)
- Adaptive coaching with confidence building
- Business plan generation with milestone-based tracking
- Market research and competitive analysis
- Terminal-compatible progress visualization
- Micro-task chunking engine
- Dual-mode: standalone + project-anchored
- `/my-business` dashboard

**Should Have (Important — Post-MVP Early):**
- Marketing and go-to-market strategy
- Legal structure guidance
- Financial modeling and pricing strategy

**Could Have (Nice to Have — Post-MVP Later):**
- Operations and launch planning
- Team building and HR guidance
- Template library with professional disclaimers
- Gamification with streaks and achievements

**Won't Have (Out of Scope — This Initiative):**
- GUI/web interface
- Integration with external business tools (Stripe, QuickBooks)
- AI-generated legal documents (liability concern)
- Actual business formation filing

### 6.2 Impact-Effort Matrix

```
                    HIGH EFFORT
                         |
    Major Projects       |       Avoid
    - Financial Model    |       - GUI Interface
    - Legal Templates    |       - External Tool Integration
                         |
HIGH IMPACT -------------|------------- LOW IMPACT
                         |
    Quick Wins           |       Fill-ins
    - Assessment Engine  |       - Template Library
    - Coaching Sessions  |       - HR Guidance
    - Business Plan      |
    - Progress Viz       |
                    LOW EFFORT
```

**Quick Wins:** Assessment engine, coaching sessions, business plan, progress visualization
**Major Projects:** Financial modeling, legal templates (post-MVP)
**Fill-ins:** Template library, HR/team guidance
**Avoid:** GUI interface, external integrations

### 6.3 Recommended Sequence (Epic Order)

1. **EPIC-A:** Assessment & Coaching Core — Everything depends on knowing the user
2. **EPIC-B:** Business Planning & Viability — Core deliverable users expect
3. **EPIC-C:** Market Research & Competition — Validates the business idea
4. **EPIC-D:** Marketing & Customer Acquisition — How to reach customers
5. **EPIC-E:** Legal & Compliance — Business structure and IP protection
6. **EPIC-F:** Financial Planning & Modeling — Revenue projections and pricing
7. **EPIC-G:** Operations & Launch — How to actually launch
8. **EPIC-H:** Team Building & HR — Scaling the business
9. **EPIC-R:** Revisitation — Re-evaluate and integrate after each epic

---

## 7. Handoff to Ideation

### 7.1 Summary for /ideate

This brainstorm session has produced the following inputs for ideation:

**Problem to Solve:**
> Developers and aspiring entrepreneurs build projects but never turn them into businesses due to intertwined barriers: lack of business knowledge, lack of confidence, and executive dysfunction (ADHD/neurodivergent challenges).

**Primary Users:**
- Solo developer: Has a project, wants to turn it into a business
- Aspiring entrepreneur: Has a business idea, needs structure and validation

**Success Looks Like:**
> An AI-powered business coaching framework that adapts to each user's cognitive style, builds confidence, and guides them from project/idea to viable business through milestone-based plans.

**Key Constraints:**
- Claude Code Terminal only (no GUI)
- Markdown-only skills with progressive disclosure
- Development in `src/` tree, tests in `tests/`
- Must read 6 context files before processing

**Must-Have Capabilities:**
- User assessment engine
- Adaptive coaching with confidence building
- Business plan generation with milestones
- Market research integration
- Terminal progress visualization
- Micro-task chunking
- Dual-mode: standalone + project-anchored

### 7.2 Recommended Next Steps

1. **Review this document** - Verify accuracy of all captured decisions
2. **Run /ideate** - Transform into formal requirements
   - This brainstorm will be auto-detected
   - Core inputs will be pre-populated
3. **After ideation** - Run `/create-epic` for EPIC-A first

### 7.3 Open Questions for Ideation

| Question | Context | Who Can Answer |
|----------|---------|----------------|
| What specific ADHD research to encode? | References need evidence-based patterns | Research phase |
| How to persist user profile across sessions? | YAML file in devforgeai/specs/business/ | Architecture decision |
| Should coaching sessions have a max frequency? | Prevent dependency on AI coaching | User research |

---

## Appendix A: Session Metadata

- **Brainstorm ID:** BRAINSTORM-011
- **Created:** 2026-02-21
- **Duration:** ~45 minutes
- **Questions Asked:** 10
- **Phases Completed:** 7/7
- **Facilitator:** DevForgeAI
- **Confidence Level:** High

---

## Appendix B: Raw Session Data

<details>
<summary>Click to expand raw session responses</summary>

### Phase 1 Responses (Stakeholder Discovery)
- **Primary user:** Both solo developers AND aspiring entrepreneurs equally
- **Key barrier:** All barriers equally (overwhelm + self-doubt + ADHD) — intertwined
- **AI persona:** Adaptive blend — shifts between coach and consultant dynamically
- **Assessment approach:** Combination (self-report + guided questions) — NEVER diagnoses

### Phase 2 Responses (Problem Exploration)
- **Ideal flow:** Both plan generation + ongoing coaching (not one-shot)
- **Independence:** Both standalone (no code project) + project-anchored modes
- **MVP scope:** Full MBA suite — all domains designed upfront, delivered via iterative agile epics
- **Epic revisitation:** After each epic completes, re-brainstorm to integrate with what exists

### Phase 3 Responses (Opportunity Mapping)
- **Plan duration:** Milestone-based with soft time targets (7-180 day range)
- **Legal/templates:** Tiered — guidance only (MVP) → templates with disclaimers (post-MVP)
- **ADHD UX:** All three combined (chunk sizing + pacing + visual progress) — terminal-compatible

### Phase 4-6 Responses
- Captured in design decisions and hypothesis sections above

</details>

---

## Appendix C: Skill Architecture Detail

### Skills (9 total)

| Skill | Dev Path | Purpose |
|-------|----------|---------|
| assessing-entrepreneur | `src/claude/skills/assessing-entrepreneur/` | User assessment & adaptive profile |
| coaching-entrepreneur | `src/claude/skills/coaching-entrepreneur/` | Confidence building & ongoing coaching |
| planning-business | `src/claude/skills/planning-business/` | Business plan & strategy |
| researching-market | `src/claude/skills/researching-market/` | Market research & competitive analysis |
| marketing-business | `src/claude/skills/marketing-business/` | Marketing & customer acquisition |
| advising-legal | `src/claude/skills/advising-legal/` | Legal & compliance guidance |
| managing-finances | `src/claude/skills/managing-finances/` | Financial planning & modeling |
| operating-business | `src/claude/skills/operating-business/` | Operations & launch |
| building-team | `src/claude/skills/building-team/` | HR & team building |

### Commands (10 total)

| Command | Dev Path | Invokes |
|---------|----------|---------|
| `/assess-me` | `src/claude/commands/assess-me.md` | assessing-entrepreneur |
| `/coach-me` | `src/claude/commands/coach-me.md` | coaching-entrepreneur |
| `/business-plan` | `src/claude/commands/business-plan.md` | planning-business |
| `/market-research` | `src/claude/commands/market-research.md` | researching-market |
| `/marketing-plan` | `src/claude/commands/marketing-plan.md` | marketing-business |
| `/legal-check` | `src/claude/commands/legal-check.md` | advising-legal |
| `/financial-model` | `src/claude/commands/financial-model.md` | managing-finances |
| `/ops-plan` | `src/claude/commands/ops-plan.md` | operating-business |
| `/build-team` | `src/claude/commands/build-team.md` | building-team |
| `/my-business` | `src/claude/commands/my-business.md` | orchestrator (reads all business artifacts) |

### Subagents (4 new)

| Agent | Dev Path | Tools |
|-------|----------|-------|
| business-coach | `src/claude/agents/business-coach.md` | Read, Grep, Glob, AskUserQuestion |
| market-analyst | `src/claude/agents/market-analyst.md` | Read, Grep, Glob, WebSearch, WebFetch |
| financial-modeler | `src/claude/agents/financial-modeler.md` | Read, Write, Glob, Grep |
| entrepreneur-assessor | `src/claude/agents/entrepreneur-assessor.md` | Read, Glob, Grep, AskUserQuestion |

### Artifact Storage

```
devforgeai/specs/business/
├── user-profile.yaml
├── business-plan/
├── market-research/
├── financial/
├── legal/
├── marketing/
├── operations/
└── coaching/
```

---

## Appendix D: Epic Dependency Chain

```
EPIC-A (Assessment & Coaching) ─── MVP Phase 1
  │
  ├──→ EPIC-B (Business Planning) ─── MVP Phase 2
  │      │
  │      ├──→ EPIC-C (Market Research) ─── MVP Phase 3
  │      │      │
  │      │      └──→ EPIC-D (Marketing) ─── Post-MVP Phase 1
  │      │             │
  │      │             └──→ EPIC-F (Financial) ─── Post-MVP Phase 3
  │      │
  │      └──→ EPIC-E (Legal) ─── Post-MVP Phase 2
  │             │
  │             └──→ EPIC-G (Operations) ─── Post-MVP Phase 4
  │                    │
  │                    └──→ EPIC-H (Team Building) ─── Post-MVP Phase 5
  │
  └──→ EPIC-R (Revisitation) ─── After each epic completes
```

---

## Key Files for Context

| File | Purpose |
|------|---------|
| `/home/bryan/.claude/plans/jiggly-launching-backus.md` | Full plan with progress checkpoints |
| `devforgeai/specs/context/tech-stack.md` | Technology constraints |
| `devforgeai/specs/context/architecture-constraints.md` | Architectural rules |
| `devforgeai/specs/context/source-tree.md` | Directory structure (dual-path) |
| `devforgeai/specs/context/anti-patterns.md` | Forbidden patterns |
| `devforgeai/specs/context/coding-standards.md` | Code style standards |
| `devforgeai/specs/context/dependencies.md` | Package dependencies |
| `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/` | Anthropic prompt engineering |
| `.claude/skills/claude-code-terminal-expert/references/skills/` | Anthropic skill design |

## Glossary

- **Skill**: A capability module in `.claude/skills/` — Markdown that expands inline when invoked
- **Subagent**: A specialized AI worker in `.claude/agents/` — executes via `Task()` tool
- **Slash command**: A user command (e.g., `/dev`) in `.claude/commands/` that invokes skills
- **Context file**: One of 6 constraint files in `devforgeai/specs/context/`
- **TDD**: Test-Driven Development — Red → Green → Refactor cycle
- **Epic**: A large feature broken into multiple user stories
- **Milestone**: A completion checkpoint (not calendar-based) in the adaptive business plan
- **Lean Canvas**: A 1-page business model template (9 blocks)
- **TAM/SAM/SOM**: Total/Serviceable/Obtainable Addressable Market
- **Progressive disclosure**: Loading detailed docs on-demand from `references/` subdirectory
- **Dual-path architecture**: Dev in `src/`, operational in `.claude/`, copy after QA
