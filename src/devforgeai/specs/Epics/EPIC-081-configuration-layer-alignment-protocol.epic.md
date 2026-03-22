---
id: EPIC-081
title: Configuration Layer Alignment Protocol
status: Planning
start_date: 2026-02-22
target_date: 2026-03-14
total_points: 16
completed_points: 0
created: 2026-02-22
owner: Framework Owner
tech_lead: DevForgeAI AI Agent
team: DevForgeAI

source_requirements: "devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md"
source_brainstorm: "devforgeai/specs/brainstorms/BRAINSTORM-012-configuration-layer-alignment-protocol.brainstorm.md"
complexity_score: 32
complexity_tier: "Tier 2 - Moderate (32/60)"
architecture_review_complexity: "3/10 post-mitigation"
---

# Epic: Configuration Layer Alignment Protocol

## Business Goal

Eliminate cross-layer configuration drift and contradictions by codifying a 5-step validation methodology (CLAP) as automated framework tooling. No existing validator checks CLAUDE.md, the system prompt, or rules against context files — and none checks context files against each other.

**Evidence (from ENH-CLAP-001 investigation on GPUXtend project):**

During GPUXtend system prompt tuning, a manual 5-step reasoning process uncovered 5 HIGH-severity gaps:

| Finding | Severity | Layers |
|---------|----------|--------|
| `std::call_once` described as implementation pattern but FORBIDDEN in anti-patterns.md | HIGH | CLAUDE.md vs anti-patterns.md |
| No platform constraint in system prompt | HIGH | System prompt vs tech-stack.md |
| No build system routing in system prompt | HIGH | System prompt vs tech-stack.md |
| No subagent routing for C++ native layer | HIGH | System prompt vs architecture-constraints.md |
| No sprint state awareness | MEDIUM | System prompt vs architecture-constraints.md |

**Root Cause:** All existing validators (context-validator, tech-stack-detector, /validate-stories, context-preservation-validator, /audit-orphans) check in ONE direction only. None performs cross-layer pairwise comparison.

**Value delivered:**
- Automated detection of configuration contradictions (wrong AI behavior)
- Automated detection of configuration gaps (suboptimal AI delegation)
- ADR propagation drift monitoring
- Integrated validation in /create-context workflow (Phase 5.5)

**Source provenance:** ENH-CLAP-001 → Requirements spec (clap-configuration-layer-alignment-requirements.md) → This epic

## Success Metrics

- **SC-1:** Contradiction detection precision >90% — Test with known CLAUDE.md vs anti-patterns contradictions
- **SC-2:** False positive rate 0% for prose similarity — Verify exact claim matching, not semantic similarity
- **SC-3:** Validation check completeness: 15/15 checks implemented — Audit against validation matrix
- **SC-4:** Phase 5.5 blocking behavior: 100% block on HIGH contradictions — Test with HIGH severity finding
- **SC-5:** /audit-alignment JSON output: 100% schema compliance — Validate against Appendix A schema
- **SC-6:** Audit execution time <60 seconds full audit — Performance benchmark

**Measurement Plan:**
- Baseline: Manual audit of current DevForgeAI project as ground truth
- Per-story: Smoke test each deliverable against DevForgeAI's own configuration layers
- Final: Full `/audit-alignment` run against DevForgeAI project, verify all 15 checks execute
- Review frequency: After each story completion

## Scope

### In Scope

### Feature 1: alignment-auditor Subagent + Validation Matrix (Foundation)
- Create read-only validator subagent using canonical agent template v2.0.0
- Model: haiku (text comparison, not code generation)
- Tools: Read, Glob, Grep only (read-only)
- Core agent file ≤500 lines per ADR-012 progressive disclosure
- Implements all 15 validation checks: CC-01 through CC-10 (contradiction), CMP-01 through CMP-04 (completeness), ADR-01 (propagation)
- Validation matrix in progressive-disclosure reference file (loaded on-demand)
- Structured JSON output per Appendix A schema in requirements spec
- Distinguishes contradictions (wrong behavior) from gaps (suboptimal behavior)
- Reports line numbers for all findings; proposes resolutions respecting layer mutability
- **Files to create:** `.claude/agents/alignment-auditor.md`, `.claude/agents/alignment-auditor/references/validation-matrix.md`
- **Pattern reference:** `.claude/agents/context-validator.md` (similar read-only validator)
- **Acceptance criteria guidance:** 12 ACs covering template compliance, model, tools, line limit, checks, input handling, output schema, resolution proposals, exact text matching
- **Estimated points:** 5

