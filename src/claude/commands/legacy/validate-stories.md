---
name: validate-stories
description: Validate stories against context files and trace custody chain provenance
argument-hint: "[STORY-ID|EPIC-ID|STORY-A..STORY-B|all] [--chain] [--force]"
---

# /validate-stories Command

Validates story files against constitutional context files and optionally traces
the full custody chain from brainstorms through requirements, epics, and sprints.

## Purpose

Validates one or more stories against the 6 context files to identify compliance issues,
and optionally traces full document provenance to detect broken chains, missing ADRs,
circular dependencies, ambiguous acceptance criteria, and stale labels.

## Usage

/validate-stories STORY-042              # Context validation (single story)
/validate-stories all                    # Context validation (all stories)
/validate-stories --since=STORY-100      # Context validation (stories >= ID)
/validate-stories STORY-013..STORY-033   # Custody chain audit (range)
/validate-stories EPIC-003               # Custody chain audit (all stories in epic)
/validate-stories STORY-042 --chain      # Custody chain audit (single story + back-chain)
/validate-stories all --chain            # Custody chain audit (everything)
/validate-stories EPIC-003 --force       # Regenerate from scratch (ignore existing audit)

## Workflow

### Phase 0: Input Resolution + Resume Detection

0. Parse $ARGUMENTS:

   # Extract flags
   chain_mode = "--chain" in $ARGUMENTS
   force_mode = "--force" in $ARGUMENTS
   args_clean = $ARGUMENTS without "--chain" and "--force"

   # Determine scope mode
   IF args_clean matches "^STORY-\d+$":
     mode = "single"
     story_id = args_clean
   ELIF args_clean == "all" OR args_clean == "":
     mode = "all"
   ELIF args_clean starts with "--since=":
     since_id = extract_story_id(args_clean)
     mode = "since"
   ELIF args_clean matches "^STORY-\d+\.\.STORY-\d+$":
     [range_start, range_end] = args_clean.split("..")
     mode = "range"
     chain_mode = true   # Range always implies chain
   ELIF args_clean matches "^EPIC-\d+$":
     epic_id = args_clean
     mode = "epic"
     chain_mode = true   # Epic always implies chain
   ELSE:
     HALT: "Invalid argument. Use: STORY-XXX, all, --since=STORY-XXX, STORY-A..STORY-B, or EPIC-XXX"

   # Derive audit file path (for chain mode)
   IF chain_mode:
     SWITCH mode:
       "single": scope_str = story_id
       "all":    scope_str = "all-stories"
       "since":  scope_str = f"since-{since_id}"
       "range":  scope_str = f"stories-{extract_num(range_start)}-{extract_num(range_end)}"
       "epic":   scope_str = epic_id
     AUDIT_FILE = f"devforgeai/qa/audit/custody-chain-audit-{scope_str}.md"

     # Resume detection — atomic-execution model (Wave 4c).
     # The subagent custody-chain-auditor runs the audit as a single Task() call.
     # Section-level resume (counting `^## [0-9]+\.` sections in partial AUDIT_FILE)
     # is no longer applicable because there is no partial state — the subagent
     # either returns a complete audit_file_content envelope or it doesn't.
     # The .in-progress marker file enables crash detection.
     IF force_mode:
       Bash(f"rm -f {AUDIT_FILE} {AUDIT_FILE}.in-progress")

     ELIF file_exists(f"{AUDIT_FILE}.in-progress"):
       AskUserQuestion:
         Question: "Previous audit run crashed — partial state detected (.in-progress marker). Restart from scratch?"
         Header: "Crashed audit"
         Options:
           - "Restart with --force (Recommended)"
             Description: "Delete partial state and re-run"
           - "Cancel"
             Description: "Abort; investigate manually"
       IF user_choice == "Restart with --force":
         Bash(f"rm -f {AUDIT_FILE} {AUDIT_FILE}.in-progress")
         # proceed to fresh run below
       ELSE:
         RETURN

     ELIF file_exists(AUDIT_FILE):
       Display: f"Audit already complete at {AUDIT_FILE}. Use --force to regenerate."
       RETURN

   # Note (Wave 4c): chain_mode dispatch is handled inside the subagent.
   # Primary no longer GOTOs Phase 2 for non-chain mode; the subagent receives
   # CHAIN_MODE as a parameter and skips Phase 1 inventory + Phase 3 chain audit
   # internally when chain_mode=false.


