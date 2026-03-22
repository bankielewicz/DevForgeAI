# Configuration Layer Alignment Protocol (CLAP) - Requirements Specification

**Version:** 1.0
**Date:** 2026-02-22
**Status:** Draft
**Author:** DevForgeAI Ideation (from ENH-CLAP-001)
**Complexity Score:** 32/60 (Tier 2 - Moderate)
**Source:** ENH-CLAP-001 (GPUXtend system prompt alignment investigation)

---

## 1. Project Overview

### 1.1 Project Context

| Attribute | Value |
|-----------|-------|
| **Type** | Brownfield (Framework Enhancement) |
| **Domain** | Developer Tooling / Configuration Integrity |
| **Timeline** | 1-2 sprints (~2-3 weeks) |
| **Team** | Solo framework development |
| **Estimated Effort** | 16 story points |

### 1.2 Problem Statement

**Framework users** experience **configuration drift and contradictions** because **no existing validator performs cross-layer configuration analysis**, resulting in **conflicting instructions delivered to the AI orchestrator, suboptimal delegation, and incorrect behavior**.

**Evidence (from ENH-CLAP-001 investigation on GPUXtend project):**

During GPUXtend system prompt tuning, a manual 5-step reasoning process uncovered 5 actionable gaps:

| Finding | Layer A | Layer B | Severity |
|---------|---------|---------|----------|
| `std::call_once` described as implementation pattern | CLAUDE.md line 45 | anti-patterns.md #3 (FORBIDDEN) | HIGH — Direct contradiction |
| No platform constraint in system prompt | System prompt (absent) | tech-stack.md lines 64-70 (Windows 11 x64) | HIGH — Missing awareness |
| No build system routing in system prompt | System prompt (absent) | tech-stack.md (3 build systems: Cargo, CMake, pnpm) | HIGH — Missing routing |
| No subagent routing for C++ native layer | System prompt (absent) | architecture-constraints.md layer table | HIGH — Wrong delegation |
| No sprint state awareness | System prompt (absent) | architecture-constraints.md sprint annotations | MEDIUM — Stale suggestions |

**Root Cause:** All existing validators check in ONE direction only:

| Existing Validator | What It Checks | What It CANNOT Check |
|--------------------|----------------|----------------------|
| `context-validator` | Source code vs context files | CLAUDE.md vs context files |
| `tech-stack-detector` | Project files vs tech-stack.md | System prompt vs tech-stack.md |
| `/validate-stories` | Story content vs context files | Context files vs each other |
| `context-preservation-validator` | Story provenance chain | ADR propagation to context files |
| `/audit-orphans` | Filesystem hygiene | Configuration layer alignment |

**None reads CLAUDE.md, the system prompt, or rules against context files. None reads context files against each other.**

### 1.3 Solution Overview

Codify the manual 5-step reasoning methodology as a repeatable **Configuration Layer Alignment Protocol (CLAP)** with 4 framework components:

1. **`alignment-auditor` subagent** — Read-only validator that performs pairwise comparison across all configuration layers (CLAUDE.md, system prompt, 6 context files, rules, ADRs)
2. **`/audit-alignment` command** — User-facing entry point for on-demand auditing with layer filtering and fix proposals
3. **Phase 5.5 in `designing-systems` skill** — Automatic alignment check after `/create-context` creates context files, before epic creation
4. **ADR-021** — Decision record documenting the CLAP methodology and its integration

### 1.4 The 5-Step CLAP Methodology

This is the exact reasoning chain that discovered each finding, now codified for automation:

**Step 1 — Layer Identification:** Catalogue every configuration surface that Claude loads at session start.

