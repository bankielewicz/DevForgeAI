# Prompt Engineering Improvement from Anthropic Repos - Requirements Specification

**Version:** 1.0
**Date:** 2026-02-04
**Status:** Draft
**Author:** DevForgeAI Ideation
**Complexity Score:** 31/60 (Tier 2: Moderate)
**Brainstorm Ref:** BRAINSTORM-010

---

## 1. Project Overview

### 1.1 Project Context
**Type:** Brownfield (existing framework improvement)
**Domain:** AI Framework / Developer Tooling
**Timeline:** Flexible (~22 weeks across 3 epics)
**Team:** 1 developer (Framework Owner + Claude/Opus orchestration)

### 1.2 Problem Statement
DevForgeAI framework stakeholders experience **inconsistent and unreliable results from subagents and skills** because prompts were written ad-hoc without a systematic methodology based on proven prompt engineering principles, resulting in **QA fix cycles, wasted time on off-target outputs, and inconsistent quality across agents**.

### 1.3 Solution Overview
Systematically extract prompt engineering best practices from Anthropic's 13 official repos and apply them to DevForgeAI's 32+ subagents, 17 skills, and 39 commands through a structured research → template → pilot → evaluate → rollout pipeline.

### 1.4 Success Criteria
- All 13 Anthropic repos mined with 30+ actionable patterns cataloged
- Unified templates created for agents, skills, and commands
- 3 pilot agents improved with measurable quality increase
- All 88+ components migrated without regressions
- Zero breaking changes to existing command interface

---

## 2. User Roles & Personas

### 2.1 Primary Users

| Role | Count | Interaction |
|------|-------|-------------|
| Framework Owner | 1 | Directs research, approves templates, validates results |
| Opus (Orchestrator) | 1 | Executes workflows, delegates to subagents |

### 2.2 User Personas

**Persona 1: Framework Owner**
- **Role:** Product owner and primary developer of DevForgeAI
- **Goals:** Improve prompt quality across all agents/skills; capture reusable patterns; build new capabilities; reduce QA fix cycles
- **Needs:** Research-backed methodology, measurable improvement, scalable templates
- **Pain Points:** QA rework, inconsistent agent outputs, no systematic methodology

**Persona 2: Opus (Orchestrating Agent)**
- **Role:** Claude Code orchestrator that delegates to subagents
- **Goals:** Better delegation patterns, improved context preservation, reduced hallucination
- **Needs:** Clear agent system prompts, consistent subagent behavior, reliable tool use patterns
- **Pain Points:** Inconsistent subagent responses, drift in skill phase execution

**Persona 3: End Users (Slash Command Users)**
- **Role:** Developers using DevForgeAI slash commands
- **Goals:** Reliable, high-quality output from every command
- **Needs:** Commands that work consistently, intuitive question patterns
- **Pain Points:** Inconsistent quality, need to re-run commands for acceptable output

---

## 3. Functional Requirements

### 3.1 User Stories

#### Research & Knowledge Capture (EPIC-060)
1. As a Framework Owner, I want all 5 Anthropic courses mined for prompt engineering patterns, so that I have a comprehensive methodology foundation
2. As a Framework Owner, I want patterns from the 9-chapter tutorial extracted with DevForgeAI applicability mapping, so that I know which patterns apply to which components
3. As a Framework Owner, I want implementation patterns from cookbooks and quickstarts analyzed, so that I have real-world examples to follow
4. As a Framework Owner, I want specialized patterns from dev tools and domain repos captured, so that I can improve domain-specific agents
5. As a Framework Owner, I want a structured research artifact persisted in devforgeai/specs/, so that knowledge survives across sessions
6. As a Framework Owner, I want new capabilities enabled by Anthropic patterns identified, so that the framework can grow

