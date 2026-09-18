# Refactor Story Quality Checks — Authoritative Spec

**Sprint:** B (Woolly v1 initiative — `/home/bryan/.claude/plans/woolly-v1-reconstruction.md`)
**Status:** Spec — consumed by `src/claude/scripts/devforgeai_cli/validators/refactor_story.py` (D3) and the `devforgeai-validate scan-refactor-story` CLI (D4).
**Supersedes:** Inline logic in `.claude/commands/validate-stories.md` lines 443-528 (which will be replaced by a CLI invocation in D6 only after the Sprint B parity test (D7) passes bit-identical against the reference corpus).
**Origin:** STORY-457 revert — refactor stories that ship with size-only / structure-only acceptance criteria have empirically lost user-facing content (help text, error messages, governance output) during implementation. These four checks catch that class of defect at story-creation time by scanning the story file for the absence of content-preservation signals.

---

## Applicability

A story is subject to these checks if and only if its YAML frontmatter contains `type: refactor`. Stories with any other `type` value (`feature`, `documentation`, `bugfix`, or unset) are NOT subject to these checks; the scanner returns an empty findings list with `valid: true` and `ac_count_inspected: 0`.

---

## Input Contract

The scanner reads a single `.story.md` file and operates on three regions of the story content:

1. **Acceptance Criteria "Then" clauses** — the concatenation of every `<then>` element text across all `<acceptance_criteria>` blocks. If the story uses the legacy markdown AC format (`### AC#N: ...` followed by `Given / When / Then:` lines), the extractor falls back to collecting every line that begins with `Then` or lives under a `Then:` heading.
2. **Non-Functional Requirements section body** — the Markdown section under `## Non-Functional Requirements` (accepting variants: `## Non-Functional Requirements (NFRs)`, `## NFRs`, `## NFR`). Matched case-insensitively on section header.
3. **Definition of Done section body** — the Markdown section under `## Definition of Done`.
4. **Technical Specification section body** — used to extract file paths referenced by the story (for Check 7.8.3's target-file inspection).

All region extraction is case-insensitive on section headers. Body content comparisons below are case-insensitive unless otherwise noted.

---

## Check Catalogue (exact semantics)

Each check emits at most one finding per story. A finding's `type` field MUST be exactly one of the four `type` values listed below (these are the stable identifiers consumers depend on). Severity, summary, and remediation strings are also stable and MUST match the current `/validate-stories` output verbatim so the Sprint B parity test (D7) can assert bit-identical findings.

### Check 7.8.1 — Content-Preservation AC Present

**Purpose:** Verify that at least one acceptance criterion declares a content-preservation invariant (e.g., the refactor must not drop user-visible strings, display output, error messages, governance markers).

**Pattern:** The concatenated AC-then text MUST contain at least ONE of these case-insensitive literal substrings or regex patterns:

| Signal | Match type |
|--------|------------|
| `preserved` | literal substring (case-insensitive) |
| `backward.compat` | regex (`backward`, any single char, `compat`) — case-insensitive |
| `golden` | literal substring (case-insensitive) |
| `identical.*format` | regex (`identical`, any chars, `format`) — case-insensitive, dot-all NOT required |

If zero matches, emit:

```yaml
severity: HIGH
type: "quality/refactor_missing_preservation_ac"
affected: <story_id>
summary: "Refactor story has size/structure ACs but no content-preservation ACs"
remediation: "Add AC verifying all Display/error/governance content preserved. Use /fix-story to auto-generate."
```

### Check 7.8.2 — NFR-002 Enforcement AC Present

**Purpose:** Verify that when a story declares "backward compatibility" as an NFR, at least one AC enforces a concrete output-verification mechanism for that compatibility claim.

**Trigger condition:**
- NFR section body contains the case-insensitive literal `backward compatibility`.

**If triggered, pattern check:** The concatenated AC-then text MUST contain at least ONE of these AND combinations:

| Signal | Match type |
|--------|------------|
| `help text` AND `sections` | both case-insensitive literal substrings present in the same AC-then scope |
| `error messages` AND `format` | both case-insensitive literal substrings present in the same AC-then scope |
| `golden` OR `output.*diff` | `golden` literal OR regex `output`, any chars, `diff` (case-insensitive) |

**Scope note:** "Same AC-then scope" means the two substrings must both appear within the same AC's `<then>` clause (or the same markdown `Then:` block). The spec intent is to prevent a story from satisfying the check by mentioning `help text` in one AC and `sections` in an unrelated AC.

If triggered AND zero matches, emit:

```yaml
severity: HIGH
type: "quality/refactor_nfr_without_ac"
affected: <story_id>
summary: "NFR-002 backward compatibility declared but no AC enforces output verification"
remediation: "Add AC with golden output diffing for all invocation modes."
```

### Check 7.8.3 — AskUserQuestion Placement AC Present

**Purpose:** Verify that when a refactor story touches source files that currently contain `AskUserQuestion` invocations, at least one AC enforces the lean-orchestration-pattern.md placement rule (zero `AskUserQuestion` inside the skill; all `AskUserQuestion` calls live in the command file).

**Trigger condition:**
- Extract file paths from the Technical Specification section (see "File path extraction" below).
- For each extracted file path, if the file exists on disk (project-root-relative), read it and check whether the literal `AskUserQuestion` appears anywhere in the file content.
- If at least ONE target file contains `AskUserQuestion`, the check is triggered. The scanner short-circuits on first match (no need to read all target files).

**If triggered, pattern check:** The concatenated AC-then text MUST contain at least ONE AC-then clause that includes ALL THREE of:

| Signal | Match type |
|--------|------------|
| `AskUserQuestion` | literal substring (case-SENSITIVE) |
| `ZERO` OR `zero` OR `0` | any one of the three (the first two are case-sensitive; `0` is the literal digit) |
| `skill` | literal substring (case-sensitive) |

**Scope note:** All three signals must be in the SAME AC-then clause (not spread across multiple ACs).

If triggered AND zero matches, emit:

```yaml
severity: MEDIUM
type: "quality/refactor_askuser_placement_missing"
affected: <story_id>
summary: "Source files have AskUserQuestion but no AC enforces lean orchestration placement"
remediation: "Add AC requiring zero AskUserQuestion in skill, all in command per lean-orchestration-pattern.md line 104."
```

**File-path extraction (shared with other Phase 07 checks):**
- Parse the Technical Specification section for file paths using the same extraction logic as `extract_file_paths()` in `context-validation.md` function #2 (`validate_file_paths`).
- Patterns considered file paths: anything matching `([a-zA-Z_][\w./\\-]*\.[a-zA-Z]{1,6})`, filtered to actual file extensions present in `tech-stack.md`'s approved list (`.py`, `.ts`, `.tsx`, `.js`, `.md`, `.sh`, `.yaml`, `.yml`, `.json`).
- Paths are resolved relative to the project root; missing files are skipped without warning (do NOT emit a finding just because a referenced file is absent — that's a different class of validation).

**Non-existence fallback:** If zero target files exist on disk, the check is NOT triggered (returns no finding). Rationale: a story scheduled to touch files that don't exist yet cannot reasonably be expected to declare an AskUserQuestion placement AC.

### Check 7.8.4 — Golden Output DoD Present

**Purpose:** Verify that the Definition of Done includes explicit "capture before / diff after" items for refactor work — the operational safety net that makes Check 7.8.1's preservation claim verifiable.

**Pattern:** The Definition of Done section body MUST contain at least ONE of these case-insensitive signals:

| Signal | Match type |
|--------|------------|
| `golden output` | literal substring (case-insensitive) |
| `pre-refactoring` | literal substring (case-insensitive) |
| `output.*captured` | regex (`output`, any chars, `captured`) — case-insensitive |

If zero matches, emit:

```yaml
severity: MEDIUM
type: "quality/refactor_missing_golden_capture"
affected: <story_id>
summary: "Refactor story DoD missing golden output capture items"
remediation: "Add DoD items for pre-refactoring output capture and post-refactoring diff."
```

---

## Finding Schema (complete)

Every emitted finding has exactly these fields:

```yaml
finding_id:        <assigned by the calling Phase 07 step; NOT assigned by this scanner>
severity:          "HIGH" | "MEDIUM"                          # per-check; see Check Catalogue
type:              "quality/refactor_missing_preservation_ac"
                   | "quality/refactor_nfr_without_ac"
                   | "quality/refactor_askuser_placement_missing"
                   | "quality/refactor_missing_golden_capture"
affected:          "<story_id>"                               # e.g. "STORY-646"
summary:           <fixed string per check>
remediation:       <fixed string per check>
source_check:      "refactor-quality/7.8.1"
                   | "refactor-quality/7.8.2"
                   | "refactor-quality/7.8.3"
                   | "refactor-quality/7.8.4"
provenance:        "GROUNDED"                                 # all four checks are pattern-based on file content
```

The `source_check` field is NEW in the Sprint B migration (it did not exist in the inline `/validate-stories` implementation). It is additive: consumers that currently key off `type` continue to work unchanged. The parity test (D7) asserts all pre-existing fields are bit-identical and permits the `source_check` and `provenance` additions.

---

## Invocation Contract

Consumers invoke the scanner via:

```bash
devforgeai-validate scan-refactor-story --story-file=devforgeai/specs/Stories/STORY-NNN-*.story.md --format=json
```

Exit codes (matches the project's established 0/1/2 convention):

| Exit code | Meaning |
|-----------|---------|
| 0 | Scan succeeded. `findings` list may be empty (clean story) or non-empty. `valid: true` if `findings == []`; `valid: false` otherwise. |
| 1 | IO / parse error (story file unreadable, YAML frontmatter malformed). `findings` absent from JSON payload; `error` key contains the message. |
| 2 | Reserved for future use (will NOT be emitted by Sprint B's initial implementation). |

JSON output shape:

```json
{
  "story_file": "devforgeai/specs/Stories/STORY-646-sprint-a-wire-orphaned-validators.story.md",
  "story_id": "STORY-646",
  "story_type": "refactor",
  "applicable": true,
  "ac_count_inspected": 14,
  "findings": [
    {
      "severity": "HIGH",
      "type": "quality/refactor_missing_preservation_ac",
      "affected": "STORY-646",
      "summary": "Refactor story has size/structure ACs but no content-preservation ACs",
      "remediation": "Add AC verifying all Display/error/governance content preserved. Use /fix-story to auto-generate.",
      "source_check": "refactor-quality/7.8.1",
      "provenance": "GROUNDED"
    }
  ],
  "valid": false
}
```

When `story_type != "refactor"`, the scanner returns `applicable: false`, `findings: []`, `valid: true` — no work performed.

---

## Parity Test Contract (D7)

The Sprint B parity test runs both the pre-migration inline `/validate-stories` Phase 7 logic and the new `scan-refactor-story` CLI against a fixed corpus of at least three real refactor-type stories from `devforgeai/specs/Stories/`. For each (story, check) pair, the test asserts:

1. The CLI's `findings` list contains the SAME SET of `type` values as the inline implementation.
2. For each matched `type`, the `severity`, `summary`, `remediation`, and `affected` fields are byte-identical.
3. The CLI's ordering of findings MAY differ from the inline implementation (ordering is not guaranteed); the test compares as sets, not as lists.
4. The CLI's newly-added `source_check` and `provenance` fields do NOT cause the test to fail (they are additive per the migration-safety rule).

A failing parity test BLOCKS D6 (the `/validate-stories` command edit that removes the inline logic). The inline logic MUST remain until parity is green.

---

## Non-Goals for Sprint B

The scanner deliberately does NOT:

- Auto-fix any findings (no `--fix` flag in Sprint B; autofix-story is deferred per §3 of the Woolly v1 plan).
- Rewrite or suggest specific AC text (remediation strings point the user at `/fix-story`).
- Look at historical git blame to detect whether size-only ACs were added recently (out of scope).
- Infer intent from refactor commit messages (out of scope; spec is intentionally restricted to the story file itself).

---

## References

- Original logic: `.claude/commands/validate-stories.md` lines 443-528 (operational) / `src/claude/commands/validate-stories.md` (source — same content).
- STORY-457 revert rationale: referenced in `.claude/commands/validate-stories.md` line 435.
- Lean-orchestration placement rule (Check 7.8.3 remediation target): `.claude/rules/workflow/lean-orchestration-pattern.md` line 104.
- File-path extraction helper: `src/claude/skills/spec-driven-stories/references/context-validation.md` function #2 (`validate_file_paths`).
- Migration safety rule (bit-identical parity gate): `/home/bryan/.claude/plans/woolly-v1-reconstruction.md` §5.
- Finding-type stability guarantee: Sprint A's precedent with `nfr_provenance` findings (same `type` string preserved across inline → CLI migration).