| Layer | File(s) | Authority Level | Mutability |
|-------|---------|----------------|------------|
| System Prompt | `.claude/system-prompt-core.md` | Behavioral orchestration (identity, rules, phases) | MUTABLE (framework-owned, project-customizable) |
| CLAUDE.md | `/CLAUDE.md` | Project onboarding card (build commands, architecture overview) | MUTABLE (project-owned) |
| Context Files (6) | `devforgeai/specs/context/*.md` | Constitutional constraints (authoritative ground truth) | IMMUTABLE (changes require ADR) |
| Rules | `.claude/rules/**/*.md` | Cross-cutting enforcement (security, workflow, quality gates) | MUTABLE (framework-owned) |
| ADRs | `devforgeai/specs/adrs/*.md` | Architectural decision journal | APPEND-ONLY (supersede, don't edit) |

**Step 2 — Layer Purpose & Authority Analysis:** Determine precedence for contradiction resolution.

```
Context Files (6)  = HIGHEST AUTHORITY  (immutable, constitutional)
         defers to
System Prompt      = ORCHESTRATOR       (should reference, never contradict)
         defers to
CLAUDE.md          = SUMMARY CARD       (must be consistent derivative)
         defers to
Rules              = ENFORCEMENT        (policies about HOW, not WHAT)
         defers to
ADRs               = DECISION HISTORY   (accepted decisions must propagate UP)
```

Contradictions resolve TOWARD the highest-authority source. If CLAUDE.md says X and anti-patterns.md says NOT-X, CLAUDE.md must change.

**Step 3 — Cross-Reference Validation (Contradiction Detection):** Systematically compare claims across layers using pairwise comparison. For N layers, there are N*(N-1)/2 comparison pairs.

**Step 4 — Completeness Analysis (Delegation Fitness):** Ask "does the orchestrator know enough to delegate effectively?" Gaps cause SUBOPTIMAL behavior — the orchestrator works but delegates less precisely.

**Step 5 — Minimal Intervention Design:** Apply the principle of smallest change that closes all gaps. The layered architecture is correct. The fix is a thin bridge layer that gives the orchestrator enough awareness to delegate well.

### 1.5 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Contradiction detection precision | >90% | Test with known CLAUDE.md vs anti-patterns contradictions |
| False positive rate | 0% for prose similarity | Verify exact claim matching, not semantic similarity |
| Validation check completeness | 15/15 checks implemented | Audit against validation matrix |
| Phase 5.5 blocking behavior | 100% block on HIGH contradictions | Test with HIGH severity finding |
| /audit-alignment JSON output | 100% schema compliance | Validate against Appendix A schema |
| Audit execution time | <60 seconds full audit | Performance benchmark |

---

## 2. User Roles & Personas

### 2.1 Primary Users

| Role | Description | Usage Frequency |
|------|-------------|-----------------|
| Framework Developer | Uses /create-context to set up new projects | Per new project |
| Claude AI Orchestrator | Reads configuration layers at session start | Every session |
| Framework Maintainer | Monitors configuration drift over time | Sprint start (recommended) |

### 2.2 User Personas

**Persona 1: Project Bootstrapper**
- **Role:** Developer running /create-context on a new project
- **Goals:** Fully aligned configuration layers from day one
- **Needs:** Automatic alignment check after context file creation
- **Pain Points:** Manual multi-file comparison is tedious and error-prone; contradictions discovered late during development

**Persona 2: Claude AI Orchestrator**
- **Role:** AI agent reading all configuration layers at session start
- **Goals:** Consistent, non-contradictory instructions across all layers
- **Needs:** All layers agree on technologies, patterns, constraints, and project state
- **Pain Points:** Conflicting instructions cause wrong behavior (e.g., suggesting forbidden patterns)

**Persona 3: Framework Maintainer**
- **Role:** Monitors and maintains DevForgeAI framework health
- **Goals:** Catch configuration drift before it causes issues
- **Needs:** On-demand audit command with severity-based reporting
- **Pain Points:** No tool exists to check cross-layer alignment; drift accumulates silently

---

## 3. Functional Requirements

### 3.1 User Stories

#### FR-001: alignment-auditor Subagent

**As a** framework maintainer,
**I want** a read-only subagent that performs pairwise comparison across all configuration layers,
**So that** contradictions and gaps are detected automatically with structured evidence.

**Acceptance Criteria:**

- AC1: Subagent uses canonical agent template v2.0.0 with 10 required sections
- AC2: Model is `haiku` (text comparison task, not code generation)
- AC3: Tools restricted to Read, Glob, Grep (read-only only)
- AC4: Core agent file is ≤500 lines per ADR-012 progressive disclosure
- AC5: Implements all 15 validation checks (CC-01 through CC-10, CMP-01 through CMP-04, ADR-01) — see FR-002 for check definitions
- AC6: Reads all 6 context files as required input (HALT if any missing)
- AC7: Reads CLAUDE.md, system-prompt-core.md, rules, and ADRs as optional input (SKIP checks if missing, report as GAP)
- AC8: Output is structured JSON matching the schema defined in Appendix A of this document
- AC9: Distinguishes contradictions (content conflicts — wrong behavior) from gaps (missing content — suboptimal behavior)
- AC10: Reports line numbers for all findings
- AC11: Proposes resolutions that respect layer mutability rules (never proposes editing context files)
- AC12: Uses exact text matching for pattern names and technology names (no semantic/prose similarity matching)

**Technical Specification:**

- File: `.claude/agents/alignment-auditor.md`
- Reference file: `.claude/agents/alignment-auditor/references/validation-matrix.md`
- Pattern reference: `.claude/agents/context-validator.md` (similar read-only validator pattern)
- Frontmatter fields: name, description, tools, model, version, proactive_triggers
- Proactive triggers: "after /create-context Phase 5 completes", "after ADR acceptance", "when /audit-alignment command invoked"

#### FR-002: Validation Matrix Reference File

**As a** framework maintainer,
**I want** the complete validation check definitions stored in a progressive-disclosure reference file,
**So that** the alignment-auditor agent prompt stays lean while check logic is comprehensive.

**Acceptance Criteria:**

- AC1: Reference file contains all 15 checks organized by category (CC = Contradiction Check, CMP = Completeness Check, ADR = ADR Propagation Check)
- AC2: Each check has: id, category, severity, layer_a, layer_b, description, method, example_finding
- AC3: File is loaded on-demand by alignment-auditor during execution (not baked into agent prompt)

**Complete Validation Matrix (15 checks):**

**Contradiction Checks (CC-01 through CC-10):**

| Check ID | Severity | Layer A | Layer B | Description | Method |
|----------|----------|---------|---------|-------------|--------|
| CC-01 | HIGH | CLAUDE.md | anti-patterns.md | Pattern names in CLAUDE.md that appear in anti-patterns forbidden list | Extract all `##` headings from anti-patterns.md. For each forbidden pattern name, search CLAUDE.md for that pattern name. If found in non-warning context, flag as contradiction. |
| CC-02 | HIGH | CLAUDE.md | tech-stack.md | Technologies, versions, build commands, platform consistency | Extract technology names and versions from tech-stack.md tables. Search CLAUDE.md for each technology name. If version differs or prohibited technology is mentioned positively, flag. |
| CC-03 | MEDIUM | CLAUDE.md | architecture-constraints.md | Architecture description accuracy (layer boundaries, IPC protocol, component relationships) | Compare architecture descriptions in CLAUDE.md against architecture-constraints.md sections. Check protocol constants (header size, pipe name, max message size). |
| CC-04 | MEDIUM | CLAUDE.md | source-tree.md | File paths and component locations consistency | Extract file paths mentioned in CLAUDE.md. Verify each exists in source-tree.md directory listing. |
| CC-05 | LOW | CLAUDE.md | coding-standards.md | Code examples in CLAUDE.md follow coding-standards.md patterns | If CLAUDE.md contains code examples, verify they follow patterns defined in coding-standards.md. |
| CC-06 | MEDIUM | CLAUDE.md | dependencies.md | Listed dependencies and versions consistency | Extract dependency names from CLAUDE.md. Cross-reference with dependencies.md approved list and version pins. |
| CC-07 | HIGH | system-prompt-core.md | tech-stack.md | Platform constraint and technology references | Extract platform section from tech-stack.md. Check system prompt for platform awareness. Extract prohibited technologies and verify system prompt doesn't recommend them. |
| CC-08 | HIGH | system-prompt-core.md | architecture-constraints.md | Layer boundaries and build system understanding | Extract build system sections from architecture-constraints.md. Check system prompt for build routing awareness. Verify subagent routing covers all component types. |
| CC-09 | MEDIUM | .claude/rules/**/*.md | devforgeai/specs/context/*.md | Rule references match context constraints | Extract technology/pattern references from rule files. Verify each reference exists in the corresponding context file. |
| CC-10 | MEDIUM | devforgeai/specs/context/*.md | devforgeai/specs/context/*.md | Cross-references between 6 context files agree | Check: dependencies.md packages vs tech-stack.md technologies, source-tree.md paths vs coding-standards.md naming conventions, architecture-constraints.md layers vs source-tree.md directory structure. |

**Completeness Checks (CMP-01 through CMP-04):**

| Check ID | Severity | Source Layer | Target Layer | Description | Method |
|----------|----------|-------------|-------------|-------------|--------|
| CMP-01 | HIGH | tech-stack.md | system-prompt-core.md | Platform constraint present in system prompt | Read tech-stack.md 'Platform' or OS section. Check system prompt for platform guard statement. |
| CMP-02 | MEDIUM | tech-stack.md + source-tree.md | CLAUDE.md | All build systems and commands documented in CLAUDE.md | Extract all build system sections from tech-stack.md. For each, verify CLAUDE.md has a corresponding build command section. |
| CMP-03 | HIGH | architecture-constraints.md | system-prompt-core.md | Subagent routing for all component types | Extract component/layer types from architecture-constraints.md dependency table. Check system prompt for explicit routing of each to appropriate subagent. |
| CMP-04 | MEDIUM | architecture-constraints.md | system-prompt-core.md | Sprint/phase awareness matching current project state | Search architecture-constraints.md for sprint annotations or phase markers. If present, check system prompt for corresponding state awareness. |

**ADR Propagation Check (ADR-01):**

| Check ID | Severity | Source Layer | Target Layer | Description | Method |
|----------|----------|-------------|-------------|-------------|--------|
| ADR-01 | MEDIUM | devforgeai/specs/adrs/ADR-*.md | devforgeai/specs/context/*.md | Every accepted ADR decision reflected in relevant context file(s) | Read each ADR with status 'Accepted'. Extract the 'Decision' section. Search context files for evidence that the decision was incorporated. If missing, flag as propagation drift. |

**Example Findings per Check:**

| Check | Example Finding |
|-------|-----------------|
| CC-01 | CLAUDE.md says 'via std::call_once' but anti-patterns.md #3 forbids std::call_once |
| CC-02 | CLAUDE.md lists 'npm install' but tech-stack.md prohibits npm |
| CC-03 | CLAUDE.md says '16-byte header' but architecture-constraints.md says '24-byte header' |
| CC-04 | CLAUDE.md references 'src/hook/' but source-tree.md says 'native/hook/' |
| CC-05 | CLAUDE.md shows println!() but coding-standards.md requires tracing::info!() |
| CC-06 | CLAUDE.md mentions 'Detours 3.0' but dependencies.md pins 'Detours 4.0.1' |
| CC-07 | tech-stack.md says Windows-only but system prompt has no platform guard |
| CC-08 | architecture-constraints.md defines 3 build systems but system prompt only routes for Cargo |
| CC-09 | Rule references 'TypeScript strict mode' but tech-stack.md doesn't list TypeScript |
| CC-10 | dependencies.md lists 'express' but tech-stack.md prohibits Node.js |
| CMP-01 | tech-stack.md declares Windows 11 x64 but system prompt has no platform constraint |
| CMP-02 | tech-stack.md lists CMake build system but CLAUDE.md has no CMake build commands |
| CMP-03 | architecture-constraints.md defines C++ native layer but system prompt doesn't route it to any subagent |
| CMP-04 | architecture-constraints.md annotates Sprint 2 modules but system prompt has no sprint awareness |
| ADR-01 | ADR-003 accepted 'Use Redis for caching' but tech-stack.md has no Redis entry |

#### FR-003: /audit-alignment Command

**As a** framework maintainer,
**I want** an on-demand audit command with layer filtering and fix proposals,
**So that** I can check alignment at any time and resolve drift.

**Acceptance Criteria:**

- AC1: Command follows lean orchestration pattern (validate → set markers → invoke subagent)
- AC2: Character budget ≤10,000 (67% of 15K limit)
- AC3: Supports `--layer` argument with values: all (default), claudemd, prompt, context, rules, adrs
- AC4: Supports `--fix` argument (boolean, default false) — proposes edits for MUTABLE layers, requires AskUserQuestion approval for every proposed edit
- AC5: Supports `--output` argument with values: console (default), file (writes to `devforgeai/qa/alignment-audit-{date}.md`)
- AC6: Invokes alignment-auditor subagent via Task()
- AC7: Formats results using severity-based display (CRITICAL/HIGH/MEDIUM/LOW)
- AC8: Executive summary table showing counts per category (contradictions, gaps, ADR drift)

**--fix Mutability Rules (CRITICAL — enforced, not suggested):**

| Layer | Mutability | --fix Behavior |
|-------|-----------|----------------|
| CLAUDE.md | MUTABLE | Propose specific line edits → AskUserQuestion approval |
| system-prompt-core.md | MUTABLE | Propose `<project_context>` additions → AskUserQuestion approval |
| Context files (6) | IMMUTABLE | Flag for ADR creation (cannot auto-fix) |
| Rules | MUTABLE | Propose edits → AskUserQuestion approval |
| ADRs | APPEND-ONLY | Recommend new ADR (cannot edit existing) |

**Command Usage Examples:**

```bash
/audit-alignment                     # Full audit, all layers, console output
/audit-alignment --layer=claudemd    # CLAUDE.md vs context files only
/audit-alignment --layer=prompt      # System prompt vs context files only
/audit-alignment --fix               # Propose edits for MUTABLE layers
/audit-alignment --output=file       # Write report to devforgeai/qa/
```

**Technical Specification:**

- File: `.claude/commands/audit-alignment.md`
- Pattern reference: `.claude/commands/audit-orphans.md` (lean orchestration audit pattern)
- Model: opus
- Allowed tools: Read, Glob, Grep, Task, AskUserQuestion, Edit, Write

**Command Workflow (7 steps):**

| Step | Action | Tools |
|------|--------|-------|
| 1 | Parse arguments (--layer, --fix, --output) | None |
| 2 | Set context markers | None |
| 3 | Invoke alignment-auditor subagent via Task() | Task |
| 4 | Format results for display | None |
| 5 | If --fix, iterate findings and propose edits via AskUserQuestion | AskUserQuestion, Edit |
| 6 | If --output=file, write report | Write |
| 7 | Display summary | None |

#### FR-004: Phase 5.5 Reference File for designing-systems Skill

**As a** developer running /create-context,
**I want** automatic alignment checking after context files are created,
**So that** CLAUDE.md and system prompt are aligned with the new context files before epic creation begins.

**Acceptance Criteria:**

- AC1: Phase 5.5 is named "Prompt Alignment" and inserts between Phase 5 (Validate Spec Against Context) and Phase 6 (Epic Creation)
- AC2: Reference file follows progressive disclosure pattern (loaded on-demand, not inlined in SKILL.md)
- AC3: Phase 5.5 reads CLAUDE.md and .claude/system-prompt-core.md (graceful handling if either missing)
- AC4: Phase 5.5 invokes alignment-auditor subagent with freshly-created context files
- AC5: If contradictions found → present via AskUserQuestion with resolution options (Apply fix / Skip / Edit manually)
- AC6: If system prompt gaps found → synthesize `<project_context>` section from context files, present for approval
- AC7: If CLAUDE.md gaps found → draft missing sections (build commands, architecture overview) from context files
- AC8: If neither CLAUDE.md nor system-prompt-core.md exists → recommend creating them (informational, not blocking)
- AC9: HIGH-severity contradictions block progression to Phase 6 (mandatory resolution)
- AC10: MEDIUM/LOW contradictions may be deferred with justification (non-blocking)
- AC11: System prompt gaps are informational (project may choose not to use system prompt)

**`<project_context>` Template (for system prompt gap resolution):**

```markdown
<project_context>
## {project_name} — {one_line_description}

### Platform Constraint
{extracted_from_tech_stack_md_platform_section}

### Build System Routing
{for_each_build_system_in_tech_stack_md}

### Subagent Routing
{component_to_subagent_mapping_from_architecture_constraints_md}

### Current State
{sprint_annotations_from_architecture_constraints_md_if_present}
</project_context>
```

**Technical Specification:**

- File: `.claude/skills/designing-systems/references/prompt-alignment-workflow.md`
- Estimated size: ~200 lines
- Depends on: alignment-auditor subagent (FR-001)

**Phase 5.5 Workflow (6 steps):**

| Step | Name | Action | Tool |
|------|------|--------|------|
| 1 | Detect Configuration Layers | Read CLAUDE.md and system-prompt-core.md | Read |
| 2 | Invoke alignment-auditor | Task(subagent_type="alignment-auditor") against freshly-created context files | Task |
| 3 | Process Contradictions | Display Layer A/B text, explain authority, propose edit, AskUserQuestion | AskUserQuestion, Edit |
| 4 | Process Gaps | Synthesize project_context section, present for approval | AskUserQuestion, Edit |
| 5 | Process ADR Propagation Drift | Flag un-propagated ADRs, recommend follow-up ADR or debt tracking | AskUserQuestion |
| 6 | Report | Display summary of resolved/deferred items, proceed to Phase 6 | None |

**Postconditions:**
- Zero HIGH-severity contradictions remain unresolved (blocking)
- MEDIUM/LOW contradictions may be deferred with justification (non-blocking)
- System prompt gaps are informational — project may choose not to use system prompt

#### FR-005: SKILL.md Modification for Phase 5.5

**As a** framework maintainer,
**I want** the designing-systems SKILL.md updated to include Phase 5.5 with progressive disclosure loading,
**So that** the phase executes automatically as part of the /create-context workflow.

**Acceptance Criteria:**

- AC1: Phase 5.5 section added between Phase 5 and Phase 6 in SKILL.md
- AC2: Phase 5.5 uses on-demand reference loading: `Read(file_path=".claude/skills/designing-systems/references/prompt-alignment-workflow.md")`
- AC3: Phase 5.5 precondition: "Phase 5 (Validate Spec Against Context) completed successfully" AND "All 6 context files exist and are non-empty"
- AC4: Phase 5.5 postcondition: "Zero HIGH-severity contradictions remain unresolved"
- AC5: Estimated lines added to SKILL.md: ~30-40 (lean entry with reference loading)

**Technical Specification:**

- File to modify: `.claude/skills/designing-systems/SKILL.md` (currently 393 lines)
- Insert location: After Phase 5 section, before Phase 6 section
- Current Phase 5 reference: `references/architecture-validation.md`
- New Phase 5.5 reference: `references/prompt-alignment-workflow.md`

#### FR-006: ADR-021 — Configuration Layer Alignment Protocol

**As a** framework maintainer,
**I want** an Architecture Decision Record documenting the CLAP methodology,
**So that** the reasoning, decisions, and integration points are formally recorded.

**Acceptance Criteria:**

- AC1: ADR number is ADR-021 (next available after ADR-020)
- AC2: Status is "Accepted"
- AC3: Context section explains the validation gap (no cross-layer checking exists today)
- AC4: Decision section documents: 5-step methodology, new subagent, new command, Phase 5.5 integration
- AC5: Rationale section explains why alignment-auditor is separate from context-validator (single responsibility, different model requirements)
- AC6: Consequences section documents: trigger points, where CLAP does NOT run, mutability rules
- AC7: References section links to ENH-CLAP-001 and this requirements specification

**Technical Specification:**

- File: `devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md`
- Format: Standard ADR format (YAML frontmatter + Context/Decision/Rationale/Consequences/References sections)
- Estimated size: ~80-100 lines

#### FR-007: Memory File Updates (Documentation)

**As a** framework user,
**I want** the commands-reference, subagents-reference, and skills-reference updated,
**So that** /audit-alignment, alignment-auditor, and Phase 5.5 are discoverable.

**Acceptance Criteria:**

- AC1: `.claude/memory/commands-reference.md` — Add `/audit-alignment` entry to Framework Maintenance section (count increases from current to +1), add detailed subsection with purpose, invokes, workflow, example, output, architecture, and related commands
- AC2: `.claude/memory/subagents-reference.md` — Add `alignment-auditor` entry to subagents catalog (alphabetical), add proactive trigger mapping entry
- AC3: `.claude/memory/skills-reference.md` — Update designing-systems entry to include Phase 5.5 with reference file listing

**Technical Specification:**

- Files to modify: 3 memory files
- Estimated lines added: ~45 total (15 + 20 + 10)

### 3.2 Features Breakdown

| Feature | Stories | Priority | Effort |
|---------|---------|----------|--------|
| F1: alignment-auditor Subagent | FR-001, FR-002 | MUST (Foundation) | 5 pts |
| F2: /audit-alignment Command | FR-003 | MUST | 3 pts |
| F3: Phase 5.5 Workflow Integration | FR-004, FR-005 | MUST | 3 pts |
| F4: ADR-021 Decision Record | FR-006 | MUST | 2 pts |
| F5: Documentation Updates | FR-007 | MUST | 3 pts |

---

## 4. Data Requirements

### 4.1 Data Model

#### Entity: CLAP Audit Report (JSON Output)

The alignment-auditor subagent produces a structured JSON report. The complete schema:

```json
{
  "protocol_version": "1.0",
  "timestamp": "2026-02-22T10:30:00Z",
  "project": "{project_name}",
  "layers_found": {
    "claude_md": { "exists": true, "size_chars": 4812 },
    "system_prompt": { "exists": true, "size_chars": 3200 },
    "context_files": { "count": 6, "expected": 6 },
    "rules": { "count": 14 },
    "adrs": { "count": 2, "accepted": 2, "superseded": 0 }
  },
  "contradictions": [
    {
      "id": "CC-001",
      "severity": "HIGH",
      "check_id": "CC-01",
      "layer_a": { "file": "CLAUDE.md", "line": 45, "text": "installs CUDA hooks via std::call_once" },
      "layer_b": { "file": "devforgeai/specs/context/anti-patterns.md", "line": 53, "text": "FORBIDDEN: std::call_once for CUDA hook initialization" },
      "resolution": "Update CLAUDE.md line 45 to say 'mutex-guarded initialization (retryable on failure)'"
    }
  ],
  "gaps": [
    {
      "id": "GAP-001",
      "severity": "HIGH",
      "check_id": "CMP-01",
      "layer": ".claude/system-prompt-core.md",
      "missing": "Platform constraint (Windows 11 x64, CUDA 13+)",
      "source_of_truth": "devforgeai/specs/context/tech-stack.md lines 64-70",
      "resolution": "Add platform guard to <project_context> section"
    }
  ],
  "adr_propagation": [
    {
      "adr": "ADR-002",
      "title": "CUDA Driver API Hooks",
      "status": "Accepted",
      "reflected_in": ["anti-patterns.md #2", "anti-patterns.md #4"],
      "missing_from": [],
      "propagation_status": "FULLY_PROPAGATED"
    }
  ],
  "summary": {
    "contradictions": 1,
    "gaps": 3,
    "adr_drift": 0,
    "overall_status": "FINDINGS_DETECTED"
  }
}
```

**Status Values:** PASS, FINDINGS_DETECTED, CRITICAL_FINDINGS
**Severity Levels:** LOW, MEDIUM, HIGH, CRITICAL

### 4.2 Data Constraints

| Constraint | Rule |
|------------|------|
| Finding IDs | CC-NNN or GAP-NNN or ADR-NNN, sequential per category |
| Severity | Must be LOW, MEDIUM, HIGH, or CRITICAL |
| Line numbers | Positive integers, must reference actual file content |
| File paths | Relative to project root, forward slashes |
| Resolution text | Must respect layer mutability (never propose editing IMMUTABLE layers) |

---

## 5. Integration Requirements

### 5.1 Internal Integrations

| Integration | Direction | Purpose |
|-------------|-----------|---------|
| designing-systems Phase 5 | Predecessor → Phase 5.5 | Phase 5 completion triggers Phase 5.5 |
| designing-systems Phase 6 | Phase 5.5 → Successor | Phase 5.5 completion gates Phase 6 (epic creation) |
| /audit-alignment command | Command → alignment-auditor | On-demand invocation |
| alignment-auditor subagent | Subagent → JSON report | Produces structured audit output |

### 5.2 Trigger Points

| Trigger | When | Automatic? | What Runs |
|---------|------|-----------|-----------|
| After /create-context | Phase 5.5 | YES (automatic) | Full CLAP |
| After ADR acceptance | Post-creation | YES (proactive trigger) | ADR propagation check only |
| /audit-alignment invoked | On demand | MANUAL | Full CLAP or layer-specific |
| Sprint start | Recommended practice | MANUAL | Full CLAP to catch drift |

**Where CLAP does NOT run (to avoid workflow bloat):**
- NOT during /dev — too frequent; context-validator handles code compliance per-commit
- NOT during /qa — QA validates implementation quality, not meta-configuration
- NOT during story creation — stories reference context files, already validated by /validate-stories

### 5.3 File Modification Points

| File | Modification | Story |
|------|--------------|-------|
| `.claude/agents/alignment-auditor.md` | NEW — subagent definition | FR-001 |
| `.claude/agents/alignment-auditor/references/validation-matrix.md` | NEW — check definitions | FR-002 |
| `.claude/commands/audit-alignment.md` | NEW — command definition | FR-003 |
| `.claude/skills/designing-systems/references/prompt-alignment-workflow.md` | NEW — Phase 5.5 workflow | FR-004 |
| `.claude/skills/designing-systems/SKILL.md` | MODIFY — add Phase 5.5 entry | FR-005 |
| `devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md` | NEW — decision record | FR-006 |
| `.claude/memory/commands-reference.md` | MODIFY — add /audit-alignment | FR-007 |
| `.claude/memory/subagents-reference.md` | MODIFY — add alignment-auditor | FR-007 |
| `.claude/memory/skills-reference.md` | MODIFY — update designing-systems | FR-007 |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target | Rationale |
|--------|--------|-----------|
| Full audit execution | <60 seconds | Acceptable for on-demand audit |
| Per-check execution | <4 seconds average | 15 checks * 4s = 60s budget |
| Memory footprint | Standard haiku context | No large file processing |

### 6.2 Security

| Requirement | Implementation |
|-------------|----------------|
| Read-only operations | alignment-auditor has no Write/Edit tools |
| No sensitive data exposure | Audit report contains file paths and line numbers, not secrets |
| User approval for all edits | --fix requires AskUserQuestion for every proposed change |

### 6.3 Maintainability

| Requirement | Implementation |
|-------------|----------------|
| Validation matrix in reference file | Not hardcoded in agent prompt; easy to add new checks |
| Progressive disclosure pattern | ADR-012 compliant; agent prompt ≤500 lines |
| Severity thresholds configurable | Check severity defined in validation matrix, not hardcoded |

---

## 7. Complexity Assessment

### 7.1 Score Breakdown

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Functional | 14 | 20 | 3 personas, 15 validation checks, multi-layer analysis |
| Technical | 8 | 20 | File-based, no external services, text comparison |
| Team/Org | 5 | 10 | Solo development |
| NFR | 5 | 10 | Moderate performance, no compliance requirements |
| **Total** | **32** | **60** | |

### 7.2 Architecture Tier

**Tier 2: Moderate Application** (Score 16-30)

- **Pattern:** Read-only analysis with structured output
- **Layers:** Command → Subagent → Reference File → JSON Output
- **Database:** File-based (Markdown configuration files)
- **Deployment:** In-place framework files

### 7.3 Technology Recommendations

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Subagent model | haiku | Text comparison, not code generation; cost-efficient |
| Analysis tools | Read, Glob, Grep | Native Claude Code tools; read-only |
| Output format | JSON | Machine-parseable, structured evidence |
| Report format | Markdown | Human-readable, consistent with existing audit reports |

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: FEASIBLE

| Factor | Assessment | Risk |
|--------|------------|------|
| Subagent creation | Canonical template v2.0.0 exists | Low |
| Text comparison | Grep/Read pattern matching | Low |
| Skill enhancement | Progressive disclosure pattern exists | Low |
| Command creation | Lean orchestration pattern exists | Low |

### 8.2 Business Feasibility: FEASIBLE

| Factor | Assessment |
|--------|------------|
| Budget | No external costs (framework internal) |
| Team | Solo development capacity sufficient |
| Timeline | 1-2 sprints achievable for 16 points |

### 8.3 Risk Register

| Risk | Prob | Impact | Severity | Mitigation |
|------|------|--------|----------|------------|
| False positives from text similarity | Medium | High | HIGH | Exact claim matching only, not semantic similarity |
| Token cost of loading all layers | Low | Medium | MEDIUM | haiku model keeps costs low |
| Phase 5.5 slows /create-context | Low | Low | LOW | Opt-out possible (skip if no CLAUDE.md/prompt exists) |
| Validation matrix incomplete | Medium | Medium | MEDIUM | Start with 15 checks, extend via reference file updates |

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints

| Constraint | Source | Impact |
|------------|--------|--------|
| alignment-auditor ≤500 lines | ADR-012 (progressive disclosure) | Must use reference files for detailed logic |
| /audit-alignment ≤10K chars | Lean orchestration protocol | Command must be concise |
| Read-only subagent tools | Framework safety pattern | Cannot modify files; propose-only |
| Context files are IMMUTABLE | Framework constitution | --fix can never edit context files |
| Canonical agent template v2.0.0 | agent-generator.md | Must follow 10-section structure |

### 9.2 Business Constraints

| Constraint | Impact |
|------------|--------|
| No external services | All analysis uses native Claude Code tools |
| Solo development | Sequential implementation |

### 9.3 Locked Decisions (from ENH-CLAP-001 Open Questions)

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Name is "CLAP" (Configuration Layer Alignment Protocol) | Descriptive, memorable, already branded in ENH-CLAP-001 |
| 2 | --fix always requires AskUserQuestion approval | Consistent with immutable-first philosophy; never auto-edit |
| 3 | System prompt location is `.claude/system-prompt-core.md` | Confirmed canonical location in DevForgeAI repo |
| 4 | Rule files (.claude/rules/**/*.md) included in validation scope | Adds ~14 files but catches stale conditional rules |
| 5 | Domain reference naming uses `project-*.md` pattern | Consistent with existing references/ naming convention |
| 6 | Regeneration is on-demand only (`/audit-alignment --generate-refs`) | Simpler, avoids hidden side-effects on ADR acceptance |