#### Template Standardization (EPIC-061)
7. As a Framework Owner, I want a unified agent template with required/optional sections, so that all agents follow consistent prompt structure
8. As a Skill Developer, I want a skill SKILL.md template variant with phase instruction patterns, so that new skills are written with proven patterns
9. As a Framework Owner, I want a command template variant respecting 15K char budget, so that commands are efficient orchestrators
10. As Opus, I want agent-generator to enforce template compliance, so that non-compliant agents are blocked
11. As a Framework Owner, I want prompt versioning tracking before/after changes, so that I can rollback if quality decreases

#### Pilot, Evaluation & Rollout (EPIC-062)
12. As a Framework Owner, I want test-automator improved with unified template, so that TDD test generation improves
13. As a Framework Owner, I want ac-compliance-verifier improved with unified template, so that AC verification is more reliable
14. As a Framework Owner, I want requirements-analyst improved with unified template, so that story requirements are more complete
15. As a Framework Owner, I want a before/after evaluation pipeline, so that I can objectively measure improvements
16. As a Framework Owner, I want phased rollout in batches of 5-8, so that migration is manageable and regressions catchable
17. As an End User, I want zero breaking changes, so that existing commands continue to work reliably

### 3.2 Feature Requirements

| Epic | Feature | Priority | Effort |
|------|---------|----------|--------|
| EPIC-060 | Core Course Mining (5 courses) | P0 | Large |
| EPIC-060 | Tutorial Pattern Extraction (9 chapters) | P0 | Medium |
| EPIC-060 | Cookbook & Quickstart Analysis | P0 | Medium |
| EPIC-060 | Dev Tools & Domain Pattern Mining | P0 | Large |
| EPIC-060 | Research Artifact Creation | P0 | Medium |
| EPIC-060 | New Capability Identification | P1 | Small |
| EPIC-061 | Agent Template Design | P0 | Medium |
| EPIC-061 | Skill Template Design | P0 | Medium |
| EPIC-061 | Command Template Design | P0 | Small |
| EPIC-061 | Agent-Generator Enforcement | P0 | Medium |
| EPIC-061 | Prompt Versioning System | P1 | Medium |
| EPIC-062 | Pilot: test-automator | P0 | Medium |
| EPIC-062 | Pilot: ac-compliance-verifier | P0 | Medium |
| EPIC-062 | Pilot: requirements-analyst | P0 | Medium |
| EPIC-062 | Evaluation Pipeline | P0 | Large |
| EPIC-062 | Batch Rollout Wave 1 (validators) | P1 | Large |
| EPIC-062 | Batch Rollout Wave 2 (implementors) | P1 | Large |
| EPIC-062 | Batch Rollout Wave 3 (remaining + skills + commands) | P1 | Large |
| EPIC-062 | Quality Validation & Regression Check | P0 | Medium |

---

## 4. Data Requirements

### 4.1 Data Model

**Entity: Research Artifact**
- Purpose: Persistent knowledge document capturing prompt engineering patterns
- Location: `devforgeai/specs/research/prompt-engineering-patterns.md`
- Attributes: Pattern catalog, applicability mapping, DevForgeAI recommendations
- Relationships: Referenced by EPIC-061 templates

**Entity: Agent Template**
- Purpose: Canonical template defining required/optional sections for agents
- Location: `.claude/agents/` (template file) or `.claude/skills/devforgeai-orchestration/assets/templates/`
- Attributes: Required sections, optional sections, validation rules, category extensions
- Relationships: Enforced by agent-generator; applied to all 32+ agents

**Entity: Prompt Version Record**
- Purpose: Track before/after state of each agent/skill/command
- Location: Git history + optional version section in each file
- Attributes: Component ID, before hash, after hash, change date, change reason
- Relationships: One per migrated component

**Entity: Evaluation Result**
- Purpose: Quality score for before/after comparison
- Location: `devforgeai/specs/research/evaluation-results.md` or structured format
- Attributes: Component ID, before score, after score, rubric dimensions, pass/fail
- Relationships: One per evaluated component

