---
id: EPIC-066
title: "/dev Command & devforgeai-development Skill Anthropic Conformance Analysis"
status: Planning
start_date: 2026-02-15
target_date: 2026-03-15
total_points: 48
completed_points: 0
created: 2026-02-15
owner: DevForgeAI Framework Team
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
brainstorm: BRAINSTORM-010
---

# Epic: /dev Command & devforgeai-development Skill Anthropic Conformance Analysis

## Business Goal

Systematically analyze the `/dev` slash command and `devforgeai-development` skill against Anthropic's official Agent Skills best practices and prompt engineering guidelines. Produce a comprehensive architectural analysis with 14-category scoring, gap identification, and a prioritized remediation roadmap that transforms the skill into full Anthropic conformance while respecting all 6 constitutional context files.

**Problem:** The devforgeai-development skill (1,099 lines SKILL.md + 3,910 lines phases + ~20,280 lines references = ~25,546 total lines) has never been formally audited against Anthropic's Agent Skills specification. Known gaps include SKILL.md exceeding the 500-line target by 2.2x, non-gerund naming convention, and untested progressive disclosure depth.

**Value:** A conformant skill improves Claude's discovery accuracy, reduces context window waste, and ensures the framework's largest skill follows the platform vendor's official guidance.

**Requirements Source:** `.claude/plans/dev-command-analysis-prompt.md`

## Success Metrics

- **Metric 1:** All 14 scoring categories (N1-N14) scored with evidence, gap analysis, and remediation
- **Metric 2:** Consolidated analysis document produced matching the output template structure
- **Metric 3:** Prioritized remediation roadmap with effort estimates for all Critical/High findings
- **Metric 4:** Actionable improvement stories generated for every Critical/High finding

**Measurement Plan:**
- Tracked via deliverable file completion in `devforgeai/specs/requirements/dev-analysis/`
- 12 deliverable files = 12 stories, each independently verifiable
- Review frequency: Per-sprint review

## Scope

### In Scope

12 features (stories) producing 12 deliverable files, organized in 4 sprints with strict dependency chaining. Each deliverable is a self-contained analysis document in `devforgeai/specs/requirements/dev-analysis/`.

**Key design constraint:** No Sprint 3-4 story reads raw source files. They read ONLY compressed deliverables from prior stories. This ensures each story fits in one context window.

1. **Feature A: Ecosystem Inventory**
   - Complete inventory of all files in the devforgeai-development skill ecosystem
   - File paths, line counts, purposes, layer assignments, architecture diagram
   - Business value: Foundation for all subsequent analysis — establishes the complete scope

2. **Feature B: Scoring Rubric Extraction**
   - Extract 14 scoring categories (N1-N14) with exact quoted text and line numbers from Anthropic source docs
   - Becomes the ONLY rubric reference for Sprint 3 (scoring stories never re-read source docs)
   - Business value: Single source of truth for scoring criteria, prevents re-reading large reference files

3. **Feature C: /dev Command Analysis**
   - Analyze the /dev slash command: YAML frontmatter, argument parsing, delegation pattern, size
   - Business value: Validates the user-facing entry point follows thin command architecture

4. **Feature D: SKILL.md Analysis**
   - Analyze SKILL.md: frontmatter, body structure, phase orchestration, progressive disclosure, size violation
   - Business value: Evaluates the core skill file where most conformance gaps are expected

5. **Feature E: Phase Files Analysis**
   - Analyze all 16 phase files: execution flow, gate verification, subagent invocation map
   - Business value: Maps the complete workflow execution and identifies phase-level gaps

6. **Feature F: Reference Files Analysis**
   - Analyze all reference files: depth map, token cost estimates, progressive disclosure effectiveness
   - Business value: Identifies context window optimization opportunities in the largest content layer

7. **Feature G: Scores N1-N5 (Naming, Description, Size, Progressive Disclosure, Conciseness)**
   - Score 5 categories using rubric + Sprint 2 analysis deliverables only
   - Business value: Evaluates skill metadata and structural conformance

8. **Feature H: Scores N6-N10 (Degrees of Freedom, Workflow, Feedback Loops, XML Tags, Role Prompting)**
   - Score 5 categories using rubric + Sprint 2 analysis deliverables only
   - Business value: Evaluates prompt engineering technique conformance

9. **Feature I: Scores N11-N14 (Examples/Multishot, Chain of Thought, Architecture, Anti-Patterns)**
   - Score 4 categories using rubric + Sprint 2 analysis deliverables only
   - Business value: Evaluates advanced technique and DevForgeAI-specific conformance

10. **Feature J: Remediation Roadmap**
    - Prioritized roadmap (Critical > High > Medium) with effort estimates and impact analysis
    - Business value: Actionable plan for closing all identified gaps

11. **Feature K: Consolidated Report**
    - Final analysis document matching the output template structure exactly
    - Includes executive summary, overall score, Anthropic best practices checklist
    - Business value: Self-contained deliverable for stakeholder review

12. **Feature L: Improvement Stories**
    - User stories for each Critical/High finding using /create-story format
    - Each story includes Anthropic conformance citations
    - Business value: Direct input to sprint planning for remediation work

### Out of Scope

- Implementing any code changes to the devforgeai-development skill
- Analyzing other DevForgeAI skills (devforgeai-qa, devforgeai-orchestration, etc.)
- Modifying constitutional context files
- Creating ADRs for architectural decisions (deferred to remediation stories)

