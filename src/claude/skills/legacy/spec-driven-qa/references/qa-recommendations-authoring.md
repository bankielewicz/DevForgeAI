# QA Recommendations Authoring Guide

**Purpose:** Teach the `/qa` skill's Phase 05 authoring agent (human or AI) how to produce a `qa-recommendations.md` file that passes `devforgeai-validate validate-qa-recommendations` on the first try.

**Template:** `src/claude/skills/spec-driven-qa/assets/templates/qa-recommendations-template.md`
**Schema:** `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`
**Validator:** `src/claude/scripts/devforgeai_cli/validators/qa_recommendations.py` (CLI: `devforgeai-validate validate-qa-recommendations`)

---

## What This Artifact Is — and What It Is Not

**Is:** An AI-optimized spec file. Structured Markdown with YAML-block recommendations. Downstream Claude sessions (specifically `/dev --fix`) consume it to drive targeted remediation cycles.

**Is not:** A human-readable QA report. That is `qa-report.md` — prose, narrative, executive summary. Do not treat this file as a prose substitute.

**Is not:** A CI/CD JSON contract. That is `gaps.json` — pure machine consumption for automated pipelines.

**Three-artifact separation rationale:** Humans, CI, and AI have different consumption patterns. One artifact cannot serve all three without compromising each.

---

## The Fidelity Contract

Every recommendation entry MUST satisfy ALL of these at generation time. The validator refuses to emit a file with any violation.

1. **Concrete `file` path** — relative to project root. No `"various files"`, no globs.
2. **Concrete `line` or `line_range`** — integer or `[start, end]`. No `"multiple places"`.
3. **Deterministic `verification.command`** — executable as-is from project root. Must produce the same result on re-run given identical source.
4. **Observable `verification.expected`** — explicit output pattern, exit code, or JSON field assertion. No `"test passes"`, no `"output looks correct"`.
5. **Concrete remediation** — exactly one of:
   - `before_code` + `after_code` pair (code changes). Both non-null, both different.
   - `remediation_steps` list (non-code changes). Each step is an imperative, concrete action.
6. **GROUNDED or DERIVED provenance** — with one-sentence justification for DERIVED. INCONCLUSIVE is permitted ONLY when evidence is genuinely unavailable, and the reason must be spelled out.
7. **`estimated_effort_minutes`** — positive integer ≤ 480. A larger estimate means the recommendation should be split or escalated to a separate story.
8. **`blocking_release` boolean** — true/false. Must match section placement (Blocking → true; Advisory → false).

---

## Anti-Patterns the Validator Catches

These are enforced by `detect-aspirational-language`, `detect-ambiguous-qualifiers`, and `detect-stub-references` which run automatically.

| Anti-pattern | Examples | Replacement |
|--------------|----------|-------------|
| Aspirational | `"should improve"`, `"consider refactoring"`, `"could be cleaner"` | `"replaces line 54 with ..."` (verb + object) |
| Ambiguous qualifier | `"better handling"`, `"more robust"`, `"appropriate validation"` | Specify what "better" means: "adds isinstance check on line 232" |
| Unquantified | `"approximately 500ms"`, `"several files"`, `"a few tests"` | `"measured 180ms median; target 500ms per quality-gates.md line 19"` |
| Stub | `"TBD"`, `"TODO"`, `"see above"`, `"as appropriate"` | Populate the actual content. If unknown, mark INCONCLUSIVE with reason. |
| Missing evidence | DERIVED claim without a `justification` field | Add one sentence citing the heuristic. |

---

## REC-ID Convention

Format: `REC-{STORY}-{severity-initial}-{3-digit-seq}`

Examples:
- `REC-STORY-646-C-001` (first CRITICAL for STORY-646)
- `REC-STORY-646-M-005` (fifth MEDIUM)
- `REC-STORY-648-L-012` (twelfth LOW for STORY-648)

Severity initials: **C**RITICAL, **H**IGH, **M**EDIUM, **L**OW.

**Stability:** REC-IDs persist across cycles. If a recommendation is closed in Cycle 2, its ID stays in Cycle History. A re-QA in Cycle 3 that re-surfaces the same issue gets a **new** ID (e.g., `-M-006`) — it is a new observation, not a resumption.

