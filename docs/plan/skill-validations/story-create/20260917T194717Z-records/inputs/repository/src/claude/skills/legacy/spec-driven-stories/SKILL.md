---
name: spec-driven-stories
description: >
  Create user stories with acceptance criteria, technical specifications, and UI
  specifications through an 8-phase workflow with structural anti-skip enforcement.
  Prevents token optimization bias through per-phase reference loading, checkpoint
  persistence, Execute-Verify-Record enforcement, and artifact verification. Use when
  transforming feature descriptions into structured stories, generating stories from
  epic features, or creating follow-up stories for deferred work. Supports CRUD,
  authentication, workflow, and reporting story types with complete technical and UI
  specifications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - Skill
  - Bash(devforgeai-validate:*)
model: opus
effort: High
version: "2.0.0"
last-updated: "2026-05-20"
topics: user stories, acceptance criteria, technical specification, UI specification, batch, DEVARCH seed, anti-skip
---

# Spec-Driven Stories

Produce a complete, implementation-ready user story file with acceptance criteria, technical specification, UI specification (when applicable), and Definition of Done — written to `devforgeai/specs/Stories/STORY-NNN.story.md`. The story-template schema is a load-bearing contract — every downstream skill (`/dev`, `/qa`, `/release`, `/fix-story`, `/validate-stories`, `backend-architect` Phase 2.5) consumes its output shape.

**Single-file design principle (NON-NEGOTIABLE):** one story = one file. Sidecars (`STORY-NNN-notes.md`, `STORY-NNN/spec.md`, etc.) are forbidden — enforced deterministically by `stories-sidecar-write-blocker.sh` (PreToolUse[Write|Edit]). All story metadata, ACs, tech spec, UI spec, and DoD live in `STORY-NNN.story.md`.

**Context files are THE LAW:** `tech-stack.md`, `source-tree/`, `dependencies.md`, `coding-standards.md`, `architecture-constraints.md`, `anti-patterns.md`. If ambiguous or conflicting — HALT and use AskUserQuestion.

---

**INLINE-skill contract:** the orchestrator executes phase steps directly (Read/Write/Edit/Glob/Grep/AskUserQuestion/Bash). Subagents are scoped to **content-only** or **read-only** roles — `story-requirements-analyst` (Phase 02, content-only per RCA-007), `api-designer` (Phase 03 conditional, content-only), `story-self-validator` (Phase 07, read-only findings JSON). The primary writes every file.

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

---

## Story Template

**Current Version:** v3.1 (`assets/templates/story-template.md`, loaded in Phase 05).

The template carries the authoritative `SECTION_MANIFEST` (HTML-comment-embedded YAML). Phase files derive structural constants (required sections, subsections, format_version) from the manifest via `devforgeai-validate parse-manifest` — never hardcoded.

**DEVARCH-seed fields** (v3.1, optional — populated when /create-story ingests a Development Architecture seed):
- `feature_ref` — F-NN matching the source Solution/Development Architecture
- `source_devarch` — relative path to the DEVARCH document

`backend-architect` Phase 2.5 strict-HALTs when `source_devarch` is required but empty (per ADR-067/068/069).

---

## When to Use This Skill

- User runs `/create-story [feature-description | EPIC-NNN | SEED-NNN | *.development-architecture.html | --from-recommendations=STORY-NNN]`
- `/create-stories-from-rca` decomposes RCA recommendations into stories
- `/create-missing-stories` batch-creates stories for coverage gaps (via `spec-driven-coverage` Phase 04)
- spec-driven-dev creates tracking stories for deferred DoD items
- Manual: `Skill(command="spec-driven-stories")`

**Do NOT use for:** epic creation (use spec-driven-lifecycle epic mode), sprint planning (use spec-driven-lifecycle sprint mode), modifying existing stories (use Edit on the story file directly).

---

## Modes

| Mode | Trigger | Phase 01 behavior |
|------|---------|-------------------|
| `SINGLE_STORY` | Free-form feature description | Interactive AskUserQuestion for metadata |
| `EPIC_BATCH` | EPIC-NNN argument from `/create-story` | Driven by context markers set by command + spec-driven-coverage |
| `FROM_RECOMMENDATIONS` | `--from-recommendations=STORY-NNN` | Drives Step R.1–R.8 in `story-discovery-from-recommendations.md` |
| `DEVARCH_SEED` | SEED-NNN or `*.development-architecture.html` argument | Phase 01 Sub-step 1.2.0 ingests + schema-validates the seed |