## Target Sprints

### Sprint 1: Foundation

**Goal:** Establish the complete ecosystem inventory and scoring rubric as foundation for all subsequent analysis
**Estimated Points:** 6
**Features:**
- Feature A: Ecosystem Inventory (3 points)
- Feature B: Scoring Rubric Extraction (3 points)

**Key Deliverables:**
- `devforgeai/specs/requirements/dev-analysis/01-ecosystem-inventory.md`
- `devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md`

**Dependencies:** None. These stories have no prerequisites.

**Anthropic Reference Files Read:**
- `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` (1,140 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/overview.md` (345 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/*.md` (13 files, ~1,200 lines)

---

### Sprint 2: Analysis (Parallelizable)

**Goal:** Analyze all 4 layers of the devforgeai-development ecosystem, producing compressed analysis deliverables
**Estimated Points:** 18
**Features:**
- Feature C: /dev Command Analysis (3 points)
- Feature D: SKILL.md Analysis (5 points)
- Feature E: Phase Files Analysis (5 points)
- Feature F: Reference Files Analysis (5 points)

**Key Deliverables:**
- `devforgeai/specs/requirements/dev-analysis/03-dev-command-analysis.md`
- `devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md`
- `devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md`
- `devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md`

**Dependencies:** Feature A (Ecosystem Inventory) must complete first. Features C, D, E, F can execute in parallel.

**Raw Source Files Read (Sprint 2 only — last sprint to read raw source):**
- `.claude/commands/dev.md` (257 lines)
- `.claude/skills/devforgeai-development/SKILL.md` (1,099 lines)
- `.claude/skills/devforgeai-development/phases/*.md` (16 files, 3,910 lines)
- `.claude/skills/devforgeai-development/references/*.md` (~50 files, ~20,280 lines)
- `.claude/skills/devforgeai-development/INTEGRATION_GUIDE.md`
- `.claude/skills/devforgeai-development/README.md`

---

### Sprint 3: Scoring (Reads Sprint 2 Outputs + Rubric ONLY)

**Goal:** Score all 14 categories against the extracted rubric using only compressed Sprint 2 deliverables
**Estimated Points:** 15
**Features:**
- Feature G: Scores N1-N5 (5 points)
- Feature H: Scores N6-N10 (5 points)
- Feature I: Scores N11-N14 (5 points)

**Key Deliverables:**
- `devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md`
- `devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md`
- `devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md`

**Dependencies:** Feature B (Rubric) + ALL Sprint 2 features must complete. Features G, H, I can execute in parallel.

**CRITICAL CONSTRAINT:** No Sprint 3 story reads raw source files. Input is ONLY:
- `02-scoring-rubric.md` (from Feature B)
- `03-dev-command-analysis.md` through `06-reference-files-analysis.md` (from Sprint 2)

---

### Sprint 4: Synthesis (Reads Scores ONLY)

**Goal:** Produce remediation roadmap, consolidated report, and improvement stories from scoring results
**Estimated Points:** 9
**Features:**
- Feature J: Remediation Roadmap (3 points)
- Feature K: Consolidated Report (3 points)
- Feature L: Improvement Stories (3 points)

**Key Deliverables:**
- `devforgeai/specs/requirements/dev-analysis/10-remediation-roadmap.md`
- `devforgeai/specs/requirements/dev-analysis/11-consolidated-report.md`
- `devforgeai/specs/requirements/dev-analysis/12-improvement-stories.md`

**Dependencies:** Sequential — J depends on G+H+I, K depends on J + all prior, L depends on K.

**CRITICAL CONSTRAINT:** No Sprint 4 story reads raw source files. Input is ONLY Sprint 3 score deliverables (and prior deliverables for Story K).

---

## User Stories

### Feature A → Story: Ecosystem Inventory

**As a** framework architect, **I want** a complete inventory of all files in the devforgeai-development skill ecosystem, **so that** I have a precise scope for the conformance analysis.

**Acceptance Criteria:**

AC#1: Complete file inventory with line counts
- Read ALL files in `.claude/skills/devforgeai-development/` recursively
- Record: file path, line count, purpose, layer assignment (command/skill/phase/reference/supporting)
- Anthropic context: Progressive disclosure architecture requires knowing what's at each level
  (Source: overview.md, lines 42-107)
- Context constraint: Source tree must be validated against source-tree.md patterns
  (Source: devforgeai/specs/context/source-tree.md)

AC#2: Architecture diagram
- Produce ASCII diagram: User → /dev command → Skill(devforgeai-development) → Phase files → Reference files → Subagents
- Show progressive disclosure levels (L1 metadata, L2 instructions, L3 resources)
  (Source: overview.md, lines 101-107)

AC#3: Ecosystem size summary table
- Format matching output_template section 1.2 (Ecosystem Size table)
- Include totals for each layer

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/01-ecosystem-inventory.md`

---

### Feature B → Story: Scoring Rubric Extraction

**As a** framework architect, **I want** all 14 scoring categories extracted with exact quoted text and line numbers from Anthropic source documents, **so that** Sprint 3 scoring stories have a single compressed reference and never need to re-read large source files.

**Acceptance Criteria:**

AC#1: N1 — Naming Convention rubric extracted
- Quote exact text from best-practices.md lines 154-181
- CURRENT (non-conformant): `name: devforgeai-development` (Source: SKILL.md, line 2)
- TARGET (Anthropic-conformant): Gerund form recommended — e.g., `developing-features` or `implementing-tdd`
  (Source: best-practices.md, lines 156-165)
- CONTEXT FILE CONSTRAINT: Naming convention `devforgeai-[phase]` is LOCKED
  (Source: devforgeai/specs/context/coding-standards.md, line 117).  Will require ADR to rename.

AC#2: N2 — Description Quality rubric extracted
- Quote exact text from best-practices.md lines 183-227
- Include third-person requirement (line 188), discovery mechanism role (line 197)

AC#3: N3 — SKILL.md Size rubric extracted
- Quote exact text from best-practices.md lines 233-235 and 1074-1076
- CURRENT: SKILL.md is 1,099 lines (2.2x over 500-line target)
- CONTEXT FILE CONSTRAINT: Skills target 500-800 lines, max 1,000 lines
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-107)

AC#4: N4 — Progressive Disclosure rubric extracted
- Quote exact text from best-practices.md lines 228-398 and overview.md lines 42-107
- Include three-level loading model (L1/L2/L3), one-level-deep reference rule, TOC guidance

AC#5: N5 — Conciseness rubric extracted
- Quote exact text from best-practices.md lines 13-55
- Include "challenge each piece" criteria and good/bad examples

AC#6: N6 — Degrees of Freedom rubric extracted
- Quote exact text from best-practices.md lines 57-122
- Include highway/bridge/field metaphors for HIGH/MEDIUM/LOW freedom

AC#7: N7 — Workflow Structure rubric extracted
- Quote exact text from best-practices.md lines 399-488
- Include checklist pattern and sequential step guidance

AC#8: N8 — Feedback Loops rubric extracted
- Quote exact text from best-practices.md lines 492-533
- Include "run validator → fix errors → repeat" pattern

AC#9: N9 — XML Tags rubric extracted
- Quote key guidance from prompt-engineering/use-xml-tags.md
- Include clarity, accuracy, flexibility, parseability benefits

AC#10: N10 — Role Prompting rubric extracted
- Quote key guidance from prompt-engineering/give-claude-a-role.md
- Include system parameter usage and domain expert transformation

AC#11: N11 — Examples/Multishot rubric extracted
- Quote key guidance from prompt-engineering/Use-examples-multishot prompting-to-guide-Claudes-behavior.md
- Include 3-5 examples guidance, <example> tag wrapping

AC#12: N12 — Chain of Thought rubric extracted
- Quote key guidance from prompt-engineering/chain-of-thought.md
- Include structured CoT with <thinking> and <answer> tags

AC#13: N13 — Command-Skill Architecture rubric extracted
- Source: DevForgeAI architecture-constraints.md
- Commands <500 lines, thin orchestrators; Skills single responsibility; Subagents least-privilege
  (Source: devforgeai/specs/context/architecture-constraints.md)

AC#14: N14 — Anti-Patterns rubric extracted
- Quote exact text from best-practices.md lines 805-831
- Include Windows paths, too many options, deeply nested references, time-sensitive info

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md`

---

### Feature C → Story: /dev Command Analysis

**As a** framework architect, **I want** a detailed analysis of the /dev slash command, **so that** I understand whether the user-facing entry point follows Anthropic's thin command architecture.

**Acceptance Criteria:**

AC#1: YAML frontmatter analysis
- CURRENT (non-conformant): Command frontmatter uses `description: Implement user story using TDD workflow` — generic, does not include trigger conditions or key terms for discovery
  (Source: .claude/commands/dev.md, lines 1-7)
- TARGET (Anthropic-conformant): `name` and `description` fields with specific validation rules — description must include both what the skill does and when to use it, written in third person
  (Source: best-practices.md, lines 137-151, 183-227)
- CONTEXT FILE CONSTRAINT: Commands target 200-400 lines, max 500 lines. Current /dev command is 257 lines — within target range.
  (Source: devforgeai/specs/context/coding-standards.md, line 108)

AC#2: Delegation pattern analysis
- CURRENT (conformant): Command delegates via `Skill(command="devforgeai-development")` after argument parsing. Contains plan mode auto-exit, argument parsing, gaps.json auto-detection, and skill invocation — some business logic (gaps detection, remediation mode) lives in command rather than skill.
  (Source: .claude/commands/dev.md, lines 45-80)
- TARGET (Anthropic-conformant): Commands should be thin orchestrators that delegate ALL business logic to skills. "Commands invoke Skills; Skills invoke Subagents."
  (Source: best-practices.md, lines 399-403; overview.md, lines 34-38)
- CONTEXT FILE CONSTRAINT: "Commands invoke Skills; Skills invoke Subagents. Skills CANNOT invoke Commands; Subagents CANNOT invoke Skills or Commands."
  (Source: devforgeai/specs/context/architecture-constraints.md)

AC#3: Argument parsing and error handling analysis
- CURRENT (partial): Command parses STORY-ID via regex `STORY-[0-9]+`, flags via string match (`--force`, `--fix`, `--ignore-debt-threshold`). Error message on missing STORY-ID: `"Usage: /dev STORY-NNN [--force]"` — does not list all valid flags.
  (Source: .claude/commands/dev.md, lines 61-80)
- TARGET (Anthropic-conformant): Error handling should be explicit and helpful, providing clear next steps rather than punting to the user. "Scripts solve problems rather than punt to Claude."
  (Source: best-practices.md, lines 837-865)
- CONTEXT FILE CONSTRAINT: AskUserQuestion pattern is LOCKED for ALL ambiguities — if argument parsing fails, should use AskUserQuestion rather than generic error messages.
  (Source: devforgeai/specs/context/coding-standards.md, lines 83-101)

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/03-dev-command-analysis.md`

**Inputs:** `01-ecosystem-inventory.md`

---

### Feature D → Story: SKILL.md Analysis

**As a** framework architect, **I want** a detailed analysis of the SKILL.md file, **so that** I understand the primary conformance gaps in the skill's core file.

**Acceptance Criteria:**

AC#1: YAML frontmatter evaluation
- Analyze `name: devforgeai-development` against gerund convention (best-practices.md, lines 154-181)
- Analyze description against third-person and discovery requirements (best-practices.md, lines 183-227)
- CURRENT: `name: devforgeai-development` — not gerund form
  (Source: .claude/skills/devforgeai-development/SKILL.md, line 2)
- TARGET: Gerund form like `developing-with-tdd` or `implementing-features`
  (Source: best-practices.md, lines 156-165)

AC#2: Body size analysis
- CURRENT: 1,099 lines — exceeds 500-line target by 599 lines (2.2x)
  (Source: .claude/skills/devforgeai-development/SKILL.md)
- TARGET: Under 500 lines (best-practices.md, lines 233-235)
- CONTEXT FILE CONSTRAINT: Skills target 500-800 lines, max 1,000 lines
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-107)
- Identify which sections to extract to achieve <500 lines

AC#3: Progressive disclosure effectiveness
- Map what content is in SKILL.md body vs. extracted to phases/ and references/
- Check reference depth (Anthropic: one level deep from SKILL.md)
  (Source: best-practices.md, lines 228-398)
- Identify any A→B→C reference chains

AC#4: Content structure analysis
- Document section organization, heading hierarchy
- Check for table of contents (files >100 lines should have TOC)
- Evaluate conciseness (does it over-explain things Claude already knows?)
  (Source: best-practices.md, lines 13-55)

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md`

**Inputs:** `01-ecosystem-inventory.md`

---

### Feature E → Story: Phase Files Analysis

**As a** framework architect, **I want** a detailed analysis of all 16 phase files, **so that** I understand the workflow execution patterns and gate verification mechanisms.

**Acceptance Criteria:**

AC#1: Phase execution flow map
- CURRENT (non-conformant): 12 execution phases (01 through 10 including 04.5 and 05.5) plus 4 pre-planning phases (pre-02, pre-03, pre-04, pre-05) = 16 files, 3,910 lines total. Fractional phase numbering (04.5, 05.5) is non-standard and not documented in Anthropic workflow patterns.
  (Source: .claude/skills/devforgeai-development/phases/, 16 files)
- TARGET (Anthropic-conformant): "Break complex operations into clear, sequential steps. Provide checklists that Claude can copy and track progress." Workflow steps should be clean numbered sequences.
  (Source: best-practices.md, lines 399-403)
- CONTEXT FILE CONSTRAINT: Phase naming convention is standardized (Phase 01 through Phase 10) with sub-step naming only for Phase 01.
  (Source: devforgeai/specs/context/coding-standards.md, lines 141-177)

AC#2: Phase gate verification audit
- CURRENT (partial): Phase gates use `devforgeai-validate` CLI tool (e.g., `devforgeai-validate phase-init ${STORY_ID}`) with exit codes (0=proceed, 1=resume, 2=HALT). Phase 02 entry gate checks Phase 01 completion via CLI. But not all phases have explicit entry/exit gates — some transitions are implicit.
  (Source: .claude/skills/devforgeai-development/phases/phase-01-preflight.md, lines 3-13; phase-02-test-first.md, lines 44-53)
- TARGET (Anthropic-conformant): "Common pattern: Run validator → fix errors → repeat. This pattern greatly improves output quality." Every phase transition should have an explicit validation loop.
  (Source: best-practices.md, lines 492-533)
- CONTEXT FILE CONSTRAINT: Quality gates are strict — Critical/High violations block progression. Gate enforcement is mandatory at each transition.
  (Source: devforgeai/specs/context/architecture-constraints.md)

AC#3: Subagent invocation map
- CURRENT (partial): Phases invoke subagents via `Task(subagent_type="...")` — Phase 01 invokes git-validator and tech-stack-detector, Phase 02 invokes test-automator, Phase 03 invokes backend-architect, etc. Some invocations are marked MANDATORY, others are implied but not explicitly labeled.
  (Source: .claude/skills/devforgeai-development/phases/phase-01-preflight.md, lines 21-30)
- TARGET (Anthropic-conformant): Subagents should be domain specialists with least-privilege tools. Each invocation should be explicitly marked as required or optional, with clear purpose.
  (Source: overview.md, lines 80-99)
- CONTEXT FILE CONSTRAINT: "Subagents CANNOT invoke Skills or Commands." Subagent design constraints enforce domain specialization and tool restrictions.
  (Source: devforgeai/specs/context/architecture-constraints.md)

AC#4: Phase file summary table
- CURRENT: 16 phase files ranging from 179 lines (pre-02-planning.md) to 457 lines (phase-01-preflight.md). Four files exceed 300 lines (phase-01: 457, phase-04: 416, phase-09: 330, phase-06: 262).
  (Source: .claude/skills/devforgeai-development/phases/, wc -l output)
- TARGET (Anthropic-conformant): Files >100 lines should have a table of contents at the top. Content should be concise — "Does Claude really need this explanation?"
  (Source: best-practices.md, lines 13-55, 228-398)
- CONTEXT FILE CONSTRAINT: Component size limits apply — skills target 500-800 lines max 1,000. Phase files as sub-components should be proportionally sized.
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-112)

