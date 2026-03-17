---
name: designing-systems
description: HALT - do not use. Use spec-driven-architecture instead. This skill has been replaced by spec-driven-architecture which provides structural anti-skip enforcement (Execute-Verify-Gate pattern) to prevent token optimization bias. Reference files in this directory are still used by spec-driven-architecture via shared reads.
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

## Execution Model

This skill expands inline — YOU execute each phase sequentially after invocation. Do not wait passively or assume execution happens elsewhere.

---

## Purpose

This skill creates the **architectural foundation** for projects: 6 required + 1 optional context files that define boundaries AI agents must never violate.

**Generated artifacts:**
- **6 Required Context Files** (immutable constraints in `devforgeai/specs/context/`)
- **1 Optional Context File** (design-system.md for UI projects)
- **ADRs** (architecture decisions in `devforgeai/specs/adrs/`)
- **Technical Specifications** (optional, in `devforgeai/specs/`)

**Philosophy:** Locked technologies, explicit structure, approved dependencies, enforced patterns, documented decisions — all to prevent technical debt from wrong assumptions.

---

## When to Use This Skill

- Starting new projects (create initial context)
- Making technology decisions (update tech-stack + create ADR)
- Defining project structure (create/update source-tree)
- Establishing coding standards
- Context files missing (auto-invoked by development skill)
- Brownfield projects need architectural documentation

**Invoked by:** `/create-context`, `/create-epic`, discovering-requirements skill, implementing-stories skill (if context files missing)

---

## Architecture Workflow (11 Phases)

Each phase loads its reference file on-demand. Steps within phases use decimal notation (e.g., Step 1.1, Step 1.2).

---

### Phase 1: Project Context Discovery

**Purpose:** Gather project information to make informed architecture decisions. Without this discovery, context files would contain generic boilerplate instead of project-specific constraints.

**Reference:** `references/context-discovery-workflow.md`

**Step 1.1: Detect Project Mode [MANDATORY]**

Determine greenfield vs brownfield by checking existing context files:

- **6 files exist** → Brownfield mode. Skip user-input-guidance, proceed with existing constraints.
- **0 files exist** → Greenfield mode. Load `references/user-input-guidance.md` for question patterns.
- **1-5 files exist** → Partial greenfield. Load guidance to fill gaps.

**Step 1.2: Apply Question Patterns (greenfield/partial only)**

- Use **Open-Ended Discovery** for technology inventory
- Use **Explicit Classification** for architecture style (Monolithic/Microservices/Serverless/Hybrid)
- Use **Bounded Choice** for framework and database selection

See `references/architecture-user-input-integration.md` for complete pattern mappings.

**Step 1.3: Load detailed workflow**
```
Read(file_path=".claude/skills/designing-systems/references/context-discovery-workflow.md")
```

---

### Phase 2: Create Immutable Context Files

**Purpose:** Generate the 6 files that every other skill enforces as constraints. These files are the constitutional foundation — getting them wrong means every downstream decision inherits the error.

**Reference:** `references/context-file-creation-workflow.md`

Load template for each file from `assets/context-templates/`, gather decisions via AskUserQuestion, customize with project-specific info, add enforcement rules, write to `devforgeai/specs/context/`.

**Output:**
- **Required (6):** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/context-file-creation-workflow.md")
```

---

### Phase 3: Create Architecture Decision Records

**Purpose:** Document significant technical decisions so future developers (human or AI) understand WHY choices were made, not just WHAT was chosen.

**Reference:** `references/adr-creation-workflow.md` | **Policy:** `references/adr-policy.md` | **Template:** `references/adr-template.md`

Identify decisions requiring ADRs (database, ORM, framework, patterns), load template and examples from `assets/adr-examples/`, create ADR with context/decision/rationale/consequences/alternatives/enforcement sections.

**Output:** ADR files in `devforgeai/specs/adrs/`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/adr-creation-workflow.md")
```

---

### Phase 4: Create Technical Specifications

**Purpose:** Generate high-level architecture documentation that bridges business requirements and implementation details.

**Reference:** `references/technical-specification-workflow.md` | **Patterns:** `references/system-design-patterns.md`

Create functional specs (use cases, business rules, data models), API specs (endpoints, auth), database specs (schemas, indexes), NFRs (performance, security). Use AskUserQuestion for ambiguous requirements.

