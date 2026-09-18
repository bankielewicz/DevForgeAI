---
name: spec-driven-system-architecture
description: >
  Produces the System Architecture Document and the constitutional context files
  for a project through a spec-driven workflow with structural anti-skip enforcement.
  This skill is the macro/constitutional architect phase: it consumes the Project
  Management plan, locks the technology stack, defines system boundaries and
  integration topology, and emits the immutable context files plus ADRs. Use when
  the user runs /create-system-architecture or after the PM (/ideate) phase
  completes. Do NOT use for per-epic technical design (use
  spec-driven-solution-architecture).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(git:*)
  - Bash(devforgeai-validate:*)
  - Bash(gh:*)
  - Skill
model: opus
effort: High
version: "1.0.0"
last-updated: "2026-05-18"
topics: system architecture, context files, constitution, tech stack, ADR, integration topology, deployment, anti-skip
---

# Spec-Driven System Architecture

Translate the Project Management plan into the project **constitution** — the 6
immutable context files, their `.ai.md` companions, `test-plan.ai.yaml`, the
architecturally significant ADRs — and a **System Architecture Document** describing
system boundaries, integration topology, tech-stack rationale, system NFRs, and
deployment architecture. Governed by **ADR-067**.

This skill owns the **System Architect** role: the macro / constitutional phase of
the modernized DevForgeAI pipeline.

```
/brainstorm (BA) → /ideate (PM) → /create-system-architecture (THIS SKILL)
  → /create-solution-architecture (per-epic technical design)
```

**Input contract:** `ideation-output.schema.json` v1.0 — the PM plan, carried in the
YAML frontmatter of `devforgeai/specs/requirements/{project}-requirements.md`.
**Output contract:** `system-architecture-output.schema.json` v1.0 — emitted as a
self-contained HTML document with an embedded JSON data island
(`<script type="application/json" id="system-architecture-data">`).

**Context files are THE LAW.** If ambiguous or conflicts detected: HALT and use
AskUserQuestion.

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

Layer 4 (CLI phase-gate) **is wired** for this workflow as of gh#280: the `system-architecture` schema is registered in `phase_state.py` `WORKFLOW_SCHEMAS`, and Phase 00 + every phase file call `phase-init` / `phase-check` / `phase-record` / `phase-complete`. Step- and subagent-count enforcement stays deferred (empty `steps_required` / `subagents_required`, per the ADR-110 / ADR-073 precedent); the active enforcers are the boundary gate (`pre-phase-complete-boundary-check.sh`, PreToolUse exit 2 when a phase file was never `Read()` — ADR-132; `phase-entry-validator.sh` is now PostToolUse telemetry) and the phase-03 reference-manifest gate (`pre-phase-record-reference-check.sh`).

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$PROJECT_NAME` | `/create-system-architecture` argument, or the PM plan `project` field | Current directory name |
| `$PM_PLAN_PATH` | `--pm-plan=<path>` argument | null → auto-detect in Phase 01 |
| `$RESUME_ID` | `--resume SYSARCH-NNN` argument | null (new session) |
| `$MODE` | Derived from above | "new" or "resume" |

---

## Phase 00: Initialization [INLINE — Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF conversation contains "--resume SYSARCH-":
  Extract SYSARCH_ID from argument
  MODE = "resume"
ELSE:
  MODE = "new"
  PM_PLAN_PATH = extracted value of --pm-plan=<path>, or null
  PROJECT_NAME = extracted value, or current directory name
```

### Step 0.2: Handle Resume Mode

```
IF MODE == "resume":
  checkpoint_path = "devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json"
  Glob(pattern=checkpoint_path)
  IF found:
    Read(file_path=checkpoint_path)
    CURRENT_PHASE = checkpoint.progress.current_phase
    Display: "Resuming ${SYSARCH_ID} from Phase ${CURRENT_PHASE}"
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    Display: "No checkpoint found for ${SYSARCH_ID}."
    AskUserQuestion: start new vs. abort
```

### Step 0.3: Generate System Architecture ID (New Session)