AC#5: Degrees of freedom assessment
- CURRENT (mixed): Some phases use HIGH freedom (text instructions for flexible decisions like refactoring choices in phase-04), while others use LOW freedom (exact CLI commands in phase-01 entry gate). But the mapping is not explicitly documented per phase, and some fragile operations (e.g., git commit in phase-08) may have too much freedom.
  (Source: .claude/skills/devforgeai-development/phases/phase-04-refactoring.md; phase-08-git-workflow.md)
- TARGET (Anthropic-conformant): "Highway with guardrails" = HIGH freedom, "Narrow bridge with cliffs" = LOW freedom, provide exact scripts for fragile operations. Match specificity to fragility.
  (Source: best-practices.md, lines 57-122)
- CONTEXT FILE CONSTRAINT: Git operations require user approval (LOW freedom mandatory). TDD is mandatory (MEDIUM freedom — structured but context-dependent).
  (Source: devforgeai/specs/context/architecture-constraints.md; .claude/rules/core/git-operations.md)

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md`

**Inputs:** `01-ecosystem-inventory.md`

---

### Feature F → Story: Reference Files Analysis

**As a** framework architect, **I want** a detailed analysis of all reference files, **so that** I understand the progressive disclosure depth, token costs, and optimization opportunities.

**Acceptance Criteria:**

AC#1: Reference depth map
- CURRENT (non-conformant): Reference chains go 3+ levels deep. Example chain: SKILL.md → phase-01-preflight.md → references/preflight/_index.md → references/preflight/01.0-project-root.md. This is a 3-level chain (SKILL.md → phase → index → sub-file), violating the one-level-deep rule.
  (Source: .claude/skills/devforgeai-development/references/preflight/_index.md, lines 1-4: "Total Original: 3,020 lines → Now decomposed into 18 files")
- TARGET (Anthropic-conformant): "File references are one level deep." References should be directly accessible from SKILL.md — no A→B→C chains.
  (Source: best-practices.md, line 1089; best-practices.md, lines 228-398)
- CONTEXT FILE CONSTRAINT: Progressive disclosure pattern requires "Main file ≤1000 lines, references on-demand" but does not explicitly limit depth. However, anti-patterns.md forbids circular dependencies and architecture-constraints.md mandates single responsibility.
  (Source: devforgeai/specs/context/source-tree.md; devforgeai/specs/context/anti-patterns.md)

AC#2: Token cost estimate
- CURRENT (non-conformant): If ALL reference files loaded simultaneously: ~20,280 lines of references + 3,910 lines of phases + 1,099 lines of SKILL.md = ~25,289 lines (~100K+ tokens). This vastly exceeds reasonable context window usage.
  (Source: .claude/skills/devforgeai-development/references/, wc -l total: 20,280)
- TARGET (Anthropic-conformant): Progressive disclosure ensures only relevant content occupies context. L1 metadata ~100 tokens, L2 instructions <5K tokens, L3 resources loaded as-needed with "effectively unlimited" budget — but each load should be targeted, not bulk.
  (Source: overview.md, lines 101-107)
- CONTEXT FILE CONSTRAINT: Token budget constraints — Skills <1000 lines, context files <600 lines. Reference files have no explicit cap but progressive disclosure pattern implies load-on-demand, not bulk loading.
  (Source: devforgeai/specs/context/tech-stack.md)

AC#3: Reference file summary table
- CURRENT (mixed): ~50 reference files ranging from 23 lines (01.3-workflow-adapt.md) to 1,676 lines (git-workflow-conventions.md). 5 files exceed 700 lines; 3 files exceed 1,000 lines. Some files may be redundant or overlap in content.
  (Source: .claude/skills/devforgeai-development/references/, wc -l output)
- TARGET (Anthropic-conformant): "If Claude never accesses a bundled file, it might be unnecessary or poorly signaled." Reference files should be concise and only exist if they serve a clear, distinct purpose.
  (Source: best-practices.md, lines 794-803)
- CONTEXT FILE CONSTRAINT: Subagent files target 100-300 lines, max 500 lines. While reference files are not subagents, the framework's general principle of size discipline applies.
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-112)

AC#4: Largest file analysis
- CURRENT (non-conformant): 5 largest reference files total 5,897 lines:
  - git-workflow-conventions.md (1,676 lines) — 3.4x over subagent max
  - phase-06-deferral-challenge.md (1,361 lines) — 2.7x over subagent max
  - tdd-red-phase.md (1,068 lines) — 2.1x over subagent max
  - tdd-patterns.md (1,013 lines) — 2.0x over subagent max
  - slash-command-argument-validation-pattern.md (779 lines) — 1.6x over subagent max
  (Source: .claude/skills/devforgeai-development/references/, wc -l output)
- TARGET (Anthropic-conformant): "Only add context Claude doesn't already have. Challenge each piece: Does Claude really need this explanation?" Large files likely contain verbose explanations of things Claude already knows.
  (Source: best-practices.md, lines 13-55)
- CONTEXT FILE CONSTRAINT: Extract to references/ when exceeding target. But these ARE reference files — they need further decomposition or conciseness editing.
  (Source: devforgeai/specs/context/coding-standards.md, line 112)

AC#5: Preflight sub-reference analysis
- CURRENT (non-conformant): Preflight directory contains 19 files totaling ~2,208 lines, accessed via a 3-level chain: SKILL.md body → phase-01-preflight.md (line 3: "Read references/preflight/_index.md") → _index.md → individual step files (01.0-project-root.md, 01.1-git-status.md, etc.). The _index.md file serves as an intermediate routing layer.
  (Source: .claude/skills/devforgeai-development/references/preflight/_index.md, lines 1-40)
- TARGET (Anthropic-conformant): "File references are one level deep." The preflight sub-reference pattern adds an unnecessary intermediate layer (_index.md). Phase-01 should reference sub-files directly, or the index should be inlined.
  (Source: best-practices.md, line 1089)
- CONTEXT FILE CONSTRAINT: Progressive disclosure pattern is documented in source-tree.md — "Main files concise, references deep." But depth is not the same as progressive disclosure; unnecessary intermediaries add loading overhead without value.
  (Source: devforgeai/specs/context/source-tree.md)

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md`

