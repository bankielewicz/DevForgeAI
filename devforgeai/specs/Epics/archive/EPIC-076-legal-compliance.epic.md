---
id: EPIC-076
title: Legal & Compliance (Business Skills Post-MVP Phase 2)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 8
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Legal & Compliance (Business Skills Post-MVP Phase 2)

## Business Goal

Guide DevForgeAI users through fundamental legal decisions for their business — choosing a business structure, protecting intellectual property, and knowing when to engage professional legal counsel. New entrepreneurs often delay legal foundations out of confusion or fear, which creates risk. This epic provides structured, educational guidance that demystifies legal basics while always directing users to professionals for binding decisions.

**Critical safety constraint:** This epic provides educational guidance ONLY. All outputs include prominent disclaimers that the AI is not a lawyer and cannot provide legal advice. Professional referral triggers are built into every workflow.

## Success Metrics

- **Metric 1:** Business structure decision tree produces a recommended structure with rationale based on user inputs
- **Metric 2:** IP protection checklist covers copyright, trademark, patent basics, and trade secrets for software projects
- **Metric 3:** Every legal output file contains a "consult a professional" disclaimer header
- **Metric 4:** All skills < 1,000 lines; all commands < 500 lines

**Measurement Plan:**
- Structural validation tests in `tests/` verify file sizes, required sections, disclaimer presence
- Manual QA via `/legal-check` workflow
- Review frequency: After each story completion

## Scope

### In Scope

1. **Feature 1: Business Structure Decision Tree** (3 pts) — Priority: P1
   - Create decision tree in `advising-legal` skill covering LLC, S-Corp, Sole Proprietorship, C-Corp
   - Decision factors: revenue expectations, number of partners, liability exposure, tax preferences
   - Clear "consult a professional" triggers for complex situations (multi-state, international, partners)
   - Output to `devforgeai/specs/business/legal/business-structure.md`
   - Maps to: FR-017

2. **Feature 2: IP Protection Checklist for Software Projects** (2 pts) — Priority: P1
   - Add IP protection workflow to `advising-legal` skill
   - Covers: copyright (automatic), trademark (brand names), patent basics, trade secrets (code/algorithms)
   - Specific to software/SaaS projects with links to professional resources
   - Output to `devforgeai/specs/business/legal/ip-protection.md`
   - Maps to: FR-018

3. **Feature 3: /legal-check Command & Skill Assembly** (2 pts) — Priority: P1
   - Create `/legal-check` command invoking `advising-legal` skill
   - Assemble full `advising-legal` skill with progressive disclosure references
   - Integrate with user profile for adaptive pacing
   - Support both standalone and project-anchored modes

4. **Feature 4: "When to Hire a Professional" Framework** (1 pt) — Priority: P2
   - Decision framework identifying situations requiring professional legal counsel
   - Complexity indicators that trigger referral recommendations
   - Reference file with guidance on finding and working with business attorneys

### Out of Scope

