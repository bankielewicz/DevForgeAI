---
id: EPIC-060
title: "Prompt Engineering Research & Knowledge Capture"
status: Planning
start_date: TBD
target_date: TBD
total_points: 35
created: 2026-02-04
updated: 2026-02-04
source_brainstorm: BRAINSTORM-010
source_requirements: devforgeai/specs/requirements/prompt-engineering-improvement-requirements.md
---

# Epic: Prompt Engineering Research & Knowledge Capture

## Business Goal

Mine all 12 Anthropic repos for prompt engineering patterns and produce a structured research artifact with DevForgeAI applicability mapping, enabling evidence-based improvements across the entire framework. This is the foundational research phase that feeds EPIC-061 (Template Standardization) and EPIC-062 (Pilot & Rollout).

## Success Metrics

- **Metric 1:** All 12 Anthropic repos analyzed with extractable patterns cataloged (100% coverage)
- **Metric 2:** Pattern catalog contains 30+ actionable patterns mapped to DevForgeAI components
- **Metric 3:** Research artifact accessible in fresh sessions without re-reading source repos
- **Metric 4:** Each pattern has DevForgeAI applicability rating (High/Medium/Low/N/A)

## Scope

### Overview

Systematically extract prompt engineering best practices from Anthropic's 12 official repos (courses, tutorials, cookbooks, quickstarts, dev tools, domain-specific resources) and produce a structured, persistent research artifact that catalogs patterns with DevForgeAI applicability mapping. This is research-only — no changes to existing agents, skills, or commands.

### Features

1. **Core Course Mining**
   - Description: Mine 5 Anthropic courses (API fundamentals, prompt engineering, real-world prompting, evaluations, tool use) for foundational methodology patterns
   - User Value: Establishes core prompt engineering methodology from authoritative source material
   - Estimated Points: 8 story points

2. **Tutorial Pattern Extraction**
   - Description: Extract patterns from 9-chapter interactive prompt engineering tutorial (structure, clarity, roles, data separation, formatting, CoT, few-shot, hallucination avoidance, complex prompts)
   - User Value: Direct pattern extraction applicable to agent/skill prompts — most granular source
   - Estimated Points: 5 story points

3. **Cookbook & Quickstart Analysis**
   - Description: Analyze claude-cookbooks and claude-quickstarts for implementation patterns (customer support, computer use, financial data analyst)
   - User Value: Real-world implementation examples showing patterns in context
   - Estimated Points: 5 story points

4. **Dev Tools & Domain Pattern Mining**
   - Description: Mine claude-code-action, claude-code-security-review, claude-plugins-official, claude-constitution, healthcare, life-sciences, beam, original_performance_takehome for specialized patterns
   - User Value: Domain-specific patterns for specialized agents (security-auditor, deployment-engineer, etc.)
   - Estimated Points: 8 story points

5. **Research Artifact Creation**
   - Description: Create structured Markdown document in `devforgeai/specs/research/` with pattern catalog, applicability mapping, and DevForgeAI recommendations
   - User Value: Persistent knowledge document that survives across sessions and enables EPIC-061 template design
   - Estimated Points: 5 story points

6. **New Capability Identification**
   - Description: Identify new agents, skills, or capabilities enabled by Anthropic patterns that don't exist in DevForgeAI today
   - User Value: Framework growth opportunities beyond improving existing components
   - Estimated Points: 4 story points

### Out of Scope

