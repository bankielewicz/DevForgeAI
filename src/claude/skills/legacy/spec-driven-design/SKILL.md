---
name: spec-driven-design
description: Create Web, GUI, or Terminal design specifications in story, standalone, or extract mode from a customizable brief, brand, and visual direction; generate design.md, implementation artifacts, and web artifacts when the selected target is Web. Use through /create-design when a project needs a design source of truth or an existing mockup must be extracted.
argument-hint: "[STORY-NNN | brief] [--standalone] [--extract <path> [--web-artifact=<path>]] [--url=<url>]"
disable-model-invocation: true
---

# Spec-Driven Design

Run one deterministic design workflow. This skill owns design specification,
artifact generation, local rendered review, and deterministic validation.

## Provider contract

- Invoke this Claude skill through `/create-design`.
- Use `${CLAUDE_SKILL_DIR}` for every bundled phase, reference, script, contract,
  template, and asset.
- Use Claude-native file tools, Bash, user questions, image viewing, and agents
  only where a linked phase requires them.
- Treat a non-zero `devforgeai-validate` result as blocking. Never record a step
  whose verifier or material artifact failed.

## Modes and identifiers

| Mode | Input | Identifier | Workflow |
|---|---|---|---|
| story | exactly `STORY-NNN` | supplied story ID | `design` |
| standalone | brief or `--standalone` | `DESIGN-STANDALONE` | `design` |
| extract | `--extract <path> [--web-artifact=<repository-relative-html>]` | `DESIGN-EXTRACT` | `design-extract` |

Reject conflicting modes, malformed story IDs, missing extract paths, and path
traversal. Story identifiers are exactly three digits. Set `MODE`, `IDENTIFIER`,
and `WORKFLOW`, then initialize state:

For extract mode, `--web-artifact` is optional and may appear exactly once. The
invocation hook binds its repository-relative path and SHA-256. Never infer a
lint target from other discovered HTML files.

```bash
devforgeai-validate phase-init "$IDENTIFIER" \
  --workflow="$WORKFLOW" --mode="$MODE" --project-root=.
```

An exit other than 0 or the documented already-exists resume result blocks the
workflow.

## Phase router

Before each phase, read its linked file completely. Execute its required steps,
verify named outputs, record only verified receipts, and run the shared validator
before `phase-complete`.

Story and standalone route:

1. `${CLAUDE_SKILL_DIR}/phases/phase-01-context-validation.md`
2. `${CLAUDE_SKILL_DIR}/phases/phase-02-story-analysis.md`
3. `${CLAUDE_SKILL_DIR}/phases/phase-03-interactive-discovery.md`
4. `${CLAUDE_SKILL_DIR}/phases/phase-04-template-loading.md`
5. `${CLAUDE_SKILL_DIR}/phases/phase-05-code-generation.md`
6. `${CLAUDE_SKILL_DIR}/phases/phase-06-documentation.md`
7. `${CLAUDE_SKILL_DIR}/phases/phase-07-specification-validation.md`
8. `${CLAUDE_SKILL_DIR}/phases/phase-08-feedback-completion.md`

Extract route:

1. `${CLAUDE_SKILL_DIR}/phases/phase-01-context-validation.md`
2. `${CLAUDE_SKILL_DIR}/phases/phase-02a-mockup-extraction.md`
3. `${CLAUDE_SKILL_DIR}/phases/phase-06-documentation.md`
4. `${CLAUDE_SKILL_DIR}/phases/phase-07-specification-validation.md`
5. `${CLAUDE_SKILL_DIR}/phases/phase-08-feedback-completion.md`

At every phase boundary run both commands and require exit 0:

```bash
devforgeai-validate validate-design-phase "$IDENTIFIER" \
  --workflow="$WORKFLOW" --mode="$MODE" --phase="$PHASE" --project-root=.
devforgeai-validate phase-complete "$IDENTIFIER" \
  --workflow="$WORKFLOW" --phase="$PHASE" --project-root=.
```

## Required outputs

All modes produce `devforgeai/specs/ui/design.md` and
`devforgeai/specs/ui/UI-SPEC-SUMMARY.md`. Story and standalone modes also
produce the selected implementation artifact. A Web target includes a runnable
web artifact; GUI and Terminal targets use the approved source-tree location.
Record the dynamic output on step `5.5`:

```bash
devforgeai-validate phase-record "$IDENTIFIER" --workflow=design \
  --phase=05 --step=5.5 --artifact="$OUTPUT_PATH" --project-root=.
```

The CLI rejects a missing, empty, absolute, or traversing artifact path.

## Shared resources

- `${CLAUDE_SKILL_DIR}/contracts/design-context-handoff-contract.yaml`
- `${CLAUDE_SKILL_DIR}/references/design-source-of-truth-schema.md`
- `${CLAUDE_SKILL_DIR}/references/accessibility-guidelines.md`
- `${CLAUDE_SKILL_DIR}/references/web-best-practices.md`
- `${CLAUDE_SKILL_DIR}/references/gui-best-practices.md`
- `${CLAUDE_SKILL_DIR}/references/tui-best-practices.md`
- `${CLAUDE_SKILL_DIR}/scripts/validate_design_md.py`

Stop only after phase 08 completes. The registered Stop hook independently
blocks a recognized or initialized invocation that remains unfinished.
