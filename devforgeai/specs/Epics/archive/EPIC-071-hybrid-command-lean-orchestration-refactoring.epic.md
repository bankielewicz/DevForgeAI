---
id: EPIC-071
title: Hybrid Command Lean Orchestration Refactoring
status: Planning
start_date: 2026-02-20
target_date: 2026-04-15
total_points: 77
completed_points: 0
created: 2026-02-20
owner: Framework Owner
tech_lead: DevForgeAI AI Agent
team: DevForgeAI

source_requirements: "REQ-071"
source_brainstorm: "N/A"
source_plan: ".claude/plans/piped-baking-crystal.md"
source_audit: "bash .claude/scripts/audit-command-skill-overlap.sh"
complexity_score: 7.5
---

# Epic: Hybrid Command Lean Orchestration Refactoring

## Business Goal

Eliminate all 20 hybrid command violations detected by `/audit-hybrid` where commands contain >4 code blocks of business logic before `Skill()` invocation. Refactor commands to follow the lean orchestration pattern (Validate args -> Set context markers -> Invoke skill) as mandated by the DevForgeAI Lean Orchestration Protocol (`devforgeai/protocols/lean-orchestration-pattern.md`) and aligned with Anthropic's Agent Skills Best Practices.

**Value delivered:**
- 40-60% token reduction per command invocation (saves context window budget)
- Zero business logic in commands (single responsibility, easier maintenance)
- Uniform command structure (automated auditing, predictable behavior)
- Alignment with Anthropic's official guidance on skill architecture

**Problem:** 20 of 41 commands have excessive inline logic (gap detection algorithms, multi-step user interaction workflows, display formatting, data aggregation) that wastes main conversation tokens and violates the architectural boundary between commands (orchestration) and skills (execution).

## Success Metrics

- **SC-1:** Code blocks before Skill() per command: <= 4 (hard limit), <= 2 (target)
  - Measurement: `bash .claude/scripts/audit-command-skill-overlap.sh` exits 0
- **SC-2:** Command character count: <= 12K (target), <= 15K (hard limit)
  - Measurement: `/audit-budget` shows all refactored commands compliant
- **SC-3:** Business logic in commands: 0 instances of `Bash(command=`, `Task(`, or loop logic
  - Measurement: Grep forbidden patterns per command = 0 matches
- **SC-4:** Lean Orchestration Enforcement section: 100% of refactored commands
  - Measurement: Grep for "Lean Orchestration Enforcement" = 1 match per file
- **SC-5:** Token reduction: >= 40% average per command invocation
  - Measurement: Before/after token comparison during smoke testing
- **SC-6:** Line count reduction: >= 50% average across all refactored commands
  - Measurement: wc -l before vs after
- **SC-7:** Backward compatibility: 100% command invocation syntax unchanged
  - Measurement: Smoke test 3x per command with same arguments
- **SC-8:** Skill size compliance: <= 500 lines per new/extended SKILL.md body
  - Measurement: wc -l for affected SKILL.md files

**Measurement Plan:**
- Baseline: Run `/audit-hybrid` and `/audit-budget` before starting Batch 1
- Per-batch: Run both audits after each batch completes
- Final: Full regression test of all 20 commands + aggregate savings report
- Review frequency: After each batch completion

## Scope

### In Scope

**17 commands to refactor + 1 to delete + 2 new artifacts:**

### Feature 1: Epic Coverage Pipeline Refactoring
- Refactor `validate-epic-coverage.md` (463 lines, 14 blocks -> ~120 lines, <=2 blocks)
- Refactor `create-missing-stories.md` (483 lines, 10 blocks -> ~100 lines, <=2 blocks)
- **Pattern A** (Full Workflow Extraction): Extract gap detection pipeline (gap-detector.sh, generate-report.sh invocations), coverage display formatting, interactive gap resolution (single/multi-select AskUserQuestion sequences), and batch creation orchestration from commands into new skill
- Create NEW skill: `validating-epic-coverage` (gerund naming per ADR-017)
- Create NEW subagent: `epic-coverage-result-interpreter` (display formatting)
- Both commands share the same gap-detection pipeline — refactor together to avoid skill churn
- **Anthropic basis:** "Breaking down complex tasks into smaller, manageable subtasks... each subtask gets Claude's full attention" (chain-complex-prompts.md); "Use workflows for complex tasks" (best-practices.md)
- **Gold standard reference:** `.claude/commands/create-story.md` (73 lines, 1 block)
- **Files to modify:** `.claude/commands/validate-epic-coverage.md`, `.claude/commands/create-missing-stories.md`
- **Files to create:** `.claude/skills/validating-epic-coverage/SKILL.md`, `.claude/skills/validating-epic-coverage/references/`, `.claude/agents/epic-coverage-result-interpreter.md`
- **Estimated points:** 16

