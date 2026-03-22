---
id: EPIC-068
title: "Skill Responsibility Restructure & ADR-017 Rename Migration"
status: Planning
start_date: 2026-02-17
target_date: 2026-04-13
total_points: 42
completed_points: 0
created: 2026-02-17
owner: DevForgeAI Framework Team
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: "N/A - originated from EPIC-067 conformance analysis and ADR-019 architectural decision"
---

# Epic: Skill Responsibility Restructure & ADR-017 Rename Migration

## Business Goal

Restructure the brainstorming/ideation/architecture skill boundaries to enforce single-responsibility per professional role (BA/PM/Architect), then execute ADR-017 gerund renames for all three skills. This eliminates the dual-responsibility anti-pattern in the ideation skill (28 reference files / ~13,345 lines) and establishes a clean handoff chain: brainstorm.md → requirements.md → epic.md.

**Problem:** The `devforgeai-ideation` skill currently performs both PM work (requirements elicitation) and Architect work (epic decomposition, feasibility analysis, complexity assessment). Additionally, the `devforgeai-orchestration` skill owns the entire epic creation workflow (Phase 4A: 7 files, ~3,770 lines) that properly belongs in the architecture skill. This creates a triple-ownership problem: ideation owns epic analysis, orchestration owns the epic creation engine, and architecture — the natural owner — has zero epic content. The conformance analysis (EPIC-067, Finding 3.3) flagged the ideation scope as a design concern, and the two skills have overlapping feature decomposition patterns and incompatible complexity scoring scales (ideation: 0-60, orchestration: 0-10).

**Value:** Clean role separation improves skill maintainability, reduces token footprint per invocation, enables independent conformance improvements, and aligns the workflow with real-world PM/Architect responsibilities.

**References:**
- ADR-017: Skill Gerund Naming Convention (rename authorization)
- ADR-019: Skill Responsibility Restructure (responsibility migration authorization)
- EPIC-067: Ideation Anthropic Conformance Remediation (Finding 3.3)
- EPIC-065: Skill Gerund Naming Convention Migration (broader rename initiative)

## Success Metrics

- **Metric 1:** Ideation skill reference files reduced from 28 to ≤22 after migration
- **Metric 2:** All three skills renamed per ADR-017 (zero `devforgeai-` prefixed skill directories remain for these 3 skills)
- **Metric 3:** Handoff chain functional: `/brainstorm` → `/ideate` (produces YAML-structured requirements.md) → `/create-epic` (produces epic.md)
- **Metric 6:** Requirements.md uses YAML-structured schema with locked decisions — zero narrative prose in decision fields
- **Metric 4:** Zero stale `devforgeai-ideation`, `designing-systems`, or `devforgeai-brainstorming` references in codebase after sweep
- **Metric 5:** No regression — all existing workflows continue to function

**Measurement Plan:**
- Tracked via story completion in `devforgeai/specs/Stories/`
- Post-migration Grep sweep confirms zero stale references
- Functional test: run `/ideate test idea` and `/create-epic test` after each sprint

## Scope

### In Scope

12 features implementing the responsibility restructure, epic creation migration, structured requirements schema, and rename across 4 sprints.

**Primary skills affected:**
- `.claude/skills/devforgeai-orchestration/` (Phase 4A epic creation — 7 files, ~3,770 lines to migrate out)
- `.claude/skills/devforgeai-ideation/` (372 lines SKILL.md + 28 reference files — 6 files, ~2,935 lines to migrate out)
- `.claude/skills/designing-systems/` (279 lines SKILL.md + 13 reference files — receiving skill)
- `.claude/skills/devforgeai-brainstorming/` (SKILL.md + templates — rename only)

**Primary commands affected:**
- `.claude/commands/create-epic.md` (currently routes to orchestration — must re-route to architecture)
- `.claude/commands/ideate.md` (567 lines — output changes from epic to requirements)

### Features