### Batch Mode (EPIC_BATCH)

Triggered when conversation contains `**Batch Mode:** true`. Required context markers: `Story ID`, `Epic ID`, `Feature Number`, `Feature Name`, `Feature Description`, `Priority`, `Points`, `Type`, `Sprint`, `Batch Mode`, `Batch Index`.

Behavior: Phase 01 skips interactive questions and extracts metadata from markers. Phases 02–07 run unchanged. Phase 08 skips the next-action AskUserQuestion and returns to the batch loop. If required markers are missing → fall back to interactive mode.

**Batch reference caching (RCA-049):** stable reference files are pre-loaded ONCE before the loop (`references/story-discovery-batch.md` Step 0.4.5) to reduce token pressure. This is the ONLY authorized batch token optimization. Per-story subagent invocations and dynamic files (epic/sprint modified by linking) are loaded fresh each iteration. Caching does NOT authorize skipping any Execute-Verify-Record triplet.

**Post-batch structural validation (RCA-049):** `references/story-discovery-batch.md` Step 0.7 validates every created story against the SECTION_MANIFEST after the loop — HALT gate if any story is missing required sections / component IDs / format_version.

---

## Parameter Extraction

Extract from conversation context markers set by the invoking command:

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$MODE` | `/create-story` | SINGLE_STORY / EPIC_BATCH / FROM_RECOMMENDATIONS |
| `$EPIC_ID` | `/create-story` | EPIC-NNN identifier |
| `$FEATURE_DESCRIPTION` | `/create-story` | Feature description, SEED-NNN, or path |
| `$STORY_ID` | batch mode | STORY-NNN identifier |
| `$FEATURE_NUMBER` | batch mode | Feature number (e.g., 1.1) |
| `$FEATURE_NAME` | batch mode | Feature name |
| `$PRIORITY` | batch mode | High/Medium/Low/Critical |
| `$POINTS` | batch mode | Story points (Fibonacci) |
| `$TYPE` | batch mode | feature/bugfix/refactor/documentation |
| `$SPRINT` | batch mode | Sprint-N identifier |
| `$BATCH_MODE` | batch mode | true/false |
| `$BATCH_INDEX` | batch mode | 0-based index |
| `$SOURCE_STORY_ID` | FROM_RECOMMENDATIONS | Source STORY-NNN |
| `$REC_IDS_FLAG` | FROM_RECOMMENDATIONS | Optional REC-A,REC-B filter |
| `$INCLUDE_BLOCKING` | FROM_RECOMMENDATIONS | true/false |
| `$SOURCE_RCA` | /create-stories-from-rca | RCA-NNN identifier (ADR-074) |
| `$SOURCE_RECOMMENDATION` | /create-stories-from-rca | REC-N identifier (ADR-074) |
| `$ADDRESSES_WHY` | /create-stories-from-rca | 5-Whys traceability line (ADR-074 Required tier) |
| `$EVIDENCE_FILES` | /create-stories-from-rca | Comma-separated evidence paths (ADR-074 Required tier) |
| `$TEST_SPECIFICATION` | /create-stories-from-rca | Markdown test table from RCA recommendation (ADR-074 Rendered tier) |
| `$CONDITIONAL` | /create-stories-from-rca | Conditional trigger object (ADR-074 Rendered tier) |

When invoked from `/create-stories-from-rca`, the 6 RCA-derived markers above populate frontmatter `rca_traceability` fields and an `<rca_origin>` XML element in the story's Provenance section (rendered in Phase 05). See ADR-074 + `.claude/skills/spec-driven-rca/references/recommendation-contract.md` for the contract.

---

## Phase 00: Initialization [INLINE — Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF context markers already set by /create-story (Mode, Epic ID, Next Session ID in conversation):
  Confirm: "Context from /create-story: MODE=${MODE}, EPIC_ID=${EPIC_ID}, SESSION_ID=${NEXT_SESSION_ID}"
  Skip 0.2-0.3 — preflight already handled resume + session ID
  GOTO Step 0.3a
ELSE:
  Extract markers from Parameter Extraction table; defaults: $MODE="SINGLE_STORY", $TYPE="feature", $BATCH_MODE=false
```