### Feature 2: Sprint & Triage Workflow Refactoring
- Refactor `create-sprint.md` (527 lines, 11 blocks -> ~100 lines, <=3 blocks)
- Refactor `recommendations-triage.md` (382 lines, 10 blocks -> ~80 lines, <=2 blocks)
- **Patterns A+C**: Extract story discovery/filtering/capacity calculation (create-sprint), queue reading/display/selection/update (recommendations-triage), and all multi-step AskUserQuestion workflows from commands into skills
- EXTEND skill: `devforgeai-orchestration` Phase 3 (sprint planning logic absorption)
- EXTEND skill: `devforgeai-feedback` with triage mode (recommendations queue management)
- **Prerequisite from architect-reviewer:** Audit and consolidate orchestration skill's 38 reference files before extending (discoverability risk)
- **Anthropic basis:** "Concise is key -- the context window is a public good... every token competes with conversation history" (best-practices.md)
- **Files to modify:** `.claude/commands/create-sprint.md`, `.claude/commands/recommendations-triage.md`, `.claude/skills/devforgeai-orchestration/SKILL.md`, `.claude/skills/devforgeai-feedback/SKILL.md`
- **Estimated points:** 16

### Feature 3: Resume Dev Pre-Flight Extraction
- Refactor `resume-dev.md` (676 lines, 11 blocks -> ~120 lines, <=3 blocks)
- **Pattern B** (Pre-Flight Logic Extraction): Move Phase 1 pre-flight checks (context validation, tech-stack-detector invocation, spec validation), DoD analysis, and auto-detect checkpoint detection from command into skill
- EXTEND skill: `implementing-stories` with resume detection in Phase 0 (or new reference file `references/resume-detection.md`)
- **CRITICAL RISK (architect-reviewer, Impact: CRITICAL):** This is the most critical skill in the framework. `/dev` is the most-used workflow. Resume state detection inherently deals with state from previous invocations, creating tension with architecture-constraints.md's context isolation principle.
- **Mitigation:** Resume logic goes into a NEW reference file (`references/resume-detection.md`), NOT into main SKILL.md. End-to-end regression tests for `/dev` and `/resume-dev` required before and after extraction.
- **Anthropic basis:** "Progressive disclosure -- load detailed materials only when needed" (agent-skills-spec.md Three-Tier Model)
- **Files to modify:** `.claude/commands/resume-dev.md`, `.claude/skills/implementing-stories/SKILL.md` (minimal), `.claude/skills/implementing-stories/references/resume-detection.md` (NEW)
- **Estimated points:** 8

### Feature 4: Skill-Invoking Command Slimming
- Refactor `qa.md` (344 lines, 8 blocks -> ~100 lines, <=3 blocks)
- Refactor `create-ui.md` (675 lines, 8 blocks -> ~100 lines, <=3 blocks)
- Refactor `ideate.md` (374 lines, 7 blocks -> ~90 lines, <=3 blocks)
- **Pattern C** (Multi-Phase Slimming): Move CWD validation + mode inference (qa), context file validation + output verification (create-ui), brainstorm auto-detection + project mode detection + result interpretation + hook integration (ideate) from commands into respective skills' Phase 0
- EXTEND skills: `devforgeai-qa`, `devforgeai-ui-generator`, `discovering-requirements`
- Add "DO NOT" guardrail section to each command following create-story.md gold standard
- **BLOCKING PREREQUISITE (architect-reviewer, Probability: HIGH):** devforgeai-qa SKILL.md is currently 1,012 lines (12 lines OVER the 1,000-line maximum per tech-stack.md lines 375-379). Must extract existing content to `references/` files to bring it under 800 lines BEFORE absorbing qa.md logic.
- **Anthropic basis:** "Concise is key -- the context window is a public good" (best-practices.md)
- **Files to modify:** `.claude/commands/qa.md`, `.claude/commands/create-ui.md`, `.claude/commands/ideate.md`, `.claude/skills/devforgeai-qa/SKILL.md`, `.claude/skills/devforgeai-ui-generator/SKILL.md`, `.claude/skills/discovering-requirements/SKILL.md`
- **Estimated points:** 15

