---
name: designing-systems
description: Create technical specifications, ADRs, and project context documentation that prevents technical debt. Use when designing system architecture, making technology decisions, or establishing project structure. Enforces spec-driven development by creating immutable constraint files (tech-stack.md, source-tree.md, dependencies.md) that AI agents must follow.
model: claude-opus-4-6
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebFetch
  - Bash(git:*)
---

# DevForgeAI Architecture Skill

Create immutable context files and architecture documentation that prevents technical debt through explicit constraints.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "Purpose" section below and begin execution.**

---

## Purpose

This skill creates the **architectural foundation** for projects: 6 required + 1 optional context files that define boundaries AI agents must never violate.

**Generated artifacts:**
- **6 Required Context Files** (immutable constraints in `devforgeai/specs/context/`)
- **1 Optional Context File** (design-system.md for UI projects)
- **ADRs** (architecture decisions in `devforgeai/specs/adrs/`)
- **Technical Specifications** (optional, in `devforgeai/specs/`)

**Core Principle:** Prevent technical debt through explicit, enforceable constraints.

**Philosophy:**
- Locked technologies (no library substitution without ADR)
- Explicit structure (files belong in defined locations)
- Approved dependencies (no unapproved packages)
- Enforced patterns (anti-patterns forbidden)
- Documented decisions (ADRs for traceability)

---

## When to Use This Skill

**Use when:**
- Starting new projects (create initial context)
- Making technology decisions (update tech-stack + create ADR)
- Defining project structure (create/update source-tree)
- Establishing coding standards
- Context files missing (auto-invoked by development skill)
- Brownfield projects need architectural documentation

**Prerequisites:**
- None (this is typically the first skill invoked)

**Invoked by:**
- `/create-context` command
- discovering-requirements skill (after requirements discovery)
- implementing-stories skill (if context files missing)

---

## Architecture Workflow (6 Phases)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

Each phase loads its reference file on-demand for detailed implementation.

### Phase 1: Project Context Discovery

**Purpose:** Gather project information through strategic questions

**Reference:** `context-discovery-workflow.md`

Determine project type (greenfield vs brownfield), discover existing technologies/structure if brownfield, check for existing context files, analyze gaps.

**Step 0: Conditional User Input Guidance Loading [MANDATORY]**

Detect project mode and load guidance patterns conditionally:

```python
# Detect mode via context file count
context_files = Glob(pattern="devforgeai/specs/context/*.md")
context_count = len(context_files)

if context_count == 6:
    # Brownfield mode - all context files exist
    mode = "brownfield"
    Display: "Brownfield mode detected (6 context files exist). Skipping user-input-guidance.md."
    # Skip guidance, proceed with existing constraints

elif context_count == 0:
    # Greenfield mode - no context files exist
    mode = "greenfield"
    Display: "Greenfield mode detected (no context files). Loading user-input-guidance.md..."
    guidance = Read(file_path=".claude/skills/designing-systems/references/user-input-guidance.md")
    Display: "✓ Guidance loaded - applying patterns to Phase 1 questions"

else:
    # Partial greenfield - some files exist but not all
    mode = f"partial_greenfield ({context_count}/6 files)"
    Display: f"Partial context detected ({context_count}/6 files exist). Loading user-input-guidance.md to fill gaps..."
    guidance = Read(file_path=".claude/skills/designing-systems/references/user-input-guidance.md")
```

**Pattern Application (if guidance loaded):**
- **Step 1:** Use **Open-Ended Discovery** pattern for technology inventory question
- **Step 2:** Use **Explicit Classification** pattern for architecture style (4 options: Monolithic/Microservices/Serverless/Hybrid)
- **Step 3:** Use **Bounded Choice** pattern for framework selection (filtered by language)
- **Step 4:** Use **Bounded Choice** pattern for database system selection

**See:** `references/architecture-user-input-integration.md` for complete pattern mappings and examples.

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/context-discovery-workflow.md")
```

---

### Phase 2: Create Immutable Context Files

**Purpose:** Generate 6 required + 1 optional context files from templates

**Reference:** `context-file-creation-workflow.md`

Load template for each file from `assets/context-templates/`, gather decisions via AskUserQuestion, customize with project-specific info, add enforcement rules (✅/❌ examples), write to `devforgeai/specs/context/`.

**Output:**
- **Required (6):** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md
- **Optional (1):** design-system.md (UI projects only)

**This phase was 52% of the original SKILL.md - now progressively loaded.**

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/context-file-creation-workflow.md")
```

---

### Phase 3: Create Architecture Decision Records

**Purpose:** Document significant technical decisions