### Step 0.2: Resume Detection

**FROM_RECOMMENDATIONS early-exit** (story-preflight does not accept STORY-NNN args):

```
IF $MODE == "FROM_RECOMMENDATIONS":
  today = YYYY-MM-DD
  existing = Glob(pattern="devforgeai/workflows/checkpoints/SC-${today}-*.checkpoint.json")
  resumable = [cp for cp in existing if cp.mode == "FROM_RECOMMENDATIONS"
               and cp.source_story_id == $SOURCE_STORY_ID and cp.current_phase != "08"]
  IF resumable non-empty:
    AskUserQuestion: "Resume FROM_RECOMMENDATIONS session for ${SOURCE_STORY_ID}? Or start fresh?"
    IF resume → Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE
  GOTO Step 0.3
```

**Other modes:**

```
IF conversation contains resume_session from story-preflight:
  Read(resume_session.checkpoint_file)
  AskUserQuestion: "Resume session ${session_id}? Or start fresh?"
  IF resume → Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE
ELSE:
  Fallback (direct invocation, no command): Bash("devforgeai-validate story-preflight ${EPIC_ID} --project-root=. --format=json")
  Parse resume_session from JSON
```

### Step 0.3: Generate Session ID

**FROM_RECOMMENDATIONS** (filesystem scan):

```
IF $MODE == "FROM_RECOMMENDATIONS":
  existing = Glob("devforgeai/workflows/checkpoints/SC-${today}-*.checkpoint.json")
  SESSION_ID = "SC-${today}-001" if empty else f"SC-${today}-{max_seq+1:03d}"
  GOTO Step 0.3a
```

**Other modes:**

```
IF "**Next Session ID:**" marker present: SESSION_ID = marker value
ELSE: Bash("devforgeai-validate story-preflight ${EPIC_ID} --project-root=. --format=json"); parse next_session_id
GOTO Step 0.3a
```

### Step 0.3a: Optional Worktree Offer

Skip if git is unavailable in this environment (`git rev-parse --git-dir` exits non-zero →
set `$VCS_AVAILABLE=false`; proceed to Step 0.4).

**EXECUTE:**

1. VCS check: `git rev-parse --git-dir 2>/dev/null` — exit non-zero → `$VCS_AVAILABLE=false`; skip to Step 0.4.

2. Dispatch (report-only — does NOT create the worktree):
   ```
   Task(subagent_type="git-worktree-manager",
        prompt="Manage Git worktree for ${SESSION_ID}. Report action_needed ∈
        {CREATE, RESUME, REPAIR, NONE} and the suggested worktree path.")
   ```
   Bind `$WT_RESULT` (JSON response). Offer isolation when
   `action_needed ∈ {CREATE, RESUME, REPAIR}` or the working tree has uncommitted changes.

3. Offer isolation (when warranted):
   ```
   AskUserQuestion:
     Question: "Create a worktree to isolate this story session from concurrent
                /create-story or /qa runs?"
     Header: "Worktree isolation"
     Options:
       - "Create worktree now"        → create; bind $WORKTREE_PATH
       - "Continue on current branch" → record decline; $WORKTREE_PATH = ""
   ```

4. If user chose "Create worktree now":
   - Branch: `stories/${SESSION_ID}`
   - Path: `worktrees/${SESSION_ID}` (relative to repo root)
   - Create: `git worktree add worktrees/${SESSION_ID} -b stories/${SESSION_ID}`
   - Bind `$WORKTREE_PATH` to the absolute path of `worktrees/${SESSION_ID}`.
   - VERIFY: `git worktree list --porcelain` contains `$WORKTREE_PATH`. HALT on failure.

5. If user declined:
   Display: "Worktree isolation declined — running in current branch (no per-session worktree for this run)."
   Set `$WORKTREE_PATH = ""` (use main checkout).

NOTE: `phase-record` for `git-worktree-manager` is deferred to Step 0.4 (after
`phase-init` creates the state file that `phase-record` requires).

