# DevForgeAI Enhancement Proposal: ENH-CLAP-001
# Configuration Layer Alignment Protocol (CLAP) + Project Domain Reference Generation

> **Proposal ID:** ENH-CLAP-001
> **Date:** 2026-02-22
> **Origin:** GPUXtend system prompt alignment investigation
> **Author:** Claude Code (DevForgeAI orchestrator), prompted by Bryan
> **Affected Components:** `/create-context` command, `designing-systems` skill, new `alignment-auditor` subagent, new `/audit-alignment` command
> **Framework Baseline:** 41 subagents, 39 commands, 17 skills, 6 constitutional context files

---

## Executive Summary

During GPUXtend system prompt tuning, a manual 5-step reasoning process uncovered 5 actionable gaps (1 contradiction between CLAUDE.md and anti-patterns.md, 4 missing orchestrator awareness items in the system prompt). **None of the framework's existing validators perform cross-layer configuration analysis.** All current validators check in one direction only — source code or story content against context files — but never CLAUDE.md, the system prompt, or rules against context files, and never context files against each other.

This proposal codifies that reasoning methodology as a repeatable **Configuration Layer Alignment Protocol (CLAP)** and recommends 6 framework enhancements to make it automated, including a complementary **Project Domain Reference Generation** capability that extends existing subagents with project-specific expertise without creating new subagents.

---

## Part 1: The Reasoning Methodology (5 Steps)

This section documents the exact reasoning chain used to discover each finding, so the DevForgeAI team can evaluate whether the methodology itself is sound and reproducible.

### Step 1 — Layer Identification

**What was done:** Read and catalogued every configuration surface that Claude loads at session start.