### Feature 2: /audit-alignment Command
- Lean orchestration command: validate args → set markers → invoke alignment-auditor subagent
- Character budget ≤10,000 (67% of 15K limit)
- Supports `--layer` argument: all (default), claudemd, prompt, context, rules, adrs
- Supports `--fix` argument: proposes edits for MUTABLE layers, requires AskUserQuestion approval per edit
- Supports `--output` argument: console (default), file (writes to `devforgeai/qa/alignment-audit-{date}.md`)
- Severity-based display (CRITICAL/HIGH/MEDIUM/LOW)
- Executive summary table showing counts per category
- `--fix` enforces mutability rules: context files → flag for ADR (never auto-fix); CLAUDE.md/rules → propose edits; ADRs → recommend new ADR
- **Files to create:** `.claude/commands/audit-alignment.md`
- **Pattern reference:** `.claude/commands/audit-orphans.md` (lean orchestration audit pattern)
- **Acceptance criteria guidance:** 8 ACs covering lean orchestration, character budget, argument parsing, fix workflow, output formatting
- **Estimated points:** 3

### Feature 3: Phase 5.5 Workflow Integration
- Create Phase 5.5 "Prompt Alignment" reference file for designing-systems skill (~200 lines)
- Modify SKILL.md to add ~30-40 line Phase 5.5 entry between Phase 5 and Phase 6
- Phase 5.5 reads CLAUDE.md and system-prompt-core.md (graceful handling if missing)
- Invokes alignment-auditor subagent with freshly-created context files
- HIGH contradictions block Phase 6 (mandatory resolution)
- MEDIUM/LOW contradictions deferrable with justification
- System prompt gaps are informational (project may choose not to use system prompt)
- Graceful degradation: if alignment-auditor fails or returns malformed JSON, display WARNING and proceed to Phase 6 without blocking
- User escape hatch: for disputed HIGH findings, AskUserQuestion presents "Override with justification" option; override recorded as ACCEPTED_RISK
- Synthesizes `<project_context>` section from context files when system prompt gaps detected
- **Files to create:** `.claude/skills/designing-systems/references/prompt-alignment-workflow.md`
- **Files to modify:** `.claude/skills/designing-systems/SKILL.md`
- **Acceptance criteria guidance:** 13 ACs covering naming, progressive disclosure, input handling, subagent invocation, blocking behavior, deferral, informational mode, graceful degradation, user override
- **Estimated points:** 3

### Feature 4: ADR-021 Decision Record (Day 0 Prerequisite)
- Architecture Decision Record documenting CLAP methodology and integration
- Context: validation gap (no cross-layer checking exists today)
- Decision: 5-step methodology, new subagent, new command, Phase 5.5 integration
- Rationale: alignment-auditor separate from context-validator (single responsibility, different model requirements)
- Consequences: trigger points, where CLAP does NOT run, mutability rules
- **CRITICAL:** Authorizes source-tree.md updates for all new CLAP files (subagent, reference, command, skill reference)
- **CRITICAL:** Documents alignment-auditor vs context-validator boundary to prevent future SRP drift
- References ENH-CLAP-001 and requirements specification
- **Files to create:** `devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md`
- **Acceptance criteria guidance:** 8 ACs covering ADR number, status, content sections, source-tree authorization clause, SRP boundary, references
- **Estimated points:** 2

### Feature 5: Documentation & Memory File Updates
- `.claude/memory/commands-reference.md` — Add /audit-alignment entry to Framework Maintenance section
- `.claude/memory/subagents-reference.md` — Add alignment-auditor entry to catalog (alphabetical) + proactive trigger mapping
- `.claude/memory/skills-reference.md` — Update designing-systems entry to include Phase 5.5
- CLAUDE.md subagent registry — Trigger regeneration or manually update `<!-- BEGIN SUBAGENT REGISTRY -->` block
- Verify reference accuracy before writing (all referenced artifacts must exist)
- **Files to modify:** 3 memory files + CLAUDE.md registry block
- **Acceptance criteria guidance:** 4 ACs covering commands-reference, subagents-reference, skills-reference, CLAUDE.md registry
- **Estimated points:** 3

