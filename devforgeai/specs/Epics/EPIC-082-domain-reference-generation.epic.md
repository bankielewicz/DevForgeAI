---
id: EPIC-082
title: Domain Reference Generation
status: Planning
start_date: 2026-03-15
target_date: 2026-03-28
total_points: 10
completed_points: 0
created: 2026-02-22
owner: Framework Owner
tech_lead: DevForgeAI AI Agent
team: DevForgeAI

source_requirements: "devforgeai/specs/requirements/domain-reference-generation-requirements.md"
source_brainstorm: "devforgeai/specs/brainstorms/BRAINSTORM-012-configuration-layer-alignment-protocol.brainstorm.md"
complexity_score: 24
complexity_tier: "Tier 2 - Moderate (24/60)"
architecture_review_complexity: "4/10"
prerequisite_epic: "EPIC-081"
---

# Epic: Domain Reference Generation

## Business Goal

Extend existing subagents with project-specific domain expertise by auto-generating **domain reference files** derived from context files. All 41 subagents are framework-generic today — they must re-derive domain understanding from raw context files on every invocation, which is inefficient, inconsistent, and incomplete.

**Evidence (from ENH-CLAP-001 investigation on GPUXtend project):**

| Domain Knowledge Gap | Impact When Missing |
|----------------------|---------------------|
| CUDA Driver API hooking patterns | backend-architect suggests incorrect initialization sequences |
| Microsoft Detours transaction lifecycle | code-reviewer misses DllMain-safe vs unsafe API usage |
| Named Pipe IPC protocol constants | test-automator doesn't know cross-boundary test patterns |
| 11 project-specific anti-patterns | security-auditor misses domain security concerns |
| 3 separate build toolchains | test-automator runs wrong test command for component type |

**Solution:** Generate `project-*.md` reference files in existing `{agent}/references/` directories, derived 100% from context files. This follows the progressive disclosure pattern (ADR-012) without creating new subagents, preserving single source of truth.

**Key Locked Decision:** Domain references, NOT new subagents — prevents dual maintenance, preserves context files as "THE LAW", avoids agent sprawl.

**Source provenance:** ENH-CLAP-001 Part 3 → Requirements spec → This epic

## Success Metrics

- **SC-1:** Detection heuristic accuracy >80% — Test with 3+ diverse project context files
- **SC-2:** Derivation purity 100% — Manual review: no hallucinated domain knowledge
- **SC-3:** Auto-generation header present 100% — Automated check for header pattern
- **SC-4:** Core agent files unmodified — Git diff verification: 0 modifications to *.md agent files
- **SC-5:** Regeneration idempotency — Run twice, diff results: identical output

**Measurement Plan:**
- Baseline: Current subagent behavior on GPUXtend-style context files (no project references)
- Per-story: Verify generated references against source context files (exact extraction, no synthesis)
- Final: Full Phase 5.7 run on 2+ diverse project context file sets
- Review frequency: After each story completion

## Scope

### In Scope

### Feature 1: Detection Heuristic Engine (Foundation)
- Implement 4 detection heuristics (DH-01 through DH-04) that analyze context files
- Each heuristic has defined trigger condition and threshold
- Heuristics use Grep/Read only — evaluate context files without modifying them
- Returns list of triggered heuristics with agent names and content source files
- Projects with no triggered heuristics skip Phase 5.7 entirely
- **Heuristics:**
  - DH-01: backend-architect — hardware/platform-specific constraints in architecture-constraints.md
  - DH-02: test-automator — >1 language or build system in tech-stack.md
  - DH-03: security-auditor — >5 domain-specific anti-patterns in anti-patterns.md
  - DH-04: code-reviewer — language-specific patterns in 2+ languages in coding-standards.md
- **Acceptance criteria guidance:** 5 ACs covering heuristic count, trigger conditions, read-only evaluation, output format, skip behavior
- **Estimated points:** 3

### Feature 2: Reference File Template
- Standardized template with auto-generation header (source files, date, regeneration command)
- "DO NOT EDIT MANUALLY" warning
- "When to Load This Reference" section with trigger conditions
- Sections: Domain-Specific Constraints, Forbidden Patterns, Language-Specific Patterns, Build and Test Commands
- All content 100% derived from context files (derivation purity)
- `project-*.md` naming convention
- **Acceptance criteria guidance:** 6 ACs covering header, warning, sections, derivation purity, naming convention
- **Estimated points:** 2

