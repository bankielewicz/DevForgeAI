---
brainstorm_id: BRAINSTORM-010
title: "Prompt Engineering Improvement from Anthropic Repos"
created: 2026-02-04
status: complete
confidence: HIGH
topic: "Review Anthropic's official prompt engineering repos to systematically improve DevForgeAI framework's agents, skills, and commands"
next_step: "/ideate"
---

## Key Files for Context

| File | Purpose |
|------|---------|
| `.claude/agents/*.md` | 32+ subagent definitions with system prompts to be improved |
| `.claude/skills/*/SKILL.md` | 17 skill definitions with phase instructions |
| `.claude/commands/*.md` | 39 slash command definitions |
| `src/devforgeai/protocols/lean-orchestration-pattern.md` | Lean orchestration protocol governing command/skill budgets |
| `devforgeai/specs/context/tech-stack.md` | Immutable technology constraints |
| `devforgeai/specs/context/architecture-constraints.md` | Immutable architecture constraints |
| `devforgeai/specs/context/anti-patterns.md` | Forbidden patterns |
| `tmp/anthropic/courses/` | 5 Anthropic courses (API fundamentals, prompt eng, real-world, evaluations, tool use) |
| `tmp/anthropic/prompt-eng-interactive-tutorial/` | 9-chapter prompt engineering tutorial with exercises |
| `tmp/anthropic/claude-cookbooks/` | Code examples and guides for building with Claude API |
| `tmp/anthropic/claude-quickstarts/` | Foundational project templates |
| `tmp/anthropic/claude-code-action/` | GitHub Action for Claude Code |
| `tmp/anthropic/claude-code-security-review/` | Security review GitHub Action |
| `tmp/anthropic/claude-plugins-official/` | Curated plugin directory |
| `tmp/anthropic/claude-constitution/` | Claude's values and constitution document |
| `tmp/anthropic/healthcare/` | Healthcare domain skills |
| `tmp/anthropic/life-sciences/` | Life sciences domain skills |
| `tmp/anthropic/original_performance_takehome/` | Performance benchmarks |
| `tmp/anthropic/beam/` | Apache-licensed project |

## Glossary

- **Subagent**: A specialized AI worker defined in `.claude/agents/*.md` with a system prompt, tool access list, and proactive trigger mapping. DevForgeAI has 32+ subagents.
- **Skill**: A capability module defined in `.claude/skills/*/SKILL.md` containing phased workflow instructions that expand inline when invoked. DevForgeAI has 17 skills.
- **Command**: A slash command defined in `.claude/commands/*.md` that serves as the user-facing entry point, delegating to skills. DevForgeAI has 39 commands.
- **Lean Orchestration Pattern**: The architectural pattern where commands delegate to skills which delegate to subagents, with character budget constraints (15K for commands).
- **Context Files**: 6 immutable architectural constraint files in `devforgeai/specs/context/` (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md). Changes require ADR process.
- **ADR**: Architecture Decision Record - formal document required to change immutable context files. Stored in `devforgeai/specs/adrs/`.
- **Phase**: A numbered step (01-10) in a DevForgeAI skill workflow that must execute sequentially.
- **TDD**: Test-Driven Development cycle (Red -> Green -> Refactor) mandatory for all DevForgeAI development.
- **QA**: Quality Assurance validation with strict coverage thresholds (95%/85%/80%).
- **DoD**: Definition of Done - completion criteria for a story.
- **AC**: Acceptance Criteria - testable requirements for a story.
- **Treelint**: A user-developed CLI tool for AST-based code searches, designed to help Claude navigate codebases more effectively.

---

## 1. Executive Summary

DevForgeAI's 32+ subagents, 17 skills, and 39 commands produce **inconsistent and unreliable results** because their prompts were written ad-hoc without systematic methodology. Anthropic has released 13 official repos containing comprehensive prompt engineering guidance (courses, tutorials, cookbooks, quickstarts, dev tools, domain-specific resources, and reference materials) that can be mined to establish a **research-backed prompt engineering methodology** for the framework.

**Opportunity:** Systematically extract prompt engineering best practices from Anthropic's official repos and apply them to DevForgeAI to achieve consistent quality, measurable improvement, and scalable template standardization across all agents and skills.

**Confidence:** HIGH (all 7 phases complete with clear stakeholder alignment)

---

## 2. Stakeholder Map

### Primary Stakeholders (Decision Authority)

| Stakeholder | Goals | Concerns |
|---|---|---|
| **Framework Owner** | Improve prompt quality across all agents/skills; capture reusable patterns; build new capabilities; reduce QA fix cycles | Breaking changes to established workflows; scope creep across 13 repos; token budget impact; regression risk |
| **Opus (Orchestrating Agent)** | Better delegation patterns; improved context preservation; reduced hallucination; more effective AskUserQuestion interactions | Task() invocation pattern compatibility; inline expansion execution model; 39 command compatibility |