```
IF MODE == "new":
  Glob(pattern="devforgeai/specs/architecture/SYSARCH-*.system-architecture.html")
  Glob(pattern="devforgeai/workflows/SYSARCH-*-sysarch-checkpoint.json")
  SYSARCH_ID = "SYSARCH-{NNN+1}"   # zero-padded to 3 digits minimum
```

The `SYSARCH-NNN` id satisfies the `^SYSARCH-[0-9]{3,}$` pattern in
`system-architecture-output.schema.json`.

### Step 0.4: Create Checkpoint File

```
checkpoint = {
  "checkpoint_version": "1.0",
  "sysarch_id": SYSARCH_ID,
  "project_name": PROJECT_NAME,
  "pm_plan_path": PM_PLAN_PATH,
  "created_at": "<ISO 8601 timestamp>",
  "progress": { "current_phase": 1, "phases_completed": [], "total_phases": 7 },
  "phases": {
    "01": {"status": "pending"}, "02": {"status": "pending"},
    "03": {"status": "pending"}, "04": {"status": "pending"},
    "05": {"status": "pending"}, "06": {"status": "pending"},
    "07": {"status": "pending"}
  }
}

Write(file_path="devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json",
      content=JSON.stringify(checkpoint))
```

**VERIFY:** `Glob(pattern="devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json")`
returns exactly 1 file. IF not found: HALT — "Initial checkpoint was NOT created."

### Step 0.4b: Initialize CLI Phase-State (gh#280)

```bash
devforgeai-validate phase-init ${SYSARCH_ID} --workflow=system-architecture --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase-state initialized — proceed |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — phase-state could not be initialized |

This writes `devforgeai/workflows/${SYSARCH_ID}-system-architecture-phase-state.json`,
which **coexists** with the skill's own `${SYSARCH_ID}-sysarch-checkpoint.json` (Step
0.4) — the CLI file backs the boundary/reference hooks; the checkpoint backs resume.
Do NOT unify or migrate them.

### Step 0.4c: VCS-Posture Check

EXECUTE:
1. Run `git rev-parse --is-inside-work-tree 2>/dev/null` to determine VCS posture.
2. **No git repository (exit non-zero):**
   - `AskUserQuestion`: "No git repository detected. This workflow will write the immutable constitution, ADRs, and CLAUDE.md amendments with NO version control and NO rollback path. How would you like to proceed?" Options: "Initialize git first (recommended — `git init && git add -A && git commit -m 'init'`)" / "Proceed irreversibly (I accept that no rollback path exists)"
   - If user selects "Initialize git first": HALT — do not proceed until git is initialized and the skill is re-run.
   - If user selects "Proceed irreversibly": record `vcs_posture: {git: false, user_acknowledged: true}` in the checkpoint (see RECORD block below) and continue.
3. **Git repository present (exit 0):**
   - `Task(subagent_type="git-validator", ...)` for full status (dirty files, uncommitted changes, branch, remote reachability).
   - If uncommitted changes exist: surface the file list to the user before the question.
   - **Worktree isolation is now handled natively by the WorktreeCreate hook (Issue #725).** When you launch Claude Code with `claude --worktree <name>`, the hook automatically creates an isolated worktree, writes a `.devforgeai-worktree` identity marker and `.devforgeai-claim` lease, and locks the worktree. No manual worktree setup is needed. Record the isolation mode in the checkpoint (see RECORD block below).
   - If the user did NOT launch with `--worktree`, record `user_choice: "in-place"` and continue in the main checkout. The active-workflow gate (`worktree-identity-guard.sh`) remains the floor for non-worktree sessions (AC-9).

RECORD (Step 0.4c — checkpoint update): read the existing checkpoint, merge `vcs_posture`, and write it back:

```
checkpoint["vcs_posture"] = {
  "git": <true|false>,
  "user_acknowledged": <true — no-git path only, omit on git path>,
  "worktree_offered": <true — git path only, omit on no-git path>,
  "user_choice": <"isolate"|"in-place" — git path only, omit on no-git path>
}
Write(file_path="devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json",
      content=JSON.stringify(checkpoint))