### Phases 1-5 + 7: Delegated to custody-chain-auditor (Wave 4c)

Phases 1, 2, 3, 4, 5 (rendering), and 7 (refactor scan) execute inside the
`custody-chain-auditor` terminal subagent (per Anthropic Q2). Phase 0 (above)
and Phase 6 (interactive resolution, below) stay in primary. Phase 5 *Write*
of the rendered audit_file_content stays in primary for atomic write semantics
and write-permission isolation (Wave 4a precedent: subagent renders content,
primary writes file).

EXECUTE: Lock AUDIT_FILE with `.in-progress` marker (chain_mode only); delegate
chain audit to custody-chain-auditor as a single batched Task() call.

```
IF chain_mode:
  Bash(f"touch {AUDIT_FILE}.in-progress")

result = Task(subagent_type="custody-chain-auditor", prompt=f"""
  SCOPE_MODE: {mode}                      # single | all | range | epic | since
  SCOPE_ARG: {args_clean}                 # e.g., STORY-042, EPIC-091, ""
  CHAIN_MODE: {chain_mode}                # boolean — auto-true for range/epic
  AUDIT_FILE_PATH: {AUDIT_FILE if chain_mode else 'null'}
  INCLUDE_COMPLETED: {include_completed}  # default false
  SINCE_ID: {since_id if mode == 'since' else 'null'}
  RANGE_START: {range_start if mode == 'range' else 'null'}
  RANGE_END: {range_end if mode == 'range' else 'null'}

  Workflow (return per-phase state in single JSON envelope):
    Phase 1: Glob stories per scope_mode; build story_meta + chain_docs (chain_mode only)
    Phase 2: Read context files + Read context-validation.md; iterate Phase 2 Validator
             Dispatch Table; emit context/* findings
    Phase 3: chain_mode only — Read custody-chain-workflow.md; execute sub-phases
             3a (provenance/), 3b Passes 1+2 (dependency/), 3c (adr/), 3d (quality/),
             3e (coherence/, gated on 2+ stories same epic), 3f (template/, gated on
             2+ stories in scope)
    Phase 4: Synthesize all findings; compute stats + severity_breakdown
    Phase 5: chain_mode only — render audit_file_content as one markdown string;
             return as `audit_file_content` field. Do NOT Write any files; primary
             writes atomically below.
    Phase 7: For each refactor story (frontmatter type==refactor), invoke
             Bash(devforgeai-validate scan-refactor-story --story-file=... --format=json);
             map output to refactor/* findings. Runs BEFORE Phase 4 synthesis to fix
             latent bug where refactor findings were not persisted to audit file.

  References (READ at runtime — do NOT inline rules):
    - .claude/skills/spec-driven-stories/references/custody-chain-workflow.md
    - .claude/skills/spec-driven-stories/references/context-validation.md
    - .claude/rules/workflow/plan-file-archive.md
""")
state = parse_json(result)

IF state.status == "BLOCKED" AND state.get("error"):
  HALT — Display error envelope; do NOT proceed to Phase 5 Write
```

### Phase 1: Story Discovery (delegated)

EXECUTE: Surface story-discovery output.

```
phase_1 = state["per_phase"]["1"]
Display: f"Phase 1: {phase_1['summary']}"
```

VERIFY: state["per_phase"]["1"]["stories_discovered"] is an integer. (Empty scope
returns 0 with status=PASS; non-empty scope returns >=1.)


### Phase 2: Context Validation (delegated)

EXECUTE: Surface context-validation findings.