**Inputs:** `01-ecosystem-inventory.md`

---

### Feature G → Story: Scores N1-N5

**As a** framework architect, **I want** categories N1-N5 scored with evidence and remediation, **so that** the structural and metadata conformance is quantified.

**Acceptance Criteria:**

AC#1: N1 — Naming Convention scored (1-10)
- Evidence from `04-skill-md-analysis.md`
- Rubric from `02-scoring-rubric.md` (N1 section)
- Include: best practice quote, current implementation quote, gap analysis, severity, remediation

AC#2: N2 — Description Quality scored (1-10)
- Evidence from `04-skill-md-analysis.md`
- Rubric from `02-scoring-rubric.md` (N2 section)

AC#3: N3 — SKILL.md Size scored (1-10)
- Evidence from `04-skill-md-analysis.md`
- Rubric from `02-scoring-rubric.md` (N3 section)
- Include specific line reduction targets and extraction plan

AC#4: N4 — Progressive Disclosure scored (1-10)
- Evidence from `04-skill-md-analysis.md` and `06-reference-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N4 section)

AC#5: N5 — Conciseness scored (1-10)
- Evidence from `04-skill-md-analysis.md` and `06-reference-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N5 section)
- Identify verbose sections with specific line ranges

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md`

**Inputs (ONLY — no raw source files):**
- `02-scoring-rubric.md`
- `04-skill-md-analysis.md`
- `06-reference-files-analysis.md`

---

### Feature H → Story: Scores N6-N10

**As a** framework architect, **I want** categories N6-N10 scored with evidence and remediation, **so that** the prompt engineering technique conformance is quantified.

**Acceptance Criteria:**

AC#1: N6 — Degrees of Freedom scored (1-10)
- Evidence from `04-skill-md-analysis.md` and `05-phase-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N6 section)
- Assess each phase's freedom level appropriateness