### 9.4 Assumptions

| Assumption | Status |
|------------|--------|
| CLAUDE.md exists in most projects | Validated — standard practice |
| system-prompt-core.md may not exist | Validated — optional; Phase 5.5 handles gracefully |
| Context files always exist (6/6) | Validated — required by /create-context workflow |
| ADRs follow standard format with Status field | Validated — all 21 existing ADRs follow format |

---

## 10. Epic Breakdown

### 10.1 Implementation Roadmap

```
Sprint 1 (Week 1-2):
================================================================
Day 0:     STORY-472: ADR-021 (Day 0 prerequisite)            - 2 pts
Day 1-3:   STORY-473: alignment-auditor + validation matrix    - 5 pts
Day 4-6:   STORY-474: /audit-alignment command (parallel)      - 3 pts
Day 4-6:   STORY-475: Phase 5.5 reference + SKILL.md (parallel)- 3 pts
Day 7-8:   STORY-476: Memory file documentation updates        - 3 pts
================================================================
Total: 16 points in 1 sprint (stretch to 2 if needed)
```

### 10.2 Dependency Graph

```
STORY-472 (ADR-021)         [Day 0 — prerequisite, authorizes source-tree.md]
        │
        ▼
STORY-473 (alignment-auditor + matrix)    [Days 1-3 — foundation]
        │
   +────┴────+
   ▼         ▼
STORY-474  STORY-475     [Days 4-6 — parallel, both consume alignment-auditor]
(command)  (Phase 5.5)
   │         │
   +────┬────+
        │
        ▼
STORY-476 (Documentation)    [Days 7-8 — documents deliverables from F1-F4]
```