### Feature 5: Documentation-Heavy Command Trimming
- Refactor `create-epic.md` (444 lines, 6 blocks -> ~150 lines, <=3 blocks)
- Refactor `document.md` (284 lines, 6 blocks -> ~100 lines, <=3 blocks)
- Refactor `create-agent.md` (256 lines, 5 blocks -> ~100 lines, <=3 blocks)
- Refactor `rca.md` (448 lines, 5 blocks -> ~120 lines, <=3 blocks)
- Refactor `insights.md` (276 lines, 5 blocks -> ~100 lines, <=3 blocks)
- **Patterns C+E**: Move schema validation (create-epic), template listings (document), mode detection (create-agent), verbose examples (rca ~150 lines), inline help (insights) to reference files or skill Phase 0
- Create reference help files for each trimmed command
- **Anthropic basis:** "Progressive disclosure... SKILL.md serves as overview that points to detailed materials" (best-practices.md)
- **Files to modify:** `.claude/commands/create-epic.md`, `.claude/commands/document.md`, `.claude/commands/create-agent.md`, `.claude/commands/rca.md`, `.claude/commands/insights.md`
- **Files to create:** Reference help files per command
- **Estimated points:** 9

### Feature 6: Special Cases & Cleanup
- Create lightweight skill for `audit-w3.md` (240 lines, 6 blocks -> ~120 lines, <=3 blocks) — **Pattern D** (Standalone Audit to Skill)
- DELETE `dev.backup.md` (confirmed duplicate of dev.md, 258 lines, safe to delete)
- Trim `orchestrate.md` (536 lines, 6 blocks -> ~300 lines, <=3 blocks) — move ~200 lines docs to reference file
- Trim `create-stories-from-rca.md` (264 lines, 6 blocks -> ~180 lines, <=3 blocks) — move help text to reference file
- `fix-story.md` (205 lines, 6 blocks) — **FALSE POSITIVE**: All 6 blocks are legitimate argument validation. NO CHANGE needed.
- **DEPENDENCY CORRECTION (architect-reviewer):** Batch 6 extends devforgeai-orchestration (orchestrate.md trim), which Batch 2 also extends. Batch 6 must wait for Batch 2 to complete — NOT fully parallelizable.
- **Files to modify:** `.claude/commands/audit-w3.md`, `.claude/commands/orchestrate.md`, `.claude/commands/create-stories-from-rca.md`
- **Files to delete:** `.claude/commands/dev.backup.md`
- **Files to create:** `.claude/skills/auditing-w3-compliance/SKILL.md` (gerund naming per ADR-017), reference help files
- **Estimated points:** 10

### Feature 7: Borderline Command Trimming
- Trim `feedback-search.md` (398 lines, 4 blocks -> ~120 lines, <=3 blocks) — **Pattern E**: Move 250+ lines of help/examples to reference file
- `setup-github-actions.md` (132 lines, 4 blocks) — **FALSE POSITIVE**: 132 lines, all blocks are argument validation. NO CHANGE needed.
- **Anthropic basis:** "Progressive disclosure... overview that points to detailed materials" (best-practices.md)
- **Files to modify:** `.claude/commands/feedback-search.md`
- **Files to create:** Reference help file for feedback-search
- **Estimated points:** 3

### Out of Scope

- ❌ `fix-story.md` (6 blocks) — False positive, all blocks are legitimate argument validation — **Never**
- ❌ `setup-github-actions.md` (4 blocks, 132 lines) — False positive, compliant at 132 lines — **Never**
- ❌ 14 warning commands with no Skill() invocation (audit-budget, audit-hooks, audit-hybrid, audit-orphans, chat-search, dev-status, devforgeai-validate, export-feedback, feedback-config, feedback-export-data, feedback-reindex, import-feedback, prompt-version, read-constitution, validate-stories, worktrees) — **Phase 2: Separate epic for standalone command refactoring**
- ❌ Updating audit-hybrid script threshold — **Post-MVP: After baseline established**
- ❌ ADR-019 skill restructure execution — **Separate initiative, sequencing decision required**

## Target Sprints

### Sprint 1: Critical Batches (Sequential)
**Goal:** Refactor the 5 worst violators and establish patterns for remaining batches
**Estimated Points:** 40 (Features 1 + 2 + 3)
**Features:**
- Feature 1: Epic Coverage Pipeline (16 pts) — NEW skill + subagent
- Feature 2: Sprint & Triage (16 pts) — EXTEND 2 skills
- Feature 3: Resume Dev (8 pts) — EXTEND critical skill