- AI-generated legal documents (liability concern — explicit Won't Have from BRAINSTORM-011)
- Actual business formation filing
- Tax advice or tax preparation
- Contract drafting or review
- Industry-specific regulatory compliance (beyond general guidance)
- International law guidance
- Template library with legal templates (deferred to post-MVP per brainstorm decision #9)

## Target Sprints

### Sprint 1: Legal Foundations
**Goal:** Deliver business structure guidance, IP checklist, and `/legal-check` command
**Estimated Points:** 7
**Features:**
- Feature 1: Business Structure Decision Tree (STORY-A, STORY-B)
- Feature 2: IP Protection Checklist (STORY-C)
- Feature 3: /legal-check Command & Skill Assembly (STORY-D)

**Key Deliverables:**
- `src/claude/skills/advising-legal/SKILL.md` + references/
- `src/claude/commands/legal-check.md`

### Sprint 2: Professional Referral
**Goal:** Deliver "when to hire" framework
**Estimated Points:** 1
**Features:**
- Feature 4: "When to Hire a Professional" Framework (STORY-E)

**Key Deliverables:**
- `src/claude/skills/advising-legal/references/when-to-hire-professional.md`

## User Stories

1. **As a** new entrepreneur, **I want** guidance on business structure **so that** I make an informed legal decision
2. **As a** developer-entrepreneur, **I want** to understand how to protect my software IP **so that** my business asset is secure
3. **As a** user, **I want** one command (`/legal-check`) **so that** I can run the legal guidance workflow
4. **As a** user facing a complex legal situation, **I want** clear signals to consult a professional **so that** I don't make costly mistakes

## Technical Considerations

### Architecture Impact
- **1 new skill** in `src/claude/skills/` (advising-legal)
- **1 new command** in `src/claude/commands/` (legal-check)
- **No new subagents** — leverages existing `business-coach` for adaptive guidance
- **Progressive disclosure:** Skill requires `references/` directory

### Technology Decisions
- **Data format:** Markdown for legal guidance outputs
- **Skill naming:** Gerund-object convention per ADR-017 (advising-legal)
- **Profile integration:** Reads user profile from EPIC-072 for adaptive pacing (read-only)
- **Disclaimer enforcement:** Every output file auto-includes disclaimer header

### Constraints (From Context Files)
- Skills: Markdown only, < 1,000 lines, progressive disclosure required
- Commands: < 500 lines, thin invokers delegating to skills
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All skills must read 6 context files before processing

### Safety Requirements (CRITICAL)
- **NFR-S002:** All legal guidance includes "consult a professional" disclaimer
- Never implies AI can replace licensed attorneys
- Decision tree outputs are educational, not prescriptive
- Professional referral triggers at every complexity threshold
- No jurisdiction-specific advice (general US guidance with "verify in your state" warnings)

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete

- [ ] **EPIC-073 (Business Planning & Viability)** — Business structure context
  - **Status:** Planning
  - **Impact if delayed:** Legal skill works standalone; lacks business model context for tailored recommendations

- [ ] **EPIC-072 (Assessment & Coaching Core)** — User profile for adaptive pacing
  - **Status:** Planning
  - **Impact if delayed:** Works without adaptation; uses default settings

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** EPIC-073 (needs business plan context for tailored structure advice)
- **This epic blocks:** EPIC-G (Operations & Launch — needs legal foundation)

## Risks & Mitigation

### Risk 1: Users treat AI legal guidance as legal advice
- **Probability:** High
- **Impact:** Critical — liability and user harm
- **Mitigation:** Prominent disclaimers on every output; "consult a professional" triggers at every decision point; never use prescriptive language ("you should" → "consider")
- **Contingency:** Add per-session disclaimer acknowledgment if user feedback indicates confusion

### Risk 2: Legal guidance becomes jurisdiction-specific
- **Probability:** Medium
- **Impact:** High — incorrect advice for user's jurisdiction
- **Mitigation:** Scope to general US guidance only; always include "verify requirements in your state/country"
- **Contingency:** Add jurisdiction detection question at skill entry; restrict to "general educational guidance"

### Risk 3: Scope creep into contract/document generation
- **Probability:** Medium
- **Impact:** Medium — delays and liability
- **Mitigation:** Explicit out-of-scope; BRAINSTORM-011 decision #9 defers templates to post-MVP
- **Contingency:** Redirect users to professional resources for document needs

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (constraint enforcement)

### Target Users
- Solo developers needing business structure guidance
- Aspiring entrepreneurs wanting IP protection basics

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| `advising-legal/SKILL.md` | Skill | `src/claude/skills/advising-legal/` | F1, F2, F4 |
| `advising-legal/references/` | References | `src/claude/skills/advising-legal/references/` | F1, F2, F4 |
| `legal-check.md` | Command | `src/claude/commands/legal-check.md` | F3 |

**Total: 3 framework deliverables** (1 skill + 1 command + 1 reference directory)

### Reference Files (Progressive Disclosure)

| Reference File | Purpose | Feature |
|----------------|---------|---------|
| `business-structure-guide.md` | LLC vs S-Corp vs Sole Prop decision tree | F1 |
| `ip-protection-checklist.md` | Copyright, trademark, patent, trade secret guidance | F2 |
| `compliance-requirements-by-industry.md` | General compliance awareness by industry type | F1 |
| `when-to-hire-professional.md` | Professional referral triggers and guidance | F4 |

## Feature Dependency Chain

```
Feature 3 (/legal-check Command + Skill Assembly)
  ├── Feature 1 (Business Structure Decision Tree)
  │     └── Feature 4 (When to Hire Professional)
  └── Feature 2 (IP Protection Checklist)
        └── Feature 4 (When to Hire Professional)
```

## Complexity Assessment

**Score: 4.0 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 3/10 | 3 deliverables (simplest epic so far) |
| State management | 3/10 | Reads profile; writes legal artifacts; no complex state |
| Scope clarity | 8/10 | Very well-defined: structure + IP + referrals |
| Framework integration | 4/10 | Standard skill/command pattern |
| Testing strategy | 5/10 | Markdown structural tests + disclaimer presence validation |
| Safety sensitivity | 7/10 | High — disclaimer enforcement is critical |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Legal Foundations (7 pts)
Sprint 2: Professional Referral (1 pt)
================================
Total Duration: 1-2 sprints
Total Points: 8
Stories: 5
```

### Key Milestones
- [ ] **Sprint 1 Complete:** `/legal-check` generates structure recommendation and IP checklist
- [ ] **Sprint 2 Complete:** Professional referral framework available
- [ ] **Epic Complete:** Full legal guidance workflow functional with disclaimers on every output

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 7 | 4 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 1 | 1 | 0 | 0 | 0 |
| **Total** | **0%** | **8** | **5** | **0** | **0** | **0** |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
