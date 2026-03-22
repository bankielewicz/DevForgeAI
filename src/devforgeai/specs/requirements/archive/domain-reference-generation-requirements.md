# Domain Reference Generation - Requirements Specification

**Version:** 1.0
**Date:** 2026-02-22
**Status:** Draft
**Author:** DevForgeAI Ideation (from ENH-CLAP-001)
**Complexity Score:** 24/60 (Tier 2 - Moderate)
**Source:** ENH-CLAP-001 (GPUXtend system prompt alignment investigation, Part 3)

---

## 1. Project Overview

### 1.1 Project Context

| Attribute | Value |
|-----------|-------|
| **Type** | Brownfield (Framework Enhancement) |
| **Domain** | Developer Tooling / Subagent Knowledge Extension |
| **Timeline** | 1 sprint (~1-2 weeks) |
| **Team** | Solo framework development |
| **Estimated Effort** | 10 story points |
| **Prerequisite Epic** | CLAP (Configuration Layer Alignment Protocol) — must be completed first |

### 1.2 Problem Statement

**Framework subagents** experience **insufficient domain knowledge** for specialized projects because **all 41 subagents are framework-generic**, resulting in **less precise delegation, missed domain-specific constraints, and repeated context file lookups**.

**Evidence (from ENH-CLAP-001 investigation on GPUXtend project):**

GPUXtend has deep specialized domains that generic subagents lack awareness of:

| Domain Knowledge | Impact When Missing |
|------------------|---------------------|
| CUDA Driver API hooking patterns | backend-architect may suggest incorrect initialization sequences |
| Microsoft Detours transaction lifecycle | code-reviewer misses DllMain-safe vs unsafe API usage |
| Named Pipe IPC protocol constants | test-automator doesn't know cross-boundary test patterns |
| 11 project-specific anti-patterns | security-auditor misses domain security concerns |
| 3 separate build toolchains (Cargo, CMake, pnpm) | test-automator runs wrong test command for component type |

**Root Cause:** Subagents read context files at runtime but have no pre-extracted, structured domain knowledge. They must re-derive domain understanding from raw context files on every invocation. This is:
- **Inefficient:** Each invocation re-processes the same context files
- **Inconsistent:** Different invocations may extract different interpretations
- **Incomplete:** Subagents may miss domain implications not explicitly called out

**Current Architecture:** All 41 subagents are framework-generic. Project knowledge flows through context files read at runtime. The progressive disclosure extension point already exists:

```
.claude/agents/
├── backend-architect.md                     # core agent (~728 lines)
├── backend-architect/
│   └── references/
│       ├── framework-patterns.md            # generic DevForgeAI patterns
│       ├── implementation-patterns.md       # generic coding patterns
│       └── treelint-patterns.md             # generic AST patterns
```

Reference files in `{agent}/references/` are loaded on-demand via Read() calls. This IS the mechanism for domain-specific knowledge — it just has no project-specific content today.

### 1.3 Solution Overview

Extend existing subagents with project-specific expertise by generating **domain reference files** derived from context files. This follows the progressive disclosure pattern (ADR-012) without creating new subagents:

1. **Phase 5.7 in `designing-systems` skill** — After context files are validated and prompt is aligned (Phases 5-5.5), analyze context files for specialized domain knowledge
2. **Detection heuristic engine** — 4 heuristics that identify which subagents need project-specific references
3. **Reference file template** — Standardized format with auto-generation header, source citations, and regeneration instructions
4. **Integration with /audit-alignment** — `--generate-refs` flag enables on-demand regeneration

### 1.4 Why Domain References, NOT New Subagents

This is a locked decision. The analysis that led to this decision:

| Concern with New Subagents | Detail |
|---------------------------|--------|
| Dual maintenance | Domain knowledge would exist in BOTH the subagent prompt AND the context files. Updates require editing two places. |
| Breaks single source of truth | Context files are "THE LAW" — a `cuda-hook-specialist` subagent with baked-in CUDA knowledge creates an alternative authority. |
| No missing skill category | The 41 generic subagents cover every DevForgeAI skill category (implementation, testing, review, security, etc.). The gap is domain knowledge, not skill type. |
| Agent sprawl | Each project adding 3-4 custom subagents would balloon the agent registry unsustainably. |