**Reference:** `adr-creation-workflow.md` | **Policy:** `adr-policy.md` | **Template:** `adr-template.md`

Identify decisions requiring ADRs (database, ORM, framework, patterns), load template and examples from `assets/adr-examples/`, create ADR with context/decision/rationale/consequences/alternatives/enforcement sections.

**Output:** ADR files in `devforgeai/specs/adrs/`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/adr-creation-workflow.md")
```

---

### Phase 4: Create Technical Specifications

**Purpose:** Generate high-level architecture documentation

**Reference:** `technical-specification-workflow.md` | **Patterns:** `system-design-patterns.md`

Create functional specs (use cases, business rules, data models), API specs (endpoints, auth), database specs (schemas, indexes), NFRs (performance, security). Use AskUserQuestion for ambiguous requirements.

**Output:** Technical spec in `devforgeai/specs/` (optional)

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/technical-specification-workflow.md")
```

---

### Phase 5: Validate Spec Against Context

**Purpose:** Ensure specifications respect all constraints

**Reference:** `architecture-validation.md`

Load all 6 context files, validate spec compliance (technologies, packages, structure, layer boundaries, anti-patterns). Use AskUserQuestion to resolve conflicts.

**Output:** Validated specification ready for implementation

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/architecture-validation.md")
```

---

### Phase 5.5: Prompt Alignment

**Purpose:** Validate context files are consistent with configuration layers (CLAUDE.md, system-prompt-core.md) before epic creation.

**Precondition:** Phase 5 completed. All 6 context files exist in `devforgeai/specs/context/`.

**Postcondition:** All HIGH contradictions resolved, skipped with justification, or overridden with ACCEPTED_RISK + justification.

**Reference:** `prompt-alignment-workflow.md`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/prompt-alignment-workflow.md")
```

**6-Step Workflow Summary:**

1. **Detect Configuration Layers** — Check for CLAUDE.md and system-prompt-core.md (handle missing gracefully).
2. **Invoke alignment-auditor** — Call `Task(subagent_type="alignment-auditor")` with all 6 context files + detected layers. Returns JSON.
3. **Process Contradictions** — HIGH contradictions block Phase 6. MEDIUM/LOW are deferrable. Allow ACCEPTED_RISK override.
4. **Process Gaps** — Synthesize `<project_context>` from context files. Draft CLAUDE.md sections. Present for approval (non-blocking).
5. **Process ADR Drift** — Compare ADR decisions against context files. Report and optionally remediate.
6. **Report** — Compile summary. Write to `devforgeai/feedback/ai-analysis/phase-5.5-alignment.json`.

**Graceful Degradation:** If alignment-auditor fails, display WARNING and continue to Phase 6 (non-blocking).

**Output:** Alignment report. Phase 6 gate: UNBLOCKED after all HIGH findings resolved.

---

### Phase 5.7: Domain Reference Generation

**Purpose:** Generate project-specific domain reference files for subagents based on context file analysis.

**Precondition:** Phase 5.5 (Prompt Alignment) completed. All 6 context files exist in `devforgeai/specs/context/`.

**Postcondition:** Generated references contain only context-derived content (100% derivation purity).

**Reference:** `domain-reference-generation.md`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/domain-reference-generation.md")
```

**5-Step Workflow Summary:**

1. **Run Detection Heuristics** — Evaluate DH-01 through DH-04 against context files. If none trigger, skip to Phase 6.
2. **Present Recommendations** — Display triggered heuristics. AskUserQuestion: Generate all / Select individually / Skip.
3. **Generate Reference Files** — For each approved heuristic, extract context content and write `project-*.md` to agent references directory.
4. **Verify Derivation Purity** — Confirm 100% content traceability to source context files. Halt individual files on failure.
5. **Report** — Display summary of generated files, source mappings, and regeneration command.

**Non-Blocking:** If generation fails or user skips, proceed to Phase 6 without halting the workflow.

**Output:** Summary of generated domain reference files with source context file mappings.

---

### Phase 6: Epic Creation

**Purpose:** Create complete epic documents from structured requirements (handoff from ideation)

**Reference:** `epic-management.md`

**Input:** YAML-structured requirements.md (from ideation) OR legacy narrative requirements

---

#### Phase 6.1: Discovery & Context Loading

**Purpose:** Load epic context and existing project artifacts

**Load workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/epic-management.md")
```

Check for existing epics, brainstorm documents, and project context.

---

#### Phase 6.2: Requirements Input Parsing

**Purpose:** Parse YAML-structured requirements from ideation skill

**Schema:** `discovering-requirements/assets/templates/requirements-schema.yaml`
**Required Fields:** decisions, scope, success_criteria, constraints, nfrs, stakeholders
**Legacy Fallback:** If YAML not detected, use AskUserQuestion for missing fields