### Feature 3: Phase 5.7 Workflow Integration
- Create Phase 5.7 "Domain Reference Generation" reference file (~250 lines)
- Modify SKILL.md to add ~25-30 line Phase 5.7 entry after Phase 5.5, before Phase 6
- 5-step workflow: run heuristics → present recommendations via AskUserQuestion → generate files → verify no contradictions → report
- Generated files written to `.claude/agents/{agent}/references/project-{type}.md`
- Verify derivation purity: generated content contains ONLY context-derived content
- **Files to create:** `.claude/skills/designing-systems/references/domain-reference-generation.md`
- **Files to modify:** `.claude/skills/designing-systems/SKILL.md`
- **Acceptance criteria guidance:** 8 ACs covering naming, progressive disclosure, heuristic evaluation, skip behavior, user approval, file generation, purity verification, summary display
- **Estimated points:** 3

### Feature 4: /audit-alignment --generate-refs Integration
- Add `--generate-refs` flag to existing /audit-alignment command (created in EPIC-081)
- `--generate-refs` requires `--fix` flag (regeneration is a fix action)
- Regeneration overwrites existing project-*.md files with fresh content
- Re-evaluates all 4 heuristics (previously triggered heuristic may no longer trigger)
- If heuristic no longer triggers, flags project-*.md for removal (user confirmation)
- **Files to modify:** `.claude/commands/audit-alignment.md`
- **Acceptance criteria guidance:** 6 ACs covering flag behavior, fix dependency, overwrite, re-evaluation, removal flagging, cross-epic dependency
- **Estimated points:** 2

### Out of Scope

- ❌ New subagents — domain references extend existing agents via progressive disclosure only
- ❌ Automatic regeneration on context file changes — on-demand only via `/audit-alignment --generate-refs`
- ❌ Subagent core prompt modifications — references/ directory only, agent .md files untouched
- ❌ Semantic/summarized content in references — exact extraction from context files only
- ❌ Reference files for agents other than the 4 targeted (backend-architect, test-automator, security-auditor, code-reviewer)

## Target Sprints

### Sprint 1: Domain Reference Generation (Full Delivery)
**Goal:** Complete all domain reference generation deliverables in a single sprint
**Estimated Points:** 10
**Prerequisite:** EPIC-081 (CLAP) must be in **Released** status

**Days 1-3: Foundation**
- Feature 1: Detection heuristic engine (3 pts) — 4 heuristics with trigger conditions
- Feature 2: Reference file template (2 pts) — standardized template with auto-gen header

**Days 3-5: Integration**
- Feature 3: Phase 5.7 reference + SKILL.md update (3 pts) — workflow file + skill modification

**Days 5-6: Command Extension**
- Feature 4: /audit-alignment --generate-refs (2 pts) — on-demand regeneration

**Key Deliverables:**
- 4 detection heuristics operational
- Reference file template with auto-generation header
- Phase 5.7 integrated into designing-systems skill
- /audit-alignment --generate-refs flag working
- End-to-end: `/create-context` workflow includes Phase 5.7

## User Stories

1. **STORY-477:** Detection Heuristic Engine and Reference File Template (F1+F2, 5 pts)
   - **As a** framework developer, **I want** automated detection heuristics + standardized template, **so that** domain references are generated only when valuable
   - **Depends on:** STORY-476 (EPIC-081 completion)
   - **File:** `devforgeai/specs/Stories/STORY-477-detection-heuristic-engine-reference-template.story.md`
2. **STORY-478:** Phase 5.7 Domain Reference Generation Workflow Integration (F3, 3 pts)
   - **As a** developer running /create-context, **I want** automatic domain reference generation after context files are validated
   - **Depends on:** STORY-477
   - **File:** `devforgeai/specs/Stories/STORY-478-phase-5-7-domain-reference-generation.story.md`
3. **STORY-479:** /audit-alignment --generate-refs Integration (F4, 2 pts)
   - **As a** framework maintainer, **I want** to regenerate domain references on demand when context files change
   - **Depends on:** STORY-478
   - **File:** `devforgeai/specs/Stories/STORY-479-audit-alignment-generate-refs.story.md`

*Dependency chain: EPIC-081 Released → STORY-477 → STORY-478 → STORY-479*

## Technical Considerations

### Architecture Impact
- 1 new skill reference: `designing-systems/references/domain-reference-generation.md` (~250 lines)
- 1 skill modified: `designing-systems/SKILL.md` (Phase 5.7 insertion, ~25-30 lines added)
- 1 command modified: `audit-alignment.md` (--generate-refs flag, extends EPIC-081 deliverable)
- 4 per-project generated files: `project-domain.md`, `project-testing.md`, `project-security.md`, `project-review.md`
- **No subagent core files modified** — references/ directory only