```

VERIFY: `Read(file_path="devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json")` — confirm `vcs_posture` key is present. If missing: HALT — checkpoint was not updated.

### Step 0.4d: Remote-Posture Check (first-publish)

Runs only when Step 0.4c confirms a git repository is present (`vcs_posture.git == true`).
Skip entirely when `vcs_posture.git == false`.

EXECUTE:
1. **Detect remote posture:**
   - `git remote get-url origin 2>/dev/null` → capture the remote URL (empty = no remote configured).
   - If URL is non-empty: `git fetch origin --no-tags 2>/dev/null`; then `git ls-remote --heads origin 2>/dev/null` → capture remote branch list and populate remote-tracking refs.
2. **Classify (evaluate in order — first match wins):**
   - `collision` — `origin` exists, `git ls-remote --heads origin` is non-empty, AND `git merge-base --is-ancestor HEAD origin/<current-branch> 2>/dev/null` exits non-zero (no common ancestor). → **HALT**: `AskUserQuestion`: "Remote repository is non-empty and shares no common history with this local branch. Automatic publish is blocked to prevent data loss. Please resolve this manually." Options: "I will resolve manually — re-run after reconciling" / "Skip first-publish for now (record as skipped)". Never force-push.
   - `published` — `origin` exists AND `git ls-remote --heads origin` is non-empty (and not collision). Record `remote_posture.status = "published"` and skip — no push.
   - `greenfield-unpublished` — `origin` is absent OR `origin` exists but `git ls-remote --heads origin` is empty. → Offer publish (Step 3).
3. **Publish (greenfield-unpublished only) — gated by AskUserQuestion:**
   - `AskUserQuestion`: "No remote is configured (or the remote is empty). Publish the initial commit now?" Options: "Publish now (recommended)" / "Skip — I will publish later"
   - If **Skip**: record `remote_posture.status = "skipped"` and continue.
   - If **Publish now** and **origin absent** (no remote at all):
     - `AskUserQuestion`: "Enter the GitHub repository name (format: `<owner>/<name>`, will be created private):" → capture `<owner>/<name>`.
     - Execute: `gh repo create <owner>/<name> --private --source=. --remote=origin --push`
     - Verify: `git remote get-url origin` is non-empty AND `git ls-remote --heads origin` is non-empty.
     - Record: `remote_posture.status = "greenfield-unpublished-pushed"`.
   - If **Publish now** and **origin configured but empty** (remote exists, no branches):
     - Execute: `git push -u origin <current-branch>`; then `git remote set-head origin -a`
     - Verify: `git ls-remote --heads origin` is non-empty AND `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null` resolves.
     - Record: `remote_posture.status = "greenfield-unpublished-pushed"`.
4. **Idempotency:** `published` status → record only; no push.

RECORD (Step 0.4d — checkpoint update): read the existing checkpoint, merge `remote_posture`, and write it back:

```
checkpoint["remote_posture"] = {
  "status": <"published"|"greenfield-unpublished-pushed"|"collision"|"skipped">,
  "origin_url": <URL string or null>,
  "published_at": <ISO 8601 UTC string or null — set only when a push is performed in this run>
}
Write(file_path="devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json",
      content=JSON.stringify(checkpoint))