### Out of Scope

- ❌ Domain Reference Generation epic (depends on CLAP but is a separate downstream epic)
- ❌ `/audit-alignment --generate-refs` flag (deferred to Domain Reference Generation epic)
- ❌ Automated CLAP during `/dev` or `/qa` workflows (too frequent; context-validator handles per-commit)
- ❌ Semantic/prose similarity matching (exact text matching only per FR-001 AC12)
- ❌ Auto-fixing IMMUTABLE context files (contradictions in context files require ADR creation)

## Target Sprints

### Sprint 1: CLAP Foundation & Delivery
**Goal:** Complete all CLAP deliverables in a single sprint
**Estimated Points:** 16
**Execution Order:**

**Day 0: Prerequisite**
- Feature 4: ADR-021 (2 pts) — Authorizes all structural changes before implementation

**Days 1-3: Foundation**
- Feature 1: alignment-auditor subagent + validation matrix (5 pts) — Core validation engine

**Days 4-6: Consumer Artifacts (Parallel)**
- Feature 2: /audit-alignment command (3 pts) — On-demand user interface
- Feature 3: Phase 5.5 integration (3 pts) — Automatic /create-context integration

**Days 7-8: Documentation**
- Feature 5: Memory file updates (3 pts) — Discoverability and registry

**Key Deliverables:**
- ADR-021 accepted with source-tree.md authorization
- alignment-auditor subagent operational with 15 validation checks
- /audit-alignment command passes lean orchestration audit
- Phase 5.5 inserted into designing-systems skill
- All memory files and CLAUDE.md registry updated

## User Stories

1. **As a** framework maintainer, **I want** a read-only subagent that performs pairwise comparison across all configuration layers, **so that** contradictions and gaps are detected automatically with structured evidence
2. **As a** framework maintainer, **I want** an on-demand audit command with layer filtering and fix proposals, **so that** I can check alignment at any time and resolve drift
3. **As a** developer running /create-context, **I want** automatic alignment checking after context files are created, **so that** CLAUDE.md and system prompt are aligned with new context files before epic creation
4. **As a** framework user, **I want** the commands-reference, subagents-reference, and skills-reference updated, **so that** /audit-alignment, alignment-auditor, and Phase 5.5 are discoverable

*Note: Each feature decomposes into 1 detailed story via `/create-story EPIC-081`. Feature 1 combines FR-001 + FR-002 into a single atomic story.*

## Technical Considerations

### Architecture Impact
- 1 new subagent: `alignment-auditor` (haiku model, read-only tools)
- 1 new subagent reference: `alignment-auditor/references/validation-matrix.md`
- 1 new command: `audit-alignment.md` (lean orchestration pattern)
- 1 new skill reference: `designing-systems/references/prompt-alignment-workflow.md`
- 1 skill modified: `designing-systems/SKILL.md` (Phase 5.5 insertion, ~30-40 lines added)
- 1 new ADR: ADR-021
- 3 memory files updated + CLAUDE.md registry block

### Technology Decisions
- **No new technologies** — all work uses existing Markdown, JSON schema, and Claude Code native tools
- **Model choice:** haiku for alignment-auditor (text comparison, not code generation — cost-efficient)
- **Output format:** JSON (machine-parseable, structured evidence) + Markdown (human-readable reports)
- **Pattern adherence:** Lean orchestration for command, progressive disclosure for subagent, canonical template v2.0.0

### Architecture Patterns Used

| Pattern | Component | Reference |
|---------|-----------|-----------|
| Progressive Disclosure | alignment-auditor + references/ | ADR-012, established de facto with 60+ reference files |
| Lean Orchestration | /audit-alignment command | audit-orphans.md precedent |
| Read-only Subagent | alignment-auditor tools | context-validator, dead-code-detector precedent |
| Phase Insertion | designing-systems Phase 5.5 | On-demand reference loading |
| Severity Hierarchy | HIGH blocks / MEDIUM defers | Consistent with QA validation patterns |