AC#2: N7 — Workflow Structure scored (1-10)
- Evidence from `05-phase-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N7 section)
- Evaluate checklist presence and step clarity

AC#3: N8 — Feedback Loops scored (1-10)
- Evidence from `05-phase-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N8 section)
- Identify validation loop patterns (or lack thereof)

AC#4: N9 — XML Tags scored (1-10)
- Evidence from `04-skill-md-analysis.md`
- Rubric from `02-scoring-rubric.md` (N9 section)
- Assess XML tag usage for clarity and parseability

AC#5: N10 — Role Prompting scored (1-10)
- Evidence from `04-skill-md-analysis.md`
- Rubric from `02-scoring-rubric.md` (N10 section)
- Evaluate role clarity and domain specificity

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md`

**Inputs (ONLY — no raw source files):**
- `02-scoring-rubric.md`
- `04-skill-md-analysis.md`
- `05-phase-files-analysis.md`

---

### Feature I → Story: Scores N11-N14

**As a** framework architect, **I want** categories N11-N14 scored with evidence and remediation, **so that** advanced technique and architecture conformance is quantified.

**Acceptance Criteria:**

AC#1: N11 — Examples/Multishot scored (1-10)
- Evidence from `04-skill-md-analysis.md` and `05-phase-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N11 section)
- Count examples provided, assess diversity and relevance