### 4.2 Data Constraints
- All data stored as Markdown files (per tech-stack.md)
- No database required
- Version tracking via git history
- Research artifact must be <2000 lines for readability

---

## 5. Integration Requirements

### 5.1 Internal Integrations

| Integration | Direction | Purpose |
|-------------|-----------|---------|
| agent-generator ↔ template | Two-way | Validates new agents against template; generates from template |
| devforgeai-qa ↔ evaluation | One-way (QA reads) | QA validates agent compliance as part of story validation |
| Git ↔ prompt versioning | One-way (reads git) | Track before/after changes via git diff |

### 5.2 External Integrations
- None required (all work within Claude Code Terminal)

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Agent template processing must not increase response time noticeably
- Research artifact must load in single Read() call or progressive sections
- No impact to existing command response times

### 6.2 Security
- No security implications (all local file operations)
- Security-auditor agent migration must maintain OWASP Top 10 coverage
- No secrets or credentials involved

### 6.3 Scalability
- Template must scale to 32+ agents, 17 skills, 39 commands
- Research artifact must support 30+ patterns without becoming unnavigable
- Phased rollout in batches of 5-8 to manage scale

### 6.4 Stability (Critical NFR)
- **Zero breaking changes** to existing command interface
- All existing commands/skills must continue to work after migration
- Prompt versioning enables rollback within minutes if regression detected
- Phased rollout limits blast radius of any single migration batch

### 6.5 Budget
- **Token budget:** Agent prompts must fit within 15K char lean orchestration budget
- **Monetary budget:** Zero — all work within Claude Code Terminal
- **Time budget:** Flexible, no hard deadline

---

## 7. Complexity Assessment

**Total Score:** 31/60 (user-validated to Tier 2)

| Dimension | Score | Details |
|-----------|-------|---------|
| Functional | 14/20 | 3 user roles, 4 core entities, 1 integration, branching workflow |
| Technical | 8/20 | <10k records, single-user, no real-time |
| Team/Org | 3/10 | 1 developer, co-located |
| Non-Functional | 6/10 | 15K char budget constraint, no compliance |

**Architecture Tier:** Tier 2 (Moderate)
- Modular improvement batches
- Incremental rollout strategy
- Research-backed methodology

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: ✅ FEASIBLE
- All work is Markdown editing within Claude Code Terminal
- Three-layer architecture maintained
- No new dependencies or technologies
- Templates fit within existing patterns

### 8.2 Business Feasibility: ✅ FEASIBLE
- Zero external costs
- Flexible timeline (no hard deadline)
- Direct ROI: reduced QA rework cycles

### 8.3 Resource Feasibility: ✅ FEASIBLE
- 1 developer available (Framework Owner + Claude)
- No competing resource demands
- Skill gap (prompt engineering) is what this initiative addresses

### 8.4 Risk Register

| # | Risk | Category | Prob | Impact | Severity | Mitigation |
|---|------|----------|------|--------|----------|------------|
| R1 | Template too rigid | Technical | Med | High | HIGH | Category flexibility; pilot validation first |
| R2 | Token budget exceeded | Technical | Med | Med | MEDIUM | Measure during pilot; char limits per section |
| R3 | Regression after migration | Technical | Med | High | HIGH | Evaluation pipeline; versioning rollback; phased rollout |
| R4 | Patterns incompatible with CCT | Technical | Low | Med | MEDIUM | Filter by applicability; skip inapplicable |
| R5 | Scope creep (88+ files) | Business | High | Med | HIGH | Phased batches; strict sprint planning |
| R6 | Research too verbose | Technical | Med | Med | MEDIUM | Structured hierarchy; executive summary |

### 8.5 Overall Feasibility: ✅ FEASIBLE — Proceed

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints
- 15K character budget for command files (lean orchestration pattern)
- 6 immutable context files (changes require ADR process)
- Inline skill expansion model (no background processes)
- Must work within Claude Code Terminal capabilities
- Progressive disclosure: main SKILL.md <1000 lines