**Key Deliverables:**
- validating-epic-coverage skill created and operational
- epic-coverage-result-interpreter subagent created
- 5 critical commands refactored (validate-epic-coverage, create-missing-stories, create-sprint, recommendations-triage, resume-dev)
- ADR-020 created (structural changes authorization)

### Sprint 2: High Violations (Parallelizable)
**Goal:** Refactor remaining high-violation commands in parallel
**Estimated Points:** 24 (Features 4 + 5)
**Features:**
- Feature 4: Skill-Invoking Command Slimming (15 pts)
- Feature 5: Documentation-Heavy Command Trimming (9 pts)

**Key Deliverables:**
- devforgeai-qa SKILL.md reduced to under 800 lines (prerequisite)
- 8 additional commands refactored
- Reference help files created

### Sprint 3: Cleanup & Verification
**Goal:** Handle special cases, delete duplicate, run full regression
**Estimated Points:** 13 (Features 6 + 7)
**Features:**
- Feature 6: Special Cases & Cleanup (10 pts)
- Feature 7: Borderline Command Trimming (3 pts)

**Key Deliverables:**
- auditing-w3-compliance skill created
- dev.backup.md deleted
- feedback-search help extracted
- Full `/audit-hybrid` regression: 0 violations
- Full `/audit-budget` regression: all under 15K
- Aggregate token savings report

## User Stories

High-level user stories decomposed from features:

1. **As a** framework maintainer, **I want** all commands to follow the lean orchestration pattern, **so that** business logic lives exclusively in skills and subagents
2. **As a** Claude session, **I want** commands to use minimal context window tokens, **so that** more tokens are available for actual work
3. **As a** framework auditor, **I want** `/audit-hybrid` to pass with zero violations, **so that** I can trust all commands are architecturally compliant
4. **As a** developer, **I want** command invocation syntax to remain unchanged, **so that** existing workflows and documentation remain valid

*Note: Each feature decomposes into 1-3 detailed stories via `/create-story EPIC-071`*

## Technical Considerations

### Architecture Impact
- 2 new skills created: `validating-epic-coverage`, `auditing-w3-compliance` (gerund naming per ADR-017)
- 1 new subagent created: `epic-coverage-result-interpreter`
- 8 existing skills extended (devforgeai-orchestration, devforgeai-feedback, implementing-stories, devforgeai-qa, devforgeai-ui-generator, discovering-requirements, designing-systems, devforgeai-rca)
- 1 command deleted: `dev.backup.md`
- 17 commands refactored (command files only — skills receive extracted logic)
- Multiple reference help files created for trimmed commands
- **Dual-path architecture:** All changes must apply to both `src/claude/` and `.claude/` trees

### Technology Decisions
- No new technologies introduced — all work uses existing Markdown, YAML, and shell scripts
- Follows existing Agent Skills Specification v1.0 for new skill creation
- Uses existing lean orchestration protocol patterns (proven in 5 prior refactorings)

### Architectural Risks (from architect-reviewer, complexity 7.5/10)

**Risk 1: devforgeai-qa SKILL.md Size Ceiling (Probability: HIGH, Impact: HIGH)**
- Current: 1,012 lines (12 lines OVER 1,000-line maximum per tech-stack.md)
- Must reduce to under 800 lines BEFORE Feature 4 can extend it
- Mitigation: Extract existing content to references/ files first

**Risk 2: ADR-019 Collision (Probability: HIGH, Impact: MEDIUM)**
- ADR-019 moves ~3,935 lines between devforgeai-orchestration and designing-systems
- Features 2 and 4 extend the same skills ADR-019 modifies
- Mitigation: Establish sequencing contract — either ADR-019 completes first or this epic completes first

**Risk 3: implementing-stories Regression (Probability: MEDIUM, Impact: CRITICAL)**
- Feature 3 extends the most critical skill (used by /dev, the most-used workflow)
- Resume state detection creates tension with context isolation principle
- Mitigation: Resume logic in NEW reference file, not SKILL.md. Regression tests required.

**Risk 4: source-tree.md Update Cascade (Probability: HIGH, Impact: MEDIUM)**
- New skills/subagents require updating LOCKED context files (source-tree.md)
- Mitigation: Single umbrella ADR-020 authorizing all structural changes

**Risk 5: Dual-Path Architecture (Probability: MEDIUM, Impact: MEDIUM)**
- 20 commands + 8 skills = 56+ file modifications across both src/ and .claude/ trees
- Mitigation: Edit src/ first, test against src/, sync to .claude/ last