AC#2: N12 — Chain of Thought scored (1-10)
- Evidence from `04-skill-md-analysis.md` and `05-phase-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N12 section)
- Evaluate reasoning guidance and thinking prompts

AC#3: N13 — Command-Skill Architecture scored (1-10)
- Evidence from `03-dev-command-analysis.md`, `04-skill-md-analysis.md`, `05-phase-files-analysis.md`
- Rubric from `02-scoring-rubric.md` (N13 section)
- Evaluate thin command pattern, single responsibility, subagent scoping

AC#4: N14 — Anti-Patterns scored (1-10)
- Evidence from ALL Sprint 2 deliverables (03 through 06)
- Rubric from `02-scoring-rubric.md` (N14 section)
- Check: Windows paths, too many options, deep nesting, time-sensitive info

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md`

**Inputs (ONLY — no raw source files):**
- `02-scoring-rubric.md`
- `03-dev-command-analysis.md`
- `04-skill-md-analysis.md`
- `05-phase-files-analysis.md`
- `06-reference-files-analysis.md`

---

### Feature J → Story: Remediation Roadmap

**As a** framework architect, **I want** a prioritized remediation roadmap, **so that** Critical and High findings are addressed in the correct order with effort estimates.

**Acceptance Criteria:**

AC#1: Priority 1 — Critical findings table
- All findings with severity CRITICAL from scores N1-N14
- Format: Finding | File | Effort (S/M/L) | Impact