| Benefit of Domain References | Detail |
|------------------------------|--------|
| Follows existing pattern | Progressive disclosure (ADR-012) already uses `references/` for conditional loading |
| Single source of truth preserved | References are DERIVED from context files, not independent authorities |
| Extends without modifying | Existing subagents gain project expertise without changing their core prompts |
| Regenerable | When context files change, domain references can be regenerated |
| No registry changes | No new Task() agent types needed — same subagents, richer knowledge |

### 1.5 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Detection heuristic accuracy | >80% of projects needing refs correctly identified | Test with 3+ diverse project context files |
| Derivation purity | 100% of reference content derived from context files | Manual review: no hallucinated domain knowledge |
| Auto-generation header present | 100% of generated files | Automated check for header pattern |
| Core agent files unmodified | 0 modifications to *.md agent files | Git diff verification |
| Regeneration idempotency | Same input produces same output | Run twice, diff results |

---

## 2. User Roles & Personas

### 2.1 Primary Users

| Role | Description | Usage Frequency |
|------|-------------|-----------------|
| Project Bootstrapper | Runs /create-context on new project | Per new project |
| Framework Maintainer | Regenerates refs when context files change | Per ADR-driven context update |
| Subagent (indirect) | Loads project-*.md during story implementation | Every /dev invocation |

### 2.2 User Personas

**Persona 1: Project Bootstrapper**
- **Role:** Developer setting up a new project with DevForgeAI
- **Goals:** Subagents immediately effective on project-specific work
- **Needs:** Automatic generation of domain knowledge after /create-context
- **Pain Points:** Subagents give generic advice; domain nuances lost in raw context file reading

**Persona 2: Framework Maintainer**
- **Role:** Updates context files via ADR process
- **Goals:** Domain references stay in sync with updated context files
- **Needs:** On-demand regeneration command
- **Pain Points:** Stale domain references that contradict updated context files

**Persona 3: Subagent (Indirect Consumer)**
- **Role:** Reads domain references during execution
- **Goals:** Project-specific awareness for accurate analysis/implementation
- **Needs:** Structured, relevant domain knowledge in familiar reference file format
- **Pain Points:** Must re-derive domain knowledge from raw context files on every invocation

---

## 3. Functional Requirements

### 3.1 User Stories

#### FR-001: Detection Heuristic Engine

**As a** framework developer,
**I want** automated detection of which subagents need project-specific references,
**So that** domain references are only generated when they add value (not for simple projects).

**Acceptance Criteria:**

- AC1: Implements 4 detection heuristics (DH-01 through DH-04)
- AC2: Each heuristic has a defined trigger condition and threshold
- AC3: Heuristics evaluate context files without modifying them
- AC4: Returns a list of triggered heuristics with agent names and content source files
- AC5: Projects with no triggered heuristics skip Phase 5.7 entirely (no unnecessary work)

**Detection Heuristic Definitions:**