1. **Feature 1: Move Epic Creation References from Orchestration to Architecture** (Sprint 1)
   - Description: Transfer the entire Phase 4A epic creation engine (7 reference files + template) from `devforgeai-orchestration/references/` to `designing-systems/references/`
   - User Value: Architecture skill owns the epic creation workflow — the architect creates epics, not the coordinator
   - Estimated Points: 5
   - Files Moved:
     - `epic-management.md` (514 lines) — Phase 4A.1-2 discovery & context
     - `feature-decomposition-patterns.md` (903 lines) — Phase 4A.3 domain patterns
     - `feature-analyzer.md` (282 lines) — Phase 4A.3 parallel analysis
     - `dependency-graph.md` (221 lines) — Phase 4A.3 dependency detection
     - `technical-assessment-guide.md` (914 lines) — Phase 4A.4 complexity scoring
     - `epic-validation-checklist.md` (760 lines) — Phase 4A.7 validation & self-healing
     - `epic-validation-hook.md` (76 lines) — Phase 4A.6 CLI hook
     - `assets/templates/epic-template.md` (265 lines) — epic document template
   - Total: ~3,935 lines migrated

2. **Feature 2: Move Epic Analysis References from Ideation to Architecture** (Sprint 1)
   - Description: Transfer epic decomposition, feasibility analysis, and complexity assessment reference files from `devforgeai-ideation/references/` to `designing-systems/references/`
   - User Value: Consolidates all epic-related content under the architect role
   - Estimated Points: 5
   - Files Moved:
     - `epic-decomposition-workflow.md` (309 lines)
     - `feasibility-analysis-workflow.md` (543 lines)
     - `feasibility-analysis-framework.md` (~600 lines)
     - `complexity-assessment-workflow.md` (333 lines)
     - `complexity-assessment-matrix.md` (~800 lines)
     - `artifact-generation.md` (epic sections, ~350 lines)
   - Total: ~2,935 lines migrated

3. **Feature 3: Unify Complexity Scoring** (Sprint 1)
   - Description: Resolve incompatible scoring scales — ideation uses 0-60 (4 dimensions: Functional 0-20, Technical 0-20, Team/Org 0-10, NFR 0-10) while orchestration uses 0-10 (5 bands: Trivial/Low/Moderate/High/Critical). Merge into single unified scoring system owned by architecture.
   - User Value: One authoritative complexity score per epic, no conflicting assessments
   - Estimated Points: 3
   - Files Modified: `complexity-assessment-workflow.md`, `complexity-assessment-matrix.md`, `technical-assessment-guide.md` (all now in architecture)
   - Note: Resolve overlapping feature decomposition content (ideation's `epic-decomposition-workflow.md` vs orchestration's `feature-decomposition-patterns.md`) — merge into single authoritative file