Sequence numbering is per-severity-per-story: zero-pad to 3 digits for sort stability. Advanced tooling may emit 4 digits if a story crosses 999 recommendations of a single severity (extraordinarily rare; no cap in the schema).

---

## Section-Placement Rules

| Severity | Section | `blocking_release` |
|----------|---------|-------------------|
| CRITICAL | Blocking Recommendations | `true` |
| HIGH | Blocking Recommendations | `true` |
| MEDIUM | Advisory Recommendations | `false` |
| LOW | Advisory Recommendations | `false` |

Validator `_validate_section_placement` enforces this. Mismatch → HIGH violation → exit 1.

**Empty sections:** Sections with no entries MUST contain the literal text `_None._`. Never omit a Required section entirely — the SECTION_MANIFEST validator rejects missing sections.

---

## Input JSON Schema for `generate-qa-recommendations`

> **Run `devforgeai-validate generate-qa-recommendations --help` for the full documented schema.** This section summarizes required fields for quick reference.

The `--findings-file` argument expects a JSON file with this structure:

### Required Top-Level Fields

| Field | Type | Valid Values / Constraint |
|-------|------|--------------------------|
| `story_id` | string | Must match `STORY-\d{3,}` (e.g. `STORY-001`) |
| `qa_result` | enum string | `PASSED`, `PASS_WITH_WARNINGS`, `FAILED` |
| `cycle_number` | integer | `1` (only cycle 1 supported in current scope) |
| `generated_at` | string | ISO 8601 timestamp (e.g. `2026-06-14T00:00:00Z`) |
| `phase_start_timestamp` | string | ISO 8601 timestamp |
| `findings` | array | Array of finding objects (may be empty) |

### Required Per-Finding Fields

| Field | Type | Valid Values / Constraint |
|-------|------|--------------------------|
| `source_phase` | enum string | `Phase-02-Test-Quality`, `Phase-03-Coverage`, `Phase-04-Code-Review`, `Phase-05-Reporting` |
| `severity` | enum string | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `provenance` | enum string | `GROUNDED`, `DERIVED`, `INCONCLUSIVE` |
| `title` | string | Brief human-readable recommendation title |
| `file` | string | Relative path to the affected file |
| `category` | enum string | `correctness`, `security`, `performance`, `test_quality`, `coverage`, `anti_pattern`, `documentation` |
| `verification` | object | Must contain `command` (string) and `expected` (string) |
| `estimated_effort_minutes` | integer | Positive integer ≤ 480 |
| `line` OR `line_range` | int or [int, int] | Exactly one must be present: `line` (integer ≥ 1) OR `line_range` ([start, end] both ≥ 1) |
| Remediation | — | Exactly one of: `before_code` + `after_code` (both non-null strings) OR `remediation_steps` (non-empty list) |

### Conditional Per-Finding Fields

| Field | Required When |
|-------|---------------|
| `derived_justification` | `provenance == "DERIVED"` — one-sentence justification of the inference |
| `inconclusive_reason` | `provenance == "INCONCLUSIVE"` — explanation of what evidence is missing |

### Derived Fields (Computed by the Generator — NOT Read from Input)

| Field | How It Is Set |
|-------|---------------|
| `blocking_release` | Derived from `severity`: CRITICAL/HIGH → `true`, MEDIUM/LOW → `false`. Any value supplied in input is silently ignored. |

### Minimal Valid Example (`findings_input.json`)

```json
{
  "story_id": "STORY-001",
  "qa_result": "FAILED",
  "cycle_number": 1,
  "generated_at": "2026-06-14T00:00:00Z",
  "phase_start_timestamp": "2026-06-14T00:00:00Z",
  "findings": [
    {
      "source_phase": "Phase-04-Code-Review",
      "severity": "MEDIUM",
      "provenance": "GROUNDED",
      "title": "Missing encoding parameter on open() call",
      "file": "src/module.py",
      "line": 42,
      "category": "correctness",
      "before_code": "with open(path, 'r') as f:\n",
      "after_code": "with open(path, 'r', encoding='utf-8') as f:\n",
      "remediation_steps": null,
      "verification": {
        "command": "pytest tests/test_module.py::test_encoding -v",
        "expected": "1 passed"
      },
      "estimated_effort_minutes": 5
    }
  ]
}
```

