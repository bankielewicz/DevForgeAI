---
name: spec-driven-research
description: >
  Capture, persist, and query research findings across sessions through a 7-phase
  workflow with structural anti-skip enforcement. Transforms web research, competitive
  analysis, technology evaluations, and market research into structured documents that
  survive session restarts. Prevents token optimization bias through per-phase reference
  loading, checkpoint persistence, Execute-Verify-Record enforcement, and artifact
  verification. Use when conducting competitive analysis, evaluating technologies,
  researching markets, planning integrations, or investigating architecture patterns.
  Always use this skill when the user runs /research or mentions research capture,
  knowledge persistence, or structured research documentation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - AskUserQuestion
  - Task
model: opus
effort: High
---

# Spec-Driven Research

Capture and persist research findings across sessions in structured, queryable documents through a 7-phase workflow with structural anti-skip enforcement.

**Context files are THE LAW:** tech-stack.md, source-tree/, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

---

## Purpose

This skill serves as the **knowledge persistence layer** for DevForgeAI. It transforms ephemeral research (web searches, competitive analysis, technology evaluations) into persistent, structured documents that survive session restarts.

### Core Philosophy

**"Research Once, Reference Forever"** - Capture research in structured documents that survive context window clears and are queryable and reusable.

**"Evidence-Based Decision Making"** - All recommendations cite research with bidirectional traceability to epics, stories, and ADRs.

**"Knowledge Compounds Over Time"** - Research index grows with each session, related research is cross-referenced, and staleness tracking ensures currency.

---

## When to Use This Skill

### Trigger Scenarios

- Competitive analysis (AWS Kiro, Cursor, etc.)
- Technology evaluation (Treelint, new libraries)
- Market research (developer frustrations, trends)
- Integration planning (external tools, APIs)
- Architecture research (patterns, best practices)
- User runs `/research` command
- User mentions research capture or knowledge persistence

### When NOT to Use

- Documenting code implementation (use stories)
- Recording decisions (use ADRs)
- Tracking bugs/issues (use RCA)

---

## Parameter Extraction

Extract from command arguments:

| Argument | Variable | Description |
|----------|----------|-------------|
| `--resume RESEARCH-NNN` | `$RESUME_ID` | Resume existing research session |
| `--search "query"` | `$SEARCH_QUERY` | Search existing research documents |
| `--list` | `$LIST_MODE` | List all research documents |
| `--category type` | `$CATEGORY_FILTER` | Filter by category (competitive, technology, market, integration, architecture) |
| `"topic string"` | `$TOPIC` | New research topic |

---

## State Persistence

- **Phase state (CLI-managed):** `devforgeai/workflows/${RESEARCH_ID}-research-phase-state.json` — the single source of truth, created and maintained by `devforgeai-validate phase-init/record/complete`; never hand-edited.
- **References:** `references/` (self-contained within this skill)
- **Templates:** `assets/templates/` (self-contained within this skill)
- **Research Output:** `devforgeai/specs/research/`
- **Research Index:** `devforgeai/specs/research/research-index.md`

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on. It CANNOT be skipped.

### Step 0.1: Parse Arguments

Extract arguments from command invocation. Determine mode:

```
IF args contain "--resume RESEARCH-NNN":
  mode = "resume"
  RESUME_ID = extract_id(args)
ELIF args contain "--search":
  mode = "search"
  SEARCH_QUERY = extract_query(args)
  GOTO Step 0.2 (Search Mode)
ELIF args contain "--list":
  mode = "list"
  CATEGORY_FILTER = args.get("--category", null)
  GOTO Step 0.3 (List Mode)
ELSE:
  mode = "new"
  TOPIC = extract_topic(args)
```

### Step 0.2: Search Mode Branch [CONDITIONAL]

**Triggered by:** `--search query`

```
Read(".claude/skills/spec-driven-research/references/search-list-modes.md")
```

Follow search mode procedure from reference file. After displaying results, EXIT skill. No further phases execute.

### Step 0.3: List Mode Branch [CONDITIONAL]

**Triggered by:** `--list` or `--category type`

```
Read(".claude/skills/spec-driven-research/references/search-list-modes.md")
```

Follow list mode procedure from reference file. After displaying table, EXIT skill. No further phases execute.

### Step 0.4: Resume Detection