4. **Feature 4: Define Structured Requirements Schema (Context Preservation Artifact)** (Sprint 2)
   - Description: Replace the narrative prose requirements-spec-template.md with a YAML-structured schema designed for cross-session AI consumption. The schema locks decisions, eliminates ambiguity, and serves as the sole handoff artifact between ideation (Session N) and architecture (Session N+1). Format: YAML frontmatter containing ALL structured data (decisions, scope, success criteria, constraints, NFRs) with minimal markdown body for human readability only.
   - User Value: Eliminates hallucination at session boundaries — fresh sessions read locked decisions instead of re-interpreting exploratory prose
   - Estimated Points: 3
   - Files Created:
     - `.claude/skills/devforgeai-ideation/assets/templates/requirements-schema.yaml` — JSON Schema or YAML schema definition
     - `.claude/skills/devforgeai-ideation/assets/templates/requirements-template.md` — replaces current `requirements-spec-template.md`
   - Files Modified:
     - `.claude/skills/devforgeai-ideation/SKILL.md` (output format specification)
     - `.claude/skills/designing-systems/SKILL.md` (input format specification for Phase 6)
   - Schema Fields (minimum):
     ```yaml
     decisions:        # Locked choices with rejected alternatives
       - id: DR-N
         domain: ""    # e.g., "authentication", "database", "architecture"
         decision: ""  # What was chosen
         rejected:     # What was NOT chosen (with reasons)
           - option: ""
             reason: ""
         rationale: "" # Why this choice
         locked: true  # Immutable after ideation
     scope:
       in: []          # Explicitly included
       out: []         # Explicitly excluded (with deferral target)
     success_criteria:
       - id: SC-N
         metric: ""    # What to measure
         target: ""    # Quantified threshold
         measurement: ""  # How to verify
     constraints: []   # Technical, business, regulatory
     nfrs: []          # Performance, security, scalability
     stakeholders: []  # Roles, concerns, decision authority
     source_brainstorm: ""  # Back-reference for provenance
     ```
   - Design Principles:
     - **Every field is unambiguous** — no "should", "might", "consider"
     - **Rejected alternatives are explicit** — closes doors the brainstorm left open
     - **Locked flag per decision** — prevents downstream re-interpretation
     - **Source provenance** — traces back to brainstorm for audit chain

