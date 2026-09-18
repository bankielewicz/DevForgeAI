---
name: spec-driven-rca
description: >
  Unified root cause analysis with 4-layer anti-skip enforcement for both tactical
  (dev workflow diagnosis) and strategic (5 Whys RCA documents) modes. Tactical mode
  auto-triggers after 2-3 failed fix attempts during TDD, returning fix prescriptions.
  Strategic mode invoked via /rca command, producing self-contained RCA documents with
  5 Whys analysis, evidence collection, and actionable recommendations. Uses
  Execute-Verify-Record pattern at every step to prevent token optimization bias.
  Use this skill whenever root cause analysis is needed — after repeated test failures,
  integration failures, QA violations, framework breakdowns, workflow violations,
  or when the user runs /rca. Also use when the diagnosis-before-fix rule triggers
  after 3+ consecutive fix attempts on the same error.
metadata:
  author: DevForgeAI
  version: "2.1.0"
  category: quality-assurance
  agent-skills-spec-version: "1.0"
  last-updated: "2026-05-15"
  migrated-from: root-cause-diagnosis v1.0.0 + spec-driven-rca v1.0.0
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - AskUserQuestion
  - Task
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
model: opus
effort: High
---

# Spec-Driven RCA

Unified root cause analysis for the DevForgeAI framework. Operates in two modes:

- **Tactical:** Fast diagnosis during dev workflow after repeated fix failures. Returns fix prescriptions. (Phases 00-03)
- **Strategic:** Full 5 Whys RCA for framework breakdowns. Creates self-contained RCA documents. (Phases 00-02, 04-08)

**Core Principle:** Understanding WHY a failure occurred is mandatory before attempting HOW to fix it.

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

---

## Validation Modes

This skill operates in two modes, determined during Phase 00 Initialization. Context-marker extraction and mode-detection priority live in `references/parameter-extraction.md`.

| Mode | When | Phase Route | Output |
|---|---|---|---|
| **Tactical** | Auto-triggered after 3+ failed fix attempts (diagnosis-before-fix rule). Detected via `**Mode:** tactical` or `**Fix Attempts:**` context markers set by /dev. | `00 → 01 → 02 → 03 → END` | Fix prescription emitted to `tmp/${STORY_ID}/rca-prescription.json` for /dev to consume on retry (ADR-074). |
| **Strategic** | Invoked via `/rca` command. Detected via `**Mode:** strategic`, `**Issue Description:**`, or `**Command:** rca` markers — or default when no tactical markers present. | `00 → 01 → 02 → 04 → 05 → 06 → 07 → 08 → END` | Self-contained RCA document at `devforgeai/RCA/RCA-{NNN}-{slug}.md`. Phase 08 prompts to invoke `github-incident-from-rca`. |

If no markers are present after `/rca` invocation, Phase 00 Step 00.3 disambiguates via AskUserQuestion. The slimmed `/rca` command sets no context markers itself — the skill derives the issue description from the user's invocation text via `references/parameter-extraction.md`.

---

## Phase State Initialization [MANDATORY FIRST]

Derive SESSION_ID **and the workflow key** from mode and context. The workflow key
selects the phase-state schema: tactical is linear `00→01→02→03`; strategic genuinely
skips phase 03 (`00→01→02→04→05→06→07→08`) and is registered as its own key so the
shared sequential gate (`to_idx == from_idx+1`) makes `02→04` legal by construction
(OBS-1). The ENTIRE run — every `phase-init` / `phase-check` / `phase-record` /
`phase-complete` call, in this file AND in every phase file — uses `--workflow=${WORKFLOW}`
(one state file per `${SESSION_ID}-${WORKFLOW}`), never a literal:

```
IF MODE == tactical:
    SESSION_ID = "DIAG-" + STORY_ID    # Example: "DIAG-STORY-127"
    WORKFLOW   = "rca"                  # linear: 00→01→02→03
ELIF MODE == strategic:
    SESSION_ID = "RCA-" + rca_number    # Example: "RCA-031"
    WORKFLOW   = "rca-strategic"        # skips 03: 00→01→02→04→05→06→07→08
```

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=${WORKFLOW} --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "00". |
| 1 | Existing workflow | Resume. Check checkpoint file for CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Verify parameters. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Resume Detection:** If resuming, read checkpoint:
```
Read(file_path="{project-root}/tmp/.rca-checkpoint-${SESSION_ID}.yaml")
```
Extract `current_phase` and `phase_completion` to determine where to resume. In addition to
reading `current_phase` from this yaml checkpoint,
**rehydrate `composition_state` from `tmp/.rca-composition-${SESSION_ID}.json`** when that
file exists — it is the authoritative
latest merged state (strategic mode, composition phases 04-07). The yaml checkpoint still
supplies `current_phase`.