```
phase_2 = state["per_phase"]["2"]
Display: f"Phase 2: {phase_2['summary']}"
```

VERIFY: state["per_phase"]["2"] is a dict with `summary` and `findings_count`.


### Phase 3: Custody Chain Audit (delegated, sub-phases 3a-3f)

EXECUTE: Surface chain-audit findings across the 6 sub-phases.

```
phase_3 = state["per_phase"]["3"]
Display: f"Phase 3: {phase_3['summary']}"
```

VERIFY: state["per_phase"]["3"]["sub_phases_run"] includes ["3a","3b","3c","3d","3e","3f"]
when chain_mode=true (or empty list when chain_mode=false). Sub-phases 3e and 3f
may emit zero findings if their gating conditions (2+ stories same epic / 2+ stories
in scope) fail — that's documented in their summary.


### Phase 4: Synthesis (delegated)

EXECUTE: Surface synthesized stats.

```
phase_4 = state["per_phase"]["4"]
Display: f"Phase 4: {phase_4['summary']}"
```

VERIFY: state["stats"]["severity_breakdown"] is a populated dict with
CRITICAL/HIGH/MEDIUM/LOW keys.


### Phase 5: Audit File Write (PRIMARY)

EXECUTE: Write subagent-rendered content to AUDIT_FILE atomically (chain_mode only);
remove .in-progress marker; surface write confirmation.

```
phase_5 = state["per_phase"]["5"]

IF chain_mode AND state["audit_file_content"] is not null:
  Write(file_path=AUDIT_FILE, content=state["audit_file_content"])
  Bash(f"rm -f {AUDIT_FILE}.in-progress")
  Display: f"Phase 5: Audit file written to {AUDIT_FILE} ({len(state['audit_file_content'])} bytes)"
ELSE:
  # Non-chain mode: no audit file, just display summary
  Display: f"Phase 5: {phase_5['summary']}"

# Final summary line (preserves existing CLI UX)
Display: f"""

## {'Custody Chain Audit' if chain_mode else 'Context Validation'} Complete

**Stories Validated:** {state['stats']['stories_validated']}
**Compliant:** {state['stats']['compliant']}/{state['stats']['stories_validated']}
**Findings:** {state['stats']['severity_breakdown']['CRITICAL']} CRITICAL, {state['stats']['severity_breakdown']['HIGH']} HIGH, {state['stats']['severity_breakdown']['MEDIUM']} MEDIUM, {state['stats']['severity_breakdown']['LOW']} LOW
{f"**Report:** {AUDIT_FILE}" if chain_mode else ""}
"""
```

VERIFY (chain_mode only): file_exists(AUDIT_FILE) AND NOT file_exists(f"{AUDIT_FILE}.in-progress").


### Phase 6: Interactive Resolution (Optional)

6. Interactive fix-up (single story mode with violations only):

   IF mode == "single" AND stats.failed > 0:
     critical_high = [f for f in all_findings if f.severity in ["CRITICAL", "HIGH"]]

     IF critical_high:
       # Sprint B D6 migration (2026-04-24): option labels, descriptions, inner-
       # prompt question template, per-choice edit-instruction dispatch, and the
       # stable `<!-- AUDIT-DEFERRED: {finding.type} -->` marker format now live
       # in the skill reference. Command retains AskUserQuestion invocations +
       # outer control flow; content is delegated byte-for-byte.
       Read(file_path=".claude/skills/spec-driven-stories/references/fix-resolution-patterns.md")

       # Outer prompt — invoke AskUserQuestion using the exact 3 labels +
       # descriptions from § "Outer Prompt" of fix-resolution-patterns.md.
       # Question template: f"{len(critical_high)} blocking issues found. Fix now?"
       # Header: "Fix issues"
       AskUserQuestion per § "Outer Prompt" of fix-resolution-patterns.md.

       IF choice == "Fix all":
         FOR finding in critical_high:
           # Inner prompt — invoke AskUserQuestion using the exact 4 labels +
           # descriptions from § "Inner Prompt" of fix-resolution-patterns.md.
           # Question template: f"[{finding.severity}] {finding.type}: {finding.summary}\n\nHow to resolve?"
           # Header: "Resolution"
           AskUserQuestion per § "Inner Prompt" of fix-resolution-patterns.md.

           # Dispatch per § "Inner-prompt dispatch" of fix-resolution-patterns.md.
           # The "Defer to manual review" branch uses the stable marker format
           # from § "`AUDIT-DEFERRED` marker format" — verbatim:
           #   <!-- AUDIT-DEFERRED: {finding.type} -->
           Apply edit per § "Inner-prompt dispatch" of fix-resolution-patterns.md.

         # Post-loop flow per § "Post-loop flow" of fix-resolution-patterns.md.
         Display: "Re-validating after fixes..."
         GOTO Phase 2 (single story)