### Security & Compliance
- alignment-auditor has NO Write/Edit tools (read-only by design)
- Audit report contains file paths and line numbers, not secrets
- `--fix` requires AskUserQuestion approval for every proposed change (never auto-edits)
- Context files are IMMUTABLE — `--fix` flags for ADR creation, cannot auto-fix

### Performance Requirements
- Full audit execution: <60 seconds
- Per-check execution: <4 seconds average (15 checks × 4s = 60s budget)
- Memory footprint: Standard haiku context (bounded by 6 context files + CLAUDE.md + system prompt)

## Dependencies

### Internal Dependencies
- [x] **Context files (6/6):** All exist in `devforgeai/specs/context/` — Required input for alignment-auditor
  - **Status:** Complete
  - **Impact if delayed:** N/A

- [x] **Canonical agent template v2.0.0:** Exists in agent-generator references — Required for alignment-auditor creation
  - **Status:** Complete
  - **Impact if delayed:** N/A

- [x] **Lean orchestration protocol:** Exists at `devforgeai/protocols/lean-orchestration-pattern.md` — Required for /audit-alignment
  - **Status:** Complete
  - **Impact if delayed:** N/A

- [x] **ADR-012 progressive disclosure pattern:** De facto standard with 60+ agent reference files — Required for validation-matrix.md
  - **Status:** Proposed (ADR status) but de facto established in practice
  - **Impact if delayed:** None — pattern already used by 20+ agents

### Feature-Level Dependencies

```
Feature 4 (ADR-021)         [Day 0 — prerequisite, authorizes source-tree.md]
        |
        v
Feature 1 (alignment-auditor + matrix)    [Days 1-3 — foundation]
        |
   +----+----+
   v         v
Feature 2  Feature 3     [Days 4-6 — parallel, both consume alignment-auditor]
(command)  (Phase 5.5)
   |         |
   +----+----+
        |
        v
Feature 5 (Documentation)    [Days 7-8 — documents deliverables from F1-F4]
```

**Critical Path:** F4 → F1 → F2 + F3 (parallel) → F5

### External Dependencies
- None (all work is internal to the DevForgeAI framework)

### Cross-Epic Dependencies
- **Downstream:** Domain Reference Generation epic depends on CLAP being implemented first (Phase 5.7 depends on Phase 5.5; `--generate-refs` flag depends on /audit-alignment)
- **Upstream:** None — CLAP has no upstream epic dependencies

## Risks & Mitigation

### Risk 1: False Positives from Text Similarity
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Exact claim matching only (FR-001 AC12) — no semantic/prose similarity. Pattern name and technology name extraction from structured sections only.
- **Contingency:** If false positives detected, refine check patterns in validation-matrix.md (reference file, not hardcoded in agent prompt)

### Risk 2: Phase 5.5 Slows /create-context
- **Probability:** Low
- **Impact:** Low
- **Mitigation:** Opt-out when neither CLAUDE.md nor system-prompt-core.md exists (FR-004 AC8 — informational, not blocking). Graceful degradation on subagent failure (AC-12 — WARNING, proceed to Phase 6).
- **Contingency:** User can override disputed HIGH findings with justification (ACCEPTED_RISK)

### Risk 3: Token Cost of Loading All Layers
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** haiku model keeps costs low. CC-10 (cross-context comparison) bounded by 6 files. `--layer` filter enables targeted audits.
- **Contingency:** If context files grow beyond 50K chars total, CC-10 switches to targeted Grep patterns

### Risk 4: Validation Matrix Incompleteness
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Start with 15 well-defined checks (enumerated in requirements). Matrix stored in reference file for easy extension.
- **Contingency:** Add new checks via reference file updates (no agent prompt changes needed)

### Risk 5: SKILL.md Modification Risk
- **Probability:** Low
- **Impact:** Medium (touches active, frequently-invoked skill)
- **Mitigation:** Surgical insertion (~30-40 lines) between Phase 5 and Phase 6. Phase 5.5 uses on-demand reference loading (not inlined). Authorized by ADR-021.
- **Contingency:** Revert SKILL.md insertion if regression detected in /create-context workflow