---

## Phase Orchestration Loop

```
FOR phase_num in ACTIVE_PHASES:
    phase_id = format(phase_num, "02d")

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=${WORKFLOW} --from={prev} --to={phase_id}
       IF exit != 0: HALT

    2. EXECUTE PHASE:
       IF phase_id in {"04", "05", "06", "07"}:
           # Strategic-mode composition phase — delegate to the rca-document-composer
           # subagent (OPP-8). Do NOT Read/execute the phase file inline here.
           # See "Composition Phase Delegation (Phases 04-07)" below for the contract.
           Task(subagent_type="rca-document-composer",
                description="Compose RCA phase {phase_id}",
                prompt=<rendered per Composition Phase Delegation contract>)
           Parse the returned JSON envelope.
           IF envelope.status != "OK": HALT with envelope.error
           # Per-phase composition checkpoint (strategic only; phases 04, 05, 06, 07).
           # After EACH composition phase returns, the primary:
           #   (1) MERGES the returned envelope over the prior checkpoint at
           #       top-level-key granularity: the envelope wins on key conflicts, and
           #       any top-level key present in the previous checkpoint but
           #       absent from the returned envelope is restored from the previous checkpoint.
           #   (2) Writes the merged state ATOMICALLY (write to a `.tmp` sibling, then rename)
           #       to `tmp/.rca-composition-${SESSION_ID}.json` (project-scoped per
           #       operational-safety Rule 2).
           #   (3) Carries the merged `composition_state` (never the raw return envelope)
           #       into the next phase.
           composition_state = merge_checkpoint(composition_state, envelope.composition_state)
           write_atomic("tmp/.rca-composition-${SESSION_ID}.json", composition_state)  # .tmp sibling then rename
       ELSE:
           LOAD:    Read(file_path=".claude/skills/spec-driven-rca/phases/{phase_files[phase_id]}")
           EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
                    - Each step's EXECUTE instruction tells you exactly what to do
                    - Each step's VERIFY instruction tells you how to confirm it happened
                    - Each step's RECORD instruction tells you what CLI command to call
                    - The per-step `phase-record --step` calls are run here, inline.

    3. RECORD PHASE:
       IF phase_id in {"04", "05", "06", "07"}:
           # Composition phase: the subagent already ran every per-step
           # `phase-record --step=NN.M` call inside the phase file. The primary
           # records the delegation itself (--subagent satisfies the CLI, which
           # rejects a bare --phase with neither --step nor --subagent):
           devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase={phase_id} --subagent=rca-document-composer
       ELSE:
           # Inline phase: each step recorded itself via its own `--step` call
           # during EXECUTE (loop step 2). No additional phase-level record.

    4. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=${WORKFLOW} --phase={phase_id} --checkpoint-passed
       IF exit != 0: HALT
```

---

## Composition Phase Delegation (Phases 04-07)

In **strategic mode**, the four composition phases — 04 (evidence organization), 05 (recommendation generation), 06 (document creation), 07 (validation) — are delegated to the `rca-document-composer` subagent (OPP-8). Phases 00, 01, 02, 03, 08 run inline in this session; the `diagnostic-analyst` delegation in Phase 02 is unchanged. Tactical mode never reaches phases 04-07, so this section does not apply to it.

The phase files `phases/phase-0{4,5,6,7}-*.md` remain the **single source of truth** — the subagent `Read()`s and executes them. This skill does not duplicate their steps.

**Responsibility split:**

| Concern | Owner |
|---------|-------|
| `phase-check` entry gate, `phase-complete` exit gate (loop steps 1, 4) | primary |
| Delegation record `phase-record --phase=NN --subagent=rca-document-composer` (loop step 3) | primary |
| Per-step `phase-record --step=NN.M` calls written in the phase file | rca-document-composer |
| Reading the phase file + executing its EXECUTE-VERIFY-RECORD steps | rca-document-composer |
| Writing / self-healing the RCA document | rca-document-composer |
| Phases 00/01/02/03 and Phase 08 (completion + pipeline) | primary |