### Step 0.4: CLI Initialization

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=stories --project-root=${WORKTREE_PATH:-.} 2>&1
```

| Exit | Meaning | Action |
|------|---------|--------|
| 0 | New workflow | Set CURRENT_PHASE = "01"; proceed to 0.5 |
| 1 | Existing workflow | Resume: `devforgeai-validate phase-status` → CURRENT_PHASE |
| 2 | Invalid session ID | HALT — must match SC-YYYY-MM-DD-NNN |
| 127 | CLI not installed | Continue without CLI enforcement (backward compatibility) |

**RECORD** (git-worktree-manager from Step 0.3a, when `$VCS_AVAILABLE` is not `false`):
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=00 --subagent=git-worktree-manager --project-root=${WORKTREE_PATH:-.}
```

### Step 0.5: Display Session Banner

```
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Story Creation Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session: ${SESSION_ID}     Mode: ${MODE}
Epic:    ${EPIC_ID|'None'} Batch: ${BATCH_MODE}
Feature: ${FEATURE_DESCRIPTION|'None provided'}

Phases: 8 (Discovery → Requirements → Tech Spec → UI Spec → File Creation → Linking → Validation → Completion)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1. **GOTO Phase Orchestration Loop at Phase 01.**

---

## Phase Orchestration Loop

For each phase from CURRENT_PHASE to 8:

**Worktree-identity bypass:** When `$WORKTREE_PATH` is non-empty (worktree created in Step 0.3a), write `Write(file_path="${WORKTREE_PATH}/tmp/_worktree-identity-bypass.marker", content="")` immediately before each `phase-check` and `phase-complete` invocation — required by `worktree-identity-guard.sh` to allow cross-worktree state writes (single-use marker, consumed on bypass). See `.claude/rules/workflow/operational-safety.md` Rule 3.

1. **ENTRY GATE** — IF phase_id == "01": skip (phase-init IS the entry gate). ELSE: `devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from={prev} --to={phase_id} --project-root=${WORKTREE_PATH:-.}`. Exit ≠ 0 AND ≠ 127 → HALT.
2. **LOAD PHASE** — `Read(".claude/skills/spec-driven-stories/phases/{phase_files[phase_num]}")`. Load fresh.
3. **LOAD REFERENCES** — load the references listed in the phase's Contract section. All of them. Per-phase, not consolidated.
4. **EXECUTE** — follow every EXECUTE-VERIFY-RECORD triplet in the phase file, in order.
5. **EXIT GATE** — `devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase={phase_id} --checkpoint-passed --project-root=${WORKTREE_PATH:-.}`. Exit ≠ 0 AND ≠ 127 → HALT.
6. **CHECKPOINT** — update checkpoint JSON with phase completion; write to disk. Write() returns cleanly on success; trust the return value.

---

## Phase-Output Cache (Sprint 3)

Phases write per-phase JSON cache files to `tmp/${SESSION_ID}/phase-outputs/phase-NN.json` to share processed data without redundant disk reads or re-parsing. Schema: `contracts/phase-output-schema.json` (oneOf of 7 phase definitions, each carrying `schema_version` + `phase_id` discriminator constants).

**Cache-miss behavior:** readers ALWAYS fall through to fresh compute on missing file, schema_version mismatch, phase_id mismatch, or null payload. Cache miss is NEVER a HALT — the cache is a performance optimization, not a correctness requirement.

**POST-EPIC-EDIT RE-READ CAVEAT:** Phase 06.1 mutates the epic file via Edit(); Phase 07.2.5 (AC fidelity check) MUST re-read the epic from disk and ignore the cache.

---

## Phase Table

| Phase | Name | File | Subagents |
|-------|------|------|-----------|
| 00 | Initialization | (inline above) | — |
| 01 | Story Discovery & Context | `phases/phase-01-story-discovery.md` | — |
| 02 | Requirements Analysis | `phases/phase-02-requirements-analysis.md` | **story-requirements-analyst** (BLOCKING, content-only) |
| 03 | Technical Specification | `phases/phase-03-technical-specification.md` | api-designer (CONDITIONAL, content-only) |
| 04 | UI Specification | `phases/phase-04-ui-specification.md` | — |
| 05 | Story File Creation | `phases/phase-05-story-file-creation.md` | — |
| 06 | Epic/Sprint Linking | `phases/phase-06-epic-sprint-linking.md` | — |
| 07 | Self-Validation | `phases/phase-07-self-validation.md` | story-self-validator (BLOCKING, read-only findings) |
| 08 | Completion Report | `phases/phase-08-completion-report.md` | — |

**Subagent contracts** (loaded per-phase, not upfront):
- `contracts/requirements-analyst-contract.yaml` (Phase 02)
- `contracts/api-designer-contract.yaml` (Phase 03, conditional)
- `contracts/template-consumer-contract.yaml` — schema-authority relationship between `story-template.md` and consuming phase files. Phase files MUST derive structural constants from the manifest, never hardcode shadow copies (prevents RCA-048 drift).

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json`
- **References:** `references/` (self-contained within this skill)
- **Contracts:** `contracts/` (self-contained)
- **Templates:** `assets/templates/` (self-contained)
- **Scripts:** `scripts/` (self-contained)
- **Phase-output cache:** `tmp/${SESSION_ID}/phase-outputs/phase-NN.json`