| Heuristic ID | Target Agent | Trigger Condition | Detection Method | Content Sources |
|-------------|-------------|-------------------|-----------------|-----------------|
| DH-01 | backend-architect | architecture-constraints.md contains hardware-specific or platform-specific constraints | Search architecture-constraints.md for keywords: GPU, CUDA, FPGA, embedded, driver, kernel, DMA, interrupt, register, hardware, sensor, actuator, firmware | architecture-constraints.md (layer boundaries, protocol details, concurrency model), anti-patterns.md (all forbidden patterns with rationale), coding-standards.md (language-specific patterns for all project languages) |
| DH-02 | test-automator | tech-stack.md defines more than 1 language or build system | Count distinct "Language" or "Build System" entries in tech-stack.md tables. If count > 1, this project needs multi-toolchain test routing. | tech-stack.md (test frameworks per language, build commands), source-tree.md (test file location patterns per language), coding-standards.md (test naming conventions per language) |
| DH-03 | security-auditor | anti-patterns.md has more than 5 domain-specific entries | Count `##` headings in anti-patterns.md. If count > 5, project has significant domain-specific security concerns beyond generic OWASP. | anti-patterns.md (all entries with security implications), architecture-constraints.md (boundary security, permission models), coding-standards.md (security-relevant patterns) |
| DH-04 | code-reviewer | coding-standards.md has language-specific patterns in 2+ languages | Count distinct language sections in coding-standards.md. If > 1, code reviews need cross-language awareness. | anti-patterns.md (all entries as review checklist items), coding-standards.md (per-language patterns for review), dependencies.md (prohibited packages to flag in reviews), architecture-constraints.md (layer dependency rules for import review) |

#### FR-002: Reference File Template

**As a** framework maintainer,
**I want** a standardized template for generated domain reference files,
**So that** all generated references are consistent, traceable, and regenerable.

**Acceptance Criteria:**

- AC1: Template includes auto-generation header with: source files, generation date, regeneration command
- AC2: Header includes "DO NOT EDIT MANUALLY" warning
- AC3: Template includes "When to Load This Reference" section with trigger conditions
- AC4: Template includes sections for: Domain-Specific Constraints, Forbidden Patterns, Language-Specific Patterns, Build and Test Commands
- AC5: All content in generated files is extracted/derived from context files (no synthesized domain knowledge)
- AC6: Generated files follow `project-*.md` naming convention

**Reference File Template:**

```markdown
# Project Domain Reference: {agent_name}

> **Auto-generated** from context files by CLAP Phase 5.7
> **Source files:** {list_of_source_context_files}
> **Generated:** {YYYY-MM-DD}
> **Regenerate:** `/audit-alignment --generate-refs`
> **DO NOT EDIT MANUALLY** — changes will be overwritten on regeneration.
> To update this reference, update the source context files via ADR process.

## When to Load This Reference

Load this reference file when working on {project_name} stories that involve:
{trigger_conditions_derived_from_heuristic}

## Domain-Specific Constraints

{extracted_from_architecture_constraints_md}

## Forbidden Patterns (Project-Specific)

{extracted_from_anti_patterns_md_as_checklist}

## Language-Specific Patterns

{extracted_from_coding_standards_md_for_relevant_languages}

## Build and Test Commands

{extracted_from_tech_stack_md_build_sections}
```

#### FR-003: Phase 5.7 Reference File for designing-systems Skill

**As a** developer running /create-context,
**I want** automatic domain reference generation after context files are validated and prompt is aligned,
**So that** subagents have project-specific knowledge from day one.

**Acceptance Criteria:**

- AC1: Phase 5.7 is named "Domain Reference Generation" and inserts after Phase 5.5 (Prompt Alignment), before Phase 6 (Epic Creation)
- AC2: Reference file follows progressive disclosure pattern (loaded on-demand)
- AC3: Phase 5.7 evaluates all 4 detection heuristics against freshly-created context files
- AC4: If no heuristics triggered → skip generation, report "No domain references needed for this project"
- AC5: If heuristics triggered → present recommendations via AskUserQuestion: "CLAP detected {N} subagents that would benefit from project domain references. Generate these reference files?" with options: Generate all / Select individually / Skip
- AC6: For each approved reference: read source context files, extract relevant sections, populate template, write to `.claude/agents/{agent}/references/project-{type}.md`
- AC7: After generation, verify each reference file contains ONLY content derived from source context files (no hallucinated additions)
- AC8: Display summary: files generated, source context files used, regeneration instructions

**Phase 5.7 Workflow (5 steps):**