### Phase 7: Refactor Scan (delegated)

EXECUTE: Surface refactor-scan findings (executed inside the custody-chain-auditor
subagent BEFORE Phase 4 synthesis — this fixes a latent bug in the pre-Wave-4c
implementation where Phase 7 findings were extended to `all_findings` AFTER the
audit file had already been written, so they did not appear in the persisted audit).

```
phase_7 = state["per_phase"]["7"]
Display: f"Phase 7: {phase_7['summary']}"
```

VERIFY: state["per_phase"]["7"] is a dict with `summary` and `findings_count`.

References preserved (now read by the subagent at runtime):
- STORY-457 revert — refactor stories with size-only ACs led to logic loss during implementation
- Sprint B D6 migration (2026-04-24): Checks 7.8.1-7.8.4 execute inside the deterministic
  `scan-refactor-story` CLI (`src/claude/scripts/devforgeai_cli/validators/refactor_story.py`)
- Authoritative spec: `.claude/skills/spec-driven-stories/references/refactor-quality-checks.md`
- Parity baselines: `tests/sprint-b-parity/fixtures/baselines/*-baseline.json`


## Output

**Success (all compliant, context only):**
  Context Validation Complete
  Stories Validated: 15
  Compliant: 15/15 (100%)

**Chain audit with findings:**
  Custody Chain Audit Complete
  Stories Validated: 21
  Compliant: 19/21 (90.5%)
  Findings: 2 CRITICAL, 6 HIGH, 5 MEDIUM, 3 LOW
  Report: devforgeai/qa/audit/custody-chain-audit-stories-013-033.md

**Crashed run detected (Wave 4c — atomic-execution model):**
  Previous audit run crashed — partial state detected (.in-progress marker). Restart from scratch?
  > Restart with --force (Recommended)
  ... (subagent re-runs the full audit)

## Integration

**Delegates audit logic to** (Wave 4c, Anthropic Q2 terminal worker):
- `.claude/agents/custody-chain-auditor.md` — opus terminal subagent that executes
  Phases 1, 2, 3, 4, 5 (rendering), and 7. Reads at runtime:
  - `.claude/skills/spec-driven-stories/references/custody-chain-workflow.md` (sub-phases 3a-3f orchestration)
  - `.claude/skills/spec-driven-stories/references/context-validation.md` (Phase 2 dispatch table + coherence Functions #11-17)
  - `.claude/rules/workflow/plan-file-archive.md` (sub-phase 3a archive-fallback)

**Phase 6 prompt templates loaded by primary** (single-story interactive resolution):
- `.claude/skills/spec-driven-stories/references/fix-resolution-patterns.md`

**Can be called:**
- Standalone via `/validate-stories`
- Before sprint planning (ensure stories are ready)
- After bulk story creation (batch validation)
- After a crashed run (`.in-progress` marker triggers restart prompt; use `--force` to bypass)

**Related commands:**
- `/create-system-architecture` - Generate context files (required for validation)
- `/create-story` - Create new story (includes context validation)
- `/qa` - Quality validation (includes context compliance)
- `/validate-epic-coverage` - Validate epic feature coverage