---

## Integration Points

**Invoked by:** `/create-story`, `/create-stories-from-rca`, `spec-driven-coverage` Phase 04 (which is invoked by `/create-missing-stories`), `spec-driven-lifecycle` (epic/sprint decomposition), `spec-driven-dev` (deferred-work tracking).

**Provides output to:** `spec-driven-design` (AC → UI requirements), `spec-driven-dev` Phase 01 intake + `backend-architect` Phase 2.5 DEVARCH intake, `spec-driven-qa` (AC → validation targets).

See `references/integration-guide.md` for complete integration patterns.

---

## Workflow Completion Validation

```
completed_count = len(checkpoint.progress.phases_completed)
IF completed_count < 8: HALT "WORKFLOW INCOMPLETE — ${completed_count}/8 phases completed"
IF completed_count == 8: Display "All 8 phases completed"; update checkpoint.status = "completed"
```

---

## Success Criteria

- Story ID matches `STORY-\d+`
- User Story (As a / I want / So that — exactly one canonical block)
- ≥ 3 Acceptance Criteria (Given/When/Then)
- Technical specification (v2.0 YAML, components + business_rules + non_functional_requirements)
- UI specification (or explicit N/A)
- Non-functional requirements (measurable)
- Edge cases documented
- Definition of Done (checkboxes)
- Story file at `devforgeai/specs/Stories/${STORY_ID}.story.md` (single file — no sidecars)
- Epic/sprint files updated (if applicable)
- Self-validation passed (Phase 07 Checks 1–9 + story-self-validator findings)
- DEVARCH-seed fields populated (when seed was supplied)

---

## Reference Files Inventory

Loaded on-demand during workflow execution. The full inventory is documented in `references/integration-guide.md`; per-phase reference lists live in each `phases/phase-NN-*.md` Contract section. Categories:

- **Phase guides** (8) — one primary reference per phase
- **AC patterns** (4) — `acceptance-criteria-core.md`, `acceptance-criteria-domains.md`, `acceptance-criteria-refactor.md` (conditional), `acceptance-criteria-patterns.md`
- **Story discovery** (4) — `story-discovery.md`, `story-discovery-batch.md`, `story-discovery-interactive.md`, `story-discovery-from-recommendations.md`
- **Creation guides** (5) — requirements, technical-spec (×2), UI, story-file
- **Validation** (4) — story-validation-workflow, validation-checklists, context-validation, validator-traps
- **Structure & examples** (3) — story-structure-guide, story-examples, story-type-classification
- **Supporting** (5) — epic-sprint-linking, custody-chain-workflow, gap-to-story-conversion, batch-mode-configuration, completion-report
- **Schema** (3) — checkpoint-schema, contract-schema, template-version-validation
- **Workflow** (3) — error-handling, parameter-extraction, integration-guide
- **Patterns** (3) — fix-resolution-patterns, refactor-quality-checks, user-input-integration-guide

Total: 8 phase files + 30 references + 3 contracts + 1 template.

---

## Best Practices

1. **Provide a clear feature description** — minimum 10 words, specific WHO/WHAT.
2. **Associate with an epic when possible** — enables traceability + feature tracking.
3. **Ensure ACs are testable** — verifiable Given/When/Then, no vague metrics.
4. **Include UI specs for frontend work** — mockups prevent implementation ambiguity (or use design.md when present).
5. **Trust self-validation** — Phase 07 auto-corrects common issues; story-self-validator (Phase 07.2.5–7.3.7) catches RCA-050/FM-4/FM-5 patterns.