| Step | Name | Action | Tool |
|------|------|--------|------|
| 1 | Run Detection Heuristics | Evaluate DH-01 through DH-04 against context files | Read, Grep |
| 2 | Present Recommendations | AskUserQuestion with triggered heuristics and options | AskUserQuestion |
| 3 | Generate Reference Files | For each approved: read sources, extract, populate template, write | Read, Write |
| 4 | Verify No Contradictions | Compare generated content against source context files | Read, Grep |
| 5 | Report | Display files generated, sources, regeneration instructions | None |

**Postconditions:**
- Generated references contain only content derived from context files
- Each reference file includes auto-generation header with regeneration command
- No modifications to subagent core .md files (references/ directory only)

**Technical Specification:**

- File: `.claude/skills/designing-systems/references/domain-reference-generation.md`
- Estimated size: ~250 lines
- Depends on: Phase 5.5 completion (CLAP epic)

#### FR-004: SKILL.md Modification for Phase 5.7

**As a** framework maintainer,
**I want** the designing-systems SKILL.md updated to include Phase 5.7 with progressive disclosure loading,
**So that** the phase executes automatically as part of the /create-context workflow.

**Acceptance Criteria:**

- AC1: Phase 5.7 section added between Phase 5.5 and Phase 6 in SKILL.md
- AC2: Phase 5.7 uses on-demand reference loading: `Read(file_path=".claude/skills/designing-systems/references/domain-reference-generation.md")`
- AC3: Phase 5.7 precondition: "Phase 5.5 (Prompt Alignment) completed"
- AC4: Phase 5.7 postcondition: "Generated references contain only context-derived content"
- AC5: Estimated lines added to SKILL.md: ~25-30 (lean entry with reference loading)

**Technical Specification:**

- File to modify: `.claude/skills/designing-systems/SKILL.md`
- Insert location: After Phase 5.5 section (added by CLAP epic), before Phase 6 section
- New Phase 5.7 reference: `references/domain-reference-generation.md`

#### FR-005: Integration with /audit-alignment --generate-refs

**As a** framework maintainer,
**I want** to regenerate domain references on demand when context files are updated,
**So that** domain references stay in sync with the source of truth.

**Acceptance Criteria:**

- AC1: `/audit-alignment --generate-refs` flag triggers domain reference regeneration
- AC2: `--generate-refs` requires `--fix` flag (regeneration is a fix action)
- AC3: Regeneration overwrites existing `project-*.md` files with fresh content
- AC4: Regeneration re-evaluates all 4 detection heuristics (a heuristic that previously triggered may no longer trigger after context file updates)
- AC5: If a heuristic no longer triggers, the corresponding project-*.md file is flagged for removal (with user confirmation via AskUserQuestion)
- AC6: This FR creates a cross-epic dependency — the `/audit-alignment` command is created in the CLAP epic; this FR adds the `--generate-refs` flag handling

**Technical Specification:**

- File to modify: `.claude/commands/audit-alignment.md` (created in CLAP epic)
- Additional workflow step: Step 6 in command workflow (after --fix processing)
- Depends on: /audit-alignment command (CLAP epic FR-003)

### 3.2 Features Breakdown

| Feature | Stories | Priority | Effort |
|---------|---------|----------|--------|
| F1: Detection Heuristic Engine | FR-001 | MUST (Foundation) | 3 pts |
| F2: Reference File Template | FR-002 | MUST | 2 pts |
| F3: Phase 5.7 Workflow Integration | FR-003, FR-004 | MUST | 3 pts |
| F4: /audit-alignment --generate-refs | FR-005 | SHOULD | 2 pts |

---

## 4. Data Requirements

### 4.1 Generated File Locations

| Heuristic | Output File Path | Target Agent |
|-----------|-----------------|-------------|
| DH-01 | `.claude/agents/backend-architect/references/project-domain.md` | backend-architect |
| DH-02 | `.claude/agents/test-automator/references/project-testing.md` | test-automator |
| DH-03 | `.claude/agents/security-auditor/references/project-security.md` | security-auditor |
| DH-04 | `.claude/agents/code-reviewer/references/project-review.md` | code-reviewer |

### 4.2 GPUXtend Example (What Would Be Generated)

