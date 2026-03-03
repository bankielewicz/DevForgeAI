---
id: EPIC-062
title: "Pilot Improvement, Evaluation & Rollout"
status: Planning
start_date: TBD
target_date: TBD
total_points: 50
created: 2026-02-04
updated: 2026-02-04
source_brainstorm: BRAINSTORM-010
source_requirements: devforgeai/specs/requirements/prompt-engineering-improvement-requirements.md
depends_on:
  - EPIC-060
  - EPIC-061
---

# Epic: Pilot Improvement, Evaluation & Rollout

## Business Goal

Validate prompt engineering improvements through 3 pilot agents with measurable before/after evaluation, then execute phased rollout of all remaining components in manageable batches to prevent regressions. This is the execution phase that delivers concrete quality improvements across the entire framework.

## Success Metrics

- **Metric 1:** 3 pilot agents show measurable quality improvement in before/after evaluation
- **Metric 2:** Evaluation pipeline produces objective quality scores (not subjective assessment)
- **Metric 3:** All 39 agents migrated to unified template without regressions
- **Metric 4:** All 17 skill SKILL.md files improved with clearer phase instructions
- **Metric 5:** All 39 command files reviewed and improved where applicable
- **Metric 6:** Zero breaking changes to existing command interface

## Scope

### Overview

Apply the unified templates from EPIC-061 to 3 carefully selected pilot agents, build a before/after evaluation pipeline, validate improvements, then execute phased rollout of all remaining agents, skills, and commands in manageable batches (5-10 components per wave) to limit blast radius and enable regression detection.

### Features

1. **Pilot: test-automator**
   - Description: Apply unified agent template to test-automator subagent, improve system prompt with Anthropic patterns
   - User Value: Highest-impact agent — invoked in every TDD cycle (Red phase). Improvement multiplies across all /dev executions
   - Estimated Points: 5 story points
   - **Story:** STORY-391 - Pilot: Apply Unified Template to test-automator Subagent

2. **Pilot: ac-compliance-verifier**
   - Description: Apply unified agent template to ac-compliance-verifier subagent, improve system prompt with Anthropic patterns
   - User Value: Critical validation agent — invoked in Phase 4.5 and 5.5 of every /dev workflow. Reliability directly affects QA outcomes
   - Estimated Points: 3 story points
   - **Story:** STORY-392 - Pilot: Apply Unified Template to ac-compliance-verifier Subagent

3. **Pilot: requirements-analyst**
   - Description: Apply unified agent template to requirements-analyst subagent, improve system prompt with Anthropic patterns
   - User Value: Key quality gate — drives story requirement completeness. Improvement reduces downstream rework
   - Estimated Points: 4 story points
   - **Story:** STORY-393 - Pilot: Apply Unified Template to requirements-analyst Subagent

4. **Evaluation Pipeline**
   - Description: Build before/after comparison framework with scoring rubric within Claude Code Terminal. Run same prompts through old and new agent versions, compare output quality
   - User Value: Objective quality measurement enables data-driven decisions about migration success
   - Estimated Points: 8 story points
   - **Story:** STORY-394 - Build Before/After Evaluation Pipeline for Agent Migration

5. **Batch Rollout Wave 1: Validators & Analyzers**
   - Description: Migrate 10 validator/analyzer agents to unified template
   - User Value: Standardize quality-critical validation agents for consistent enforcement
   - Estimated Points: 10 story points
   - **Story:** STORY-395 - Batch Rollout Wave 1: Migrate 10 Validator/Analyzer Agents to Unified Template

6. **Batch Rollout Wave 2: Implementors & Reviewers**
   - Description: Migrate 9 implementor/reviewer agents to unified template
   - User Value: Improve code generation and review agents for better development output
   - Estimated Points: 10 story points
   - **Story:** STORY-396 - Batch Rollout Wave 2: Migrate 9 Implementor/Reviewer Agents to Unified Template

7. **Batch Rollout Wave 3: Remaining Agents + Skills + Commands**
   - Description: Migrate 17 remaining agents, review/improve all 17 skill SKILL.md files, review/improve all 39 command files
   - User Value: Complete framework-wide migration for consistent quality everywhere
   - Estimated Points: 8 story points
   - **Story:** STORY-397 - Batch Rollout Wave 3: Migrate 17 Remaining Agents, 17 Skills, and 39 Commands to Unified Template

8. **Quality Validation & Regression Check**
   - Description: Final validation pass across all migrated components — run evaluation pipeline on sample, verify zero breaking changes, confirm rollback capability
   - User Value: Confidence that migration succeeded without regressions
   - Estimated Points: 2 story points
   - **Story:** STORY-398 - Quality Validation & Regression Check for EPIC-062 Migration

### Out of Scope