Source: `src/claude/scripts/devforgeai_cli/validators/qa_recommendations_generator.py` (lines 136–382).

---

## Authoring Workflow (/qa Phase 05 Step 5.6)

```
1. Aggregate findings from Phases 02-04 in-memory.

2. For each finding, build a recommendation entry:
   a. Assign REC-ID using the convention above.
   b. Map severity → section placement.
   c. Populate file + line from grounded evidence (Phase 03 coverage report,
      Phase 04 code review output, etc.).
   d. Pick remediation type: code-change (before_code + after_code) or
      non-code (remediation_steps).
   e. Extract verification.command from the test or gate that would confirm
      closure. For coverage gaps: "pytest path/to/test.py --cov=module".
      For anti-patterns: the ast-grep pattern that should find zero matches.
   f. Provenance:
      - GROUNDED when directly backed by a file:line citation, test output,
        or context-file quote.
      - DERIVED when the finding requires inference (e.g. "likely a God Object").
        Add one-sentence justification.
      - INCONCLUSIVE only when evidence is genuinely missing. Spell out what
        evidence would be needed.

3. Write to devforgeai/qa/recommendations/{STORY_ID}-qa-recommendations.md
   using the template as scaffolding.

4. Run: devforgeai-validate validate-qa-recommendations \
        --recommendations-file=<path> --format=json

5. If exit 0: proceed. If exit 1: read violations array and re-author the
   flagged entries. Never commit a qa-recommendations.md that exits 1.

6. If exit 2: IO error. Check project-root, file permissions, schema path.
```

---

## Worked Example: Converting a Prose Finding into a Recommendation Entry

**Source (existing qa-report.md prose, line 54 finding):**

> Missing `encoding='utf-8'` on `open()` call in `subagent_contract.py` line 54. A YAML contract containing non-ASCII bytes will decode successfully on WSL and raise UnicodeDecodeError on Windows.

**Recommendation entry:**

```yaml
- id: "REC-STORY-646-M-001"
  severity: MEDIUM
  provenance: GROUNDED
  title: "Missing encoding='utf-8' on open() in subagent_contract.py"
  file: "src/claude/scripts/devforgeai_cli/validators/subagent_contract.py"
  line: 54
  category: correctness
  blocking_release: false
  before_code: |
    with open(contract_path, 'r') as f:
        return yaml.safe_load(f), None
  after_code: |
    with open(contract_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f), None
  remediation_steps: null
  verification:
    command: "pytest tests/STORY-646/test_encoding_roundtrip.py::test_utf8_bom_contract_loads_on_all_platforms -v"
    expected: "1 passed"
  estimated_effort_minutes: 2
  dependencies: []
  references:
    - source: "src/claude/scripts/devforgeai_cli/validators/subagent_contract.py"
      line_range: [54, 56]
    - source: "Python docs"
      url: "https://docs.python.org/3/library/functions.html#open"
  cycle_first_seen: 1
```

**Verification Plan table row:**

| REC-ID | Command | Expected Output |
|--------|---------|-----------------|
| `REC-STORY-646-M-001` | `pytest tests/STORY-646/test_encoding_roundtrip.py::test_utf8_bom_contract_loads_on_all_platforms -v` | `1 passed` |

> **CRITICAL — Verification Plan backtick notation:** The `_validate_cross_references()` validator (`src/claude/scripts/devforgeai_cli/validators/qa_recommendations.py:213`) detects rec_ids using the regex `` r"`(REC-STORY-\d{3,}-[CHML]-\d{3})`" ``. The rec_id in the Verification Plan table cell **MUST** be wrapped in backticks: `` `REC-STORY-NNN-M-001` ``. Plain text (`REC-STORY-NNN-M-001` without backticks) and YAML key-value notation (`rec_id: "REC-STORY-NNN-M-001"`) are **NOT** recognized — the validator will report `"Recommendation REC-... has no entry in '## Verification Plan'."` even when the row is present.

**Provenance table row:**

| Recommendation | QA Phase |
|----------------|----------|
| `REC-STORY-646-M-001` | Phase-04-Code-Review |

No `derived_justifications` entry (this is GROUNDED). No `inconclusive_reasons` entry.

---

## Cycle History Authoring Rules