AC#2: Priority 2 — High findings table
- All findings with severity HIGH from scores N1-N14

AC#3: Priority 3 — Medium findings table
- All findings with severity MEDIUM from scores N1-N14

AC#4: Estimated total effort
- Aggregate effort estimate in story points
- Recommended sprint allocation for remediation work

AC#5: Dependency ordering
- Identify which remediations must happen first (e.g., SKILL.md size reduction before progressive disclosure improvements)

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/10-remediation-roadmap.md`

**Inputs (ONLY):** `07-scores-n1-n5.md`, `08-scores-n6-n10.md`, `09-scores-n11-n14.md`

---

### Feature K → Story: Consolidated Report

**As a** framework architect, **I want** the final consolidated analysis document, **so that** all findings are assembled in one self-contained report matching the output template structure.

**Acceptance Criteria:**

AC#1: Executive summary with overall score
- Calculate weighted average of N1-N14 scores
- Top 5 Critical findings listed
- Ecosystem size summary table

AC#2: Sections 2-6 assembled from Sprint 2 deliverables
- YAML Frontmatter Analysis (from 03, 04)
- Scoring Results (from 07, 08, 09)
- File-by-File Analysis (from 03, 04, 05, 06)
- Progressive Disclosure Assessment (from 06)
- Workflow Completeness Audit (from 05)

AC#3: Section 7 — Remediation Roadmap (from 10)

AC#4: Section 8 — Anthropic Best Practices Checklist
- Reproduce the exact checklist from best-practices.md lines 1077-1108
- Mark each item [x] or [ ] based on scoring results
- Three categories: Core Quality (10 items), Code and Scripts (8 items), Testing (4 items)

AC#5: Section 9 — Appendix
- Files Read inventory, files NOT read, scoring methodology, reference links

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/11-consolidated-report.md`

**Inputs (ONLY):** ALL deliverables 01 through 10

---

### Feature L → Story: Improvement Stories

**As a** framework architect, **I want** actionable user stories generated for each Critical/High finding, **so that** remediation work can be planned via /create-sprint.

**Acceptance Criteria:**

AC#1: Story generated for each Critical finding
- User story format with acceptance criteria
- Anthropic conformance citations with file paths and line numbers
- Example gap format:
  - CURRENT (non-conformant): quoted text with source
  - TARGET (Anthropic-conformant): quoted text with source
  - CONTEXT FILE CONSTRAINT: relevant constraint with source

AC#2: Story generated for each High finding
- Same format as AC#1

AC#3: Stories respect context file constraints
- Each story must note which context files constrain the remediation
- If remediation would violate a context file, note that an ADR is required first

AC#4: Story priority ordering
- Stories ordered by: dependency first, then impact, then effort
- Recommended sprint allocation

**Deliverable:** `devforgeai/specs/requirements/dev-analysis/12-improvement-stories.md`

**Inputs (ONLY):** `10-remediation-roadmap.md`, `11-consolidated-report.md`

---

## Technical Considerations

### Architecture Impact
- No architecture changes — this is a read-only analysis epic
- Output is 12 Markdown deliverable files in `devforgeai/specs/requirements/dev-analysis/`
- Improvement stories (Feature L) may propose architecture changes, but those are separate epics

### Technology Decisions
- No new technologies — uses only Markdown documentation and existing Read/Write/Grep tools
- Compliant with zero-dependency framework model
  (Source: devforgeai/specs/context/dependencies.md)

### Context Window Management (Critical Design Decision)
- Sprint 1-2 stories read raw source files (~25,546 lines total across ecosystem)
- Sprint 3-4 stories read ONLY compressed deliverables from prior stories
- This additive architecture ensures every story fits in one context window
- No story needs to simultaneously load the entire 25,546-line ecosystem