- Applying patterns to existing agents (EPIC-062)
- Creating unified templates (EPIC-061)
- Building evaluation pipeline (EPIC-062)
- Automated prompt optimization (Won't Have per BRAINSTORM-010)
- External tool integration
- Changes to context files or ADRs

## Target Sprints

**Estimated Duration:** 3 sprints / 6 weeks

**Sprint Breakdown:**
- **Sprint 1:** F1: Core Course Mining + F2: Tutorial Pattern Extraction — 13 story points
  - Goal: Extract foundational methodology from 5 courses + 9 tutorial chapters
- **Sprint 2:** F3: Cookbook & Quickstart Analysis + F4: Dev Tools & Domain Mining + F5: Research Artifact Creation — 15 story points (sprint overlap with F5 continuing)
  - Goal: Mine remaining repos, begin assembling final research artifact
- **Sprint 3:** F5: Research Artifact Finalization + F6: New Capability Identification — 7 story points
  - Goal: Finalize artifact, identify new capabilities, validate artifact quality

## Dependencies

### External Dependencies

- **Dependency 1:** 12 Anthropic repos cloned in `tmp/anthropic/` (COMPLETE)

### Internal Dependencies

- **Dependency 1:** BRAINSTORM-010 complete (COMPLETE — provides problem statement, stakeholder analysis, hypotheses)

### Blocking Issues

- None identified. All prerequisites are met.

## Stakeholders

- **Product Owner:** Framework Owner — Directs research, approves patterns, validates applicability mapping
- **Orchestrator:** Opus — Executes research workflows, delegates to internet-sleuth subagent
- **Beneficiaries:** All DevForgeAI users (improved agent/skill/command quality downstream)

## Requirements

### Functional Requirements

#### User Stories

**User Story 1:**
```
As a Framework Owner,
I want all 5 Anthropic courses mined for prompt engineering patterns,
So that I have a comprehensive methodology foundation.
```

**Acceptance Criteria:**
- [ ] All 5 courses analyzed (API fundamentals, prompt eng, real-world, evaluations, tool use)
- [ ] Patterns extracted with DevForgeAI applicability rating
- [ ] Findings documented in structured format

**User Story 2:**
```
As a Framework Owner,
I want patterns from the 9-chapter tutorial extracted with DevForgeAI applicability mapping,
So that I know which patterns apply to which components.
```

**Acceptance Criteria:**
- [ ] All 9 chapters analyzed
- [ ] Each pattern mapped to applicable DevForgeAI component type (agent/skill/command)
- [ ] Examples provided for each high-applicability pattern

**User Story 3:**
```
As a Framework Owner,
I want implementation patterns from cookbooks and quickstarts analyzed,
So that I have real-world examples to follow.
```

**Acceptance Criteria:**
- [ ] claude-cookbooks analyzed for integration patterns
- [ ] claude-quickstarts analyzed for domain-specific prompt patterns
- [ ] Implementation patterns documented with code examples

**User Story 4:**
```
As a Framework Owner,
I want specialized patterns from dev tools and domain repos captured,
So that I can improve domain-specific agents.
```

**Acceptance Criteria:**
- [ ] All 8 remaining repos analyzed
- [ ] Domain-specific patterns mapped to relevant DevForgeAI agents
- [ ] Priority ratings assigned per pattern

**User Story 5:**
```
As a Framework Owner,
I want a structured research artifact persisted in devforgeai/specs/,
So that knowledge survives across sessions.
```

**Acceptance Criteria:**
- [ ] Research artifact created at `devforgeai/specs/research/prompt-engineering-patterns.md`
- [ ] Document contains pattern catalog with 30+ patterns
- [ ] Each pattern has: name, source, description, applicability rating, DevForgeAI recommendation
- [ ] Document is <2000 lines for readability

**User Story 6:**
```
As a Framework Owner,
I want new capabilities enabled by Anthropic patterns identified,
So that the framework can grow.
```

**Acceptance Criteria:**
- [ ] New capability opportunities documented
- [ ] Each opportunity assessed for feasibility and priority
- [ ] Recommendations aligned with existing architecture constraints

### Non-Functional Requirements (NFRs)

#### Performance
- Research artifact must load in single Read() call or progressive sections
- No impact to existing command response times

#### Stability
- Zero changes to existing agents, skills, or commands during this epic
- Research-only — no runtime impact

### Data Requirements

#### Entities

**Entity: Research Artifact**
- **Location:** `devforgeai/specs/research/prompt-engineering-patterns.md`
- **Attributes:** Pattern catalog, applicability mapping, DevForgeAI recommendations, source references
- **Relationships:** Referenced by EPIC-061 templates, feeds EPIC-062 pilot improvements
- **Constraint:** <2000 lines for readability

### Integration Requirements

#### External Systems
- None required (all work within Claude Code Terminal)

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate**
- **Score:** 31/60 points (from requirements specification complexity assessment)
- **Rationale:** Research-intensive but technically simple — all Markdown file operations within Claude Code Terminal

### Recommended Architecture Pattern
No new architecture — uses existing DevForgeAI framework patterns (Markdown documentation, progressive disclosure)

### Technology Constraints
- All output as Markdown files (per tech-stack.md)
- No new dependencies required
- Must work within Claude Code Terminal capabilities
- Research artifact stored in `devforgeai/specs/research/` (per source-tree.md)

## Risks & Constraints

### Technical Risks

**Risk 1: Research Too Verbose**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Structured hierarchy with executive summary; enforce <2000 line limit; use progressive disclosure

**Risk 2: Patterns Incompatible with CCT**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Filter by applicability during extraction; skip inapplicable patterns; document N/A rating

### Business Risks

**Risk 1: Scope Creep Across 12 Repos**
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Strict sprint planning; P0/P1/P2 priority ordering; time-box each repo analysis

### Constraints

**Constraint 1: 15K Character Budget**
- **Impact:** Research output must be efficient, not verbose
- **Mitigation:** Structured format with pattern catalog table; details in sub-sections

**Constraint 2: Immutable Context Files**
- **Impact:** Any proposed changes to context files require ADR process
- **Mitigation:** Document proposed changes as recommendations, not direct edits

## Assumptions

1. **A1:** Anthropic's prompt engineering patterns are applicable to DevForgeAI's agent/skill/command structure (validated by pilot in EPIC-062)
2. **A4:** 12 repos contain sufficient patterns for comprehensive methodology (HIGH confidence from brainstorm analysis)

## Source Material

**Complete Repo List (12 repos in `tmp/anthropic/`):**

| # | Repo Directory | Key Content | Priority |
|---|----------------|-------------|----------|
| 1 | `courses/` | 5 courses: API fundamentals, prompt eng, real-world prompting, evaluations, tool use | P0 |
| 2 | `prompt-eng-interactive-tutorial/` | 9 chapters: structure, clarity, roles, data separation, formatting, CoT, few-shot, hallucination avoidance, complex prompts | P0 |
| 3 | `claude-cookbooks/` | Code examples and integration guides | P0 |
| 4 | `claude-quickstarts/` | Customer support, computer use, financial data analyst quickstarts | P0 |
| 5 | `claude-code-action/` | GitHub Action for Claude Code | P1 |
| 6 | `claude-code-security-review/` | Security review prompts | P1 |
| 7 | `claude-plugins-official/` | Plugin directory and patterns | P1 |
| 8 | `claude-constitution/` | Claude's values document | P1 |
| 9 | `healthcare/` | Clinical trials, prior auth, FHIR API | P2 |
| 10 | `life-sciences/` | PubMed, BioRender, research tools | P2 |
| 11 | `original_performance_takehome/` | Performance benchmarks | P2 |
| 12 | `beam/` | Apache-licensed project | P2 |

## Next Steps

### Immediate Actions
1. **Sprint Planning:** Run `/create-sprint` to create Sprint 1 plan for EPIC-060
2. **Story Creation:** Run `/create-story` to decompose F1 and F2 into implementable stories
3. **Research Execution:** Begin mining Anthropic repos per sprint plan

### Pre-Development Checklist
- [x] Brainstorm complete (BRAINSTORM-010)
- [x] Requirements specification complete
- [x] 12 Anthropic repos available in `tmp/anthropic/`
- [ ] Sprint 1 stories created
- [ ] Sprint plan approved

## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-380 | Feature 1 | Mine Core Anthropic Courses for Prompt Engineering Patterns | 8 | Backlog |
| STORY-381 | Feature 2 | Extract Prompt Engineering Patterns from Interactive Tutorial | 5 | Backlog |
| STORY-382 | Feature 3 | Analyze Cookbook and Quickstart Repos for Implementation Patterns | 5 | Backlog |
| STORY-383 | Feature 4 | Mine Dev Tools and Domain Repos for Specialized Patterns | 8 | Backlog |
| STORY-384 | Feature 5 | Create Prompt Engineering Research Artifact with Pattern Catalog | 5 | Backlog |
| STORY-385 | Feature 6 | Identify New Capabilities Enabled by Anthropic Prompt Engineering Patterns | 4 | Backlog |

## Notes

- Brainstorm BRAINSTORM-010 references "13 repos" but 12 directories exist on disk. Use the 12-repo list above as source of truth.
- This epic is research-only. No changes to existing framework components.
- Research artifact feeds EPIC-061 (template design) and EPIC-062 (pilot improvements).

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2026-02-04