- **Append-only.** Each /dev remediation cycle OR /qa re-run appends one entry. Existing entries are never edited.
- **/qa invocations** emit entries with `source: "initial-qa"` (first run) or `source: "qa-validation"` (re-runs). Re-runs increment `cycle` and record newly-surfaced recommendations in `rec_ids_new`.
- **/dev --fix invocations** emit entries with `source: "remediation-cycle"` and populate `rec_ids_attempted`, `rec_ids_closed`, `rec_ids_deferred`.
- `completed_or_null` is `null` while a cycle is in flight and populated with ISO timestamp on cycle close.

---

## Common Validator Failures and Fixes

| Validator Finding | Root Cause | Fix |
|-------------------|-----------|-----|
| `"Required section '## Verification Plan' missing."` | Section omitted entirely | Add the section header and table, even if empty (place `_None._` if no entries). |
| `"Entry REC-... has severity MEDIUM but lives in Blocking Recommendations section"` | Severity-placement mismatch | Move entry to Advisory section OR elevate severity. |
| `"Recommendation REC-... has no entry in '## Verification Plan'."` | Forgot to add verification row | Add `| \`REC-ID\` | <command> | <expected> |` row. |
| `"Recommendation REC-... has no entry in '## Verification Plan'."` persists after adding a row | Verification Plan rec_id is not backtick-quoted — `_validate_cross_references()` (`qa_recommendations.py:213`) uses `` r"`(REC-STORY-\d{3,}-[CHML]-\d{3})`" `` which only matches backtick-enclosed ids | Use backtick notation: `` \`REC-STORY-NNN-M-001\` `` in the table cell. Plain text and YAML key-value notation are not detected. |
| `"Blocking entry missing required fields: ['verification']"` | Schema required field null | Populate `verification.command` and `verification.expected`. |
| `"Deferred CRITICAL recommendation REC-... has no adr_ref"` | CRITICAL deferral without ADR | Create ADR, populate `adr_ref: "ADR-054"`, OR demote severity, OR undefer. |
| `"detect-aspirational-language detected ambiguous/aspirational language"` | Used "should" / "could" / "consider" in prose | Replace with concrete verb + object. Re-run validator. |

---

## Relationship to Other Artifacts

| Artifact | Produced By | Consumed By | Mutation Pattern |
|----------|-------------|-------------|------------------|
| `qa-report.md` | /qa Phase 05 Step 5.1-5.5 | Humans, ad-hoc review | Overwritten on each /qa run |
| `gaps.json` | /qa Phase 05 | dev-preflight, CI/CD, /review-qa-reports | Overwritten on each /qa run |
| `qa-recommendations.md` | /qa Phase 05 Step 5.6 (NEW) | /dev Phase 01 Step 1.9.6 (NEW), validate-qa-recommendations CLI | **Append-only for Cycle History; overwritten sections for Blocking/Advisory/Verification Plan** |

**Why append-only for Cycle History:** Preserves the remediation timeline in one document. A reader can trace which recommendations were addressed in which cycle without reconstructing from git history.

**Why overwritten for Blocking/Advisory:** A re-QA after remediation reflects the **current** state of open findings. Previously-closed recommendations live in Cycle History, not back in Blocking.

---

## How /dev Consumes This File (Sprint 5+)

When `/dev STORY-NNN --fix` runs and `qa-recommendations.md` has open entries:

### Phase 0: Detection
- `dev-preflight` calls `qa_recommendations_status()` in-process and surfaces the `qa_recommendations` object in its JSON output (Sprint 4).
- If `qa_recommendations.open_count > 0`: `$REMEDIATION_MODE = true`, `$REMEDIATION_SOURCE = "qa-recommendations"`, `$OPEN_REC_IDS = qa_recommendations.open_rec_ids`.

### Phase 01 Step 01.9.6: Cycle Kickoff
- Invokes `devforgeai-validate phase-cycle-start --source=qa-recommendations --rec-ids=<open_rec_ids> --target-phase=02`.
- Opens a new `cycles[]` entry in `phase-state.json`.

### Phase 02 Step 1.5: Fetch Full Entries
- Invokes `devforgeai-validate qa-recommendations-get --story-id=... --rec-ids=<open_rec_ids>`.
- Returns full per-entry data including `before_code`, `after_code`, `remediation_steps`, `verification.command`, `verification.expected`.
- Stored as `$OPEN_REC_ENTRIES` for Phase 02 Step 2.3 (narrowed test generation) and Phase 03 Step 2.5.

### Phase 02 Step 2.3: Narrowed Test Generation
- test-automator receives `$OPEN_REC_ENTRIES` instead of full story ACs.
- Generates tests ONLY for the supplied REC entries using `entry.verification.command` as the test target.

### Phase 03 Step 2.5: Apply Remediation
For each entry in `$OPEN_REC_ENTRIES`:
- **Code-change path** (`before_code` + `after_code` non-null): `Edit(file_path=entry.file, old_string=entry.before_code, new_string=entry.after_code)`.
- **Steps path** (`remediation_steps` non-null): orchestrator interprets each step as an imperative action.
- After application: runs `entry.verification.command` and checks for `entry.verification.expected`. Pass adds to `$CLOSED_REC_IDS`; fail adds to `$FAILED_REC_IDS`.

### Phase 10 Step 2.5: Close Cycle
1. `devforgeai-validate phase-cycle-close --findings-closed=<closed_rec_ids>` — marks cycle completed in `phase-state.json`.
2. `devforgeai-validate mark-recommendations-closed --rec-ids=<closed_rec_ids> --cycle=N` — removes closed entries from Blocking/Advisory, appends Cycle History entry, increments "Closed in prior cycles" count.

### Re-QA Loop
User invokes `/qa STORY-NNN`. QA Phase 05 Step 5.4.5 calls `archive-qa-recommendations` (moves current file to `archive/STORY-NNN-cycle-N.md`), then Step 5.5 generates a fresh cycle-1 file.

### Authoring Implications
- **`before_code` / `after_code`**: Must be EXACT match of the target file content at the cited `file:line`. `/dev` Phase 03 uses `Edit(old_string=before_code, new_string=after_code)` which fails if the text doesn't match. Indentation, trailing newlines, and inline comments are significant.
- **`verification.command`**: Must be a real command that can be executed via `Bash()`. Example: `pytest tests/STORY-646/test_foo.py::test_bar -v`. `/dev` Phase 02 test-automator uses this to generate the matching test; Phase 03 runs it for pass/fail.
- **`verification.expected`**: A substring match applied to the command's stdout. Example: `1 passed`. Keep it concise and unambiguous.
- **`estimated_effort_minutes`**: Used by the orchestrator to estimate cycle duration but does NOT gate execution. Overestimates are harmless; underestimates cause no failure.

---

## Relationship to `story-template.md`

This template intentionally mirrors `story-template.md`'s architectural decisions:

- **SECTION_MANIFEST block at top.** Machine-parseable via `devforgeai-validate parse-manifest`. Downstream tools (including the validator itself) derive section expectations from this manifest rather than hard-coding.
- **YAML inside Markdown.** Same pattern as Technical Specification v2.0 in story files. Tooling reuse.
- **Explicit required/conditional status per section.** No implicit optional sections.

ADR-047 (template authority) and ADR-048 (template-workflow drift protections) apply to this template identically. Any change to the SECTION_MANIFEST must be backward-compatible or accompanied by a new ADR.

---

## Versioning

Template `template_version` is tracked in the frontmatter. Breaking changes (required-field additions, section removals) require:
1. Increment `template_version`.
2. Update `qa-recommendations-schema.json`.
3. Update `validate_qa_recommendations` to handle both versions (or explicitly refuse the old version with migration guidance).
4. New ADR documenting the change.

Current version: `1.0` (2026-04-14).

---

## References

- `.claude/rules/core/epistemic-integrity.md` — GROUNDED/DERIVED/INCONCLUSIVE classification.
- `.claude/rules/workflow/qa-output-fidelity.md` — Critical Rule 16 (full-fidelity requirements).
- `.claude/rules/core/quality-gates.md` — Gate 3 deferral protocol.
- `.claude/rules/core/citation-requirements.md` — Read-Quote-Cite-Verify grounding.
- `src/claude/skills/spec-driven-stories/assets/templates/story-template.md` — SECTION_MANIFEST pattern precedent.
- `src/claude/skills/spec-driven-qa/assets/schemas/gaps-schema.json` — sibling artifact schema (field conventions lifted verbatim).
