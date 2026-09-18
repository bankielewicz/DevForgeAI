# Interactive Fix-Resolution Patterns — Authoritative Spec

**Sprint:** B (Woolly v1 initiative — `/home/bryan/.claude/plans/woolly-v1-reconstruction.md`)
**Status:** Spec — consumed by `.claude/commands/validate-stories.md` Phase 6 via `Read(".claude/skills/spec-driven-stories/references/fix-resolution-patterns.md")` after Sprint B D6 lands.
**Supersedes:** Inline logic in `.claude/commands/validate-stories.md` lines 401-424 (which will be replaced by a `Read()` reference in D6; the inline `AskUserQuestion` invocations remain in the command file because they are orchestration primitives per §4 of the Woolly v1 plan — what moves is the option-text/edit-instruction/marker-format content, not the prompting mechanism itself).
**Origin:** `/validate-stories` Phase 6 Interactive Resolution — single-story mode with blocking (CRITICAL/HIGH) findings. The option labels, descriptions, per-resolution edit instructions, and `AUDIT-DEFERRED` marker format are skill-owned business patterns that drifted into the command file; this spec relocates them to their rightful home in the skill's `references/` tree.

---

## Applicability

Phase 6 of `/validate-stories` triggers interactive fix-up if and only if BOTH conditions hold:

1. `mode == "single"` — the command was invoked with a single `STORY-NNN` argument (not `all`, not `--since=`, not a `STORY-A..STORY-B` range, not an `EPIC-NNN` scope).
2. `stats.failed > 0` — Phase 2/3 produced at least one finding classified as `FAILED` (which aggregates from CRITICAL and HIGH severity entries).

If either condition is false, Phase 6 is entirely skipped and this reference is not loaded.

When both conditions hold, Phase 6 filters findings to `critical_high = [f for f in all_findings if f.severity in ["CRITICAL", "HIGH"]]` and proceeds ONLY if `critical_high` is non-empty. MEDIUM and LOW findings never drive interactive resolution.

---

## Input Contract

Phase 6 of `/validate-stories` loads this reference and uses it to populate two `AskUserQuestion` invocations, then dispatches user responses to the edit instructions below. The runtime state the command must already hold before loading this reference:

| Variable | Type | Source |
|----------|------|--------|
| `story_id` | str (e.g. `STORY-646`) | Phase 0 scope resolution |
| `story_file` | path | Phase 1 `Glob` result |
| `critical_high` | list[Finding] | Phase 4 synthesis output |
| `all_findings` | list[Finding] | same |

A `Finding` has at minimum these fields (used by this spec):

- `severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"`
- `type: str` — stable machine-readable identifier (e.g. `quality/refactor_missing_preservation_ac`, `context/tech_stack_violation`)
- `summary: str` — single-line human-readable summary

---

## Outer Prompt (triage — one invocation per `/validate-stories` run)

Populated by `/validate-stories` Phase 6 using these exact strings (no substitution beyond `{count}`):

```
AskUserQuestion:
  Question: "{count} blocking issues found. Fix now?"
  Header:   "Fix issues"
  Options:
    - label: "Fix all"
      description: "Walk through each violation and resolve"
    - label: "Show details only"
      description: "Display details, don't fix"
    - label: "Skip"
      description: "Exit without changes"
```

where `{count} = len(critical_high)`.

### Outer-prompt dispatch

| User selection | Action |
|----------------|--------|
| `Fix all` | Enter the per-finding loop (see "Inner Prompt" below) |
| `Show details only` | Display each finding's `{severity}`/`{type}`/`{summary}` on stdout. NO edits. NO re-validation. Exit Phase 6 cleanly. |
| `Skip` | Exit Phase 6 cleanly. No display, no edits. |

**Label/description byte-identity rule:** The three option labels and three descriptions above MUST be used verbatim in the command file's `AskUserQuestion` call. They are user-visible strings with no substitution; any future label change is a breaking UX change and requires a cross-reference update in this spec plus a migration-safety parity check.

---

## Inner Prompt (per-finding — one invocation per entry in `critical_high`)