5. **Feature 5: Add Epic Creation Phases to Architecture SKILL.md** (Sprint 2)
   - Description: Add Phase 6: Epic Creation with 8 sub-phases (from orchestration's Phase 4A); add progressive disclosure references to all migrated files; register subagent invocations for `requirements-analyst` and `architect-reviewer`; define input format (accepts YAML requirements from F4 schema)
   - User Value: Architecture skill becomes the "Architect" role — receives structured requirements, produces epics
   - Estimated Points: 5
   - Files Modified: `.claude/skills/designing-systems/SKILL.md` (grows from 279 → ~380 lines, well under 1,000-line limit)

6. **Feature 6: Remove Phase 4A from Orchestration SKILL.md** (Sprint 2)
   - Description: Remove Phase 4A (Epic Creation) mode from orchestration; update `mode-detection.md` to remove epic creation context marker detection; remove epic-related entries from `subagent-registry.md`; orchestration retains: story lifecycle, sprint planning, audit deferrals, QA retry
   - User Value: Orchestration focuses on its core responsibility — workflow coordination, not content creation
   - Estimated Points: 3
   - Files Modified: `.claude/skills/devforgeai-orchestration/SKILL.md`, `references/mode-detection.md`, `references/subagent-registry.md`

7. **Feature 7: Slim Ideation SKILL.md — Remove Architect Phases + Adopt Structured Output** (Sprint 2)
   - Description: Remove epic decomposition, feasibility, and complexity phases from ideation SKILL.md; update completion handoff to produce YAML-structured requirements.md (per F4 schema) instead of epic.md; remove `artifact-generation.md` epic code path (keep requirements generation); update self-validation workflow
   - User Value: Ideation becomes the focused "PM" role — produces structured, locked requirements only
   - Estimated Points: 3
   - Files Modified: `.claude/skills/devforgeai-ideation/SKILL.md`, `references/completion-handoff.md`, `references/artifact-generation.md`

8. **Feature 8: Update Command Routing** (Sprint 3)
   - Description: Change `/create-epic` command from `Skill(command="devforgeai-orchestration")` to invoke architecture skill directly; update `/ideate` command output to produce requirements.md not epic.md; move `skill-output-schemas.yaml` epic schema to architecture skill; update error handling references
   - User Value: Clean command chain: `/ideate` → requirements.md → `/create-epic` → epic.md (via architecture skill)
   - Estimated Points: 3
   - Files Modified: `.claude/commands/create-epic.md`, `.claude/commands/ideate.md`

9. **Feature 9: Rename Architecture Skill** (Sprint 3)
   - Description: Rename `designing-systems` directory to `designing-systems` (or chosen gerund name per ADR-017); update all cross-references across codebase
   - User Value: Conformance with Anthropic Agent Skills naming best practices; shorter, descriptive name
   - Estimated Points: 5
   - Files Modified: Directory rename + ~50-80 cross-reference updates
   - ADR: ADR-017 (already accepted)

10. **Feature 10: Re-evaluate and Rename Ideation Skill** (Sprint 3)
    - Description: After slimming (F7), evaluate remaining scope and choose appropriate gerund name; rename directory; update all cross-references; fold STORY-431 AC#2 trigger phrases into description update
    - User Value: Name accurately reflects the slimmed PM-focused scope
    - Estimated Points: 3
    - Files Modified: Directory rename + ~80-120 cross-reference updates
    - Note: Final name TBD after Feature 7 completes — will be decided based on remaining responsibility

11. **Feature 11: Rename Brainstorming Skill** (Sprint 4)
    - Description: Rename `devforgeai-brainstorming` to `brainstorming` (drop prefix only, already gerund form); update cross-references
    - User Value: Simplest rename — just prefix removal
    - Estimated Points: 2
    - Files Modified: Directory rename + cross-reference updates

12. **Feature 12: Update Context Files and Codebase Sweep** (Sprint 4)
    - Description: Update source-tree.md, architecture-constraints.md, and coding-standards.md with new skill names, directory paths, and responsibility descriptions; run full codebase Grep sweep to verify zero stale references
    - User Value: Constitutional files reflect the new reality; zero technical debt
    - Estimated Points: 2
    - Files Modified: `devforgeai/specs/context/source-tree.md`, `architecture-constraints.md`, `coding-standards.md`, CLAUDE.md, memory files

### Out of Scope

- Renaming other `devforgeai-` prefixed skills (devforgeai-qa, devforgeai-release, etc.) — covered by EPIC-065
- Restructuring other skill boundaries beyond brainstorming/ideation/architecture/orchestration
- Moving non-epic orchestration content (sprint planning, story lifecycle, audit deferrals stay in orchestration)
- Re-running the conformance analysis (separate task after migration)
- Changes to the installer `src/` tree (handled by separate sync workflow)

## Target Sprints

### Sprint 1: File Migration + Scoring Unification (Weeks 1-2)

**Goal:** Move ALL epic-related reference files from orchestration AND ideation into architecture; resolve overlapping/conflicting content
**Estimated Points:** 13
**Features:**
- Feature 1: Move Epic Creation References from Orchestration → Architecture (5 points)
- Feature 2: Move Epic Analysis References from Ideation → Architecture (5 points)
- Feature 3: Unify Complexity Scoring (3 points)

**Rationale:** Do the invasive file migration first while directory names are stable. Unify scoring during migration (before files are referenced by new SKILL.md phases). This is the highest-risk sprint — ~6,870 lines of reference content moving.

**Validation:** All 14 migrated files exist in `designing-systems/references/`. No duplicate feature decomposition or complexity scoring files remain in source skills.

---

### Sprint 2: Requirements Schema + SKILL.md Restructure (Weeks 3-4)

**Goal:** Define the structured requirements schema, then update all three SKILL.md files — architecture gains Phase 6, orchestration loses Phase 4A, ideation sheds architect phases and adopts structured output
**Estimated Points:** 14
**Features:**
- Feature 4: Define Structured Requirements Schema (3 points) — **do first** (defines I/O contract)
- Feature 5: Add Epic Creation Phases to Architecture SKILL.md (5 points)
- Feature 6: Remove Phase 4A from Orchestration SKILL.md (3 points)
- Feature 7: Slim Ideation SKILL.md + Adopt Structured Output (3 points)

**Rationale:** Schema defined first (F4) because it specifies the output format for ideation and input format for architecture. Then all three SKILL.md files updated atomically. The schema is the "contract" between Session N (ideation) and Session N+1 (architecture).

**Validation:** Architecture SKILL.md has Phase 6 with 8 sub-phases and accepts YAML requirements input. Orchestration SKILL.md has no Phase 4A. Ideation SKILL.md produces structured YAML requirements (not narrative PRD, not epic).

---

### Sprint 3: Command Routing + Renames (Weeks 5-6)

**Goal:** Re-route `/create-epic` to architecture, rename the two restructured skills
**Estimated Points:** 11
**Features:**
- Feature 8: Update Command Routing (3 points)
- Feature 9: Rename Architecture → `designing-systems` (5 points)
- Feature 10: Re-evaluate + Rename Ideation → TBD (3 points)

**Rationale:** Commands re-routed first (F8), then renames (F9, F10). Architecture renamed before ideation (receiving skill, smaller blast radius).

**Dependencies:** Sprint 2 must complete (SKILL.md phases finalized before command routing).

---

### Sprint 4: Rename Brainstorming + Final Sweep (Weeks 7-8)

**Goal:** Complete the last rename and verify zero stale references
**Estimated Points:** 4
**Features:**
- Feature 11: Rename Brainstorming → `brainstorming` (2 points)
- Feature 12: Context Files + Codebase Sweep (2 points)

**Rationale:** Brainstorming is the simplest rename (prefix drop only). Final sweep verifies the entire migration is clean.

**Validation:** `Grep(pattern="devforgeai-(ideation|architecture|brainstorming)")` returns zero matches.

---

## Dependencies

### Internal Dependencies

- [x] **ADR-017:** Gerund naming convention accepted (2026-02-16)
- [x] **ADR-019:** Responsibility restructure accepted (2026-02-17)
- [ ] **EPIC-067 STORY-425 through STORY-430:** Ideation conformance fixes should complete before or concurrently with Sprint 1-2 (they modify ideation files that will be restructured)

### External Dependencies
- None. All changes are internal to the framework.

### Blocking Issues

- **Potential Blocker:** EPIC-067 stories (STORY-425-430) modify the same ideation skill files. If those stories are in progress during Sprint 1-2, merge conflicts are possible.
  - **Mitigation:** Complete EPIC-067 Sprint 1-2 (STORY-425-428) before starting EPIC-068 Sprint 1. Alternatively, implement EPIC-068 Sprint 1-2 first, then apply EPIC-067 changes to the restructured files.

### Story Dependencies

```
Sprint 1:  F1 (Move Orchestration Files) ─────────────────┐
           F2 (Move Ideation Files) ── (parallel w/F1)     │
           F3 (Unify Scoring) ←── F1,F2                    │
                                                            │
Sprint 2:  F4 (Requirements Schema) ←── F3  ** DO FIRST ** │
           F5 (Update Arch SKILL.md) ←── F1,F2,F3,F4       │
           F6 (Remove Orch Phase 4A) ←── F1                 │
           F7 (Slim Ideation + Schema Output) ←── F2,F4     │
                                                            │
Sprint 3:  F8 (Update Commands) ←── F5,F6                  │
           F9 (Rename Architecture) ←── F5,F8               │
           F10 (Rename Ideation) ←── F7                     │
                                                            │
Sprint 4:  F11 (Rename Brainstorming) (independent)         │
           F12 (Sweep) ←── F9,F10,F11                      │
```

## Stakeholders

- **Product Owner:** Framework Team — Ensures restructure aligns with framework improvement goals
- **Tech Lead:** DevForgeAI AI Agent — Executes migration workflow

## Risks & Mitigation

### Risk 1: Broken handoff between ideation and architecture
- **Probability:** Medium
- **Impact:** High — `/ideate` → `/create-epic` chain would break
- **Mitigation:** Feature 8 updates both commands atomically in same sprint. Test with `/ideate test idea` after changes.
- **Contingency:** Revert command changes, keep both skills owning epic creation temporarily

### Risk 2: Orchestration Phase 4A removal breaks /create-epic
- **Probability:** Medium
- **Impact:** High — `/create-epic` would invoke a non-existent phase
- **Mitigation:** Feature 8 (command re-routing) must complete in same sprint as or after Feature 6 (Phase 4A removal). Sequential dependency enforced.
- **Contingency:** Temporarily keep Phase 4A as thin wrapper delegating to architecture

### Risk 3: Missing reference file pointers after migration
- **Probability:** Medium
- **Impact:** Medium — skill would fail to load reference at runtime
- **Mitigation:** Post-migration Grep scan for old paths. Feature 12 sweep catches any stragglers.
- **Contingency:** Symlinks from old paths to new paths as temporary bridge

### Risk 4: EPIC-067 merge conflicts
- **Probability:** High
- **Impact:** Low — both epics modify ideation files
- **Mitigation:** Sequence EPIC-067 Sprint 1-2 before EPIC-068, or merge carefully. All changes are Markdown (no binary conflicts).
- **Contingency:** Manual merge with diff review

### Risk 5: Cross-reference blast radius larger than estimated
- **Probability:** Medium
- **Impact:** Low — more files to update than planned
- **Mitigation:** Feature 12 sweep is specifically designed to catch all stale references. Conservative 8-week timeline provides buffer.

## Architecture Considerations

### Architecture Impact
- Skill responsibility boundaries redefined (ADR-019)
- No new architecture patterns — all changes within existing skill ecosystem
- Command-skill handoff introduces explicit YAML-structured requirements.md intermediate artifact
- Three-layer architecture unchanged (Skills → Subagents → Commands)

### Technology Decisions
- No new technologies — changes are to Markdown prompt files only
- YAML schema for requirements.md — consistent with existing frontmatter patterns
- Compliant with zero-dependency framework model (Source: devforgeai/specs/context/dependencies.md)

### Context File Constraints
All migration must respect:
1. `devforgeai/specs/context/tech-stack.md` — Native tools only
2. `devforgeai/specs/context/source-tree.md` — File location rules (will be updated in F12)
3. `devforgeai/specs/context/coding-standards.md` — Gerund naming per ADR-017
4. `devforgeai/specs/context/architecture-constraints.md` — Single responsibility per skill (will be updated in F12)
5. `devforgeai/specs/context/anti-patterns.md` — No monolithic components

## Supersedes

- **STORY-431** (EPIC-067): "Evaluate Gerund Naming Convention and Add Trigger Phrases" — the naming evaluation (AC#1) is resolved by ADR-017; the rename (AC#3) is covered by Features 9-11; the trigger phrases (AC#2) should be folded into Feature 10 (ideation rename)
- **EPIC-065 partially:** This epic covers the rename for 3 of 14 skills. EPIC-065 covers the remaining 11.

## Progress Tracking

### Story Links

Stories to be created via `/create-story` for each feature.

| Feature | Story ID | Title | Sprint | Points | Status |
|---------|----------|-------|--------|--------|--------|
| F1 | STORY-432 | Move Epic Creation References from Orchestration → Architecture | Sprint 1 | 5 | Backlog |
| F2 | STORY-433 | Move Epic Analysis References from Ideation → Architecture | Sprint 1 | 5 | Backlog |
| F3 | STORY-434 | Unify Complexity Scoring Systems | Sprint 1 | 3 | Backlog |
| F4 | STORY-435 | Define Structured Requirements Schema (YAML) | Sprint 2 | 3 | Backlog |
| F5 | STORY-436 | Add Epic Creation Phases to Architecture SKILL.md | Sprint 2 | 5 | Backlog |
| F6 | STORY-437 | Remove Phase 4A from Orchestration SKILL.md | Sprint 2 | 3 | Backlog |
| F7 | STORY-438 | Slim Ideation SKILL.md + Adopt Structured Output | Sprint 2 | 3 | Backlog |
| F8 | STORY-439 | Update /create-epic and /ideate Command Routing | Sprint 3 | 3 | Backlog |
| F9 | STORY-440 | Rename designing-systems → designing-systems | Sprint 3 | 5 | Backlog |
| F10 | STORY-441 | Re-evaluate and Rename Ideation Skill | Sprint 3 | 3 | Backlog |
| F11 | STORY-442 | Rename devforgeai-brainstorming → brainstorming | Sprint 4 | 2 | Backlog |
| F12 | STORY-443 | Update Context Files + Codebase Sweep | Sprint 4 | 2 | Backlog |

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1: File Migration + Scoring | Ready | 13 | 3 | 0 | 0 | 0 |
| Sprint 2: Schema + SKILL.md Restructure | Ready | 14 | 4 | 0 | 0 | 0 |
| Sprint 3: Commands + Renames | Ready | 11 | 3 | 0 | 0 | 0 |
| Sprint 4: Final Rename + Sweep | Ready | 4 | 2 | 0 | 0 | 0 |
| **Total** | **0%** | **42** | **12** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 42
- **Completed:** 0
- **Remaining:** 42

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════════
Week 1-2:  Sprint 1 — File Migration + Scoring Unification     13pts
Week 3-4:  Sprint 2 — Requirements Schema + SKILL.md Restructure 14pts
Week 5-6:  Sprint 3 — Command Routing + Renames                11pts
Week 7-8:  Sprint 4 — Final Rename + Codebase Sweep             4pts
════════════════════════════════════════════════════════════════
Total Duration: 8 weeks (conservative)
Target Completion: 2026-04-13
```

### Key Milestones
- [ ] **Milestone 1:** Sprint 1 complete — All epic-related files consolidated in architecture skill; unified scoring system
- [ ] **Milestone 2:** Sprint 2 complete — YAML requirements schema defined; Architecture SKILL.md has Phase 6; orchestration has no Phase 4A; ideation produces structured requirements
- [ ] **Milestone 3:** Sprint 3 complete — `/create-epic` routes to architecture; architecture and ideation skills use gerund names
- [ ] **Milestone 4:** Sprint 4 complete — Zero stale `devforgeai-` references in codebase

## Next Steps

### Immediate Actions
1. ~~Mark STORY-431 (EPIC-067) as superseded by EPIC-068~~ ✅
2. Assess EPIC-067 Sprint 1-2 sequencing relative to this epic
3. Create stories for Sprint 1 features via `/create-story`
4. Begin Sprint 1 implementation

### Pre-Development Checklist
- [x] ADR-017 accepted (gerund naming authorization)
- [x] ADR-019 accepted (responsibility restructure authorization)
- [x] Epic document created with feature breakdown
- [x] Features renumbered in execution order (F1-F12 sequential by sprint)
- [ ] STORY-431 marked as superseded
- [ ] Stories created for Sprint 1 (F1, F2, F3)

## Notes

- **Ideation skill name TBD:** The final name for the ideation skill will be decided after Feature 7 (slimming) completes. Once the remaining scope is clear, the right gerund name will be chosen. Candidates include `scoping-features`, `scoping-products`, `drafting-requirements`, `refining-ideas`.
- **Architecture skill name `designing-systems`:** This is the proposed name. If the user prefers a different gerund, it can be changed in Feature 9.
- **STORY-431 AC#2 (trigger phrases):** The trigger phrases requirement from STORY-431 should be folded into Feature 10 (ideation rename) since we're already updating the SKILL.md description.
- **Relationship to EPIC-065:** EPIC-065 covers the gerund rename for all 14 `devforgeai-` prefixed skills. This epic covers 3 of those 14. After this epic completes, EPIC-065's remaining scope is 11 skills.
- **Context preservation rationale:** The YAML requirements schema (F4) exists specifically to prevent hallucination at session boundaries. Each DevForgeAI workflow runs in a fresh session — the structured artifact ensures decisions made in Session N are locked and unambiguous for Session N+1.

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-17