### Technology Decisions
- **No new technologies** — Grep, Read, Write (existing Claude Code tools)
- **Template-based generation** — extract from context files, populate template sections
- **Heuristic detection** — keyword/count analysis via Grep patterns

## Reference Loading Decision

**DECISION:** Approach A (orchestration-driven) is selected. The implementing-stories skill detects `project-*.md` files in agent `references/` directories and passes their paths to subagent `Task()` calls.

**Rationale:** This approach preserves SRP (architecture-constraints.md) by keeping subagent prompts unchanged while enabling reference discovery at the orchestration layer. Full analysis: `devforgeai/specs/adrs/ADR-022-subagent-reference-loading.md` (includes all 3 candidate approaches and detailed consequences).

## Implementation Guidance

See ADR-022 (`devforgeai/specs/adrs/ADR-022-subagent-reference-loading.md`) for orchestration-driven loading details, including workflow steps, per-feature requirements, and architecture rationale.

**Key Points for Feature Implementations:**
- **Feature 1+2:** Heuristic output must include agent name and `project-*.md` path; auto-gen header must include `Load via: Read(file_path="...")` line for discovery.
- **Feature 3+4:** Phase 5.7 reference and regenerated files MUST preserve `Load via:` header convention.

### Security & Compliance
- Generated references contain no secrets (context files enforce no-hardcoded-secrets rule)
- All generated content is 100% derived from existing approved context files
- No new external dependencies

### Performance Requirements
- Heuristic evaluation: <10 seconds for all 4 heuristics
- Reference generation: <30 seconds per file
- Full Phase 5.7: <120 seconds total

## Dependencies

### Internal Dependencies (EPIC-081 — BLOCKING)
- [x] **Phase 5.5 in SKILL.md:** Phase 5.7 inserts AFTER Phase 5.5 — EPIC-081 Feature 3
  - **Status:** Not Started (EPIC-081 in Planning)
  - **Impact if delayed:** EPIC-082 cannot start

- [x] **/audit-alignment command:** --generate-refs flag extends this command — EPIC-081 Feature 2
  - **Status:** Not Started (EPIC-081 in Planning)
  - **Impact if delayed:** EPIC-082 Feature 4 blocked

- [x] **alignment-auditor subagent:** Phase 5.7 may reuse for verification — EPIC-081 Feature 1
  - **Status:** Not Started (EPIC-081 in Planning)
  - **Impact if delayed:** Verification step falls back to manual Grep checks

### Internal Dependencies (This Epic)
- [x] **4 target agent references/ directories exist:** backend-architect, test-automator, security-auditor, code-reviewer
  - **Status:** Complete — all 4 verified to have references/ subdirectories
  - **Impact if delayed:** N/A

### Feature-Level Dependencies

```
[EPIC-081 CLAP - Released] ────────────────────────────────
                              │ (blocking prerequisite)
                              ▼
Feature 1+2 (heuristics + template)    [Days 1-3 — foundation]
                              │
                              ▼
Feature 3 (Phase 5.7 + SKILL.md)      [Days 3-5 — integration]
                              │
                              ▼
Feature 4 (--generate-refs flag)       [Days 5-6 — command extension]
```

**Critical Path:** EPIC-081 Released → F1+F2 → F3 → F4

### External Dependencies
- None (all work is internal to the DevForgeAI framework)

## Risks & Mitigation

### Risk 1: Subagent Reference Loading Mechanism Unresolved
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Three approaches documented (orchestration-driven, explicit opt-in, framework auto-load). Resolve during F3 story implementation. References exist and are loadable regardless — the question is discovery.
- **Contingency:** Initially document loading convention in generated file headers ("Load via: `Read(file_path=...)`"); implement discovery mechanism in follow-up story

### Risk 2: Detection Heuristic False Negatives
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Conservative thresholds (e.g., >1 language for DH-02, >5 anti-patterns for DH-03). User can always run `/audit-alignment --generate-refs` manually.
- **Contingency:** Add new heuristics to reference file (not hardcoded in SKILL.md)

### Risk 3: Generated Content Drifts from Source (Derivation Purity)
- **Probability:** Low
- **Impact:** High
- **Mitigation:** Verification step in Phase 5.7 workflow compares generated sections against source context files. Auto-generation header includes source file list for manual tracing.
- **Contingency:** `/audit-alignment --generate-refs` regenerates from scratch

### Risk 4: EPIC-081 Completion Delay
- **Probability:** Medium
- **Impact:** High (blocks this entire epic)
- **Mitigation:** EPIC-081 has clear 2-week timeline. This epic's start date (2026-03-15) provides buffer.
- **Contingency:** Defer this epic to next sprint if CLAP is delayed