Loop invariant: iterate `critical_high` in whatever order Phase 4's `sort_by_severity(all_findings)` produced (stable; CRITICAL before HIGH; tie-break by `finding_id` ascending per §Phase 4 of the command's prioritization; parity test MUST preserve this order).

For each `finding` in `critical_high`:

```
AskUserQuestion:
  Question: "[{severity}] {type}: {summary}\n\nHow to resolve?"
  Header:   "Resolution"
  Options:
    - label: "Fix in story"
      description: "I'll provide the correct value"
    - label: "Create required ADR"
      description: "Needed for tech decisions"
    - label: "Update context file"
      description: "Requires ADR first"
    - label: "Defer to manual review"
      description: "Flag for later"
```

where `{severity}`, `{type}`, and `{summary}` come from the current `finding` object. The three f-string substitutions are:

- `{severity}` — one of the enum values `CRITICAL` / `HIGH` (the `critical_high` filter guarantees no `MEDIUM`/`LOW` enters this loop).
- `{type}` — the finding's `type` field, inserted literally (no quoting, no escaping).
- `{summary}` — the finding's `summary` field, inserted literally.

The `\n\n` between `{summary}` and `How to resolve?` is a literal two-newline separator. This is part of the user-visible question text; do NOT alter it.

### Inner-prompt dispatch

| User selection | Edit instruction |
|----------------|-------------------|
| `Fix in story` | 1. Issue an additional `AskUserQuestion` asking the user for the correct value (free-text). 2. Call `Edit(file_path=story_file, old_string=<problematic_text>, new_string=<user_provided_value>)`. The `problematic_text` is identified from the finding's payload (`file:line` context; specifics out of scope for this spec — they live in the Phase-4 finding builder). |
| `Create required ADR` | Display the literal message: `Run /create-story for ADR, then re-validate` — one line, plain stdout. No edits to the story file. Re-validation prompt is handled by the post-loop flow below; see "Post-loop flow". |
| `Update context file` | Display the literal message: `Create ADR first, update context, re-validate` — one line, plain stdout. No edits to the story file. Context files are IMMUTABLE per `.claude/rules/workflow/configuration-layer-mutability.md`; the command MUST NOT offer to edit them directly and MUST NOT perform a context-file `Edit()`. |
| `Defer to manual review` | Call `Edit(file_path=story_file, old_string=<finding_context_line>, new_string="<!-- AUDIT-DEFERRED: {finding.type} -->\n<finding_context_line>")` OR append the marker to the story's `## Notes` section (implementation choice — the parity-critical requirement is that the marker STRING is emitted verbatim; placement strategy is local to the command and not observable via parity test). See "AUDIT-DEFERRED marker format" below. |

**Display-only messages (byte-identity rule):** The two `Create ADR` / `Update context` display strings above MUST be emitted verbatim. They are user-facing guidance; any rewording is a UX change requiring parity-test consideration.

---

## `AUDIT-DEFERRED` marker format (stable — parity-critical)

Every deferral MUST emit a marker matching this exact format:

```html
<!-- AUDIT-DEFERRED: {finding.type} -->
```

- `<!--` and `-->` are literal HTML comment delimiters. A single space separates `<!--` from `AUDIT-DEFERRED:` and a single space separates `{finding.type}` from `-->`.
- `AUDIT-DEFERRED:` is the exact literal prefix (uppercase, colon-terminated). The colon is followed by a single space before `{finding.type}`.
- `{finding.type}` is the finding's `type` field (e.g. `quality/refactor_missing_preservation_ac`, `context/unapproved_technology`). Inserted verbatim — no quoting, no URL-encoding, no whitespace collapse.
- No trailing whitespace inside the comment body.

The marker enables two downstream consumers to detect deferrals by grep:

1. `/fix-story` automated remediation — reads existing markers to skip already-deferred findings on re-validation.
2. `/validate-stories --chain` custody-chain audit — counts deferrals per story in its audit summary.

Both consumers depend on the STRING FORMAT being stable. Do NOT change the marker format without a coordinated update to both consumers.

### Placement rule (non-parity-critical)

The command's placement of the marker within the story file is a local implementation detail and NOT covered by the bit-identical parity test. Acceptable placements:

