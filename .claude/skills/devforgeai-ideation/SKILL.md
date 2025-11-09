---
name: devforgeai-ideation
description: Transform business ideas and problems into structured requirements through guided discovery, requirements elicitation, and feasibility analysis. Use when starting new projects (greenfield), planning features for existing systems (brownfield), or exploring solution spaces before architecture and development. Supports simple apps through multi-tier platforms via progressive complexity assessment.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebFetch
  - Bash(git:*)
  - Skill
  - TodoWrite
model: claude-sonnet-4-5-20250929
---

# DevForgeAI Ideation Skill

Transform raw business ideas, problems, and opportunities into structured, actionable requirements that drive spec-driven development with zero technical debt.

## Purpose

This skill serves as the **entry point** for the entire DevForgeAI framework. It transforms vague business ideas into concrete, implementable requirements through systematic discovery, requirements elicitation, complexity assessment, and feasibility analysis.

**Use BEFORE architecture and development skills.**

### Core Philosophy

**"Start with Why, Then What, Then How"**
- **Why:** Business value, user needs, success metrics
- **What:** Functional/non-functional requirements, constraints
- **How:** Technical approach (delegated to architecture skill)

**"Ask, Don't Assume"**
- Use AskUserQuestion for ALL ambiguities
- Never infer requirements from incomplete information
- Validate assumptions explicitly

**"Right-size the Solution"**
- Progressive complexity assessment (simple → enterprise)
- Don't over-engineer simple problems
- Don't under-architect complex platforms

---

## When to Use This Skill

### ✅ Trigger Scenarios

- User has business idea without technical specs
- Starting greenfield projects ("I want to build...")
- Adding major features to existing systems
- Exploring solution spaces and feasibility
- User requests requirements discovery or epic creation

### ❌ When NOT to Use

- Context files already exist (use devforgeai-architecture to update)
- Story-level work (use devforgeai-story-creation)
- Technical implementation (use devforgeai-development)

---

## Ideation Workflow (6 Phases)

Each phase loads its reference file on-demand for detailed implementation.

### Phase 1: Discovery & Problem Understanding
**Reference:** `discovery-workflow.md` | **Questions:** 5-10 | **Output:** Problem statement, user personas, scope boundaries

Determine project type (greenfield/brownfield), analyze existing system, explore problem space, define scope.

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/discovery-workflow.md")`

### Phase 2: Requirements Elicitation
**Reference:** `requirements-elicitation-workflow.md` + `requirements-elicitation-guide.md` | **Questions:** 10-60 | **Output:** Functional/NFR requirements, data models, integrations

Systematic questioning to extract user stories, data entities, external integrations, and quantified NFRs.

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/requirements-elicitation-workflow.md")`

### Phase 3: Complexity Assessment & Architecture Planning
**Reference:** `complexity-assessment-workflow.md` + `complexity-assessment-matrix.md` | **Output:** Complexity score (0-60), tier (1-4), tech recommendations

Score across 4 dimensions: Functional (0-20), Technical (0-20), Team/Org (0-10), NFR (0-10). Maps to architecture tier.

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/complexity-assessment-workflow.md")`

### Phase 4: Epic & Feature Decomposition
**Reference:** `epic-decomposition-workflow.md` + `domain-specific-patterns.md` | **Output:** 1-3 epics, 3-8 features/epic, roadmap

Break initiative into epics (4-8 week efforts), features (1-2 sprints), and high-level stories (1-5 days).

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/epic-decomposition-workflow.md")`

### Phase 5: Feasibility & Constraints Analysis
**Reference:** `feasibility-analysis-workflow.md` + `feasibility-analysis-framework.md` | **Output:** Feasibility assessment, risk register

Evaluate technical/business/resource feasibility, identify risks with mitigations, validate brownfield constraints.

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/feasibility-analysis-workflow.md")`

---

### Phase 6: Requirements Documentation & Handoff
**Workflow:** 3 sub-phases | **Output:** Epic documents, requirements spec (optional), completion summary

**6.1-6.3 Artifact Generation:** Generate epics, optional requirements spec, verify creation, transition to architecture
**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/artifact-generation.md")`

**6.4 Self-Validation:** Validate artifacts, auto-correct issues, HALT on critical failures
**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/self-validation-workflow.md")`

**6.5-6.6 Completion & Handoff:** Present summary, determine next action (greenfield→architecture, brownfield→orchestration)
**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/completion-handoff.md")`

---

## AskUserQuestion Usage

**10-60 strategic questions** across 6 phases (Phase 1: 5-10, Phase 2: 10-60, Phases 3-6: 1-8 each). All question patterns, templates, and best practices in `user-interaction-patterns.md`.

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/user-interaction-patterns.md")`

---

## Error Handling

**6 error types:** Incomplete answers, artifact failures, complexity errors, validation failures, constraint conflicts, directory issues. Each has detection logic and recovery procedures (self-heal → retry → report).

**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/error-handling.md")`

---

## Integration

**→ devforgeai-architecture** (greenfield: create context files) | **→ devforgeai-orchestration** (brownfield: sprint planning)

**Outputs:** Epic documents, requirements specs, complexity tier, technology recommendations

---

## Success Criteria

- [ ] Business problem defined (measurable)
- [ ] 1-3 epics with 3-8 features each
- [ ] Complexity scored (0-60, tier 1-4)
- [ ] Feasibility confirmed, risks mitigated
- [ ] Epic documents generated, validated
- [ ] Next action determined
- [ ] No critical ambiguities

**Token Budget:** ~35K-100K (isolated context)

---

## Reference Files

Load these on-demand during workflow execution:

### Phase Workflows (10 files - NEW)
- **discovery-workflow.md** - Phase 1: Problem understanding (274 lines)
- **requirements-elicitation-workflow.md** - Phase 2: Question flow (368 lines)
- **complexity-assessment-workflow.md** - Phase 3: Scoring algorithm (308 lines)
- **epic-decomposition-workflow.md** - Phase 4: Feature breakdown (309 lines)
- **feasibility-analysis-workflow.md** - Phase 5: Constraints check (378 lines)
- **artifact-generation.md** - Phase 6.1-6.3: Document generation (689 lines)
- **self-validation-workflow.md** - Phase 6.4: Quality checks (351 lines)
- **completion-handoff.md** - Phase 6.5-6.6: Summary and next action (721 lines)
- **user-interaction-patterns.md** - AskUserQuestion templates (411 lines)
- **error-handling.md** - Recovery procedures for 6 error types (1,062 lines)

### Supporting Guides (6 files - existing)
- **requirements-elicitation-guide.md** - Domain-specific question patterns (659 lines)
- **complexity-assessment-matrix.md** - Complete 0-60 scoring rubric (617 lines)
- **domain-specific-patterns.md** - Decomposition patterns by domain (744 lines)
- **feasibility-analysis-framework.md** - Feasibility checklists (587 lines)
- **validation-checklists.md** - Quality validation procedures (604 lines)
- **output-templates.md** - Summary templates, tech recommendations (780 lines)

**Total:** 16 reference files, 8,862 lines (loaded progressively, not upfront)

---

## Best Practices

1. **Ask strategic questions** - User-guided discovery
2. **Progressive questioning** - Broad→specific (5→60 questions)
3. **Validate assumptions** - Confirm before documenting
4. **Document early risks** - Phase 5 feasibility analysis
5. **Clear handoff** - Next action: architecture or orchestration

---

**The goal:** Transform business ideas into structured, actionable requirements with zero ambiguity, enabling downstream skills to implement with zero technical debt.