### Anthropic Reference Files
All scoring references originate from:
- `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` (1,140 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/overview.md` (345 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/overview.md` (72 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/be-clear-and-direct.md` (68 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/Use-examples-multishot prompting-to-guide-Claudes-behavior.md` (51 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-of-thought.md` (92 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/use-xml-tags.md` (66 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/give-claude-a-role.md` (111 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-complex-prompts.md` (143 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/long-context-tips.md` (87 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/extended-thinking-tips.md` (399 lines)

### Constitutional Context File Constraints
All remediation stories (Feature L) must respect:
1. `devforgeai/specs/context/tech-stack.md` — Framework-agnostic design, native tools only
2. `devforgeai/specs/context/source-tree.md` — File location rules, naming conventions
3. `devforgeai/specs/context/dependencies.md` — Zero-dependency model
4. `devforgeai/specs/context/coding-standards.md` — Size limits (Skills 500-800/1000), naming conventions
5. `devforgeai/specs/context/architecture-constraints.md` — 3-layer architecture, single responsibility
6. `devforgeai/specs/context/anti-patterns.md` — Forbidden patterns, severity levels

## Dependencies

### Internal Dependencies
- [x] **Dependency 1:** Anthropic Skills reference files must exist
  - **Status:** Complete
  - **Location:** `.claude/skills/claude-code-terminal-expert/references/skills/` and `references/prompt-engineering/`

- [x] **Dependency 2:** devforgeai-development skill ecosystem must exist
  - **Status:** Complete
  - **Location:** `.claude/skills/devforgeai-development/`

- [x] **Dependency 3:** Constitutional context files must exist
  - **Status:** Complete
  - **Location:** `devforgeai/specs/context/` (6 files)

### External Dependencies
- None. This is an internal analysis epic with no external service dependencies.

### Story Dependencies (Critical — enforces additive architecture)

```
Sprint 1:  A ──────────────────────────────────────────────────┐
           B ──────────────────────────────────────┐           │
                                                   │           │
Sprint 2:  C ←── A                                 │           │
           D ←── A           (C, D, E, F parallel) │           │
           E ←── A                                 │           │
           F ←── A                                 │           │
                                                   ▼           ▼
Sprint 3:  G ←── B + C,D,E,F
           H ←── B + C,D,E,F  (G, H, I parallel)
           I ←── B + C,D,E,F

Sprint 4:  J ←── G,H,I        (sequential)
           K ←── J + all prior
           L ←── K
```

## Risks & Mitigation

### Risk 1: Context window overflow in Sprint 2 analysis stories
- **Probability:** Medium
- **Impact:** High — analysis would be incomplete
- **Mitigation:** Sprint 2 stories read only their assigned layer (command/skill/phases/references), not all layers simultaneously
- **Contingency:** Split large-layer stories (e.g., F: Reference Files) into sub-stories if needed

### Risk 2: Scoring subjectivity in Sprint 3
- **Probability:** Low
- **Impact:** Medium — scores may not be reproducible
- **Mitigation:** Rubric extraction (Story B) provides exact criteria with quoted text; scoring must cite specific evidence
- **Contingency:** Include confidence level (HIGH/MEDIUM/LOW) with each score

### Risk 3: Context file naming convention conflict with Anthropic gerund recommendation
- **Probability:** High
- **Impact:** Medium — remediation may require ADR to update coding-standards.md
- **Mitigation:** Story B documents the conflict explicitly; Story L improvement stories note ADR requirement
- **Contingency:** Accept current naming if ADR process determines context file constraint takes priority

## Stakeholders

### Primary Stakeholders
- **Product Owner:** Framework Team — Ensures analysis aligns with framework improvement goals
- **Tech Lead:** DevForgeAI AI Agent — Executes analysis workflow

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════
Week 1:    Sprint 1 — Foundation (Stories A, B)
Week 2:    Sprint 2 — Analysis (Stories C, D, E, F — parallel)
Week 3:    Sprint 3 — Scoring (Stories G, H, I — parallel)
Week 4:    Sprint 4 — Synthesis (Stories J → K → L — sequential)
════════════════════════════════════════════════════════════
Total Duration: 4 weeks
Target Completion: 2026-03-15
```

### Key Milestones
- [ ] **Milestone 1:** Sprint 1 complete — Ecosystem inventory + scoring rubric extracted
- [ ] **Milestone 2:** Sprint 2 complete — All 4 analysis layers documented
- [ ] **Milestone 3:** Sprint 3 complete — All 14 categories scored
- [ ] **Milestone 4:** Sprint 4 complete — Remediation roadmap, consolidated report, improvement stories

## Progress Tracking

### Story Links

| Feature | Story ID | Title | Sprint | Points | Status |
|---------|----------|-------|--------|--------|--------|
| A | STORY-413 | Ecosystem Inventory | Sprint-1 | 3 | Backlog |
| B | STORY-414 | Scoring Rubric Extraction | Sprint-1 | 3 | Backlog |
| C | STORY-415 | /dev Command Analysis | Sprint-2 | 3 | Backlog |
| D | STORY-416 | SKILL.md Analysis | Sprint-2 | 5 | Backlog |
| E | STORY-417 | Phase Files Analysis | Sprint-2 | 5 | Backlog |
| F | STORY-418 | Reference Files Analysis | Sprint-2 | 5 | Backlog |
| G | STORY-419 | Scores N1-N5 | Sprint-3 | 5 | Backlog |
| H | STORY-420 | Scores N6-N10 | Sprint-3 | 5 | Backlog |
| I | STORY-421 | Scores N11-N14 | Sprint-3 | 5 | Backlog |
| J | STORY-422 | Remediation Roadmap | Sprint-4 | 3 | Backlog |
| K | STORY-423 | Consolidated Report | Sprint-4 | 3 | Backlog |
| L | STORY-424 | Improvement Stories | Sprint-4 | 3 | Backlog |

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1: Foundation | Ready | 6 | 2 | 0 | 0 | 0 |
| Sprint 2: Analysis | Ready | 18 | 4 | 0 | 0 | 0 |
| Sprint 3: Scoring | Blocked | 15 | 3 | 0 | 0 | 0 |
| Sprint 4: Synthesis | Blocked | 9 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **48** | **12** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 48
- **Completed:** 0
- **Remaining:** 48
- **Stories Created:** 12 (2026-02-17)

## Retrospective (Post-Epic)

*To be completed after epic completes*

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-17
**Stories Created:** 2026-02-17 by devforgeai-story-creation skill