This concrete example shows what the detection heuristics would produce for the GPUXtend project:

| Reference File | Extends Agent | Content Source | Derived From |
|---------------|---------------|----------------|-------------|
| `backend-architect/references/project-domain.md` | backend-architect | CUDA Driver API patterns, Detours transaction lifecycle, Named Pipe IPC protocol, Patient Hook pattern, V5 address separation, fail-safe passthrough requirement | architecture-constraints.md, anti-patterns.md, coding-standards.md |
| `test-automator/references/project-testing.md` | test-automator | CMake/CTest patterns for native layer, `cargo test` for Rust, `pnpm test` for frontend, cross-boundary IPC test patterns | tech-stack.md, source-tree.md, coding-standards.md |
| `security-auditor/references/project-security.md` | security-auditor | DllMain constraints (no CRT calls in attach), env var injection guard (`GPUXTEND_INJECTED`), Named Pipe permission model, hook DLL export requirements | anti-patterns.md, architecture-constraints.md |
| `code-reviewer/references/project-review.md` | code-reviewer | 11 anti-patterns as structured review checklist, DriverStore vs System32 check, protocol header consistency (C++ and Rust), CRT runtime matching (/MT vs /MD) | anti-patterns.md, coding-standards.md, dependencies.md |

### 4.3 Data Constraints

| Constraint | Rule |
|------------|------|
| File naming | Must follow `project-*.md` pattern (e.g., `project-domain.md`, `project-testing.md`) |
| Content derivation | 100% of content must be extractable from context files; no synthesized knowledge |
| Auto-generation header | Required in every generated file; includes source list and regeneration command |
| No core agent modification | Generated files go in `references/` subdirectory only; agent .md files are untouched |
| Idempotency | Regeneration from same context files produces identical output |

---

## 5. Integration Requirements

### 5.1 Internal Integrations

| Integration | Direction | Purpose |
|-------------|-----------|---------|
| designing-systems Phase 5.5 | Predecessor → Phase 5.7 | Phase 5.5 completion triggers Phase 5.7 |
| designing-systems Phase 6 | Phase 5.7 → Successor | Phase 5.7 completion enables Phase 6 (epic creation) |
| /audit-alignment command | Command → Phase 5.7 logic | --generate-refs flag invokes regeneration |
| backend-architect subagent | Phase 5.7 → references/ | Generated project-domain.md loaded during /dev |
| test-automator subagent | Phase 5.7 → references/ | Generated project-testing.md loaded during /dev |
| security-auditor subagent | Phase 5.7 → references/ | Generated project-security.md loaded during /qa |
| code-reviewer subagent | Phase 5.7 → references/ | Generated project-review.md loaded during /qa |

### 5.2 Cross-Epic Dependencies

| Dependency | Direction | Detail |
|-----------|-----------|--------|
| CLAP Epic → This Epic | BLOCKING upstream | Phase 5.5 must exist before Phase 5.7 can insert after it |
| CLAP Epic → This Epic | BLOCKING upstream | /audit-alignment command must exist before --generate-refs flag can be added |
| This Epic → Subagent Loading | DOWNSTREAM | Subagents must be aware that project-*.md files may exist and should be loaded |

**Implementation order:** The CLAP epic MUST complete before this Domain Reference Generation epic begins.

### 5.3 File Modification Points

| File | Modification | Story |
|------|--------------|-------|
| `.claude/skills/designing-systems/references/domain-reference-generation.md` | NEW — Phase 5.7 workflow | FR-003 |
| `.claude/skills/designing-systems/SKILL.md` | MODIFY — add Phase 5.7 entry | FR-004 |
| `.claude/commands/audit-alignment.md` | MODIFY — add --generate-refs handling | FR-005 |
| `.claude/memory/skills-reference.md` | MODIFY — update designing-systems entry | FR-004 |
| `.claude/agents/backend-architect/references/project-domain.md` | GENERATED (per-project) — not in framework source | FR-003 |
| `.claude/agents/test-automator/references/project-testing.md` | GENERATED (per-project) — not in framework source | FR-003 |
| `.claude/agents/security-auditor/references/project-security.md` | GENERATED (per-project) — not in framework source | FR-003 |
| `.claude/agents/code-reviewer/references/project-review.md` | GENERATED (per-project) — not in framework source | FR-003 |