**Critical Path:** STORY-472 → STORY-473 → STORY-474 + STORY-475 (parallel) → STORY-476

### 10.3 Cross-Epic Dependency

This epic has a **downstream dependency** from the Domain Reference Generation epic:

- Domain Reference Generation Phase 5.7 depends on Phase 5.5 existing (this epic)
- Domain Reference Generation `/audit-alignment --generate-refs` flag depends on /audit-alignment command (this epic)
- This epic does NOT depend on Domain Reference Generation (no upstream dependency)

**Implementation order:** This CLAP epic MUST complete before the Domain Reference Generation epic begins.

### 10.4 Epic Summary

| Epic | Features | Points | Status |
|------|----------|--------|--------|
| CLAP | 5 features (7 FRs) | 16 pts | Planning |

---

## 11. Next Steps

1. **Epic Creation:** `/create-epic Configuration Layer Alignment Protocol` — Creates EPIC file from this requirements specification
2. **Story Creation:** `/create-story` for each of the 6 stories (STORY-A through STORY-F)
3. **Sprint Planning:** `/create-sprint` — Assign stories to sprint
4. **Development:** `/dev STORY-XXX` — Implement via TDD workflow
5. **QA Validation:** `/qa STORY-XXX` — Validate each story

---

## Appendices

### A. Console Output Example