## Stakeholders

### Primary Stakeholders
- **Framework Owner:** Approves ADR-021, reviews alignment-auditor output, validates Phase 5.5 integration
- **DevForgeAI AI Agent:** Executes /create-context workflow with Phase 5.5, uses /audit-alignment for drift detection

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════════
Day 0:     ADR-021 (prerequisite — authorizes all structural changes)
Days 1-3:  Feature 1 — alignment-auditor + validation matrix (foundation)
Days 4-6:  Feature 2 + Feature 3 (parallel — command + Phase 5.5)
Days 7-8:  Feature 5 — Documentation & memory file updates
Day 9:     Full regression: /audit-alignment against DevForgeAI project
════════════════════════════════════════════════════════════════
Total Duration: ~2 weeks (1 sprint)
Target Release: 2026-03-14
```

### Key Milestones
- [ ] **M1:** ADR-021 accepted with source-tree.md authorization (Day 0)
- [ ] **M2:** alignment-auditor operational — 15/15 checks execute against DevForgeAI (Day 3)
- [ ] **M3:** /audit-alignment command passes lean orchestration audit (Day 6)
- [ ] **M4:** Phase 5.5 integrated — /create-context workflow includes alignment check (Day 6)
- [ ] **M5:** All documentation updated, CLAUDE.md registry regenerated (Day 8)
- [ ] **M6:** Full audit run against DevForgeAI project — schema-compliant JSON output (Day 9)

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 16 | 5 | 0 | 0 | 0 |
| **Total** | **0%** | **16** | **5** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 16
- **Completed:** 0
- **Remaining:** 16

## Verification Plan

### Per-Story Verification
1. **ADR-021:** Verify source-tree.md authorization clause, correct ADR number, Accepted status
2. **alignment-auditor:** Verify 15/15 checks execute, JSON schema compliance, ≤500 lines, haiku model
3. **/audit-alignment:** Verify lean orchestration (≤10K chars, ≤4 code blocks), --layer/--fix/--output flags work
4. **Phase 5.5:** Verify insertion point between Phase 5 and Phase 6, reference loading works, HIGH blocks Phase 6, graceful degradation on failure
5. **Documentation:** Verify all 3 memory files updated, CLAUDE.md registry includes alignment-auditor

### Final Verification
1. Run `/audit-alignment` against DevForgeAI project — verify schema-compliant JSON output
2. Run `/audit-alignment --layer=claudemd` — verify targeted audit works
3. Verify Phase 5.5 executes correctly in a `/create-context` dry run
4. Confirm all 15 validation checks produce findings or PASS (no silent skips)

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md` | Full requirements with validation matrix, JSON schema, examples |
| `devforgeai/specs/brainstorms/BRAINSTORM-012-configuration-layer-alignment-protocol.brainstorm.md` | Original proposal (1,264 lines) |
| `.claude/agents/context-validator.md` | Read-only validator subagent pattern reference |
| `.claude/commands/audit-orphans.md` | Lean orchestration audit command pattern reference |
| `.claude/agents/agent-generator/references/canonical-agent-template.md` | Canonical agent template v2.0.0 |
| `devforgeai/specs/adrs/ADR-020-structural-changes-authorization.md` | ADR authorization precedent |

## Retrospective (Post-Epic)

*To be completed after epic completes*

### What Went Well
- [To be filled]

### What Could Be Improved
- [To be filled]

### Lessons Learned
- [To be filled]

### Metrics Achieved
- **SC-1 (Contradiction precision):** [Actual vs >90% target]
- **SC-2 (False positive rate):** [Actual vs 0% target]
- **SC-3 (Check completeness):** [Actual vs 15/15 target]
- **SC-4 (Phase 5.5 blocking):** [Actual vs 100% target]
- **SC-5 (JSON schema):** [Actual vs 100% target]
- **SC-6 (Execution time):** [Actual vs <60s target]

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-22
**Complexity Score:** 32/60 (Tier 2 — Moderate), 3/10 post-mitigation (architect-reviewer)
**Source:** ENH-CLAP-001 → Requirements spec → requirements-analyst validation → architect-reviewer assessment