### Secondary Stakeholders (Users/Beneficiaries)

| Stakeholder | Goals | Concerns |
|---|---|---|
| **Subagent Authors / Agent Generator** | Updated templates with Anthropic best practices; better system prompt patterns | Mass update of 32+ agents; agent-generator template revision; backward compatibility |
| **Skill Developers** | Better phase instructions reducing AI drift; improved validation checkpoints | 17 skills with extensive reference files need audit; lean orchestration preserved |
| **End Users** | More accurate AI responses; fewer QA failures; better story generation | Command interface must not change; question patterns stay intuitive |
| **QA Pipeline** | Stronger validation prompts; better anti-pattern detection | False positive/negative rate changes; quality gate enforcement |

### Tertiary Stakeholders

| Stakeholder | Impact |
|---|---|
| RCA Process | Better 5 Whys prompts; existing RCAs reference current patterns |
| Documentation System | Improved documentation-writer subagent |
| Feedback/Insights System | Better session-miner and observation-extractor |
| Context File System | Immutability constraint must be respected |

### Key Conflicts

1. **Scope vs. stability** - 13 repos is a large surface area; updating 32+ agents risks destabilization
2. **Token budget vs. quality** - Better prompts may increase character counts beyond 15K limits
3. **Innovation vs. immutability** - New patterns may require ADR process for context file changes
4. **Template revision vs. consistency** - Updated templates create inconsistency with existing agents

---

## 3. Problem Statement

> DevForgeAI framework stakeholders experience **inconsistent and unreliable results from subagents and skills** because prompts were written ad-hoc without a systematic methodology based on proven prompt engineering principles, resulting in **QA fix cycles, wasted time on off-target outputs, and inconsistent quality across agents**.

### Root Cause Analysis (5 Whys)

1. **Why** do agents produce inconsistent results? → Prompts lack systematic engineering methodology
2. **Why** is there no methodology? → Prompts were created organically as features were built
3. **Why** weren't best practices applied? → Anthropic's official guidance wasn't systematically reviewed and incorporated
4. **Why** did partial improvements regress? → No scale strategy - fixes to one agent weren't propagated; changes sometimes broke other agents
5. **Why** couldn't improvements be measured? → No before/after evaluation framework for prompt quality

### Current State

- **Status:** Automated but broken - templates and patterns exist but produce poor/inconsistent results
- **Pain Points:** Agent system prompts, skill phase instructions, tool use patterns, output formatting (all 4 areas)
- **Business Impact:** QA rework, time waste, inconsistency across all agents
- **Previous Attempts:** Partially worked - failed due to no methodology, no scale strategy, and regressions

---

## 4. Opportunity Map

### Source Material (13 Anthropic Repos)

| Repo | Key Topics | DevForgeAI Application |
|---|---|---|
| **courses** | 5 courses: API fundamentals, prompt eng, real-world, evaluations, tool use | Core methodology source |
| **prompt-eng-interactive-tutorial** | 9 chapters: structure, clarity, roles, data separation, formatting, chain-of-thought, few-shot, hallucination avoidance, complex prompts | Direct pattern extraction for agent/skill prompts |
| **claude-cookbooks** | Code examples and integration guides | Implementation patterns |
| **claude-quickstarts** | Customer support, computer use, financial data analyst | Domain-specific prompt patterns |
| **claude-code-action** | GitHub Action for Claude Code | CI/CD integration patterns |
| **claude-code-security-review** | Security review prompts | Security audit subagent improvement |
| **claude-plugins-official** | Plugin directory and patterns | Plugin architecture reference |
| **claude-constitution** | Claude's values document | Alignment and safety prompt patterns |
| **healthcare** | Clinical trials, prior auth, FHIR API | Domain-specific skill patterns |
| **life-sciences** | PubMed, BioRender, research tools | MCP integration patterns |
| **original_performance_takehome** | Performance benchmarks | Evaluation methodology |
| **beam** | Apache-licensed project | TBD |

### Ideal State Vision

- **Consistent quality:** Every subagent produces reliable, high-quality output every time
- **Self-improving:** Framework learns from each execution and improves prompts over time
- **Measurable:** Prompt quality is tracked with metrics and can be objectively evaluated

### Adjacent Opportunities

- **Agent template standardization:** Create a unified template so all agents follow the same prompt structure
- **Prompt versioning:** Track prompt changes over time to identify and roll back regressions
- **Treelint CLI integration:** Leverage AST-based code search in agent workflows