**Note:** The generated `project-*.md` files are per-project outputs. They are NOT framework source files. They are created in the project's working copy when /create-context (Phase 5.7) runs or when `/audit-alignment --generate-refs` is invoked.

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target | Rationale |
|--------|--------|-----------|
| Heuristic evaluation | <10 seconds for all 4 | Simple keyword/count analysis |
| Reference generation | <30 seconds per file | Read + extract + template population |
| Full Phase 5.7 | <120 seconds total | Acceptable for one-time project setup |

### 6.2 Maintainability

| Requirement | Implementation |
|-------------|----------------|
| Heuristics in reference file | Not hardcoded in SKILL.md; easy to add new heuristics |
| Template in reference file | Not hardcoded; template changes don't require skill modification |
| Regenerable outputs | /audit-alignment --generate-refs recreates from source |

### 6.3 Data Integrity

| Requirement | Implementation |
|-------------|----------------|
| Derivation purity | Generated content must be traceable to specific context file sections |
| No hallucination | Subagent generating references uses exact extraction, not summarization |
| Source attribution | Each section in generated file cites source context file and section |

---

## 7. Complexity Assessment

### 7.1 Score Breakdown

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Functional | 10 | 20 | 3 personas, 4 heuristics, template-based generation |
| Technical | 6 | 20 | File-based, no external services, text extraction |
| Team/Org | 4 | 10 | Solo development |
| NFR | 4 | 10 | Moderate performance, data integrity focus |
| **Total** | **24** | **60** | |

### 7.2 Architecture Tier

**Tier 2: Moderate Application** (Score 16-30)

- **Pattern:** Heuristic detection + template-based generation
- **Layers:** Skill Phase → Heuristic Engine → Template → File Output
- **Database:** File-based (context files → reference files)

### 7.3 Technology Recommendations

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Heuristic evaluation | Grep + Read | Pattern matching against context files |
| Template population | Read + Write | Extract sections, populate template, write output |
| Verification | Read + Grep | Compare generated content against source |

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: FEASIBLE

| Factor | Assessment | Risk |
|--------|------------|------|
| Progressive disclosure exists | ADR-012 pattern in place | Low |
| Reference file directories exist | All 4 target agents have references/ dirs | Low |
| Context file parsing | Standard Grep/Read operations | Low |
| Template population | String extraction and assembly | Low |

### 8.2 Risk Register

| Risk | Prob | Impact | Severity | Mitigation |
|------|------|--------|----------|------------|
| Heuristic false negatives (misses project needing refs) | Medium | Medium | MEDIUM | Conservative thresholds; user can run /audit-alignment --generate-refs manually |
| Generated content drifts from source | Low | High | MEDIUM | Verification step compares output against source |
| Subagents don't load project-*.md files | Medium | Medium | MEDIUM | Document loading convention; add loading hints to agent prompts if needed |
| Template too generic for diverse projects | Medium | Low | LOW | Template has optional sections; sections are omitted if context file lacks relevant content |

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| No new subagents | Locked Decision DR-1 | Extend existing agents via references only |
| References derived from context files | Locked Decision DR-2 | No independent domain knowledge in references |
| project-*.md naming convention | Locked Decision DR-3 | Consistent naming across all agent references |
| On-demand regeneration only | Locked Decision DR-4 | No auto-trigger on context file changes |
| Progressive disclosure (ADR-012) | Framework constraint | Reference files loaded on-demand |