```

VERIFY: `Read(file_path="devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json")` — confirm `remote_posture` key is present. If missing: HALT. For newly-pushed paths (`greenfield-unpublished-pushed`): `git ls-remote --heads origin` must be non-empty (confirms push succeeded). For `published` and `skipped` paths: checkpoint key presence is sufficient.

### Step 0.5: Display Initialization Banner

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI System Architecture Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session: ${SYSARCH_ID}
Mode: ${MODE}
Project: ${PROJECT_NAME}
Phases: 7 (PM Ingestion > Context Discovery > Context Files >
           ADR > System Design > Architecture Review > Document)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1. **GOTO Phase Orchestration Loop at Phase 01.**

---

## Phase Orchestration Loop

For each phase from CURRENT_PHASE to 7:

1. **LOAD PHASE:** `Read(file_path=".claude/skills/spec-driven-system-architecture/phases/{phase_file}")`
   — Read the phase file FRESH. Do NOT skip this step.
2. **LOAD REFERENCES:** Each phase file specifies which references to load from
   `.claude/skills/spec-driven-system-architecture/references/`. Load them ALL via
   `Read()`. Do NOT skip or summarize.
3. **EXECUTE STEPS:** Follow EVERY step's EXECUTE-VERIFY-RECORD triplet in the phase
   file, IN ORDER. Do NOT compress or skip steps.
4. **EXIT CRITERIA:** Verify ALL mandatory exit conditions listed in the phase file
   before proceeding.
5. **UPDATE CHECKPOINT:** Set `phases[phase_id].status = "completed"`, add to
   `phases_completed`, advance `current_phase`.
6. **VERIFY CHECKPOINT:** `Read()` the checkpoint — confirm the update persisted.
7. **DISPLAY TRANSITION:** Show phase completion and the next phase name.

---

## Phase Table

| Phase | Name | File | Subagents |
|-------|------|------|-----------|
| 01 | PM Plan Ingestion & Validation | `phases/phase-01-pm-plan-ingestion.md` | — |
| 02 | Context Discovery | `phases/phase-02-context-discovery.md` | **tech-stack-detector** (brownfield) |
| 03 | Constitutional Context Files | `phases/phase-03-constitutional-context-files.md` | **ai-rule-extractor** (×6), **test-plan-architect** |
| 04 | ADR Creation | `phases/phase-04-adr-creation.md` | — |
| 05 | System Design | `phases/phase-05-system-design.md` | — |
| 06 | Architecture Review | `phases/phase-06-architecture-review.md` | **alignment-auditor**, **architect-reviewer** (BLOCKING) |
| 07 | System Architecture Document | `phases/phase-07-system-architecture-document.md` | — |

No phase is conditional — all 7 run on every invocation.

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/${SYSARCH_ID}-sysarch-checkpoint.json`
- **Updated:** After every phase completion
- **Verified:** Via `Glob()` after every write
- **Resume:** Read checkpoint, set `CURRENT_PHASE` from `progress.current_phase`,
  resume loop

---

## Workflow Completion Validation

```
IF len(phases_completed) < 7:
    HALT "WORKFLOW INCOMPLETE — ${len(phases_completed)}/7 phases accounted for"

Verify: Glob("devforgeai/specs/context/*.md") returns >= 6 files
Verify: Glob("devforgeai/specs/context/*.ai.md") returns >= 6 files
Verify: Glob("devforgeai/specs/context/test-plan.ai.yaml") returns 1 file
Verify: Glob("devforgeai/specs/adrs/ADR-*.md") returns >= 1 new ADR
Verify: Glob("devforgeai/specs/architecture/${SYSARCH_ID}-*.system-architecture.html")
        returns the System Architecture Document
```

IF any verification fails: HALT and report the missing artifact.

---

## Success Criteria

- All 7 phases executed (no skipping)
- PM plan read from disk and validated against `ideation-output.schema.json` v1.0
  (Phase 01) — never consumed from conversation memory
- All 6 constitutional context files exist in `devforgeai/specs/context/`, with
  their 6 `.ai.md` companions and `test-plan.ai.yaml`
- At least 1 architecturally significant ADR created
- Architecture review passed (Phase 06, architect-reviewer BLOCKING)
- System Architecture Document on disk as self-contained HTML with a schema-valid
  JSON data island
- `handoff.recommended_approach` populated for `/create-solution-architecture`
- All ambiguities resolved via AskUserQuestion

---

## Deviation Protocol

If you need to deviate from ANY phase step:
1. HALT immediately
2. Use AskUserQuestion to explain the deviation and get user consent
3. Only proceed with explicit user approval
4. Record the deviation in the checkpoint under a `deviations` key

**Without user consent, no deviation is permitted.**