---

## 5. Constraints

| Type | Constraint | Impact |
|---|---|---|
| **Budget** | Time only - no external tool costs | Must use only Claude Code Terminal capabilities |
| **Timeline** | No hard deadline - ongoing improvement | Can be thorough rather than rushed |
| **Technical** | 15K char command budget (lean orchestration) | Prompts must be efficient, not verbose |
| **Technical** | 6 immutable context files | Changes require ADR process |
| **Technical** | Inline skill expansion model | No background process patterns |
| **Technical** | Must work within Claude Code Terminal | No external evaluation tools |
| **Process** | Must use DevForgeAI workflow (story/dev/QA) | Changes go through standard pipeline |
| **Process** | No breaking changes | Existing commands/skills must keep working |
| **Process** | Incremental rollout | Phased approach, not big-bang |

---

## 6. Hypotheses

| ID | Hypothesis | Success Criteria | Validation Approach | Risk if Wrong |
|---|---|---|---|---|
| **H1** | Anthropic's prompt engineering patterns fit within DevForgeAI's architectural constraints and improve agent output quality without exceeding token budgets | Measurable quality improvement in pilot agents within 15K char budget | Apply patterns to 2-3 agents, compare before/after outputs | Wasted research effort; patterns too verbose for DevForgeAI |
| **H2** | A unified agent template based on Anthropic best practices can scale across all 32+ agents incrementally without regressions | Migrate 5 agents without breaking existing behavior | Create template, pilot on low-risk agents first | Template too rigid or too flexible; one-size-doesn't-fit-all |
| **H3** | A prompt evaluation pipeline is feasible within Claude Code Terminal (no external tools) | Automated quality scores for agent outputs | Build eval inspired by Anthropic's prompt_evaluations course | No objective measurement possible within constraints |
| **H4** | Knowledge captured in a research artifact persists and is actionable across sessions | Future sessions can apply patterns without re-reading all 13 repos | Create research document, test application in fresh session | Knowledge too verbose or context-dependent to transfer |

**All four hypotheses are critical to validate.**

---

## 7. Prioritization

### MoSCoW Classification

| Priority | Capability |
|---|---|
| **Must Have** | Research & knowledge capture from all 13 repos |
| **Must Have** | Unified agent template standardization |
| **Must Have** | Pilot agent improvements (2-3 agents) |
| **Should Have** | Prompt evaluation pipeline (within Claude Code Terminal) |
| **Should Have** | Prompt versioning |
| **Could Have** | Mass migration of all 32+ agents |
| **Won't Have** | Self-improving prompts (automated optimization) |
| **Won't Have** | External tool integration |

### Impact-Effort Matrix

```
                    HIGH IMPACT
                        |
   Quick Wins:          |    Major Projects:
   - Knowledge capture  |    - Unified template
   - Pattern catalog    |    - Evaluation pipeline
                        |    - Mass migration
  ──────────────────────+───────────────────
                        |
   Fill-ins:            |    Avoid:
   - Prompt versioning  |    - Self-improving prompts
                        |    - External tools
                        |
                    LOW IMPACT
        LOW EFFORT              HIGH EFFORT
```

### Recommended Sequence

1. **Research all 13 repos** → Extract and catalog prompt engineering patterns
2. **Create pattern catalog** → Structured research document with DevForgeAI applicability mapping
3. **Build unified agent template** → Standardized prompt structure based on extracted patterns
4. **Pilot 2-3 agents** → Apply template to selected agents (suggest: test-automator, ac-compliance-verifier, requirements-analyst)
5. **Evaluate results** → Compare before/after quality, measure token impact
6. **Incremental rollout** → Migrate remaining agents in priority batches

---

## 8. Recommended Next Steps

1. **Run `/ideate`** to transform this brainstorm into formal requirements with epic/feature breakdown
2. **During ideation, consider:**
   - Epic structure: Research → Template → Pilot → Evaluate → Rollout
   - Each repo category could map to a research story
   - Pilot agents should be high-impact, moderate-risk
3. **After ideation:** `/create-context` if new context files are needed for prompt engineering standards

---

## 9. Session Metadata

| Field | Value |
|---|---|
| Session ID | BRAINSTORM-010 |
| Date | 2026-02-04 |
| Duration | ~25 minutes |
| Phases Completed | 7/7 |
| Questions Asked | ~20 |
| Confidence | HIGH |
| Market Research | Skipped (focused on Anthropic repos only) |
| Stakeholders Identified | 10 (2 primary, 4 secondary, 4 tertiary) |
| Hypotheses | 4 (all critical) |
| Conflicts | 4 identified with resolutions |