**composition_state** — the accumulating object passed phase-to-phase. Before the loop reaches phase 04, seed it from phases 00/01/02:

```
composition_state = {
    rca_meta:           { number, title, date, reporter, component, severity },   # Phase 00
    issue:              { description, statement },                                # Phase 00/01
    five_whys:          [ {n, question, answer, evidence}, ... 5 entries ],         # Phase 02
    files_examined:     [ {path, lines, finding, excerpt, significance, supports_why}, ... ],  # Phase 01
    related_rcas:       [ {number, title, relationship}, ... ],                     # Phase 01
    diagnostic_analyst: <Phase 02 diagnostic-analyst output, passed through verbatim>,  # informational
    routing:            { involves_workflow, touches_code, touches_rust }           # derived from issue + 5 Whys
}
```

Each delegated phase returns `composition_state` augmented with its output (04 → `evidence`, 05 → `recommendations`, 06 → `document_path`, 07 → `validation_verdict`). Merge the returned object over the prior checkpoint per the checkpoint contract above, then pass the merged `composition_state` into the next phase's Task call. After phase 07, hand the final merged `composition_state` to Phase 08.

> **Durability of `composition_state` (OBS-3).** `composition_state` is **checkpointed by the
> primary after every composition phase** to `tmp/.rca-composition-${SESSION_ID}.json` with
> merge-restore semantics (merge the returned envelope over the prior checkpoint at
> top-level-key granularity; **write to a `.tmp` sibling, then rename**). A finding therefore
> becomes **durable at each composition-phase boundary** — not only once phase 06 renders the
> RCA document. **Honest caveat:** durability is **per-phase** — a crash MID-phase loses only
> that phase's in-flight augmentation (the last checkpoint, written at the previous phase
> boundary, survives). A downstream phase whose return envelope **omits** a carried top-level
> key **no longer loses it**: the merge restores that key from the previous checkpoint
> (any top-level key present in the previous checkpoint but absent from the returned envelope
> is restored from the previous checkpoint). On resume, `composition_state` is rehydrated from
> this checkpoint file when it exists.

**Task prompt template** (loop step 2, composition branch):