### Security & Compliance
- No security changes — refactoring is structural, not behavioral
- All commands maintain identical user-facing behavior (backward compatibility)
- No new external dependencies introduced

### Performance Requirements
- Per-command token reduction: >= 40% in main conversation
- Per-command character budget: <= 12K target, <= 15K hard limit
- New SKILL.md files: <= 500 lines (Anthropic Agent Skills Spec recommendation)

## Dependencies

### Internal Dependencies
- [x] **Lean Orchestration Protocol:** `devforgeai/protocols/lean-orchestration-pattern.md` exists with templates and case studies
  - **Status:** Complete
  - **Impact if delayed:** N/A

- [ ] **ADR-020 (Structural Changes Authorization):** Must authorize new skills, new subagents, source-tree.md updates, dev.backup.md deletion
  - **Status:** Not Started (create before Feature 1)
  - **Impact if delayed:** Blocks Features 1, 6 (new skill creation)

- [ ] **devforgeai-qa SKILL.md Size Reduction:** Must reduce from 1,012 to under 800 lines
  - **Status:** Not Started (prerequisite for Feature 4)
  - **Impact if delayed:** Blocks Feature 4

- [ ] **ADR-019 Sequencing Decision:** Determine if ADR-019 executes before or after this epic
  - **Status:** Not Started (sequencing decision needed)
  - **Impact if delayed:** Risk of merge conflicts in Features 2, 4

### External Dependencies
- None (all work is internal to the DevForgeAI framework)

## Risks & Mitigation

### Risk 1: devforgeai-qa Size Ceiling
- **Probability:** High
- **Impact:** High
- **Mitigation:** Extract existing content to references/ files before Feature 4 starts
- **Contingency:** If extraction proves complex, defer qa.md refactoring to a follow-up epic

### Risk 2: ADR-019 Collision
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Establish sequencing contract with ADR-019 before starting Feature 2
- **Contingency:** If collision unavoidable, resolve merge conflicts at batch boundaries

### Risk 3: implementing-stories Regression
- **Probability:** Medium
- **Impact:** Critical
- **Mitigation:** Regression tests before/after Feature 3; resume logic in reference file, not SKILL.md
- **Contingency:** Revert Feature 3 if regression detected; keep resume-dev.md as-is

### Risk 4: Batch 6 Parallelization Incorrect
- **Probability:** High
- **Impact:** Medium
- **Mitigation:** Corrected sequencing: Batch 6 depends on Batch 2 (both modify orchestration). Only Batches 4, 5, 7 are truly parallel.
- **Contingency:** If parallelization needed, split Batch 6's orchestrate.md trim from the rest

### Risk 5: Naming Convention Non-Compliance
- **Probability:** High (original plan used non-gerund names)
- **Impact:** Low
- **Mitigation:** Corrected per ADR-017: `validating-epic-coverage` (not devforgeai-epic-validation), `auditing-w3-compliance` (not devforgeai-w3-audit)

## Stakeholders

### Primary Stakeholders
- **Framework Owner:** Approves refactoring patterns, batch sequencing, false positive classifications
- **DevForgeAI AI Agent:** Executes /dev and /qa workflows, maintains backward compatibility

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════════
Week 1-3:  Sprint 1 - Critical Batches (Features 1, 2, 3)
           Sequential: F1 → F2 → F3
           Prerequisites: ADR-020, baseline audit
Week 4-5:  Sprint 2 - High Violations (Features 4, 5)
           Parallel: F4 || F5
           Prerequisites: devforgeai-qa size reduction
Week 6-7:  Sprint 3 - Cleanup & Verification (Features 6, 7)
           F6 after F2 complete; F7 parallel
           Final: Full regression + savings report