## Stakeholders

### Primary Stakeholders
- **Framework Owner:** Approves reference loading mechanism decision, reviews generated reference quality
- **DevForgeAI AI Agent:** Executes /create-context with Phase 5.7, loads generated references during /dev

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════════
Prerequisite: EPIC-081 (CLAP) must reach Released status
Days 1-3:  Features 1+2 — Detection heuristics + reference template
Days 3-5:  Feature 3 — Phase 5.7 workflow + SKILL.md modification
Days 5-6:  Feature 4 — /audit-alignment --generate-refs flag
Day 7:     End-to-end test: /create-context → Phase 5.7 → verify refs
════════════════════════════════════════════════════════════════
Total Duration: ~1.5 weeks (1 sprint)
Target Release: 2026-03-28
```

### Key Milestones
- [ ] **M0:** EPIC-081 (CLAP) reaches Released status (prerequisite)
- [ ] **M1:** 4 heuristics operational + template defined (Day 3)
- [ ] **M2:** Phase 5.7 integrated into designing-systems skill (Day 5)
- [ ] **M3:** /audit-alignment --generate-refs working (Day 6)
- [ ] **M4:** End-to-end: /create-context produces domain references for test project (Day 7)

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 10 | 3 (STORY-477, 478, 479) | 0 | 0 | 3 (EPIC-081 prerequisite) |
| **Total** | **0%** | **10** | **3** | **0** | **0** | **3** |

### Burndown
- **Total Points:** 10
- **Completed:** 0
- **Remaining:** 10

## Verification Plan

### Per-Story Verification
1. **F1+F2 (heuristics + template):** Run all 4 heuristics against DevForgeAI's own context files; verify template output format; verify derivation purity
2. **F3 (Phase 5.7):** Verify SKILL.md insertion between Phase 5.5 and Phase 6; run Phase 5.7 against test context files; verify AskUserQuestion flow
3. **F4 (--generate-refs):** Verify flag requires --fix; verify regeneration overwrites; verify heuristic re-evaluation; verify stale file removal prompt

### Final Verification
1. Run `/create-context` on test project → verify Phase 5.7 executes after Phase 5.5
2. Verify generated project-*.md files contain ONLY context-derived content (manual audit)
3. Run `/audit-alignment --generate-refs --fix` → verify regeneration produces identical output
4. Verify git diff shows 0 modifications to subagent core .md files

## The Complete /create-context Workflow (Post Both Epics)

```
/create-context
  Phase 1-5:   Create & validate 6 context files          (EXISTING)
  Phase 5.5:   Align system prompt & CLAUDE.md             (EPIC-081 - CLAP)
  Phase 5.7:   Generate project domain references          (THIS EPIC)
  Phase 6-7:   Epic creation & success report              (EXISTING)
```

Every new DevForgeAI project automatically gets:
1. 6 constitutional context files (existing)
2. A tuned system prompt `<project_context>` section (CLAP)
3. Project-specific domain references for relevant subagents (this epic)

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `devforgeai/specs/requirements/domain-reference-generation-requirements.md` | Full requirements with heuristic definitions, template, GPUXtend example |
| `devforgeai/specs/Epics/EPIC-081-configuration-layer-alignment-protocol.epic.md` | Prerequisite CLAP epic |
| `devforgeai/specs/brainstorms/BRAINSTORM-012-configuration-layer-alignment-protocol.brainstorm.md` | Original proposal Part 3 |
| `.claude/agents/backend-architect.md` | Example target agent with existing references/ |
| `devforgeai/specs/adrs/ADR-012-subagent-progressive-disclosure.md` | Progressive disclosure pattern |

## Retrospective (Post-Epic)

*To be completed after epic completes*

### What Went Well
- [To be filled]

### What Could Be Improved
- [To be filled]

### Lessons Learned
- [To be filled]

### Metrics Achieved
- **SC-1 (Heuristic accuracy):** [Actual vs >80% target]
- **SC-2 (Derivation purity):** [Actual vs 100% target]
- **SC-3 (Auto-gen header):** [Actual vs 100% target]
- **SC-4 (Core agents unmodified):** [Actual vs 0 modifications target]
- **SC-5 (Regeneration idempotency):** [Actual vs identical output target]

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-22
**Complexity Score:** 24/60 (Tier 2 — Moderate), 4/10 (architect-reviewer)
**Source:** ENH-CLAP-001 Part 3 → Requirements spec → requirements-analyst validation → architect-reviewer assessment
**Prerequisite:** EPIC-081 (Configuration Layer Alignment Protocol) must reach Released status