```
IF mode == "resume":
  # Derive state from the CLI-managed research phase-state (single source of truth).
  Run: devforgeai-validate phase-status ${RESUME_ID} --workflow=research --project-root=. --format=json
  IF the command exits 0 (CLI state file exists):
    Parse the JSON; set CURRENT_PHASE from its `current_phase` field
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    # Resume by loading existing research doc
    research_files = Glob(pattern=f"devforgeai/specs/research/{RESUME_ID}-*.research.md")
    IF research_files found:
      Read the research document
      RESEARCH_ID = RESUME_ID
      mode = "expand"
      Continue to Step 0.5
    ELSE:
      HALT -- "Research {RESUME_ID} not found"

# Check for an existing in-progress research workflow (new mode) via the CLI research state.
existing_states = Glob(pattern="devforgeai/workflows/RESEARCH-*-research-phase-state.json")
FOR each state file, read its progression via: devforgeai-validate phase-status <RESEARCH_ID> --workflow=research --format=json
IF any research workflow is not yet complete (phase 06 missing or not checkpoint-passed):
  AskUserQuestion:
    Question: "Found existing research session in progress. Resume or start fresh?"
    Header: "Resume"
    Options:
      - label: "Resume session"
        description: "Continue from last checkpoint"
      - label: "Start fresh"
        description: "Begin new research session"
  IF "Resume": set CURRENT_PHASE from that workflow's phase-status `current_phase`, GOTO Phase Orchestration Loop at CURRENT_PHASE
```

### Step 0.5: Generate Research ID

```
existing_files = Glob("devforgeai/specs/research/RESEARCH-*.research.md")

# Extract IDs (gap-aware)
ids = []
FOR each file in existing_files:
  match = regex("RESEARCH-(\d{3})", basename(file))
  IF match: ids.append(int(match.group(1)))

next_id = max(ids) + 1 IF ids ELSE 1
RESEARCH_ID = f"RESEARCH-{next_id:03d}"
```

### Step 0.6: CLI Initialization

```bash
devforgeai-validate phase-init ${RESEARCH_ID} --workflow=research --project-root=. 2>&1
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${RESEARCH_ID} --workflow=research` to get CURRENT_PHASE. |
| 2 | Invalid ID | HALT. Must match RESEARCH-NNN pattern. |
| 127 | CLI not installed | Continue without CLI enforcement (backward compatibility). |

### Step 0.7: Confirm CLI Phase State

`devforgeai-validate phase-init` (Step 0.6) already created and now owns the authoritative
phase state at `devforgeai/workflows/${RESEARCH_ID}-research-phase-state.json`. The skill does
not write a separate hand-maintained checkpoint — phase progression is recorded exclusively
through the `phase-record` / `phase-complete` CLI calls in each phase's Exit Gate, and read
back via `phase-status --workflow=research --format=json`.

**VERIFY:** `devforgeai-validate phase-status ${RESEARCH_ID} --workflow=research --project-root=. --format=json` exits 0.

### Step 0.8: Display Session Banner

```
Display:
"------------------------------------------------------------
  DevForgeAI Research Session
------------------------------------------------------------

Research ID: ${RESEARCH_ID}
Mode: ${mode}
Topic: ${TOPIC || 'To be defined in Phase 01'}

Phases: 7 (Initialization > Topic Definition > Research Execution > Findings Synthesis > Documentation > Cross-Reference > Completion)
------------------------------------------------------------"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 7):  # Phases 01-06

    1. ENTRY GATE: devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from={prev} --to={phase_id} --project-root=.
       IF exit != 0 AND exit != 127: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-research/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT rely on memory of previous reads.

    3. REFERENCE: Read the phase's reference files as specified in the phase Contract section.
       References are in references/ (self-contained within this skill).

    4. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.

    5. EXIT GATE: devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0 AND exit != 127: HALT
       (phase-complete records phase completion in the CLI-managed research state — no
        separate checkpoint file is written.)
```

---

## Phase Table

| Phase | Name | File | Steps | Required Subagents |
|-------|------|------|-------|--------------------|
| 00 | Initialization | (inline above) | 8 | none |
| 01 | Topic Definition | `phases/phase-01-topic-definition.md` | 4 | none |
| 02 | Research Execution | `phases/phase-02-research-execution.md` | 3 | internet-sleuth (BLOCKING) |
| 03 | Findings Synthesis | `phases/phase-03-findings-synthesis.md` | 4 | none |
| 04 | Documentation | `phases/phase-04-documentation.md` | 5 | none |
| 05 | Cross-Reference | `phases/phase-05-cross-reference.md` | 2 | none |
| 06 | Completion Summary | `phases/phase-06-completion-summary.md` | 2 | none |

