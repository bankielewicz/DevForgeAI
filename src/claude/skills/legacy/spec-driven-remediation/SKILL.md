---
name: spec-driven-remediation
description: >
  Apply automated and guided fixes to story, epic, and context files based on
  structured audit findings with 4-layer anti-skip enforcement. Classifies findings
  by fix complexity, applies safe automated fixes, guides interactive fixes with
  user confirmation, verifies all changes, and produces a fix report. Uses
  Execute-Verify-Record pattern at every step to prevent token optimization bias.
  Use when /fix-story is invoked, when audit findings need remediation, or when
  custody chain validation produces findings requiring correction. Make sure to
  use this skill whenever the user mentions fixing stories, remediating audit
  findings, applying fixes from /validate-stories output, or addressing custody
  chain violations.
metadata:
  author: DevForgeAI
  version: "2.0.0"
  category: story-lifecycle
  agent-skills-spec-version: "1.0"
  last-updated: "2026-03-18"
  migrated-from: story-remediation v1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
model: opus
effort: High
---

# Spec-Driven Remediation

Apply automated and guided fixes to story, epic, and context files based on structured audit findings from `/validate-stories`. Every step uses Execute-Verify-Record to prevent token optimization bias from skipping phases.

**Audit findings are the input. Fixed files are the output. User approval gates every structural change.**

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow: the `devforgeai-validate` phase gates, the `settings.json`-registered `.claude/hooks/` scripts, and `.claude/hooks/phase-steps-registry.json` (ADR-076).

---

## Parameter Extraction

Extract parameters from conversation context markers set by `/fix-story` command. See `references/parameter-extraction.md` for the extraction algorithm.

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$FIX_MODE` | /fix-story | Input mode: audit_file, story_id, or epic_id |
| `$AUDIT_FILE` | /fix-story | Path to audit file |
| `$DRY_RUN` | /fix-story | true = preview only, no file modifications |
| `$AUTO_ONLY` | /fix-story | true = skip interactive and ADR fixes |
| `$FINDING_FILTER` | /fix-story | F-NNN for single finding, "all" for everything |

---

## Phase State Initialization [MANDATORY FIRST]

Derive SESSION_ID from audit file name:
```
SESSION_ID = "FIX-" + basename(AUDIT_FILE).replace(".md", "")
# Example: "FIX-custody-chain-audit-stories-413-424"
```

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=remediation --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "00". |
| 1 | Existing workflow | Resume. Check checkpoint file for CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Verify audit file path. |
| 127 | CLI not installed | HALT. Restore the validator before any governed operation. |

**Resume Detection:** If resuming, read checkpoint:
```
Read(file_path="{project-root}/tmp/.remediation-checkpoint-${SESSION_ID}.yaml")
```
Extract `current_phase` and `phase_completion` to determine where to resume.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 06):
    phase_id = format(phase_num, "02d")

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from={prev} --to={phase_id}
       IF exit != 0: HALT

    2. LOAD: Read(file_path="phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase={phase_id}

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase={phase_id} --checkpoint-passed
       IF exit != 0: HALT
```

**Dry Run Skip Path:** If `$DRY_RUN == true`, Phase 02 exits early and skips directly to Phase 05 (report only, no modifications).

| Phase | Name | File |
|-------|------|------|
| 00 | Context Loading + Finding Extraction | `phases/phase-00-context-loading.md` |
| 01 | Finding Triage + Classification | `phases/phase-01-triage.md` |
| 02 | Safety Preview | `phases/phase-02-preview.md` |
| 03 | Fix Execution | `phases/phase-03-execution.md` |
| 04 | Post-Fix Verification | `phases/phase-04-verification.md` |
| 05 | Fix Report + Session Record | `phases/phase-05-reporting.md` |

---

## State Persistence

**Phase State:** `devforgeai/workflows/${SESSION_ID}-remediation-phase-state.json`
**Session Memory:** `.claude/memory/sessions/${SESSION_ID}-remediation-session.md`
**Checkpoint:** `{project-root}/tmp/.remediation-checkpoint-${SESSION_ID}.yaml`
**References:** `references/checkpoint-schema.md`, `references/memory-file-operations.md`

---

## Workflow Completion Validation

```
IF completed_count < 6: HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases"
IF completed_count == 6: "All 6 phases completed - Remediation workflow passed"
```

---

## Success Criteria

- [ ] All findings loaded and classified correctly
- [ ] Automated fixes applied only after user confirmation
- [ ] Interactive fixes presented with clear resolution options
- [ ] All applied fixes pass post-fix verification
- [ ] Fix report generated with accurate summary
- [ ] Session record appended to audit file for resume capability
- [ ] No files modified without user approval (--dry-run respected)
- [ ] Deferred items properly marked with AUDIT-DEFERRED comments

---

## Reference Files

### Phase Execution (phases/ directory)

| File | Phase |
|------|-------|
| phase-00-context-loading.md | Context Loading + Finding Extraction |
| phase-01-triage.md | Finding Triage + Classification |
| phase-02-preview.md | Safety Preview |
| phase-03-execution.md | Fix Execution |
| phase-04-verification.md | Post-Fix Verification |
| phase-05-reporting.md | Fix Report + Session Record |

### Supporting References (references/ directory)

| File | Purpose |
|------|---------|
| fix-actions-catalog.md | Classification matrix and fix procedures for each finding type |
| fix-verification-workflow.md | Per-type verification procedures and feedback loop protocol |
| context-validation.md | Context file constraint validation rules |
| checkpoint-schema.md | Checkpoint YAML schema for remediation sessions |
| memory-file-operations.md | Session memory file read/write operations |
| parameter-extraction.md | Audit file resolution and parameter extraction algorithm |

### Templates (assets/templates/ directory)

| File | Purpose |
|------|---------|
| fix-report-template.md | Fix session report markdown template |
| checkpoint-template.yaml | Checkpoint YAML structure template |