### 9.2 Business Constraints
- No breaking changes to existing interface
- All changes through standard DevForgeAI workflow (story/dev/QA)
- Incremental rollout required (no big-bang migration)
- No automated prompt optimization (human-reviewed only)

### 9.3 Assumptions (Require Validation)
- **A1:** Anthropic's prompt engineering patterns are applicable to DevForgeAI's agent/skill/command structure (validated by pilot in EPIC-062)
- **A2:** A single unified template can accommodate all agent categories with optional sections (validated during EPIC-061 template design)
- **A3:** Before/after evaluation within Claude Code Terminal produces meaningful quality signals (validated by evaluation pipeline in EPIC-062)
- **A4:** 13 repos contain sufficient patterns for comprehensive methodology (HIGH confidence from brainstorm analysis)

---

## 10. Epic Breakdown

### Epic Roadmap

```
EPIC-060 (Research)     ──→ EPIC-061 (Template)    ──→ EPIC-062 (Pilot & Rollout)
  Sprint 1-3 (6 wks)        Sprint 4-5 (6 wks)         Sprint 6-10 (10 wks)
  35 pts                     30 pts                      50 pts
```

### Epic Summaries

| Epic | Title | Points | Features | Sprints | Duration |
|------|-------|--------|----------|---------|----------|
| EPIC-060 | Research & Knowledge Capture | 35 | 6 | 3 | 6 weeks |
| EPIC-061 | Template Standardization & Enforcement | 30 | 5 | 2 | 6 weeks |
| EPIC-062 | Pilot, Evaluation & Rollout | 50 | 8 | 5 | 10 weeks |
| **Total** | | **115** | **19** | **10** | **~22 weeks** |

### Dependency Chain
- EPIC-060 must complete before EPIC-061 (research feeds template design)
- EPIC-061 must complete before EPIC-062 (templates needed for migration)
- Some overlap possible: EPIC-061 can start during EPIC-060 Sprint 3

---

### 10.1 Per-Epic Specifications

The following subsections provide the detail needed for `/create-epic` to generate compliant epic documents without ambiguity. Each subsection captures decisions made during the ideation session.

---

#### 10.1.1 EPIC-060: Prompt Engineering Research & Knowledge Capture

**Business Goal:**
Mine all 12 Anthropic repos for prompt engineering patterns and produce a structured research artifact with DevForgeAI applicability mapping, enabling evidence-based improvements across the entire framework.

**Success Metrics (EPIC-060 specific):**
- All 12 Anthropic repos analyzed with extractable patterns cataloged (100% coverage)
- Pattern catalog contains 30+ actionable patterns mapped to DevForgeAI components
- Research artifact accessible in fresh sessions without re-reading source repos
- Each pattern has DevForgeAI applicability rating (High/Medium/Low/N/A)

**Scope — In:**
1. Core Course Mining — Mine 5 Anthropic courses (API fundamentals, prompt engineering, real-world prompting, evaluations, tool use)
2. Tutorial Pattern Extraction — Extract patterns from 9-chapter interactive prompt engineering tutorial
3. Cookbook & Quickstart Analysis — Analyze claude-cookbooks and claude-quickstarts for implementation patterns
4. Dev Tools & Domain Pattern Mining — Mine claude-code-action, claude-code-security-review, claude-plugins-official, claude-constitution, healthcare, life-sciences, beam, original_performance_takehome
5. Research Artifact Creation — Create structured Markdown document in `devforgeai/specs/research/` with pattern catalog and applicability mapping
6. New Capability Identification — Identify new agents/skills/capabilities enabled by Anthropic patterns