When `/audit-alignment` runs, the expected console output format:

```
=====================================================
  CONFIGURATION LAYER ALIGNMENT AUDIT (CLAP v1.0)
=====================================================

Layers Found:
  CLAUDE.md             : OK (4,812 chars)
  system-prompt-core.md : OK (3,200 chars)
  Context Files         : 6/6
  Rules                 : 14 files
  ADRs                  : 2 (both Accepted)

-----------------------------------------------------
CONTRADICTIONS (1 found)
-----------------------------------------------------

[HIGH] CC-01: CLAUDE.md vs anti-patterns.md

  CLAUDE.md line 45:
  > "installs CUDA hooks via std::call_once"

  anti-patterns.md lines 53-67:
  > "FORBIDDEN: std::call_once for CUDA hook init"
  > "Must allow retry - mutex+atomic pattern required"

  Resolution: Update CLAUDE.md line 45
  Fix: /audit-alignment --fix --layer=claudemd

-----------------------------------------------------
GAPS (3 found)
-----------------------------------------------------

[HIGH] CMP-01: Missing platform constraint
  Source: tech-stack.md lines 64-70
  Target: system-prompt-core.md <project_context>

[HIGH] CMP-03: Missing subagent routing for native C++ code
  Source: architecture-constraints.md lines 22-36
  Target: system-prompt-core.md <project_context>

[MEDIUM] CMP-04: Missing sprint awareness
  Source: architecture-constraints.md sprint annotations
  Target: system-prompt-core.md <project_context>

-----------------------------------------------------
ADR PROPAGATION (0 drift)
-----------------------------------------------------

  ADR-001 -> tech-stack.md         [PROPAGATED]
  ADR-002 -> anti-patterns.md #2,4 [PROPAGATED]

=====================================================
SUMMARY: 1 contradiction, 3 gaps, 0 ADR drift
STATUS: FINDINGS_DETECTED
=====================================================
```