```
Read(file_path=".claude/skills/discovering-requirements/assets/templates/requirements-schema.yaml")
```

---

#### Phase 6.3: Feature Decomposition

**Purpose:** Decompose requirements into epic features using requirements-analyst subagent

```
Read(file_path=".claude/skills/designing-systems/references/feature-decomposition.md")
Task(subagent_type="requirements-analyst", description="Decompose requirements into features")
```

---

#### Phase 6.4: Technical Assessment

**Purpose:** Assess technical complexity using architect-reviewer subagent

```
Read(file_path=".claude/skills/designing-systems/references/complexity-assessment-workflow.md")
Task(subagent_type="architect-reviewer", description="Assess epic technical complexity")
```

---

#### Phase 6.5: Epic Document Generation

**Purpose:** Generate complete epic document from analyzed features

**Load workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/artifact-generation.md")
```

Assemble epic content: title, description, features, acceptance criteria, NFRs, dependencies.

---

#### Phase 6.6: Validation & Self-Healing

**Purpose:** Validate epic against checklist and fix issues automatically

**Load workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/epic-validation-checklist.md")
```

Run validation checks. If issues found, attempt self-healing corrections. If unresolvable, prompt user.

---

#### Phase 6.7: Epic File Creation

**Purpose:** Write validated epic to file system

**Load workflow:**
```
Read(file_path=".claude/skills/designing-systems/assets/templates/epic-template.md")
Read(file_path=".claude/skills/designing-systems/references/epic-validation-hook.md")
```

Write epic to `devforgeai/specs/Epics/EPIC-NNN-[title].epic.md`

---

#### Phase 6.8: Post-Epic Feedback Hook

**Purpose:** Non-blocking feedback collection per STORY-028

```
TRY: Skill(command="devforgeai-feedback", args="--context=epic-creation")
CATCH: Display warning but do not block epic creation
```

---

## Ambiguity Detection

**CRITICAL:** Use AskUserQuestion for ANY ambiguity - technology choices unclear, multiple valid options, conflicting requirements, version/security/performance/compliance decisions.

**See `references/ambiguity-detection-guide.md` for complete scenarios.**

---

## Brownfield Projects

Existing codebases require discovery → gap analysis → migration strategy decision (gradual/full refactor/accept current) → transitional context files.

**See `references/brownfield-integration.md` for complete workflow.**

**Repository Map Integration (STORY-373):** For brownfield analysis, query `treelint map --ranked --format json` to generate a ranked symbol importance map. See `references/brownfield-map-integration.md` for integration details.

---

## Integration with Other Skills

**From:** discovering-requirements (YAML-structured requirements → architecture Phase 6)
**To:** devforgeai-orchestration (story planning), implementing-stories (implementation)
**Provides:** 6 context files (enforced by all skills), ADRs (traceability), Technical specs (guidance), Epic documents (Phase 6)

---

## Asset Templates

**Context Templates (6 files, 3,922 lines):**
- tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**ADR Examples (6 files, 5,157 lines):**
- Database selection, ORM selection, State management, Clean Architecture, Deployment strategy, Scope changes

**All templates in `assets/` load on-demand.**

---

## Reference Files

**Workflow Files (6 files - Load per phase 1-5):**
- context-discovery-workflow.md, context-file-creation-workflow.md, adr-creation-workflow.md, technical-specification-workflow.md, architecture-validation.md, brownfield-integration.md

**Epic Creation Files (10 files - Load per Phase 6 sub-phases):**
- epic-management.md, feature-decomposition.md, feature-analyzer.md, complexity-assessment-workflow.md, complexity-assessment-matrix.md, artifact-generation.md, epic-validation-checklist.md, epic-template.md, epic-validation-hook.md, technical-assessment-guide.md

**Guide Files (4 files - Load as needed):**
- adr-policy.md, adr-template.md, ambiguity-detection-guide.md, system-design-patterns.md

---

## Scripts

- `scripts/init_context.sh` - Initialize context files for new projects
- `scripts/validate_spec.py` - Validate spec against existing context

---

## Success Criteria

Architecture phase complete when:

- [ ] All 6 required context files exist in `devforgeai/specs/context/`
- [ ] Optional design-system.md created if UI project
- [ ] Context files non-empty (no placeholders)
- [ ] At least 1 ADR created (initial architecture decision)
- [ ] All ambiguities resolved (via AskUserQuestion)
- [ ] Validation passes (Phase 5)
- [ ] Ready for story planning (next: devforgeai-orchestration)

**The goal:** Zero ambiguity = Zero technical debt from wrong assumptions.