**Scope — Out:**
- ❌ Applying patterns to agents (EPIC-062)
- ❌ Creating unified templates (EPIC-061)
- ❌ Building evaluation pipeline (EPIC-062)
- ❌ Automated prompt optimization (Won't Have per brainstorm)
- ❌ External tool integration

**Sprint-Level Feature Assignments:**

| Sprint | Features | Goal | Points |
|--------|----------|------|--------|
| Sprint 1 | F1: Core Course Mining, F2: Tutorial Pattern Extraction | Extract foundational methodology from 5 courses + 9 tutorial chapters | 13 |
| Sprint 2 | F3: Cookbook & Quickstart Analysis, F4: Dev Tools & Domain Mining, F5: Research Artifact Creation | Mine remaining repos, assemble final research artifact | 15 |
| Sprint 3 | F6: New Capability Identification | Identify new capabilities, validate artifact quality | 7 |

**Source Material — Complete Repo List (12 repos in `tmp/anthropic/`):**

| # | Repo Directory | Key Content | Priority |
|---|----------------|-------------|----------|
| 1 | `courses/` | 5 courses: API fundamentals, prompt eng, real-world prompting, evaluations, tool use | P0 — Core methodology |
| 2 | `prompt-eng-interactive-tutorial/` | 9 chapters: structure, clarity, roles, data separation, formatting, CoT, few-shot, hallucination avoidance, complex prompts | P0 — Direct pattern source |
| 3 | `claude-cookbooks/` | Code examples and integration guides | P0 — Implementation patterns |
| 4 | `claude-quickstarts/` | Customer support, computer use, financial data analyst quickstarts | P0 — Domain prompt patterns |
| 5 | `claude-code-action/` | GitHub Action for Claude Code | P1 — CI/CD patterns |
| 6 | `claude-code-security-review/` | Security review prompts | P1 — Security auditor improvement |
| 7 | `claude-plugins-official/` | Plugin directory and patterns | P1 — Plugin architecture |
| 8 | `claude-constitution/` | Claude's values document | P1 — Alignment/safety patterns |
| 9 | `healthcare/` | Clinical trials, prior auth, FHIR API | P2 — Domain skill patterns |
| 10 | `life-sciences/` | PubMed, BioRender, research tools | P2 — MCP integration patterns |
| 11 | `original_performance_takehome/` | Performance benchmarks | P2 — Evaluation methodology |
| 12 | `beam/` | Apache-licensed project | P2 — TBD |

**Note:** Brainstorm BRAINSTORM-010 references "13 repos" but 12 directories exist on disk. Use the 12-repo list above as source of truth.

**Dependencies:**
- [x] BRAINSTORM-010 complete (provides problem statement, stakeholder analysis, hypotheses)
- [x] 12 Anthropic repos cloned in `tmp/anthropic/`

---

#### 10.1.2 EPIC-061: Unified Template Standardization & Enforcement

**Business Goal:**
Create canonical templates for agents, skills, and commands based on EPIC-060 research patterns, with automated enforcement via the agent-generator subagent and prompt versioning for tracking changes and enabling rollback.

**Success Metrics (EPIC-061 specific):**
- Canonical agent template created with required/optional sections (validated against 3+ diverse existing agents)
- Skill SKILL.md and command template variants created and documented
- agent-generator enforces template compliance on all new/updated agents (0% non-compliant creation)
- Prompt versioning tracks before/after changes for all modified agents
- All templates fit within 15K char command budget constraint

**Scope — In:**
1. Agent Template Design — Canonical template with required sections (identity, purpose, tools, output format, constraints, examples) and optional sections per category (validator, implementor, analyzer, formatter)
2. Skill Template Design — SKILL.md variant with phase instruction patterns, progressive disclosure structure, reference file loading
3. Command Template Design — Command variant respecting 15K char lean orchestration budget
4. Agent-Generator Enforcement — Update `agent-generator.md` to validate new/updated agents against canonical template; block non-compliant agents with specific error messages
5. Prompt Versioning System — Version tracking mechanism for before/after prompt changes per component

**Scope — Out:**
- ❌ Applying templates to existing agents (EPIC-062)
- ❌ Research and pattern extraction (EPIC-060)
- ❌ Automated prompt optimization
- ❌ External evaluation tools

**Sprint-Level Feature Assignments:**

| Sprint | Features | Goal | Points |
|--------|----------|------|--------|
| Sprint 1 | F1: Agent Template, F2: Skill Template, F3: Command Template | Design all 3 template variants from research findings | 14 |
| Sprint 2 | F4: Agent-Generator Enforcement, F5: Prompt Versioning | Build enforcement + version tracking | 16 |

**Template Design Decisions (from ideation session):**
- **Standardization level:** Full standardization — single canonical template with required sections, optional sections, and validation rules enforced by agent-generator
- **Enforcement mechanism:** agent-generator validates at creation time; non-compliant agents are blocked
- **No --skip-validation flag** unless emergency (must be logged as deviation)

**Dependencies:**
- [ ] EPIC-060 must complete first (research patterns feed template design)

---

#### 10.1.3 EPIC-062: Pilot Improvement, Evaluation & Rollout

**Business Goal:**
Validate prompt engineering improvements through 3 pilot agents with measurable before/after evaluation, then execute phased rollout of all remaining components in manageable batches to prevent regressions.

**Success Metrics (EPIC-062 specific):**
- 3 pilot agents show measurable quality improvement in before/after evaluation
- Evaluation pipeline produces objective quality scores (not subjective assessment)
- All 39 agents migrated to unified template without regressions
- All 17 skill SKILL.md files improved with clearer phase instructions
- All 39 command files reviewed and improved where applicable
- Zero breaking changes to existing command interface

**Scope — In:**
1. Pilot: test-automator
2. Pilot: ac-compliance-verifier
3. Pilot: requirements-analyst
4. Evaluation Pipeline (before/after comparison within Claude Code Terminal)
5. Batch Rollout Wave 1 — Validators/Analyzers
6. Batch Rollout Wave 2 — Implementors
7. Batch Rollout Wave 3 — Remaining agents + Skills + Commands
8. Quality Validation & Regression Check

**Scope — Out:**
- ❌ Research (EPIC-060)
- ❌ Template creation (EPIC-061)
- ❌ Automated prompt optimization
- ❌ Self-improving prompts

**Pilot Agent Selection Rationale:**
| Agent | Why Selected |
|-------|-------------|
| `test-automator` | Highest-impact agent — invoked in every TDD cycle (Red phase). Improvement here multiplies across all /dev executions. |
| `ac-compliance-verifier` | Critical validation agent — invoked in Phase 4.5 and 5.5 of every /dev workflow. Reliability directly affects QA outcomes. |
| `requirements-analyst` | Key quality gate — drives story requirement completeness. Improvement reduces downstream rework in dev and QA. |

**Sprint-Level Feature Assignments:**

| Sprint | Features | Goal | Points |
|--------|----------|------|--------|
| Sprint 1 | F1: Pilot test-automator, F2: Pilot ac-compliance-verifier, F3: Pilot requirements-analyst | Apply template to 3 pilots, initial quality assessment | 12 |
| Sprint 2 | F4: Evaluation Pipeline | Build before/after comparison framework with scoring rubric | 8 |
| Sprint 3 | F5: Batch Rollout Wave 1 | Migrate validator/analyzer agents | 10 |
| Sprint 4 | F6: Batch Rollout Wave 2 | Migrate implementor agents | 10 |
| Sprint 5 | F7: Batch Rollout Wave 3, F8: Quality Validation | Migrate remaining + skills + commands; final validation | 10 |

**Evaluation Approach (from ideation session):**
- **Method:** Before/after comparison — run same prompts through old and new agent versions, compare output quality with scoring rubric
- **No automation:** All improvements human-reviewed (per brainstorm Won't Have)
- **Rollback:** Prompt versioning (EPIC-061) enables instant rollback per agent

**Complete Agent Roster — Rollout Wave Assignments (39 agents):**

**Pilot Agents (Sprint 1 — 3 agents):**
- `test-automator`
- `ac-compliance-verifier`
- `requirements-analyst`

**Wave 1: Validators & Analyzers (Sprint 3 — 10 agents):**
- `anti-pattern-scanner`
- `context-validator`
- `context-preservation-validator`
- `coverage-analyzer`
- `code-quality-auditor`
- `deferral-validator`
- `dependency-graph-analyzer`
- `file-overlap-detector`
- `pattern-compliance-auditor`
- `tech-stack-detector`

**Wave 2: Implementors & Reviewers (Sprint 4 — 9 agents):**
- `backend-architect`
- `frontend-developer`
- `code-reviewer`
- `refactoring-specialist`
- `integration-tester`
- `api-designer`
- `deployment-engineer`
- `security-auditor`
- `code-analyzer`

**Wave 3: Remaining Agents + Skills + Commands (Sprint 5 — 17 agents + 17 skills + 39 commands):**

*Remaining agents:*
- `agent-generator` (update last — it enforces the template, so update it after template is proven)
- `architect-reviewer`
- `documentation-writer`
- `framework-analyst`
- `git-validator`
- `git-worktree-manager`
- `ideation-result-interpreter`
- `internet-sleuth`
- `observation-extractor`
- `qa-result-interpreter`
- `dev-result-interpreter`
- `session-miner`
- `sprint-planner`
- `stakeholder-analyst`
- `story-requirements-analyst`
- `technical-debt-analyzer`
- `ui-spec-formatter`

*Skills (17 — review and improve SKILL.md files):*
All skills in `.claude/skills/*/SKILL.md` — apply skill template variant from EPIC-061.

*Commands (39 — review and improve):*
All commands in `.claude/commands/*.md` — apply command template variant from EPIC-061.

**Dependencies:**
- [ ] EPIC-060 must complete (research patterns available)
- [ ] EPIC-061 must complete (templates and enforcement ready)

---

## 11. Next Steps

1. **Sprint Planning:** Run `/create-sprint` to begin Sprint 1 planning for EPIC-060
2. **Story Creation:** Run `/create-story` to decompose EPIC-060 features into stories
3. **Research Execution:** Begin mining Anthropic repos per EPIC-060 plan

---

## Appendices

### A. Glossary

| Term | Definition |
|------|-----------|
| Subagent | Specialized AI worker defined in `.claude/agents/*.md` |
| Skill | Capability module in `.claude/skills/*/SKILL.md` with phased workflow |
| Command | Slash command in `.claude/commands/*.md` (user entry point) |
| Lean Orchestration | Pattern where commands (15K char) delegate to skills which delegate to subagents |
| Context Files | 6 immutable constraint files in `devforgeai/specs/context/` |
| ADR | Architecture Decision Record for changing immutable constraints |
| TDD | Test-Driven Development (Red → Green → Refactor) |
| CCT | Claude Code Terminal — the execution environment |

### B. References

| Document | Location |
|----------|----------|
| Brainstorm | `devforgeai/specs/brainstorms/BRAINSTORM-010-prompt-engineering-from-anthropic-repos.brainstorm.md` |
| Tech Stack | `devforgeai/specs/context/tech-stack.md` |
| Architecture Constraints | `devforgeai/specs/context/architecture-constraints.md` |
| Anti-Patterns | `devforgeai/specs/context/anti-patterns.md` |
| Lean Orchestration | `src/devforgeai/protocols/lean-orchestration-pattern.md` |
| Epic Template | `.claude/skills/devforgeai-orchestration/assets/templates/epic-template.md` |

### C. Open Questions

1. **Q1:** Should the research artifact be a single large document or split by repo category? (Decision: TBD during EPIC-060 Sprint 1)
2. **Q2:** How many template sections should be "required" vs "optional"? (Decision: TBD during EPIC-061 based on research findings)
3. **Q3:** What specific rubric dimensions should the evaluation pipeline use? (Decision: TBD during EPIC-062 Sprint 2)

---

**Requirements Specification Version:** 1.0
**Last Updated:** 2026-02-04