### 9.2 Locked Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| DR-1 | Domain references, NOT new subagents | Preserves single source of truth, follows progressive disclosure, prevents agent sprawl |
| DR-2 | References are DERIVED from context files | Regenerable, not independent authorities; context files remain "THE LAW" |
| DR-3 | Naming convention is `project-*.md` | Consistent with existing references/ pattern (e.g., `framework-patterns.md`, `implementation-patterns.md`) |
| DR-4 | On-demand regeneration only | `/audit-alignment --generate-refs`; avoids hidden side-effects on ADR acceptance |

### 9.3 Assumptions

| Assumption | Status |
|------------|--------|
| All 4 target agents have references/ subdirectories | Validated — backend-architect, test-automator, security-auditor, code-reviewer all have references/ dirs |
| Context files contain sufficient domain knowledge for extraction | Validated — GPUXtend context files have detailed domain constraints |
| Subagents can be taught to load project-*.md files | Validated — progressive disclosure pattern already has on-demand loading |
| CLAP epic will be completed before this epic | Assumption — prerequisite dependency |

---

## 10. Epic Breakdown

### 10.1 Implementation Roadmap

```
Sprint N (after CLAP epic completion):
================================================================
Day 1-2:   STORY-A: Detection heuristic engine (4 heuristics)  - 3 pts
Day 2-3:   STORY-B: Reference file template                    - 2 pts
Day 3-5:   STORY-C: Phase 5.7 reference + SKILL.md update      - 3 pts
Day 5-6:   STORY-D: /audit-alignment --generate-refs flag      - 2 pts
================================================================
Total: 10 points in 1 sprint
```

### 10.2 Dependency Graph

```
[CLAP EPIC - COMPLETED] ──────────────────────────────────────
                              │ (blocking prerequisite)
                              ▼
STORY-A (Detection heuristics) ──┬──────────────────────────┐
                                 │                          │
STORY-B (Reference template) ────┘                          │
         [A and B are co-dependent,                         │
          deliver together]                                 │
                                 │                          │
                                 ▼                          │
                      STORY-C (Phase 5.7)                   │
                                 │                          │
                                 └──────────┬───────────────┘
                                            │
                                            ▼
                                 STORY-D (--generate-refs)
```

**Critical Path:** CLAP Epic → STORY-A+B → STORY-C → STORY-D

### 10.3 Cross-Epic Dependencies

| This Epic Needs | From CLAP Epic | Specific Deliverable |
|----------------|----------------|---------------------|
| Phase 5.5 exists in SKILL.md | FR-005 (CLAP) | Phase 5.7 inserts AFTER Phase 5.5 |
| /audit-alignment command exists | FR-003 (CLAP) | --generate-refs flag extends existing command |
| alignment-auditor subagent exists | FR-001 (CLAP) | Phase 5.7 may reuse alignment-auditor for verification |

### 10.4 The General Pattern for Any New DevForgeAI Project

After both epics are implemented, the `/create-context` workflow becomes:

```
/create-context
  Phase 1-5:   Create & validate 6 context files          (EXISTING)
  Phase 5.5:   Align system prompt & CLAUDE.md             (CLAP EPIC)
  Phase 5.7:   Generate project domain references          (THIS EPIC)
  Phase 6-7:   Epic creation & success report              (EXISTING)
```

**Every new DevForgeAI project automatically gets:**
1. 6 constitutional context files (existing)
2. A tuned system prompt `<project_context>` section (CLAP)
3. Project-specific domain references for relevant subagents (this epic)

### 10.5 Epic Summary

| Epic | Features | Points | Status | Prerequisite |
|------|----------|--------|--------|-------------|
| Domain Reference Generation | 4 features (5 FRs) | 10 pts | Planning | CLAP epic |

---

## 11. Next Steps

1. **Complete CLAP Epic first** — All CLAP stories must reach "Released" status
2. **Epic Creation:** `/create-epic Domain Reference Generation` — Creates EPIC file from this requirements specification
3. **Story Creation:** `/create-story` for each of the 4 stories (STORY-A through STORY-D)
4. **Sprint Planning:** `/create-sprint` — Assign stories to sprint
5. **Development:** `/dev STORY-XXX` — Implement via TDD workflow
6. **QA Validation:** `/qa STORY-XXX` — Validate each story