When building this prompt the primary MUST **serialize the merged `composition_state`** —
the latest checkpoint content (`tmp/.rca-composition-${SESSION_ID}.json`), never the raw
return envelope of any single phase — into the prompt. This is the channel that carries
restored top-level keys (e.g. a finding a prior phase's envelope omitted) into phase 06's
document.

```
Task(subagent_type="rca-document-composer",
     description="Compose RCA phase {phase_id}",
     prompt="""
PHASE: {phase_id}
SESSION_ID: {SESSION_ID}
WORKFLOW: {WORKFLOW}        # always "rca-strategic" (composition phases are strategic-only)
composition_state:
{merged composition_state (latest checkpoint) serialized as JSON}

Execute phase {phase_id} per your agent contract: read the phase file, run every
EXECUTE-VERIFY-RECORD step, run the per-step phase-record CLI calls (with
--workflow=${WORKFLOW}), and return the augmented composition_state JSON envelope.
""")
```

On `envelope.status == "BLOCKED"`: HALT and surface `envelope.error`. Do NOT retry blind, and do NOT fall back to inline composition — inline fallback would skip the subagent contract and desync the phase-record step registry.

---

## Phase Index

| Phase | Name | Tactical | Strategic | File | Required Subagents |
|-------|------|----------|-----------|------|--------------------|
| 00 | Initialization | Yes | Yes | `phases/phase-00-initialization.md` | None |
| 01 | Capture | Yes | Yes | `phases/phase-01-capture.md` | None |
| 02 | Investigation | Yes | Yes | `phases/phase-02-investigation.md` | diagnostic-analyst |
| 03 | Prescription | Yes | No | `phases/phase-03-prescription.md` | None |
| 04 | Evidence Organization | No | Yes | `phases/phase-04-evidence-organization.md` | rca-document-composer |
| 05 | Recommendation Generation | No | Yes | `phases/phase-05-recommendation-generation.md` | rca-document-composer |
| 06 | RCA Document Creation | No | Yes | `phases/phase-06-document-creation.md` | rca-document-composer |
| 07 | Validation & Self-Check | No | Yes | `phases/phase-07-validation.md` | rca-document-composer |
| 08 | Completion & Pipeline | No | Yes | `phases/phase-08-completion.md` | None |

---

## HALT: NO FIX ATTEMPTS UNTIL Phase 02 COMPLETES

This is a blocking requirement for BOTH modes. Any code changes, edits, or operations targeting production or test files are FORBIDDEN until the investigation phase produces a report. Violation of this rule constitutes shotgun debugging and invalidates the diagnosis.

If prior fix attempts >= 3 without completing Phase 02, escalate to user:
```
AskUserQuestion: "{count} fix attempts have failed without diagnosis.
Systematic investigation is required. Proceed with full diagnosis? [Y/n]"
```

---

## Escalation Protocol (Tactical Mode)

### 3-Attempt Escalation Rule

| Attempt | Action |
|---------|--------|
| 1-2 | Normal fix-test cycle (no diagnosis needed) |
| 3 | HALT. Invoke full spec-driven-rca skill in tactical mode |
| 4 | If diagnosis prescription fails, try next hypothesis |
| 5 | HALT. Escalate to user via AskUserQuestion |

### Escalation Message Template

After attempt 5 (or after all hypotheses exhausted):
```
AskUserQuestion: "Persistent failure after diagnosis and {N} fix attempts.

Error: {error_message}
Diagnosis: {top_hypothesis}
Attempts: {fix_attempt_count}

Options:
1. Provide additional context or hints
2. Skip this acceptance criterion (requires justification)
3. Pause and investigate manually"
```

---

## State Persistence

**Phase State:** `devforgeai/workflows/${SESSION_ID}-${WORKFLOW}-phase-state.json` (tactical: `…-rca-…`; strategic: `…-rca-strategic-…`)
**Session Memory:** `.claude/memory/sessions/${SESSION_ID}-rca-session.md`
**Checkpoint:** `{project-root}/tmp/.rca-checkpoint-${SESSION_ID}.yaml`
**Composition Checkpoint:** `tmp/.rca-composition-${SESSION_ID}.json` (strategic mode, composition phases 04-07; merged envelope; rehydrated on resume)

---

## Reference Files (Progressive Loading)

References are loaded on-demand by each phase. Do NOT pre-load all references.

| Phase | Reference File | Purpose |
|-------|---------------|---------|
| 00 | `references/parameter-extraction.md` | Context marker extraction for both modes |
| 01 (strategic) | `references/framework-integration-points.md` | Determine which files to read |
| 02 (tactical) | `references/investigation-patterns.md` | 6 failure category taxonomy |
| 02 (strategic) | `references/5-whys-methodology.md` | How to perform effective 5 Whys |
| 04 | `references/evidence-collection-guide.md` | Evidence quality criteria |
| 05 | `references/recommendation-framework.md` | Priority criteria, implementation details |
| 05 | `references/recommendation-contract.md` | Tiered field contract for downstream consumers (ADR-074) |
| 06 | `references/rca-writing-guide.md` | RCA document standards |
| — | `references/workflow-integration.md` | Dev workflow integration hooks (external consumers) |
| — | `references/rca-help.md` | Command help and examples |

## Asset Templates (Strategic Mode)

| Asset | Purpose |
|-------|---------|
| `assets/5-whys-template.md` | 5 Whys section template for RCA document |
| `assets/evidence-section-template.md` | Evidence organization template |
| `assets/rca-document-template.md` | Full RCA document template |
| `assets/recommendation-template.md` | Recommendation subsection template |

---

## Integration with DevForgeAI Framework

### Iteration Log as Evidence Source

The iteration log is an evidence source for RCA analysis, alongside the story file, test output, and code diff. During Phase 01 (Capture) evidence gathering, read the iteration log to extract cycle timeline evidence:

```
devforgeai-validate iteration-log-status ${STORY_ID} --format=json
```

**Cycle Timeline Evidence:**
- Each cycle's `dev.approach_summary` documents what was tried
- Each cycle's `qa.blocking_issues` documents what failed and why
- The combination of approach_summary and blocking_issues across cycles forms a timeline of evidence showing the progression of the issue

**Hypothesis Generation from Spinning Wheels:**
- `spinning_wheels.repeated_root_causes` directly informs "Why #1" hypothesis generation
- If the same root cause appears across multiple cycles, it should be the primary hypothesis
- repeated_root_causes provides pre-analyzed data that accelerates the 5 Whys process

**Graceful Degradation:**
- If the iteration log is missing or unavailable: proceed with standard evidence gathering (story file, test output, code diff) without timeline data

### Invoked By

**Commands:**
- `/rca` slash command (strategic mode, primary invocation)

**Automatic Triggers (tactical mode):**
- `diagnosis-before-fix` rule after 3+ failed fix attempts
- spec-driven-dev Phase 03 (Green) after 2+ test failures
- spec-driven-dev Phase 05 (Integration) on non-environment failures
- spec-driven-qa Phase 02 (Deep Analysis) on CRITICAL/HIGH violations

**Manual Invocation:**
```
**Mode:** tactical
**Story ID:** STORY-NNN
**Error:** {error message}
**Fix Attempts:** {count}

Skill(command="spec-driven-rca")
```

### Subagents

| Subagent | Role | Phase | Required |
|----------|------|-------|----------|
| diagnostic-analyst | Read-only spec drift detection against 6 context files | Phase 02 | Yes (both modes) |
| rca-document-composer | Composes the RCA document — reads & executes phases 04-07; owns per-step phase-record calls; writes the RCA document | Phases 04-07 | Yes (strategic mode) |

### Related Skills

- spec-driven-dev (triggers tactical mode on test failures; consumes `rca-prescription.json` on Phase 03 retry per ADR-074)
- spec-driven-qa (triggers tactical mode on validation failures)
- spec-driven-stories (consumes RCA recommendations via /create-stories-from-rca per `references/recommendation-contract.md`)
- github-incident-from-rca (Phase 08 hand-off — strategic-mode completion offers to invoke for GitHub issue creation; sole `gh issue create` site)

---

## Workflow Completion Validation

```
IF MODE == tactical:
    IF completed_phases < 4: HALT "WORKFLOW INCOMPLETE - {count}/4 phases"
    IF completed_phases == 4: "Tactical diagnosis complete - returning prescription"

IF MODE == strategic:
    IF completed_phases < 8: HALT "WORKFLOW INCOMPLETE - {count}/8 phases"
    IF completed_phases == 8: "Strategic RCA complete - document created"
```

---

## Success Criteria

### Tactical Mode
- [ ] All 4 phases executed in order (00 → 01 → 02 → 03)
- [ ] No fix attempts before Phase 02 completion
- [ ] diagnostic-analyst subagent invoked in Phase 02
- [ ] At least one hypothesis with confidence >= 0.5 (enforced by `conviction-gate.sh`)
- [ ] Prescription includes specific file paths and actions
- [ ] `tmp/${STORY_ID}/rca-prescription.json` emitted with `next_action="resume-phase-03"` (enforced by `pre-rca-prescription-write.sh`)

### Strategic Mode
- [ ] All 8 phases executed in order (00 → 01 → 02 → 04 → 05 → 06 → 07 → 08)
- [ ] diagnostic-analyst subagent invoked in Phase 02
- [ ] Composition phases 04-07 delegated to rca-document-composer subagent
- [ ] 5 Whys complete with evidence
- [ ] Root cause validated (4 criteria)
- [ ] RCA document created at `devforgeai/RCA/RCA-{NNN}-{slug}.md`
- [ ] 3+ recommendations with exact implementation details
- [ ] Self-containedness check passed
- [ ] Completion report displayed

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0.0 | 2026-03-18 | Initial creation. Merged root-cause-diagnosis v1.0.0 (tactical 4-phase) and spec-driven-rca v1.0.0 (strategic 8-phase) into unified spec-driven skill with Execute-Verify-Record anti-skip enforcement. |
| 2.1.0 | 2026-05-15 | OPP-8: strategic-mode composition phases 04-07 delegated to the new `rca-document-composer` subagent. Phase Orchestration Loop dispatches 04-07 via `Task()`; primary retains phase-boundary gates, phase-level `phase-record`, and Phase 08. Phase files 04-07 unchanged (Option C). Added "Composition Phase Delegation" section. |
| 2.2.0 | 2026-05-20 | ADR-074 modernization: slimmed `/rca` to ≤25 lines (Orchestration Thinness Invariant); collapsed Execution Model Self-Check into hook-backed enforcement (3 new hooks: `pre-rca-recommendation-write.sh`, `pre-rca-document-write.sh`, `pre-rca-prescription-write.sh`); collapsed Validation Modes prose into 2-row table referencing `parameter-extraction.md`; published `references/recommendation-contract.md` (tiered Required/Rendered/Context contract); Phase 03 now emits `tmp/${STORY_ID}/rca-prescription.json` for /dev to consume on retry; Phase 08 offers `github-incident-from-rca` hand-off. SKILL.md 475 → ~408 lines. |