**Output:** Technical spec in `devforgeai/specs/` (optional — skip if project scope doesn't warrant it)

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/technical-specification-workflow.md")
```

---

### Phase 5: Validate Spec Against Context

**Purpose:** Catch contradictions between the technical spec and context files before they propagate into stories and code. A spec that references a library not in tech-stack.md will cause every downstream story to fail validation.

**Reference:** `references/architecture-validation.md`

Load all 6 context files, validate spec compliance (technologies, packages, structure, layer boundaries, anti-patterns). Use AskUserQuestion to resolve conflicts.

**Output:** Validated specification ready for implementation

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/architecture-validation.md")
```

---

### Phase 6: Prompt Alignment

**Purpose:** Validate context files are consistent with configuration layers (CLAUDE.md, system-prompt-core.md) before epic creation. Misalignment between context files and the prompt layers causes confusing contradictions during development.

**Precondition:** Phase 5 completed. All 6 context files exist in `devforgeai/specs/context/`.

**Postcondition:** All HIGH contradictions resolved, skipped with justification, or overridden with ACCEPTED_RISK + justification.

**Reference:** `references/prompt-alignment-workflow.md`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/prompt-alignment-workflow.md")
```

**6-Step Workflow Summary:**

1. **Detect Configuration Layers** — Check for CLAUDE.md and system-prompt-core.md (handle missing gracefully).
2. **Invoke alignment-auditor** — Call `Task(subagent_type="alignment-auditor")` with all 6 context files + detected layers. Returns JSON.
3. **Process Contradictions** — HIGH contradictions block Phase 7. MEDIUM/LOW are deferrable. Allow ACCEPTED_RISK override.
4. **Process Gaps** — Synthesize `<project_context>` from context files. Draft CLAUDE.md sections. Present for approval (non-blocking).
5. **Process ADR Drift** — Compare ADR decisions against context files. Report and optionally remediate.
6. **Report** — Compile summary. Write to `devforgeai/feedback/ai-analysis/phase-6-alignment.json`.

**Graceful Degradation:** If alignment-auditor fails, display WARNING and continue to Phase 7 (non-blocking).

---

### Phase 7: Domain Reference Generation

**Purpose:** Generate project-specific domain reference files for subagents based on context file analysis. Subagents perform better when they have domain-specific context rather than generic instructions.

**Precondition:** Phase 6 (Prompt Alignment) completed. All 6 context files exist.

**Postcondition:** Generated references contain only context-derived content (100% derivation purity).

**Reference:** `references/domain-reference-generation.md`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/domain-reference-generation.md")
```

**5-Step Workflow Summary:**

1. **Run Detection Heuristics** — Evaluate DH-01 through DH-04 against context files. If none trigger, skip to Phase 8.
2. **Present Recommendations** — Display triggered heuristics. AskUserQuestion: Generate all / Select individually / Skip.
3. **Generate Reference Files** — For each approved heuristic, extract context content and write `project-*.md` to agent references directory.
4. **Verify Derivation Purity** — Confirm 100% content traceability to source context files. Halt individual files on failure.
5. **Report** — Display summary of generated files, source mappings, and regeneration command.

**Non-Blocking:** If generation fails or user skips, proceed to Phase 8 without halting.

---

### Phase 8: Architecture Review

**Purpose:** An independent review of the generated context files catches blind spots. The architect-reviewer subagent evaluates the files from a different perspective than the generation logic, surfacing coherence issues, impractical constraints, and missing concerns.

**Precondition:** Phases 1-7 completed. All 6 context files exist.

**Reference:** `references/architecture-review-workflow.md`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/architecture-review-workflow.md")
```

**Step 8.1: Invoke architect-reviewer subagent**

```
Task(
  subagent_type="architect-reviewer",
  prompt="Review the generated context files in devforgeai/specs/context/ for:
  1. Architectural soundness - Do layer boundaries prevent tight coupling?
  2. Technology coherence - Are selected technologies compatible?
  3. Completeness - Are all project concerns addressed?
  4. Consistency - Do files align with each other?
  5. Practicality - Are constraints realistic and enforceable?
  Focus on critical issues that would cause problems during development.
  Provide specific recommendations for any concerns."
)
```

**Step 8.2: Present concerns to user**

If the reviewer raises concerns, use AskUserQuestion with options:
- Accept recommendations and update files
- Keep current approach (document rationale)
- Hybrid approach (accept some, reject others)

**Step 8.3: Apply changes**

Update context files with approved changes using Edit tool. Create an ADR documenting the review decisions if significant changes were made.

---

### Phase 9: Design System Generation

**Purpose:** UI projects need a design-system.md to enforce visual consistency — without it, frontend developers (human or AI) make inconsistent styling decisions across components.

**Precondition:** Phase 8 completed. tech-stack.md exists.

**Non-Blocking:** If not a UI project, skip entirely and proceed to Phase 10.

**Step 9.1: Detect UI project**

Read `devforgeai/specs/context/tech-stack.md` and check for frontend technologies:
- React, Vue, Angular, Svelte
- Next.js, Nuxt, SvelteKit
- React Native, Flutter, Ionic

If no UI framework detected, skip to Phase 10.

**Step 9.2: Gather design preferences**

Use AskUserQuestion:
- **Custom design system** — Provide color palette, typography, spacing, border radius, shadow style preferences
- **Framework-based** — Material UI, Chakra UI, shadcn/ui, etc. (document in tech-stack.md and dependencies.md)
- **Skip** — Proceed without design system (warn that frontend consistency may suffer)

**Step 9.3: Generate design-system.md**

```
Read(file_path=".claude/skills/designing-systems/assets/context-templates/design-system.md")
```

Customize template with user preferences and write to:
```
Write(file_path="devforgeai/specs/context/design-system.md", content="[customized template]")
```

Includes: Design tokens (colors, typography, spacing, shadows, borders), component guidelines, accessibility standards (WCAG 2.1 AA), responsive breakpoints, animation standards, framework integration patterns.

---

### Phase 10: Post-Creation Validation & Report

**Purpose:** Catch incomplete or placeholder content before the architecture phase is declared done. A context file with TODO markers will cause every downstream validation to fail with confusing errors.

**Precondition:** Phases 1-9 completed (or skipped where non-blocking).

**Reference:** `references/post-creation-validation.md`

**Load detailed workflow:**
```
Read(file_path=".claude/skills/designing-systems/references/post-creation-validation.md")
```

**Step 10.1: Verify file completeness**

```
Glob(pattern="devforgeai/specs/context/*.md")
```

Confirm all 6 required files exist and each is non-empty (>100 characters).

**Step 10.2: Check for placeholder content**

```
Grep(pattern="TODO|TBD|\\[FILL IN\\]|\\[TO BE DETERMINED\\]", path="devforgeai/specs/context/", output_mode="files_with_matches")
```

If placeholders found, report files and line numbers. Use AskUserQuestion to resolve each placeholder. Update files with final values.

**Step 10.3: Verify ADR creation**

```
Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
```

At minimum, expect ADR-001 (primary language selection). Additional ADRs for framework, database, and significant choices.

**Step 10.4: Display success report**

```
Architecture Complete

Generated Files:
  tech-stack.md          - [N] technologies defined
  source-tree.md         - [N] layers structured
  dependencies.md        - [N] packages approved
  coding-standards.md    - [N] standards defined
  architecture-constraints.md - [N] constraints enforced
  anti-patterns.md       - [N] anti-patterns forbidden
  [design-system.md      - Design tokens and guidelines (if UI project)]

ADRs Created:
  ADR-001: [Decision title]
  ADR-002: [Decision title]
  [...]

Architecture Review: PASSED
Validation: All checks green

Next Steps:
  1. Review context files in devforgeai/specs/context/
  2. Customize if needed (add project-specific constraints)
  3. Run /create-epic to define your first epic
  4. Run /create-sprint to plan your first sprint
```

---

### Phase 11: Epic Creation

**Purpose:** Create complete epic documents from structured requirements (handoff from ideation). This phase runs when invoked via `/create-epic` — it's skipped when the skill is invoked via `/create-context`.

**Reference:** `references/epic-management.md`

**Input:** YAML-structured requirements.md (from ideation) OR legacy narrative requirements

---

#### Step 11.1: Discovery & Context Loading

Load epic context and existing project artifacts.

```
Read(file_path=".claude/skills/designing-systems/references/epic-management.md")
```

Check for existing epics, brainstorm documents, and project context.

---

#### Step 11.2: Requirements Input Parsing

Parse YAML-structured requirements from ideation skill.

**Schema:** `discovering-requirements/assets/templates/requirements-schema.yaml`
**Required Fields:** decisions, scope, success_criteria, constraints, nfrs, stakeholders
**Legacy Fallback:** If YAML not detected, use AskUserQuestion for missing fields

```
Read(file_path=".claude/skills/discovering-requirements/assets/templates/requirements-schema.yaml")
```

---

#### Step 11.3: Feature Decomposition

Decompose requirements into epic features using requirements-analyst subagent.

```
Read(file_path=".claude/skills/designing-systems/references/feature-decomposition.md")
Task(subagent_type="requirements-analyst", description="Decompose requirements into features")
```

---

#### Step 11.4: Technical Assessment

Assess technical complexity using architect-reviewer subagent.

```
Read(file_path=".claude/skills/designing-systems/references/complexity-assessment-workflow.md")
Task(subagent_type="architect-reviewer", description="Assess epic technical complexity")
```

---

#### Step 11.5: Epic Document Generation

Generate complete epic document from analyzed features.

```
Read(file_path=".claude/skills/designing-systems/references/artifact-generation.md")
```

Assemble epic content: title, description, features, acceptance criteria, NFRs, dependencies.

---

#### Step 11.6: Validation & Self-Healing

Validate epic against checklist and fix issues automatically.

```
Read(file_path=".claude/skills/designing-systems/references/epic-validation-checklist.md")
```

Run validation checks. If issues found, attempt self-healing corrections. If unresolvable, prompt user.

---

#### Step 11.7: Epic File Creation

Write validated epic to file system.

```
Read(file_path=".claude/skills/designing-systems/assets/templates/epic-template.md")
Read(file_path=".claude/skills/designing-systems/references/epic-validation-hook.md")
```

Write epic to `devforgeai/specs/Epics/EPIC-NNN-[title].epic.md`

---

#### Step 11.8: Post-Epic Feedback Hook

Non-blocking feedback collection.

```
TRY: Skill(command="devforgeai-feedback", args="--context=epic-creation")
CATCH: Display warning but do not block epic creation
```

---

## Ambiguity Detection

Use AskUserQuestion for ANY ambiguity — technology choices unclear, multiple valid options, conflicting requirements, version/security/performance/compliance decisions. Guessing leads to technical debt.

See `references/ambiguity-detection-guide.md` for complete scenarios.

---

## Brownfield Projects

Existing codebases require discovery, gap analysis, migration strategy decision (gradual/full refactor/accept current), then transitional context files.

See `references/brownfield-integration.md` for complete workflow.

**Repository Map Integration:** For brownfield analysis, query `treelint map --ranked --format json` to generate a ranked symbol importance map. See `references/brownfield-map-integration.md` for details.

---

## Integration with Other Skills

**From:** discovering-requirements (YAML-structured requirements -> architecture Phase 11)
**To:** devforgeai-orchestration (story planning), implementing-stories (implementation)
**Provides:** 6 context files (enforced by all skills), ADRs (traceability), Technical specs (guidance), Epic documents (Phase 11)

---

## Asset Templates

**Context Templates (7 files):**
- tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md, design-system.md

**ADR Examples (6 files):**
- Database selection, ORM selection, State management, Clean Architecture, Deployment strategy, Scope changes

All templates in `assets/` load on-demand.

---

## Reference Files

**Core Workflow (Phases 1-5):**
- context-discovery-workflow.md, context-file-creation-workflow.md, adr-creation-workflow.md, technical-specification-workflow.md, architecture-validation.md

**Post-Creation (Phases 6-10):**
- prompt-alignment-workflow.md, domain-reference-generation.md, architecture-review-workflow.md, post-creation-validation.md

**Epic Creation (Phase 11):**
- epic-management.md, feature-decomposition.md, feature-analyzer.md, complexity-assessment-workflow.md, complexity-assessment-matrix.md, artifact-generation.md, epic-validation-checklist.md, epic-template.md, epic-validation-hook.md, technical-assessment-guide.md

**Guides (load as needed):**
- adr-policy.md, adr-template.md, ambiguity-detection-guide.md, system-design-patterns.md, brownfield-integration.md, brownfield-map-integration.md, user-input-guidance.md, architecture-user-input-integration.md, create-epic-help.md

---

## Scripts

- `scripts/init_context.sh` — Initialize context files for new projects
- `scripts/validate_spec.py` — Validate spec against existing context

---

## Success Criteria

Architecture phase complete when:

- [ ] All 6 required context files exist in `devforgeai/specs/context/`
- [ ] Optional design-system.md created if UI project
- [ ] Context files non-empty (no placeholders)
- [ ] At least 1 ADR created (initial architecture decision)
- [ ] All ambiguities resolved (via AskUserQuestion)
- [ ] Architecture review passed (Phase 8)
- [ ] Validation passes (Phase 10)
- [ ] Ready for story planning (next: devforgeai-orchestration)