---

## Appendices

### A. GPUXtend Example: project-domain.md (What Would Be Generated for backend-architect)

```markdown
# Project Domain Reference: backend-architect

> **Auto-generated** from context files by CLAP Phase 5.7
> **Source files:** architecture-constraints.md, anti-patterns.md, coding-standards.md
> **Generated:** 2026-02-22
> **Regenerate:** `/audit-alignment --generate-refs`
> **DO NOT EDIT MANUALLY** — changes will be overwritten on regeneration.

## When to Load This Reference

Load this reference file when working on GPUXtend stories that involve:
- CUDA Driver API hook implementation
- Named Pipe IPC protocol changes
- Native C++ layer modifications
- Cross-boundary (C++ <-> Rust) interactions

## Domain-Specific Constraints

### CUDA Driver API Hooking
- All hooks MUST use Patient Hook pattern (mutex-guarded initialization, retryable on failure)
- V5 address separation: intercepted vs original function addresses stored separately
- Fail-safe passthrough: if hook initialization fails, original CUDA function MUST still work

### Named Pipe IPC Protocol
- Pipe name: \\.\pipe\GPUXtend
- Header size: 24 bytes (type: u8, flags: u8, reserved: u16, payload_length: u32, ...)
- Max message size: 64KB
- Protocol is synchronous request-response

### Concurrency Model
- Hook DLL: single-threaded initialization, multi-threaded dispatch
- Service layer: async Rust (tokio runtime)
- No shared mutable state between layers (IPC enforces boundary)

## Forbidden Patterns (Project-Specific)

- [ ] std::call_once for hook initialization (consumed on first attempt, blocks retries)
- [ ] CRT calls in DllMain DLL_PROCESS_ATTACH (deadlock risk with loader lock)
- [ ] Direct GPU memory access from service layer (must go through hook DLL)
- [ ] Hardcoded DriverStore paths (use dynamic resolution)
- [ ] Mixed /MT and /MD CRT runtimes in same process
- [ ] ... (remaining 6 anti-patterns extracted from anti-patterns.md)

## Language-Specific Patterns

### C++ (Native Layer)
- RAII for all resource management
- COM-style error codes (HRESULT) at API boundary
- Structured exception handling (SEH) for crash resilience

### Rust (Service Layer)
- thiserror for error types
- tracing for instrumentation (not println!)
- anyhow at binary boundaries only

## Build and Test Commands

### Native C++ (CMake)
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build

### Rust Service (Cargo)
cargo build --release
cargo test

### Frontend (pnpm)
pnpm install
pnpm test
```

### B. Glossary

| Term | Definition |
|------|------------|
| Domain Reference | A project-specific reference file generated from context files, extending a generic subagent with specialized knowledge |
| Detection Heuristic | A rule that evaluates context files to determine if a specific subagent needs a domain reference |
| Progressive Disclosure | ADR-012 pattern where agent knowledge is split between core prompt and on-demand reference files |
| Derivation Purity | The principle that generated references contain ONLY content from context files, with no synthesized additions |

### C. References

- **ENH-CLAP-001:** `tmp/ENH-CLAP-001-configuration-layer-alignment-protocol.md` (source proposal, Part 3)
- **ADR-012:** Progressive Disclosure (agent reference file pattern)
- **CLAP Requirements:** `devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md` (prerequisite epic)
- **backend-architect.md:** `.claude/agents/backend-architect.md` (example of agent with existing references/)
- **test-automator.md:** `.claude/agents/test-automator.md` (example of agent with existing references/)

### D. Open Questions

None — all questions from ENH-CLAP-001 resolved with locked decisions (see Section 9.2).

---

**Requirements Specification Version:** 1.0
**Created:** 2026-02-22
**Last Updated:** 2026-02-22
**Source:** ENH-CLAP-001 (Part 3)
**Prerequisite:** CLAP Configuration Layer Alignment Requirements