| Layer | File(s) | Authority Level | Mutability |
|-------|---------|----------------|------------|
| System Prompt | `.claude/system-prompt-core.md` | Behavioral orchestration (identity, rules, phases) | MUTABLE (framework-owned, project-customizable) |
| CLAUDE.md | `/CLAUDE.md` | Project onboarding card (build commands, architecture overview) | MUTABLE (project-owned) |
| Context Files (6) | `devforgeai/specs/context/*.md` | Constitutional constraints (authoritative ground truth) | IMMUTABLE (changes require ADR) |
| Rules | `.claude/rules/**/*.md` | Cross-cutting enforcement (security, workflow, quality gates) | MUTABLE (framework-owned) |
| ADRs | `devforgeai/specs/adrs/*.md` | Architectural decision journal | APPEND-ONLY (supersede, don't edit) |

**Reasoning:** Claude's behavior is shaped by ALL of these layers simultaneously. If they contradict each other, Claude receives conflicting instructions. No existing validator reads all layers together — each validator reads exactly one pair of surfaces.

**What exists today:**
- `context-validator` → source code vs context files
- `tech-stack-detector` → project files (Cargo.toml, package.json) vs tech-stack.md
- `/validate-stories` → story files vs context files
- `context-preservation-validator` → story→epic→brainstorm provenance chain
- `/audit-orphans` → filesystem hygiene (byte-size drift)
- `prompt-version` → SHA-256 snapshots for rollback (safety mechanism, not validation)

**None reads CLAUDE.md, the system prompt, or rules against context files. None reads context files against each other.**

---

### Step 2 — Layer Purpose & Authority Analysis

**What was done:** Determined the intended role and precedence of each layer.

```
Context Files (6)  = HIGHEST AUTHORITY  (immutable, constitutional, "THE LAW")
         ↑ defers to
System Prompt      = ORCHESTRATOR       (should reference, never contradict)
         ↑ defers to
CLAUDE.md          = SUMMARY CARD       (must be consistent derivative)
         ↑ defers to
Rules              = ENFORCEMENT        (policies about HOW, not WHAT)
         ↑ defers to
ADRs               = DECISION HISTORY   (accepted decisions must propagate UP)
```

**Reasoning:** Understanding precedence is critical because contradictions must be resolved TOWARD the highest-authority source. If CLAUDE.md says X and anti-patterns.md says NOT-X, CLAUDE.md must change (not anti-patterns.md).

This precedence is stated in the system prompt (lines 141-143: *"This prompt defines identity and behavioral constraints. CLAUDE.md provides operational procedures. In conflict, this prompt takes precedence."*) but is **never enforced by tooling**.

---

### Step 3 — Cross-Reference Validation (Contradiction Detection)

**What was done:** Systematically compared claims across layers using pairwise comparison.

| Finding | Layer A | Layer B | Detection Method | Severity |
|---------|---------|---------|-----------------|----------|
| `std::call_once` contradiction | CLAUDE.md line 45: *"installs CUDA hooks via `std::call_once`"* | anti-patterns.md #3 (lines 51-67): *"FORBIDDEN — consumed on first attempt, blocks all retries"* | Searched CLAUDE.md for pattern names mentioned in anti-patterns.md forbidden list | HIGH |
| Missing platform guard | System prompt (absent) | tech-stack.md lines 64-70: *"Windows 11 x64"* | Checked if system prompt reflects platform constraints from tech-stack.md | HIGH |
| Missing build system routing | System prompt (absent) | tech-stack.md (3 separate build system sections: Cargo, CMake, pnpm) | Checked if system prompt knows about all build toolchains | HIGH |
| Missing subagent routing | System prompt (absent) | architecture-constraints.md layer dependency table | Checked if system prompt maps component types to correct subagents | HIGH |
| Missing sprint awareness | System prompt (absent) | architecture-constraints.md sprint annotations | Checked if system prompt knows what is built vs planned | MEDIUM |

**Reasoning:** Cross-referencing is pairwise — for N layers, there are N*(N-1)/2 comparison pairs. The framework has **zero tools** that compare CLAUDE.md vs context files, system prompt vs context files, or context files vs each other.

---

### Step 4 — Completeness Analysis (Delegation Fitness)

**What was done:** Asked "does the orchestrator know enough to delegate effectively?"

| Question | Answer | Source of Truth | Impact |
|----------|--------|----------------|--------|
| Does the orchestrator know the platform? | NO | tech-stack.md says Windows-only | Could suggest Linux/Unix solutions |
| Does it know all build systems? | NO | 3 toolchains (Cargo/CMake/pnpm) | Can't route stories to correct test commands |
| Does it know which subagent handles C++? | NO | `backend-architect` listed for Rust only | Native C++ stories may get wrong subagent |
| Does it know current sprint state? | NO | Sprint 1 complete, Sprint 2 in backlog | May suggest implementing already-built components |

**Reasoning:** This is different from contradiction detection (Step 3). Contradictions cause WRONG behavior. Gaps cause SUBOPTIMAL behavior — the orchestrator works, but delegates less precisely because it lacks project awareness.

---

### Step 5 — Minimal Intervention Design

**What was done:** Applied the principle of smallest change that closes all gaps.

| Change | Size | Scope |
|--------|------|-------|
| Fixed CLAUDE.md `std::call_once` → `mutex-guarded initialization` | 1 line | Eliminated contradiction |
| Added `<project_context>` section to system prompt | 28 lines | Added platform guard, build routing, subagent routing, sprint awareness |
| Core framework behaviors | 0 lines changed | 12-phase workflow, TDD, HALT triggers, delegation mandate — all untouched |

**Reasoning:** The layered architecture is correct. The system prompt SHOULD be mostly generic. The context files SHOULD carry project constraints. The fix is a thin bridge layer (`<project_context>`) that gives the orchestrator enough awareness to delegate well — without duplicating what context files already specify.

---

## Part 2: Framework Enhancement — CLAP

### The Validation Gap Map

| Check Type | Exists Today? | Existing Tool | Proposed Tool |
|------------|---------------|---------------|---------------|
| Source code vs context files | ✅ YES | `context-validator` subagent | — |
| Project files vs tech-stack.md | ✅ YES | `tech-stack-detector` subagent | — |
| Story content vs context files | ✅ YES | `/validate-stories` command | — |
| Story provenance chain | ✅ YES | `context-preservation-validator` | — |
| Filesystem drift | ✅ YES | `/audit-orphans` | — |
| **CLAUDE.md vs context files** | ❌ NO | Nothing | `alignment-auditor` subagent |
| **System prompt vs project state** | ❌ NO | Nothing | `alignment-auditor` subagent |
| **Context file vs context file** | ❌ NO | Nothing | `alignment-auditor` subagent |
| **ADRs reflected in context files** | ❌ NO | Nothing | `alignment-auditor` subagent |
| **Holistic cross-layer audit** | ❌ NO | Nothing | `/audit-alignment` command |

### Proposed: 3 Components

#### Component 1: `alignment-auditor` subagent (NEW)

| Property | Value |
|----------|-------|
| Type | New subagent |
| Model | haiku (text comparison, not code generation) |
| Tools | Read, Glob, Grep (read-only) |
| Size target | ~400-500 lines with references/ |
| Category | Validator (per canonical template categories) |

**Validation matrix:**

| Check ID | Layer A | Layer B | What to Compare | Severity |
|----------|---------|---------|-----------------|----------|
| CC-01 | CLAUDE.md | anti-patterns.md | Pattern names in CLAUDE.md that appear in anti-patterns forbidden list | HIGH |
| CC-02 | CLAUDE.md | tech-stack.md | Technologies, versions, build commands, platform | HIGH |
| CC-03 | CLAUDE.md | architecture-constraints.md | Architecture description accuracy | MEDIUM |
| CC-04 | CLAUDE.md | source-tree.md | File paths and component locations | MEDIUM |
| CC-05 | CLAUDE.md | coding-standards.md | Code examples consistency | LOW |
| CC-06 | CLAUDE.md | dependencies.md | Listed dependencies consistency | MEDIUM |
| CC-07 | System prompt | tech-stack.md | Platform constraint, technologies | HIGH |
| CC-08 | System prompt | architecture-constraints.md | Layer boundaries, build systems | HIGH |
| CC-09 | Rules | Context files | Rule references match context constraints | MEDIUM |
| CC-10 | Context files | Each other | Cross-references between 6 files agree | MEDIUM |
| ADR-01 | Accepted ADRs | Context files | Every accepted ADR reflected in context files | MEDIUM |
| CMP-01 | tech-stack.md | System prompt | Platform guard present | HIGH |
| CMP-02 | tech-stack.md + source-tree.md | CLAUDE.md | All build commands documented | MEDIUM |
| CMP-03 | architecture-constraints.md | System prompt | Subagent routing for all component types | HIGH |
| CMP-04 | Sprint annotations | System prompt | Sprint/phase awareness present | MEDIUM |

**Output:** Structured JSON with contradictions, gaps, ADR propagation status, and proposed resolutions (see Appendix A for schema).

**Why a new subagent (not enhancing `context-validator`):**
- `context-validator` checks **source code** against context files. Its scope is code compliance.
- `alignment-auditor` checks **configuration layers** against each other. Its scope is meta-configuration integrity.
- Mixing them violates single responsibility.
- Different model requirements: `context-validator` needs code understanding; `alignment-auditor` needs text comparison (haiku sufficient).

#### Component 2: `/audit-alignment` command (NEW)

| Property | Value |
|----------|-------|
| Type | New command |
| Family | Joins `/audit-deferrals`, `/audit-budget`, `/audit-hooks`, `/audit-w3`, `/audit-orphans` |
| Size target | ~250-350 lines (lean orchestration pattern) |
| Character budget | <10K chars (67% of 15K limit) |

```bash
/audit-alignment                     # full audit, all layers
/audit-alignment --layer=claudemd    # CLAUDE.md vs context files only
/audit-alignment --layer=prompt      # system prompt vs context files only
/audit-alignment --fix               # propose edits for MUTABLE layers
/audit-alignment --output=file       # write report to devforgeai/qa/
```

**`--fix` behavior (respects mutability):**
- CLAUDE.md findings → propose specific line edits, require AskUserQuestion approval
- System prompt findings → propose `<project_context>` additions, require approval
- Context file findings → flag for ADR creation (context files are IMMUTABLE — cannot auto-fix)
- ADR propagation drift → recommend context file update + ADR process

#### Component 3: Phase 5.5 in `designing-systems` skill (ENHANCEMENT)

| Property | Value |
|----------|-------|
| Type | Enhancement to existing skill |
| Location | Between Phase 5 (Validate Spec Against Context) and Phase 6 (Epic Creation) |
| Size addition | ~100-150 lines in SKILL.md + reference file |

**Workflow:**
1. Read CLAUDE.md and system-prompt-core.md (if they exist)
2. Invoke `alignment-auditor` subagent against freshly-created context files
3. If contradictions found → present via AskUserQuestion with resolution options
4. If system prompt gaps found → propose `<project_context>` section derived from context files
5. If neither file exists → recommend creating CLAUDE.md with build commands and architecture overview

**This closes the biggest gap:** `/create-context` will no longer produce 6 context files and then leave the system prompt completely untouched.

### Trigger Points

| Trigger | When | Automatic? | What Runs |
|---------|------|-----------|-----------|
| After `/create-context` | Phase 5.5 | YES | Full CLAP |
| After ADR acceptance | Post-creation hook | YES | ADR propagation check only |
| `/audit-alignment` invoked | On demand | MANUAL | Full CLAP or layer-specific |
| Sprint start | Recommended practice | MANUAL | Full CLAP to catch drift |

**Where CLAP does NOT run (to avoid bloat):**
- NOT during `/dev` (too frequent; `context-validator` handles code compliance per-commit)
- NOT during `/qa` (QA validates implementation quality, not meta-configuration)
- NOT during story creation (stories reference context files, already validated by `/validate-stories`)

---

## Part 3: Project-Specific Domain References (Dynamic Subagent Enhancement)

### The Question

When a project like GPUXtend has deep specialized domains (CUDA Driver API hooking, Microsoft Detours, Named Pipe protocols, DllMain constraints), should DevForgeAI create project-specific subagents like `cuda-hook-specialist` or `detours-expert`?

### Analysis

**Current architecture:** All 41 subagents are framework-generic. Project knowledge flows through context files read at runtime. From `backend-architect.md` Phase 1: *"Context files are THE LAW. If ANY file is missing, HALT."*

**The progressive disclosure extension point already exists:**
```
.claude/agents/
├── backend-architect.md                     # core agent (~728 lines)
├── backend-architect/
│   └── references/
│       ├── framework-patterns.md            # generic DevForgeAI patterns
│       ├── implementation-patterns.md       # generic coding patterns
│       └── treelint-patterns.md            # generic AST patterns
├── test-automator.md                        # core agent (~546 lines)
├── test-automator/
│   └── references/
│       ├── common-patterns.md
│       ├── coverage-optimization.md
│       ├── remediation-mode.md              # loaded only when mode matches
│       └── ...
```

Reference files in `{agent}/references/` are loaded on-demand via Read() calls embedded in agent workflow steps. This IS the mechanism for domain-specific knowledge.

### Recommendation: Domain Reference Files, NOT New Subagents

**Why NOT new subagents:**

| Concern | Detail |
|---------|--------|
| Dual maintenance | Domain knowledge would exist in BOTH the subagent prompt AND the context files. Updates require editing two places. |
| Breaks single source of truth | Context files are "THE LAW" — a `cuda-hook-specialist` subagent with baked-in CUDA knowledge creates an alternative authority. |
| No missing skill category | The 41 generic subagents cover every DevForgeAI skill category (implementation, testing, review, security, deployment, etc.). The gap is domain knowledge, not skill type. |
| Agent sprawl | Each project adding 3-4 custom subagents would balloon the agent registry unsustainably. |

**Why domain reference files instead:**

| Benefit | Detail |
|---------|--------|
| Follows existing pattern | Progressive disclosure (ADR-012) already uses `references/` for conditional loading |
| Single source of truth preserved | References are DERIVED from context files, not independent authorities |
| Extends without modifying | Existing subagents gain project expertise without changing their core prompts |
| Regenerable | When context files change, domain references can be regenerated from them |
| No registry changes | No new Task() agent types needed — same subagents, richer knowledge |

### What Would Be Generated for GPUXtend (Example)

| Reference File | Extends Agent | Content Source | Derived From |
|---------------|---------------|----------------|-------------|
| `backend-architect/references/project-domain.md` | backend-architect | CUDA Driver API patterns, Detours transaction lifecycle, Named Pipe IPC protocol, Patient Hook pattern, V5 address separation, fail-safe passthrough requirement | architecture-constraints.md, anti-patterns.md, coding-standards.md |
| `test-automator/references/project-testing.md` | test-automator | CMake/CTest patterns for native layer, `cargo test` for Rust, `pnpm test` for frontend, cross-boundary IPC test patterns | tech-stack.md, source-tree.md, coding-standards.md |
| `security-auditor/references/project-security.md` | security-auditor | DllMain constraints (no CRT calls in attach), env var injection guard (`GPUXTEND_INJECTED`), Named Pipe permission model, hook DLL export requirements | anti-patterns.md, architecture-constraints.md |
| `code-reviewer/references/project-review.md` | code-reviewer | 11 anti-patterns as structured review checklist, DriverStore vs System32 check, protocol header consistency (C++ ↔ Rust), CRT runtime matching (/MT vs /MD) | anti-patterns.md, coding-standards.md, dependencies.md |

### Integration: Phase 5.7 in `designing-systems` skill — Domain Reference Generation

After Phase 5.5 (Prompt Alignment), add Phase 5.7:

1. **Analyze** the 6 context files for specialized domain knowledge not covered by generic subagent expertise
2. **Identify** which existing subagents would benefit from project-specific references
3. **Generate** domain reference files derived from context file content
4. **Place** files in `{agent}/references/project-*.md` pattern
5. **Verify** generated references don't contradict their source context files

**Detection heuristics (when does a project need domain references?):**

| Signal | Threshold | Action |
|--------|-----------|--------|
| `anti-patterns.md` entries | >5 domain-specific entries | Generate security-auditor + code-reviewer project references |
| `tech-stack.md` build systems | >1 language/build system | Generate test-automator multi-toolchain reference |
| `architecture-constraints.md` | Hardware-specific or platform-specific constraints | Generate backend-architect domain reference |
| `coding-standards.md` | Language-specific patterns in 2+ languages | Generate code-reviewer cross-language reference |

### The General Pattern for Any New DevForgeAI Project

```
/create-context
  Phase 1-5:   Create & validate 6 context files          (EXISTING)
  Phase 5.5:   Align system prompt & CLAUDE.md             (NEW — CLAP)
  Phase 5.7:   Generate project domain references          (NEW — Domain References)
  Phase 6-7:   Epic creation & success report              (EXISTING)
```

**Every new DevForgeAI project automatically gets:**
1. ✅ 6 constitutional context files (existing)
2. 🆕 A tuned system prompt `<project_context>` section (CLAP)
3. 🆕 Project-specific domain references for relevant subagents (domain generation)

---

## Part 4: Summary for DevForgeAI Team

### Enhancement Roadmap

| # | Enhancement | Type | Estimated Size | Priority | Rationale |
|---|-------------|------|---------------|----------|-----------|
| 1 | `alignment-auditor` subagent | New subagent | ~400-500 lines | **HIGH** | Foundation for all CLAP checks |
| 2 | `/audit-alignment` command | New command | ~250-350 lines | **HIGH** | User-facing entry point for on-demand auditing |
| 3 | Phase 5.5 in `designing-systems` | Skill enhancement | ~100-150 lines + reference | **HIGH** | Closes the `/create-context` → system prompt gap |
| 4 | Phase 5.7 domain reference generation | Skill enhancement | ~150-200 lines + reference | **MEDIUM** | Extends subagent capabilities per-project |
| 5 | ADR documenting CLAP methodology | ADR | ~80-100 lines | **HIGH** | Decision record for the protocol |
| 6 | Documentation updates | Docs | ~150-200 lines | **MEDIUM** | commands-ref, subagents-ref, skills-ref |

**Total estimated scope:** ~1,500-2,000 lines across 6-8 files
**Estimated effort:** ~6-8 hours of DevForgeAI framework development

### Relationship to Existing Workflows

```
                    EXISTING                          PROPOSED
                    ────────                          ────────
/create-context  →  "What are the constraints?"
                    (6 context files)
                                                     CLAP (Phase 5.5)
                                                     → "Is the orchestrator aligned?"
                                                     (system prompt, CLAUDE.md)

                                                     Domain Refs (Phase 5.7)
                                                     → "Do subagents have domain knowledge?"
                                                     (agent reference files)

/audit-alignment →  (does not exist)                 On-demand re-check of all layers
                                                     (catches drift over time)
```

This is NOT a replacement for `/create-context`. It is a **natural extension** of the workflow — completing the configuration surface that `/create-context` currently leaves untouched.

### Open Questions for DevForgeAI Team

1. **Naming:** Is "Configuration Layer Alignment Protocol (CLAP)" the right name, or would "Configuration Surface Integrity" (CSI) or "Layer Coherence Audit" (LCA) be preferred?

2. **`--fix` approval mode:** Should `--fix` directly edit CLAUDE.md, or always require user approval via AskUserQuestion? (Recommendation: always require approval, consistent with the "immutable-first" philosophy.)

3. **System prompt location:** Where does DevForgeAI expect `system-prompt-core.md` to live? Is `.claude/` the canonical location? This affects Phase 5.5 read/write targeting.

4. **Rule file validation scope:** Should CLAP validate `.claude/rules/**/*.md` for consistency with context files? This adds ~14 files to the validation surface but catches stale conditional rules.

5. **Domain reference naming convention:** Should project-specific references follow `project-domain.md` or `{project-name}-domain.md` or `domain-{project-name}.md`?

6. **Regeneration trigger:** Should domain references auto-regenerate when context files are updated via ADR, or only on explicit `/audit-alignment --fix`?

---

## Appendix A: alignment-auditor Output Schema

```json
{
  "protocol_version": "1.0",
  "timestamp": "2026-02-22T10:30:00Z",
  "project": "GPUXtend",
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
  "domain_reference_recommendations": [
    {
      "agent": "backend-architect",
      "reference_file": "project-domain.md",
      "trigger": "architecture-constraints.md has hardware-specific constraints",
      "content_sources": ["architecture-constraints.md", "anti-patterns.md", "coding-standards.md"]
    }
  ],
  "summary": {
    "contradictions": 1,
    "gaps": 3,
    "adr_drift": 0,
    "domain_references_recommended": 4,
    "overall_status": "FINDINGS_DETECTED"
  }
}
```

---

## Appendix B: Example Console Output

```
=====================================================
  CONFIGURATION LAYER ALIGNMENT AUDIT (CLAP v1.0)
=====================================================

Layers Found:
  CLAUDE.md             : ✅ (4,812 chars)
  system-prompt-core.md : ✅ (3,200 chars)
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
  > "Must allow retry — mutex+atomic pattern required"

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

  ADR-001 → tech-stack.md         [✅ PROPAGATED]
  ADR-002 → anti-patterns.md #2,4 [✅ PROPAGATED]

-----------------------------------------------------
DOMAIN REFERENCES (4 recommended)
-----------------------------------------------------

  backend-architect/references/project-domain.md
  test-automator/references/project-testing.md
  security-auditor/references/project-security.md
  code-reviewer/references/project-review.md

  Generate: /audit-alignment --fix --generate-refs

=====================================================
SUMMARY: 1 contradiction, 3 gaps, 0 ADR drift
         4 domain references recommended
STATUS: FINDINGS_DETECTED
=====================================================
```

---

## Appendix C: Implementation Specifications (Structured)

### C.1 — alignment-auditor Subagent Specification

```json
{
  "subagent_spec": {
    "metadata": {
      "name": "alignment-auditor",
      "version": "1.0.0",
      "category": "Validator",
      "model": "haiku",
      "tools": ["Read", "Glob", "Grep"],
      "size_target_lines": { "core": 300, "max_with_refs": 500 },
      "proactive_triggers": [
        "after /create-context Phase 5 completes",
        "after ADR acceptance",
        "when /audit-alignment command invoked"
      ]
    },
    "inputs": {
      "required": [
        {
          "name": "context_files",
          "paths": [
            "devforgeai/specs/context/tech-stack.md",
            "devforgeai/specs/context/source-tree.md",
            "devforgeai/specs/context/dependencies.md",
            "devforgeai/specs/context/coding-standards.md",
            "devforgeai/specs/context/architecture-constraints.md",
            "devforgeai/specs/context/anti-patterns.md"
          ],
          "behavior_if_missing": "HALT — context files are constitutional"
        }
      ],
      "optional": [
        {
          "name": "claude_md",
          "path": "CLAUDE.md",
          "behavior_if_missing": "SKIP claude_md checks, report as GAP"
        },
        {
          "name": "system_prompt",
          "path": ".claude/system-prompt-core.md",
          "behavior_if_missing": "SKIP prompt checks, report as GAP"
        },
        {
          "name": "rules",
          "glob": ".claude/rules/**/*.md",
          "behavior_if_missing": "SKIP rule checks"
        },
        {
          "name": "adrs",
          "glob": "devforgeai/specs/adrs/ADR-*.md",
          "behavior_if_missing": "SKIP ADR propagation checks"
        }
      ]
    },
    "outputs": {
      "format": "JSON",
      "schema_ref": "See Appendix A",
      "status_values": ["PASS", "FINDINGS_DETECTED", "CRITICAL_FINDINGS"],
      "severity_levels": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    },
    "constraints": {
      "DO": [
        "Read all configuration layers before any comparison",
        "Use exact text matching for pattern names and technology names",
        "Report line numbers for all findings",
        "Propose resolutions that respect layer mutability rules",
        "Distinguish contradictions (wrong) from gaps (missing)"
      ],
      "DO_NOT": [
        "Modify any file (read-only analysis only)",
        "Use Bash for file operations",
        "Skip any check in the validation matrix",
        "Auto-resolve findings (always propose, never apply)",
        "Report false positives from prose similarity (match specific claims only)"
      ]
    }
  }
}
```

### C.2 — /audit-alignment Command Specification

```json
{
  "command_spec": {
    "metadata": {
      "name": "audit-alignment",
      "family": "audit",
      "character_budget_max": 10000,
      "pattern_reference": ".claude/commands/audit-orphans.md"
    },
    "arguments": {
      "--layer": {
        "type": "enum",
        "values": ["all", "claudemd", "prompt", "context", "rules", "adrs"],
        "default": "all",
        "description": "Restrict audit to specific configuration layer"
      },
      "--fix": {
        "type": "boolean",
        "default": false,
        "description": "Propose edits for MUTABLE layers (requires AskUserQuestion approval)"
      },
      "--output": {
        "type": "enum",
        "values": ["console", "file"],
        "default": "console",
        "description": "Output target. 'file' writes to devforgeai/qa/alignment-audit-{date}.md"
      },
      "--generate-refs": {
        "type": "boolean",
        "default": false,
        "description": "Generate project domain reference files for subagents. Requires --fix."
      }
    },
    "workflow": [
      { "step": 1, "action": "Parse arguments", "tools": [] },
      { "step": 2, "action": "Set context markers", "tools": [] },
      { "step": 3, "action": "Invoke alignment-auditor subagent via Task()", "tools": ["Task"] },
      { "step": 4, "action": "Format results for display", "tools": [] },
      { "step": 5, "action": "If --fix, iterate findings and propose edits via AskUserQuestion", "tools": ["AskUserQuestion", "Edit"] },
      { "step": 6, "action": "If --generate-refs, invoke domain reference generation", "tools": ["Task", "Write"] },
      { "step": 7, "action": "If --output=file, write report", "tools": ["Write"] }
    ],
    "mutability_rules": {
      "CLAUDE.md": "MUTABLE — --fix can propose edits with user approval",
      "system-prompt-core.md": "MUTABLE — --fix can propose edits with user approval",
      "context_files": "IMMUTABLE — --fix flags for ADR creation, cannot edit",
      "rules": "MUTABLE — --fix can propose edits with user approval",
      "adrs": "APPEND-ONLY — --fix can recommend new ADR, cannot edit existing"
    }
  }
}
```

### C.3 — CLAP Validation Matrix (Machine-Readable)

```json
{
  "validation_matrix": {
    "version": "1.0",
    "check_categories": {
      "CC": "Contradiction Check — content in Layer A conflicts with Layer B",
      "CMP": "Completeness Check — information in source layer missing from target layer",
      "ADR": "ADR Propagation Check — accepted decision not reflected in context files"
    },
    "checks": [
      {
        "id": "CC-01",
        "category": "CC",
        "severity": "HIGH",
        "layer_a": "CLAUDE.md",
        "layer_b": "devforgeai/specs/context/anti-patterns.md",
        "description": "Does CLAUDE.md describe any pattern listed as forbidden in anti-patterns.md?",
        "method": "Extract all ## headings from anti-patterns.md. For each forbidden pattern name, search CLAUDE.md for that pattern name. If found in non-warning context, flag as contradiction.",
        "example_finding": "CLAUDE.md says 'via std::call_once' but anti-patterns.md #3 forbids std::call_once"
      },
      {
        "id": "CC-02",
        "category": "CC",
        "severity": "HIGH",
        "layer_a": "CLAUDE.md",
        "layer_b": "devforgeai/specs/context/tech-stack.md",
        "description": "Are all technologies, versions, and build commands consistent between CLAUDE.md and tech-stack.md?",
        "method": "Extract technology names and versions from tech-stack.md tables. Search CLAUDE.md for each technology name. If version differs or prohibited technology is mentioned positively, flag.",
        "example_finding": "CLAUDE.md lists 'npm install' but tech-stack.md prohibits npm"
      },
      {
        "id": "CC-03",
        "category": "CC",
        "severity": "MEDIUM",
        "layer_a": "CLAUDE.md",
        "layer_b": "devforgeai/specs/context/architecture-constraints.md",
        "description": "Does CLAUDE.md accurately describe the architecture (layer boundaries, IPC protocol, component relationships)?",
        "method": "Compare architecture descriptions in CLAUDE.md against architecture-constraints.md sections. Check protocol constants (header size, pipe name, max message size).",
        "example_finding": "CLAUDE.md says '16-byte header' but architecture-constraints.md says '24-byte header'"
      },
      {
        "id": "CC-04",
        "category": "CC",
        "severity": "MEDIUM",
        "layer_a": "CLAUDE.md",
        "layer_b": "devforgeai/specs/context/source-tree.md",
        "description": "Are file paths and component locations in CLAUDE.md consistent with source-tree.md?",
        "method": "Extract file paths mentioned in CLAUDE.md. Verify each exists in source-tree.md directory listing.",
        "example_finding": "CLAUDE.md references 'src/hook/' but source-tree.md says 'native/hook/'"
      },
      {
        "id": "CC-05",
        "category": "CC",
        "severity": "LOW",
        "layer_a": "CLAUDE.md",
        "layer_b": "devforgeai/specs/context/coding-standards.md",
        "description": "Are code examples in CLAUDE.md consistent with coding-standards.md patterns?",
        "method": "If CLAUDE.md contains code examples, verify they follow patterns defined in coding-standards.md.",
        "example_finding": "CLAUDE.md shows println!() but coding-standards.md requires tracing::info!()"
      },
      {
        "id": "CC-06",
        "category": "CC",
        "severity": "MEDIUM",
        "layer_a": "CLAUDE.md",
        "layer_b": "devforgeai/specs/context/dependencies.md",
        "description": "Are dependency names and versions in CLAUDE.md consistent with dependencies.md?",
        "method": "Extract dependency names from CLAUDE.md. Cross-reference with dependencies.md approved list and version pins.",
        "example_finding": "CLAUDE.md mentions 'Detours 3.0' but dependencies.md pins 'Detours 4.0.1'"
      },
      {
        "id": "CC-07",
        "category": "CC",
        "severity": "HIGH",
        "layer_a": "system-prompt-core.md",
        "layer_b": "devforgeai/specs/context/tech-stack.md",
        "description": "Does the system prompt reference correct technologies and platform constraints?",
        "method": "Extract platform section from tech-stack.md. Check system prompt for platform awareness. Extract prohibited technologies and verify system prompt doesn't recommend them.",
        "example_finding": "tech-stack.md says Windows-only but system prompt has no platform guard"
      },
      {
        "id": "CC-08",
        "category": "CC",
        "severity": "HIGH",
        "layer_a": "system-prompt-core.md",
        "layer_b": "devforgeai/specs/context/architecture-constraints.md",
        "description": "Does the system prompt understand layer boundaries and build systems?",
        "method": "Extract build system sections from architecture-constraints.md. Check system prompt for build routing awareness. Verify subagent routing covers all component types.",
        "example_finding": "architecture-constraints.md defines 3 build systems but system prompt only routes for Cargo"
      },
      {
        "id": "CC-09",
        "category": "CC",
        "severity": "MEDIUM",
        "layer_a": ".claude/rules/**/*.md",
        "layer_b": "devforgeai/specs/context/*.md",
        "description": "Do rule files reference constraints that context files actually define?",
        "method": "Extract technology/pattern references from rule files. Verify each reference exists in the corresponding context file.",
        "example_finding": "Rule references 'TypeScript strict mode' but tech-stack.md doesn't list TypeScript"
      },
      {
        "id": "CC-10",
        "category": "CC",
        "severity": "MEDIUM",
        "layer_a": "devforgeai/specs/context/*.md",
        "layer_b": "devforgeai/specs/context/*.md",
        "description": "Do cross-references between the 6 context files agree?",
        "method": "Check: dependencies.md packages vs tech-stack.md technologies, source-tree.md paths vs coding-standards.md naming conventions, architecture-constraints.md layers vs source-tree.md directory structure.",
        "example_finding": "dependencies.md lists 'express' but tech-stack.md prohibits Node.js"
      },
      {
        "id": "ADR-01",
        "category": "ADR",
        "severity": "MEDIUM",
        "layer_a": "devforgeai/specs/adrs/ADR-*.md",
        "layer_b": "devforgeai/specs/context/*.md",
        "description": "Is every accepted ADR decision reflected in the relevant context file(s)?",
        "method": "Read each ADR with status 'Accepted'. Extract the 'Decision' section. Search context files for evidence that the decision was incorporated. If missing, flag as propagation drift.",
        "example_finding": "ADR-003 accepted 'Use Redis for caching' but tech-stack.md has no Redis entry"
      },
      {
        "id": "CMP-01",
        "category": "CMP",
        "severity": "HIGH",
        "source_layer": "devforgeai/specs/context/tech-stack.md",
        "target_layer": "system-prompt-core.md",
        "description": "Is the platform constraint from tech-stack.md present in the system prompt?",
        "method": "Read tech-stack.md 'Platform' or OS section. Check system prompt for platform guard statement.",
        "example_finding": "tech-stack.md declares Windows 11 x64 but system prompt has no platform constraint"
      },
      {
        "id": "CMP-02",
        "category": "CMP",
        "severity": "MEDIUM",
        "source_layer": "devforgeai/specs/context/tech-stack.md + source-tree.md",
        "target_layer": "CLAUDE.md",
        "description": "Are all build systems and their commands documented in CLAUDE.md?",
        "method": "Extract all build system sections from tech-stack.md. For each, verify CLAUDE.md has a corresponding build command section.",
        "example_finding": "tech-stack.md lists CMake build system but CLAUDE.md has no CMake build commands"
      },
      {
        "id": "CMP-03",
        "category": "CMP",
        "severity": "HIGH",
        "source_layer": "devforgeai/specs/context/architecture-constraints.md",
        "target_layer": "system-prompt-core.md",
        "description": "Does the system prompt have subagent routing for all component types defined in architecture-constraints.md?",
        "method": "Extract component/layer types from architecture-constraints.md dependency table. Check system prompt for explicit routing of each to appropriate subagent.",
        "example_finding": "architecture-constraints.md defines C++ native layer but system prompt doesn't route it to any subagent"
      },
      {
        "id": "CMP-04",
        "category": "CMP",
        "severity": "MEDIUM",
        "source_layer": "devforgeai/specs/context/architecture-constraints.md",
        "target_layer": "system-prompt-core.md",
        "description": "Does the system prompt have sprint/phase awareness matching the current project state?",
        "method": "Search architecture-constraints.md for sprint annotations or phase markers. If present, check system prompt for corresponding state awareness.",
        "example_finding": "architecture-constraints.md annotates Sprint 2 modules but system prompt has no sprint awareness"
      }
    ]
  }
}
```

### C.4 — Phase 5.5 Workflow Definition (designing-systems enhancement)

```xml
<workflow_phase id="5.5" name="Prompt Alignment" parent_skill="designing-systems">
  <description>
    After context files are created and validated (Phase 5), check whether
    CLAUDE.md and system-prompt-core.md are aligned with the new context files.
    Generate or propose updates to close any gaps.
  </description>

  <preconditions>
    <condition>Phase 5 (Validate Spec Against Context) completed successfully</condition>
    <condition>All 6 context files exist and are non-empty</condition>
  </preconditions>

  <steps>
    <step order="1" name="Detect Configuration Layers">
      <action>Read CLAUDE.md and .claude/system-prompt-core.md</action>
      <tool>Read</tool>
      <on_missing>
        <if target="CLAUDE.md">
          <action>Flag as GAP — recommend creating CLAUDE.md with build commands and architecture overview</action>
          <proposal_template>
            Extract from context files:
            - Project name and description (architecture-constraints.md header)
            - Build commands per language (tech-stack.md build system sections)
            - Architecture diagram (architecture-constraints.md layer table)
            - Key protocol constants (architecture-constraints.md IPC section)
            - Crate/module responsibilities (source-tree.md top-level directories)
          </proposal_template>
        </if>
        <if target="system-prompt-core.md">
          <action>Flag as GAP — recommend creating project_context section</action>
          <note>System prompt may not exist for all projects. This is informational, not blocking.</note>
        </if>
      </on_missing>
    </step>

    <step order="2" name="Invoke alignment-auditor">
      <action>
        Task(subagent_type="alignment-auditor", prompt="Run CLAP validation
        against freshly-created context files. Target layers: CLAUDE.md and
        system-prompt-core.md. Return structured JSON report.")
      </action>
      <tool>Task</tool>
      <input>All 6 context files + CLAUDE.md + system-prompt-core.md</input>
      <output>JSON report per Appendix A schema</output>
    </step>

    <step order="3" name="Process Contradictions">
      <condition>report.contradictions.length > 0</condition>
      <action>
        For each contradiction:
        1. Display Layer A text and Layer B text with line numbers
        2. Explain which layer has higher authority (context files always win)
        3. Propose specific edit to the lower-authority layer
        4. AskUserQuestion: "Apply this fix?" [Yes / Skip / Edit manually]
      </action>
      <tool>AskUserQuestion, Edit</tool>
      <authority_resolution>
        Context files WIN over CLAUDE.md (context files are immutable constitutional)
        Context files WIN over system prompt
        System prompt precedence stated in prompt itself (lines 141-143)
        If context file is wrong, recommend ADR creation instead of editing
      </authority_resolution>
    </step>

    <step order="4" name="Process Gaps">
      <condition>report.gaps.length > 0</condition>
      <action>
        For system prompt gaps:
        1. Synthesize a project_context section from context files
        2. Include: platform constraint, build system routing, subagent routing, sprint state
        3. Present proposed section to user
        4. AskUserQuestion: "Add this to system-prompt-core.md?" [Yes / Edit / Skip]

        For CLAUDE.md gaps:
        1. Identify missing sections (build commands, architecture, etc.)
        2. Draft content from context files
        3. Present proposed additions
        4. AskUserQuestion: "Add this to CLAUDE.md?" [Yes / Edit / Skip]
      </action>
      <tool>AskUserQuestion, Edit</tool>
      <project_context_template>
        <![CDATA[
<project_context>
## {project_name} — {one_line_description}

{platform_and_build_systems_from_tech_stack_md}

### Build System Routing
{for_each_build_system_in_tech_stack_md}

### Platform Constraint
{platform_section_from_tech_stack_md}

### Subagent Routing
{component_to_subagent_mapping_from_architecture_constraints_md}

### Current State
{sprint_annotations_from_architecture_constraints_md}
</project_context>
        ]]>
      </project_context_template>
    </step>

    <step order="5" name="Process ADR Propagation Drift">
      <condition>report.adr_propagation has items with propagation_status != "FULLY_PROPAGATED"</condition>
      <action>
        For each un-propagated ADR:
        1. Display ADR title and decision
        2. Show which context file should be updated
        3. Since context files are IMMUTABLE, recommend creating a new ADR
           to formally update the context file, or flag as known technical debt
        4. AskUserQuestion: "Create follow-up ADR to update context file?" [Yes / Skip / Defer to backlog]
      </action>
      <tool>AskUserQuestion</tool>
    </step>

    <step order="6" name="Report">
      <action>
        Display summary:
        - Contradictions found and resolved
        - Gaps found and addressed
        - ADR drift flagged
        - Files modified (if any)
        Proceed to Phase 5.7 (Domain Reference Generation) or Phase 6 (Epic Creation)
      </action>
    </step>
  </steps>

  <postconditions>
    <condition>Zero HIGH-severity contradictions remain unresolved (blocking)</condition>
    <condition>MEDIUM/LOW contradictions may be deferred with justification (non-blocking)</condition>
    <condition>System prompt gaps are informational — project may choose not to use system prompt</condition>
  </postconditions>
</workflow_phase>
```

### C.5 — Phase 5.7 Domain Reference Generation Workflow

```xml
<workflow_phase id="5.7" name="Domain Reference Generation" parent_skill="designing-systems">
  <description>
    After context files are validated and prompt is aligned (Phases 5-5.5),
    analyze context files for specialized domain knowledge that should be
    extracted into project-specific reference files for existing subagents.
    This extends subagent capabilities without creating new subagents.
  </description>

  <preconditions>
    <condition>Phase 5.5 (Prompt Alignment) completed</condition>
    <condition>All 6 context files exist and are non-empty</condition>
  </preconditions>

  <detection_heuristics>
    <heuristic id="DH-01" agent="backend-architect">
      <trigger>architecture-constraints.md contains hardware-specific or platform-specific constraints</trigger>
      <detection_method>
        Search architecture-constraints.md for: GPU, CUDA, FPGA, embedded, driver,
        kernel, DMA, interrupt, register, hardware, sensor, actuator, firmware
      </detection_method>
      <output_file>backend-architect/references/project-domain.md</output_file>
      <content_sources>
        architecture-constraints.md (layer boundaries, protocol details, concurrency model),
        anti-patterns.md (all forbidden patterns with rationale),
        coding-standards.md (language-specific patterns for all project languages)
      </content_sources>
    </heuristic>

    <heuristic id="DH-02" agent="test-automator">
      <trigger>tech-stack.md defines more than 1 language or build system</trigger>
      <detection_method>
        Count distinct "Language" or "Build System" entries in tech-stack.md tables.
        If count > 1, this project needs multi-toolchain test routing.
      </detection_method>
      <output_file>test-automator/references/project-testing.md</output_file>
      <content_sources>
        tech-stack.md (test frameworks per language, build commands),
        source-tree.md (test file location patterns per language),
        coding-standards.md (test naming conventions per language)
      </content_sources>
    </heuristic>

    <heuristic id="DH-03" agent="security-auditor">
      <trigger>anti-patterns.md has more than 5 domain-specific entries</trigger>
      <detection_method>
        Count ## headings in anti-patterns.md. If count > 5, project has
        significant domain-specific security concerns beyond generic OWASP.
      </detection_method>
      <output_file>security-auditor/references/project-security.md</output_file>
      <content_sources>
        anti-patterns.md (all entries with security implications),
        architecture-constraints.md (boundary security, permission models),
        coding-standards.md (security-relevant patterns)
      </content_sources>
    </heuristic>

    <heuristic id="DH-04" agent="code-reviewer">
      <trigger>coding-standards.md has language-specific patterns in 2+ languages</trigger>
      <detection_method>
        Count distinct language sections in coding-standards.md. If > 1,
        code reviews need cross-language awareness.
      </detection_method>
      <output_file>code-reviewer/references/project-review.md</output_file>
      <content_sources>
        anti-patterns.md (all entries as review checklist items),
        coding-standards.md (per-language patterns for review),
        dependencies.md (prohibited packages to flag in reviews),
        architecture-constraints.md (layer dependency rules for import review)
      </content_sources>
    </heuristic>
  </detection_heuristics>

  <reference_file_template>
    <![CDATA[
# Project Domain Reference: {agent_name}

> **Auto-generated** from context files by CLAP Phase 5.7
> **Source files:** {list_of_source_context_files}
> **Regenerate:** `/audit-alignment --generate-refs`
> **DO NOT EDIT MANUALLY** — changes will be overwritten on regeneration.
> To update this reference, update the source context files via ADR process.

## When to Load This Reference

Load this reference file when working on {project_name} stories that involve:
{trigger_conditions}

## Domain-Specific Constraints

{extracted_from_architecture_constraints_md}

## Forbidden Patterns (Project-Specific)

{extracted_from_anti_patterns_md_as_checklist}

## Language-Specific Patterns

{extracted_from_coding_standards_md_for_relevant_languages}

## Build and Test Commands

{extracted_from_tech_stack_md_build_sections}
    ]]>
  </reference_file_template>

  <steps>
    <step order="1" name="Run Detection Heuristics">
      <action>Evaluate each heuristic (DH-01 through DH-04) against context files</action>
      <output>List of triggered heuristics with agent names and content sources</output>
    </step>

    <step order="2" name="Present Recommendations">
      <action>
        AskUserQuestion: "CLAP detected {N} subagents that would benefit from
        project domain references. Generate these reference files?"
        Options: [Generate all / Select individually / Skip]
      </action>
      <tool>AskUserQuestion</tool>
    </step>

    <step order="3" name="Generate Reference Files">
      <condition>User approved generation</condition>
      <action>
        For each approved reference:
        1. Read source context files listed in the heuristic
        2. Extract relevant sections (constraints, patterns, forbidden items)
        3. Populate reference_file_template
        4. Write to .claude/agents/{agent}/references/project-{type}.md
      </action>
      <tool>Read, Write</tool>
    </step>

    <step order="4" name="Verify No Contradictions">
      <action>
        For each generated reference, verify content matches source context files.
        Generated references are DERIVED — they must not add, modify, or omit
        constraints from the source.
      </action>
    </step>

    <step order="5" name="Report">
      <action>
        Display: files generated, source context files used, and instructions
        for regeneration (/audit-alignment --generate-refs)
      </action>
    </step>
  </steps>

  <postconditions>
    <condition>Generated references contain only content derived from context files</condition>
    <condition>Each reference file includes auto-generation header with regeneration command</condition>
    <condition>No modifications to subagent core .md files (references only)</condition>
  </postconditions>
</workflow_phase>
```

### C.6 — File Inventory (All Files to Create or Modify)

```json
{
  "file_inventory": {
    "new_files": [
      {
        "path": ".claude/agents/alignment-auditor.md",
        "type": "subagent_definition",
        "estimated_lines": 300,
        "template": "canonical-agent-template v2.0.0",
        "model": "haiku",
        "tools": ["Read", "Glob", "Grep"],
        "depends_on": []
      },
      {
        "path": ".claude/agents/alignment-auditor/references/validation-matrix.md",
        "type": "subagent_reference",
        "estimated_lines": 200,
        "content": "Full validation matrix from Appendix C.3 in prose form with examples",
        "depends_on": [".claude/agents/alignment-auditor.md"]
      },
      {
        "path": ".claude/commands/audit-alignment.md",
        "type": "command_definition",
        "estimated_lines": 300,
        "pattern_reference": ".claude/commands/audit-orphans.md",
        "character_budget": 10000,
        "depends_on": [".claude/agents/alignment-auditor.md"]
      },
      {
        "path": ".claude/skills/designing-systems/references/prompt-alignment-workflow.md",
        "type": "skill_reference",
        "estimated_lines": 200,
        "content": "Phase 5.5 detailed workflow from Appendix C.4",
        "depends_on": []
      },
      {
        "path": ".claude/skills/designing-systems/references/domain-reference-generation.md",
        "type": "skill_reference",
        "estimated_lines": 250,
        "content": "Phase 5.7 detailed workflow from Appendix C.5",
        "depends_on": []
      },
      {
        "path": "devforgeai/specs/adrs/ADR-XXX-configuration-layer-alignment-protocol.md",
        "type": "adr",
        "estimated_lines": 100,
        "content": "Decision to add CLAP, rationale, 5-step methodology, enforcement",
        "depends_on": []
      }
    ],
    "modified_files": [
      {
        "path": ".claude/skills/designing-systems/SKILL.md",
        "type": "skill_definition",
        "modification": "Add Phase 5.5 (Prompt Alignment) and Phase 5.7 (Domain Reference Generation) sections with on-demand reference loading",
        "estimated_lines_added": 80,
        "depends_on": [
          ".claude/skills/designing-systems/references/prompt-alignment-workflow.md",
          ".claude/skills/designing-systems/references/domain-reference-generation.md"
        ]
      },
      {
        "path": ".claude/memory/commands-reference.md",
        "type": "documentation",
        "modification": "Add /audit-alignment entry to Framework Maintenance section",
        "estimated_lines_added": 15
      },
      {
        "path": ".claude/memory/subagents-reference.md",
        "type": "documentation",
        "modification": "Add alignment-auditor entry with model, tools, and invocation pattern",
        "estimated_lines_added": 20
      },
      {
        "path": ".claude/memory/skills-reference.md",
        "type": "documentation",
        "modification": "Update designing-systems entry to include Phase 5.5 and 5.7",
        "estimated_lines_added": 10
      }
    ],
    "total_new_files": 6,
    "total_modified_files": 4,
    "total_estimated_lines": "1,475-1,775"
  }
}
```

### C.7 — Implementation Dependency Graph

```json
{
  "dependency_graph": {
    "phases": [
      {
        "phase": 1,
        "name": "Foundation",
        "deliverables": [
          ".claude/agents/alignment-auditor.md",
          ".claude/agents/alignment-auditor/references/validation-matrix.md"
        ],
        "blocked_by": [],
        "estimated_effort": "2-3 hours"
      },
      {
        "phase": 2,
        "name": "Command Interface",
        "deliverables": [
          ".claude/commands/audit-alignment.md"
        ],
        "blocked_by": ["phase_1"],
        "estimated_effort": "1-2 hours"
      },
      {
        "phase": 3,
        "name": "Workflow Integration",
        "deliverables": [
          ".claude/skills/designing-systems/references/prompt-alignment-workflow.md",
          ".claude/skills/designing-systems/references/domain-reference-generation.md",
          ".claude/skills/designing-systems/SKILL.md (modified)"
        ],
        "blocked_by": ["phase_1"],
        "estimated_effort": "2-3 hours",
        "note": "Can run in parallel with Phase 2"
      },
      {
        "phase": 4,
        "name": "Documentation & ADR",
        "deliverables": [
          "devforgeai/specs/adrs/ADR-XXX-configuration-layer-alignment-protocol.md",
          ".claude/memory/commands-reference.md (modified)",
          ".claude/memory/subagents-reference.md (modified)",
          ".claude/memory/skills-reference.md (modified)"
        ],
        "blocked_by": ["phase_2", "phase_3"],
        "estimated_effort": "1 hour"
      }
    ]
  }
}
```