════════════════════════════════════════════════════════════════
Total Duration: ~7 weeks
Target Release: 2026-04-15
```

### Key Milestones
- [ ] **M1:** ADR-020 created and approved (before Feature 1 starts)
- [ ] **M2:** Feature 1 complete — new skill operational, 2 critical commands refactored
- [ ] **M3:** Features 1-3 complete — 5 critical commands refactored (end Sprint 1)
- [ ] **M4:** devforgeai-qa reduced to under 800 lines (prerequisite for Sprint 2)
- [ ] **M5:** Features 4-5 complete — 8 additional commands refactored (end Sprint 2)
- [ ] **M6:** All features complete, `/audit-hybrid` exits 0, savings report generated (end Sprint 3)

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | In Progress | 40 | 5 | 1 | 0 | 0 |
| Sprint 2 | Not Started | 24 | 6 | 0 | 0 | 0 |
| Sprint 3 | Not Started | 13 | 3 | 0 | 0 | 0 |
| **Total** | **21%** | **77** | **14** | **1** | **0** | **0** |

### Burndown
- **Total Points:** 77
- **Completed:** 16
- **Remaining:** 61

## Verification Plan

### Per-Command (after each refactoring)
1. `/audit-hybrid` — command shows <=4 blocks before Skill()
2. Grep for forbidden patterns: `Bash(command=`, `Task(`, `FOR .* in .*:` — 0 matches
3. Grep for required pattern: `Skill(command=` — exactly 1 match
4. Verify `## Lean Orchestration Enforcement` section exists with "DO NOT" guardrails
5. Character count < 12,000 (target) / < 15,000 (hard limit)
6. Smoke test 3x with valid arguments

### Per-Batch (after completing each feature)
1. Run `/audit-hybrid` — all batch commands pass
2. Compare before/after token usage
3. Verify dual-path sync (src/ matches .claude/)

### Final (all features complete)
1. `/audit-hybrid` shows 0 violations (exit code 0)
2. `/audit-budget` shows all commands under 15K
3. Full regression: invoke all 20 commands once with valid input
4. Aggregate token savings report across all refactored commands

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `devforgeai/specs/requirements/hybrid-command-lean-orchestration-requirements.md` | Full requirements with all audit data, patterns, and Anthropic citations |
| `.claude/plans/piped-baking-crystal.md` | Original refactoring roadmap plan |
| `devforgeai/protocols/lean-orchestration-pattern.md` | Lean orchestration constitutional protocol with case studies |
| `.claude/commands/create-story.md` | Gold standard command (73 lines, 1 block) — reference for all refactored commands |
| `.claude/commands/dev.md` | Successfully refactored command (527→131 lines, STORY-051) |
| `.claude/scripts/audit-command-skill-overlap.sh` | Audit script for verification |
| `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` | Anthropic Agent Skills Best Practices |
| `.claude/skills/claude-code-terminal-expert/references/skills/agent-skills-spec.md` | Agent Skills Specification v1.0 |
| `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-complex-prompts.md` | Anthropic Prompt Chaining Guidance |

## Refactoring Patterns Reference

Commands must be refactored using one of these 5 approved patterns. Each pattern's extraction steps and Anthropic citations are fully documented in REQ-071 (`devforgeai/specs/requirements/hybrid-command-lean-orchestration-requirements.md`, field: `refactoring_patterns`).

| Pattern | Name | For | Commands |
|---------|------|-----|----------|
| **A** | Full Workflow Extraction | Embedded validation + display + interaction | validate-epic-coverage, create-missing-stories, create-sprint, recommendations-triage |
| **B** | Pre-Flight Logic Extraction | Inline pre-flight validation / DoD parsing | resume-dev |
| **C** | Multi-Phase Slimming | Excessive pre/post-skill logic | ideate, create-epic, create-ui, document, create-agent, rca, insights, qa |
| **D** | Standalone Audit to Skill | Audit commands without skill delegation | audit-w3 |
| **E** | Documentation Trimming | Bloated help text / examples / error handling | feedback-search, orchestrate, create-stories-from-rca, rca, insights, create-epic, document, create-agent |

## Gold Standard Command Template

All refactored commands must follow this structure (reference: `.claude/commands/create-story.md`):

```markdown
---
description: [Brief]
argument-hint: [args]
model: opus
allowed-tools: Glob, Skill, AskUserQuestion
---

# /command-name - Title

[One-line description.]

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- [4-5 explicitly forbidden actions specific to this command]

**DO (command responsibilities only):**
- Validate argument format
- Set context markers
- Invoke skill immediately after validation

## Phase 0: Argument Validation

[1-2 code blocks max: regex validation + AskUserQuestion fallback]

## Phase 1: Invoke Skill

Skill(command="target-skill")

**Skill handles ALL workflow.**

## Error Handling

[Table, 3-5 rows max]

## References

- Skill: [path]
- Pattern: devforgeai/protocols/lean-orchestration-pattern.md

**Command follows lean orchestration: Validate -> Set markers -> Invoke skill**
```

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-20
**Complexity Score:** 7.5/10 (architect-reviewer assessment)
**Source:** REQ-071 requirements + /audit-hybrid results + Anthropic documentation analysis