### B. Glossary

| Term | Definition |
|------|------------|
| CLAP | Configuration Layer Alignment Protocol — 5-step methodology for cross-layer validation |
| Contradiction | Content in Layer A directly conflicts with Layer B (causes WRONG behavior) |
| Gap | Information present in source layer but missing from target layer (causes SUBOPTIMAL behavior) |
| ADR Propagation Drift | Accepted ADR decision not reflected in relevant context file(s) |
| Layer Mutability | Whether a configuration layer can be directly edited (MUTABLE, IMMUTABLE, APPEND-ONLY) |

### C. References

- **ENH-CLAP-001:** `tmp/ENH-CLAP-001-configuration-layer-alignment-protocol.md` (source proposal, 1,264 lines)
- **ADR-012:** Progressive Disclosure (agent size limit, reference file pattern)
- **audit-orphans.md:** `.claude/commands/audit-orphans.md` (lean orchestration audit pattern reference)
- **context-validator.md:** `.claude/agents/context-validator.md` (read-only validator agent pattern reference)
- **architecture-validation.md:** `.claude/skills/designing-systems/references/architecture-validation.md` (current Phase 5 implementation)
- **agent-generator.md:** `.claude/agents/agent-generator.md` (canonical agent template v2.0.0)

### D. Open Questions

None — all 6 questions from ENH-CLAP-001 resolved with locked decisions (see Section 9.3).

---

**Requirements Specification Version:** 1.0
**Created:** 2026-02-22
**Last Updated:** 2026-02-22
**Source:** ENH-CLAP-001