---

## Required Subagents Per Phase

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 02 | internet-sleuth | BLOCKING - Must invoke via Task() and use output. Fallback to direct WebSearch/WebFetch if unavailable. |

**All other phases:** No subagents required. Direct tool calls (Read, Write, Glob, Grep, AskUserQuestion, WebSearch, WebFetch).

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Workflow Completion Validation

```
# Derive completion from the CLI-managed research state — the single source of truth.
status_json = devforgeai-validate phase-status ${RESEARCH_ID} --workflow=research --project-root=. --format=json
completed_count = count of phases in {01..06} whose status == "completed" AND checkpoint_passed == true
IF completed_count < 6:
    HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases completed"
IF completed_count == 6:
    Display "All 6 phases completed - Workflow validation passed"
```

---

## Success Criteria

Complete research generated with:
- [ ] Valid research ID (RESEARCH-NNN format)
- [ ] Research topic defined with category
- [ ] Research questions captured
- [ ] Findings with evidence and citations
- [ ] Recommendations ranked by priority
- [ ] Sources with credibility assessment
- [ ] Research document written to devforgeai/specs/research/
- [ ] Research index updated
- [ ] Cross-references created (if applicable)
- [ ] Checkpoint updated to "completed"

---

## Reference Files Inventory

Load these on-demand during workflow execution:

### Phase Files (7 files in `phases/`)

| Phase File | Primary Reference (in `references/`) | Additional References |
|------------|--------------------------------------|----------------------|
| `phase-01-topic-definition.md` | `parameter-extraction.md` | -- |
| `phase-02-research-execution.md` | `internet-sleuth-delegation.md` | `search-strategies.md` |
| `phase-03-findings-synthesis.md` | `citation-standards.md` | -- |
| `phase-04-documentation.md` | `research-workflow.md` | -- |
| `phase-05-cross-reference.md` | (self-contained) | -- |
| `phase-06-completion-summary.md` | (self-contained) | -- |

### Reference Files (6 files in `references/`)
- **parameter-extraction.md** - Argument parsing, category code mapping
- **research-workflow.md** - Core workflow patterns, ID generation, slug generation, frontmatter schema
- **citation-standards.md** - Source citing formats, evidence quoting, confidence levels
- **search-strategies.md** - Fallback search strategies by category, search optimization tips
- **internet-sleuth-delegation.md** - Subagent contract, category-to-mode mapping, Task() template
- **search-list-modes.md** - Search and list mode handling (conditional branches in Phase 00)

### Assets (2 templates in `assets/templates/`)
- **research-template.md** - Research document template (YAML + markdown)
- **sleuth-report-template.md** - Internet-sleuth 9-section report template with YAML frontmatter (absorbed from internet-sleuth-integration per ADR-045)

### Sleuth Methodology References (5 files in `references/sleuth-methodology/`)
- **research-principles.md** - Core research principles, evidence standards, framework integration (always loaded by internet-sleuth)
- **discovery-mode-methodology.md** - Discovery mode workflow: feasibility assessment, alternatives identification (conditional)
- **repository-archaeology-guide.md** - GitHub mining: search strategy, quality scoring, pattern extraction (conditional)
- **competitive-analysis-patterns.md** - Market analysis: SWOT, positioning maps, pricing analysis (conditional)
- **skill-coordination-patterns.md** - Task invocation patterns for internet-sleuth coordination by other skills

**Note:** Sleuth methodology files absorbed from `internet-sleuth-integration` per ADR-045. Loaded by the `internet-sleuth` subagent via progressive disclosure.

**Total:** 7 phase files + 6 reference files + 5 sleuth methodology files + 2 templates = 20 files + SKILL.md = 21 files

---

## Best Practices

1. **Provide clear research topic** - Specific topics yield better research than broad ones
2. **Select accurate category** - Category determines research strategy and internet-sleuth mode
3. **Define research questions upfront** - Questions guide the research focus
4. **Review findings for accuracy** - AI research requires human verification
5. **Link to epics/ADRs when relevant** - Bidirectional traceability strengthens the knowledge base

**See phase-specific reference files for detailed procedures.**