- Inline adjacent to the problematic line/AC block (ideal — visible context).
- In the story's `## Notes` section at the bottom of the file (fallback — always valid target).
- In a dedicated `## Deferred Audit Findings` section if one exists (story-template-dependent; only if present).

If the command chooses inline placement, it should prepend a newline so the marker occupies its own line.

---

## Post-loop flow

After the per-finding loop completes (whether all findings resolved, some deferred, or the user aborted mid-loop):

1. Display the literal string `Re-validating after fixes...` on stdout.
2. `GOTO` Phase 2 of the command — re-run context validation on the (now-edited) single story. Phase 2 re-computes `all_findings` from scratch against the updated story content.

**Parity-critical:** The display string `Re-validating after fixes...` is user-visible and must be byte-identical to the pre-migration version.

---

## Finding Schema (inputs this spec reads)

This spec does NOT define `Finding` — it consumes the schema Phase 4 produces. The fields this spec depends on:

| Field | Type | Used by |
|-------|------|---------|
| `severity` | `"CRITICAL" | "HIGH" | "MEDIUM" | "LOW"` | Outer-prompt filter (`critical_high`); inner-prompt interpolation |
| `type` | string | Inner-prompt interpolation; `AUDIT-DEFERRED` marker body |
| `summary` | string | Inner-prompt interpolation |

Any consumer changing the `Finding` shape (e.g. adding required fields, renaming existing ones) MUST update this spec and run the Sprint B parity test.

---

## Parity Test Contract (D7 — shared with refactor-quality-checks.md)

The Sprint B parity test harness runs both the pre-migration inline `/validate-stories` Phase 6 logic and the post-migration `Read()`-driven version against a fixed corpus of at least three real stories each with at least one CRITICAL or HIGH finding. For each (story, resolution-path) pair, the test asserts:

1. The outer `AskUserQuestion` is invoked with the exact option labels, descriptions, and header defined in this spec.
2. The inner `AskUserQuestion` is invoked once per entry in `critical_high`, with question text matching the `f"[{severity}] {type}: {summary}\n\nHow to resolve?"` template byte-identically.
3. The `AUDIT-DEFERRED: {finding.type}` marker emitted by the `Defer to manual review` branch matches the exact string format specified above (tested by writing a fake story, invoking the deferral path, and reading back via `Grep`).
4. The display-only messages (`Run /create-story for ADR, then re-validate`, `Create ADR first, update context, re-validate`, `Re-validating after fixes...`) are emitted verbatim.

Parity test failure BLOCKS D6 (the command-file edit that removes the inline content). The inline content remains until all four assertions are green.

---

## Non-Goals for Sprint B

This spec deliberately does NOT:

- Modify the `AskUserQuestion` tool's invocation mechanism — the command still calls `AskUserQuestion` directly; only the option-text content migrates to the skill.
- Provide automatic fix suggestions (the `Fix in story` path still requires the user to type the correct value).
- Extend deferral semantics beyond the single-marker format (e.g., no expiry dates, no assignee fields, no severity overrides).
- Handle the `Update context file` path with any action other than displaying guidance — context file edits are deferred to a separate workflow via `/create-story` for an ADR.

---

## References

- **Original logic:** `.claude/commands/validate-stories.md` lines 392-426 (Phase 6: Interactive Resolution).
- **Context-file immutability rule** (referenced by `Update context file` branch): `.claude/rules/workflow/configuration-layer-mutability.md`.
- **ADR creation reference** (referenced by `Create required ADR` branch): `/create-story` command + `devforgeai/specs/adrs/` convention.
- **`/fix-story` consumer** (reads `AUDIT-DEFERRED` markers): `.claude/commands/fix-story.md` — reads markers to skip already-deferred findings.
- **Migration safety rule** (bit-identical parity gate): `/home/bryan/.claude/plans/woolly-v1-reconstruction.md` §5.
- **Sibling Sprint B spec** (sharing D7 parity infrastructure): `src/claude/skills/spec-driven-stories/references/refactor-quality-checks.md`.
- **Severity-sort precedent** (inner-loop iteration order): Phase 4 `sort_by_severity(all_findings)` in `.claude/commands/validate-stories.md`.