- Research and pattern extraction (EPIC-060)
- Template creation (EPIC-061)
- Automated prompt optimization (Won't Have per BRAINSTORM-010)
- Self-improving prompts
- External evaluation tools

## Target Sprints

**Estimated Duration:** 5 sprints / 10 weeks

**Sprint Breakdown:**
- **Sprint 1:** F1: Pilot test-automator + F2: Pilot ac-compliance-verifier + F3: Pilot requirements-analyst — 12 story points
  - Goal: Apply template to 3 pilots, initial quality assessment
- **Sprint 2:** F4: Evaluation Pipeline — 8 story points
  - Goal: Build before/after comparison framework with scoring rubric
- **Sprint 3:** F5: Batch Rollout Wave 1 (Validators & Analyzers) — 10 story points
  - Goal: Migrate 10 validator/analyzer agents
- **Sprint 4:** F6: Batch Rollout Wave 2 (Implementors & Reviewers) — 10 story points
  - Goal: Migrate 9 implementor/reviewer agents
- **Sprint 5:** F7: Batch Rollout Wave 3 + F8: Quality Validation — 10 story points
  - Goal: Migrate remaining agents + skills + commands; final validation

## Dependencies

### External Dependencies

- None required (all work within Claude Code Terminal)

### Internal Dependencies

- **Dependency 1:** EPIC-060 must complete (research patterns available for improvement)
- **Dependency 2:** EPIC-061 must complete (templates and enforcement mechanism ready)

### Blocking Issues

- None identified, assuming EPIC-060 and EPIC-061 complete successfully

## Stakeholders

- **Product Owner:** Framework Owner — Approves pilot results, validates evaluation scores, approves wave rollouts
- **Orchestrator:** Opus — Executes migration workflows, runs evaluation pipeline
- **Affected:** All DevForgeAI users (improved command/skill output quality)

## Requirements

### Functional Requirements

#### User Stories

**User Story 12:**
```
As a Framework Owner,
I want test-automator improved with unified template,
So that TDD test generation improves.
```

**Acceptance Criteria:**
- [ ] test-automator system prompt updated to unified template
- [ ] Anthropic patterns applied (chain-of-thought, structured output, examples)
- [ ] Before/after comparison shows measurable improvement
- [ ] No regression in existing TDD workflows

**User Story 13:**
```
As a Framework Owner,
I want ac-compliance-verifier improved with unified template,
So that AC verification is more reliable.
```

**Acceptance Criteria:**
- [ ] ac-compliance-verifier system prompt updated to unified template
- [ ] Verification accuracy maintained or improved
- [ ] No regression in Phase 4.5/5.5 workflow

**User Story 14:**
```
As a Framework Owner,
I want requirements-analyst improved with unified template,
So that story requirements are more complete.
```

**Acceptance Criteria:**
- [ ] requirements-analyst system prompt updated to unified template
- [ ] Story requirement completeness maintained or improved
- [ ] No regression in /create-story workflow

**User Story 15:**
```
As a Framework Owner,
I want a before/after evaluation pipeline,
So that I can objectively measure improvements.
```

**Acceptance Criteria:**
- [ ] Evaluation pipeline runs within Claude Code Terminal (no external tools)
- [ ] Scoring rubric defined with objective dimensions
- [ ] Before/after comparison produces numeric quality scores
- [ ] Pipeline reusable across all migration waves

**User Story 16:**
```
As a Framework Owner,
I want phased rollout in batches of 5-10,
So that migration is manageable and regressions catchable.
```

**Acceptance Criteria:**
- [ ] Wave 1: 10 validators/analyzers migrated
- [ ] Wave 2: 9 implementors/reviewers migrated
- [ ] Wave 3: 17 remaining agents + 17 skills + 39 commands migrated
- [ ] Each wave validated before next wave begins
- [ ] Rollback exercised for at least 1 component to verify capability

**User Story 17:**
```
As an End User,
I want zero breaking changes,
So that existing commands continue to work reliably.
```

**Acceptance Criteria:**
- [ ] All existing slash commands work identically before and after migration
- [ ] No command interface changes (arguments, options, output format)
- [ ] Quality improves but behavior remains compatible
- [ ] Regression test suite passes for all waves

### Non-Functional Requirements (NFRs)

#### Performance
- No increase in agent response times after template migration
- Evaluation pipeline completes within reasonable timeframe per component

#### Stability
- Zero breaking changes to existing command interface (CRITICAL)
- Prompt versioning enables rollback within minutes per component
- Phased rollout limits blast radius of any single migration batch

### Data Requirements

#### Entities

**Entity: Evaluation Result**
- **Location:** `devforgeai/specs/research/evaluation-results.md` or structured format
- **Attributes:** Component ID, before score, after score, rubric dimensions, pass/fail
- **Relationships:** One per evaluated component

### Integration Requirements

- **agent-generator:** Must enforce template compliance (enabled by EPIC-061)
- **prompt versioning:** Must track all changes (enabled by EPIC-061)
- **evaluation pipeline:** New capability built in this epic

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate**
- **Score:** 31/60 points (inherited from overall initiative)
- **Rationale:** Individual migrations are straightforward; scale (88+ components) and evaluation pipeline add complexity

### Recommended Architecture Pattern
Uses existing DevForgeAI framework patterns:
- Agent updates via Edit() tool (standard pattern)
- Evaluation via structured prompts within Claude Code Terminal
- Batch management via sprint planning

### Technology Constraints
- All updates as Markdown file edits (per tech-stack.md)
- No new dependencies required
- Must work within Claude Code Terminal capabilities
- Agent size limits maintained (per source-tree.md)

## Pilot Agent Selection Rationale

| Agent | Why Selected | Impact Scope |
|-------|-------------|--------------|
| `test-automator` | Highest-impact — invoked in every TDD cycle (Red phase) | All /dev executions |
| `ac-compliance-verifier` | Critical validation — invoked in Phase 4.5 and 5.5 | All /dev workflow quality gates |
| `requirements-analyst` | Key quality gate — drives story requirement completeness | All /create-story executions |

## Complete Agent Roster — Rollout Wave Assignments

### Pilot Agents (Sprint 1 — 3 agents)
- `test-automator`
- `ac-compliance-verifier`
- `requirements-analyst`

### Wave 1: Validators & Analyzers (Sprint 3 — 10 agents)
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

### Wave 2: Implementors & Reviewers (Sprint 4 — 9 agents)
- `backend-architect`
- `frontend-developer`
- `code-reviewer`
- `refactoring-specialist`
- `integration-tester`
- `api-designer`
- `deployment-engineer`
- `security-auditor`
- `code-analyzer`

### Wave 3: Remaining Agents (Sprint 5 — 17 agents)
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

### Wave 3: Skills (Sprint 5 — 17 skills)
All skills in `.claude/skills/*/SKILL.md` — apply skill template variant from EPIC-061.

### Wave 3: Commands (Sprint 5 — 39 commands)
All commands in `.claude/commands/*.md` — apply command template variant from EPIC-061.

## Risks & Constraints

### Technical Risks

**Risk 1: Regression After Migration**
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Evaluation pipeline validates each wave; prompt versioning enables instant rollback; phased rollout limits blast radius

**Risk 2: Scope Creep (88+ Files)**
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Phased batches with strict sprint planning; time-box each wave; defer low-priority components if needed

### Business Risks

**Risk 1: Quality Not Measurably Better**
- **Probability:** Low
- **Impact:** High
- **Mitigation:** Evaluation pipeline provides objective measurement; if pilot shows no improvement, reassess template before continuing

### Constraints

**Constraint 1: Zero Breaking Changes**
- **Impact:** Migration must preserve all existing behavior
- **Mitigation:** Before/after evaluation; regression testing; phased rollout

**Constraint 2: Human Review Required**
- **Impact:** All improvements must be human-reviewed (no automated optimization per brainstorm Won't Have)
- **Mitigation:** Batch size limits (5-10 per wave) make review manageable

## Assumptions

1. **A1:** Anthropic's prompt engineering patterns improve agent output quality (validated by pilot results)
2. **A2:** Unified template accommodates all agent categories (validated during EPIC-061)
3. **A3:** Before/after evaluation within Claude Code Terminal produces meaningful quality signals (validated by evaluation pipeline)

## Evaluation Approach (from Ideation)

- **Method:** Before/after comparison — run same prompts through old and new agent versions, compare output quality with scoring rubric
- **No automation:** All improvements human-reviewed (per brainstorm Won't Have)
- **Rollback:** Prompt versioning (EPIC-061) enables instant rollback per agent

## Next Steps

### Immediate Actions
1. **Wait for EPIC-060 + EPIC-061:** Research and templates must be available
2. **Story Creation:** Run `/create-story` to decompose pilot features into implementable stories
3. **Pilot Execution:** Begin with test-automator (highest impact)

### Pre-Development Checklist
- [ ] EPIC-060 research artifact complete and reviewed
- [ ] EPIC-061 templates created and validated
- [ ] EPIC-061 agent-generator enforcement active
- [ ] EPIC-061 prompt versioning system operational
- [ ] Sprint 1 stories created
- [ ] Sprint plan approved
- [ ] Before-state captured for all 3 pilot agents

## Notes

- agent-generator is updated LAST in Wave 3 because it enforces the template — update it only after template is proven across all other agents
- Wave 3 is the largest wave (17 agents + 17 skills + 39 commands) — may need to split into sub-waves if too large
- Evaluation pipeline design should be informed by Anthropic's `prompt_evaluations` course from EPIC-060

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2026-02-04
