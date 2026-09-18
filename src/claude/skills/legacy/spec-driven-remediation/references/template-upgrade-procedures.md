# Template Upgrade Fix Procedures

**Purpose:** Authoritative procedures for applying `template/*` finding fixes during `/fix-story` Phase 03. This is the Single Source of Truth (SSOT) for template-upgrade transformations.

**Read by:** `/fix-story` Phase 03 Execution (`phase-03-execution.md` Step 1 for automated procedures, Step 2 for interactive procedures). Phase 04 Verification consumes the verification checks listed at the end of each procedure.

**Companion reference:** Detection rules live in `src/claude/skills/spec-driven-stories/references/template-version-validation.md`. Findings emitted by that reference are consumed by procedures here.

**Snippet library:** Section-body scaffolds referenced as `snippet_key` strings live in `src/claude/skills/spec-driven-remediation/assets/templates/template-upgrade-snippets.md`.

---

## Conventions Used Throughout

### Snippet lookup helper

```
def read_snippet(key: str) -> str:
    """Read the named snippet body from the snippet library."""
    Read(file_path = ".claude/skills/spec-driven-remediation/assets/templates/template-upgrade-snippets.md")
    Locate the literal markers `<!-- SNIPPET: {key} -->` and `<!-- END_SNIPPET -->`.
    Return the body text between the markers (exclusive of marker lines).
    If marker pair not found: HALT — snippet library is incomplete.
```

### Date constant

```
TODAY = current date as YYYY-MM-DD (ISO-8601 calendar date at fix-application time)
```

### AUDIT-DEFERRED marker constructor

```
def DEFERRED_MARKER(category: str) -> str:
    """Canonical marker format used by every procedure that scaffolds non-derivable content."""
    return f"<!-- AUDIT-DEFERRED: {category} — added by /fix-story --upgrade on {TODAY}. Populate when context available. -->"
```

**Important:** the marker prefix `<!-- AUDIT-DEFERRED: template/` is the allowlist key consumed by `custody-chain-workflow.md` Sub-phase 3a. Do not deviate from this format — variations will produce false-positive `provenance/broken_brainstorm_ref` findings on subsequent `/validate-stories` runs.

### Edit safety principle

Every transformation uses `Edit(file_path=..., old_string=..., new_string=...)` with explicit deltas. No `Write()` of entire-file replacements except in P1's append-at-end branch (and even there, the new content is purely additive — it appends, never overwrites existing content).

### Checkpoint state

All procedures update the per-finding entry in the remediation checkpoint at `tmp/.remediation-checkpoint-${SESSION_ID}.yaml` with `status: applied | deferred | failed` and a `change_summary` string. Phase 03 step records and Phase 04 verification both read this state.

---

## P1 — fix_template_missing_section_required_scaffold

**Trigger:** `template/missing_section` finding where `_section_status == "Required"`

**Classification:** automated

**Inputs:**

- `target_file` — story file path from `finding.affected[0]` resolved against `devforgeai/specs/Stories/`
- `section_name` — `finding._section_name` (e.g., `"Provenance"`, `"Technical Limitations"`)
- `snippet_key` — derived from `finding.remediation` (the substring inside `snippet key: '...'`) OR from the section name via the mapping in `template-version-validation.md` Rule 1 table

**Execution:**

```
snippet_body = read_snippet(snippet_key)
marker       = DEFERRED_MARKER("template/section_content_pending")

Read(file_path = target_file) → content

# Insertion anchor: insert BEFORE existing '## Notes' header if present,
# else append at end of file. '## Notes' is universally the last canonical H2.

IF "\n## Notes\n" in content:
    new_section_block = f"## {section_name}\n\n{marker}\n\n{snippet_body}\n\n"
    Edit(
        file_path  = target_file,
        old_string = "\n## Notes\n",
        new_string = f"\n{new_section_block}## Notes\n"
    )
ELSE:
    # No Notes section either — append at EOF with leading separator
    new_section_block = f"\n## {section_name}\n\n{marker}\n\n{snippet_body}\n"
    Write(file_path = target_file, content = content + new_section_block)
```

**Failure modes:**

- `read_snippet` fails (key not in library) → mark finding `failed`, record error in checkpoint, do NOT modify story file
- `Edit` fails (`old_string` not found) → mark finding `failed`; this implies story content changed between Phase 2 detection and Phase 3 execution (concurrent edit)

**Verification (Phase 04):**

```
grep -c "^## {section_name}$" {target_file}                       == 1
grep -c "AUDIT-DEFERRED: template/section_content_pending" {target_file}   >= 1
```

Both must hold for `status = applied`.

---

## P2 — fix_template_missing_section_optional

**Trigger:** `template/missing_section` finding where `_section_status == "Conditional"`

**Classification:** automated

**Difference from P1:** No AUDIT-DEFERRED marker. Conditional sections may be intentionally absent in some stories; inserting an empty scaffold is sufficient.

**Execution:** Identical to P1 except:

```
marker = ""                              # no marker
new_section_block = f"## {section_name}\n\n{snippet_body}\n\n"
# Rest of logic identical
```

**Verification:**

```
grep -c "^## {section_name}$" {target_file}  == 1
```

(No marker grep — Conditional sections do not carry one.)

---

## P3 — fix_template_missing_frontmatter_field_derivable

**Trigger:** `template/missing_frontmatter_field` finding where `_field_derivability == "derivable"`

**Classification:** automated

**Inputs:**

- `target_file` — story file path
- `field_name` — `finding._field_name` (one of: `advisory`, `source_gap`, `source_story`, `from_recommendations`, `source_recommendations`, `cycle_recorded`, `depends_on`)
- `default_value` — `finding._field_default`

**Execution:**

```
Read(file_path = target_file) → content

# Frontmatter is bounded by '---\n' (start of file) and the next '\n---\n'.
# We want to insert the new field as the LAST line before the closing '---'.

# Parse out the closing '---' position
fm_end_match = re.search(r"\n(.+?)\n---\n", content[3:], re.DOTALL)
# content[3:] skips the leading '---' opening delimiter
# group(1) is the last non-empty line before closing '---'

last_field_line = fm_end_match.group(1).rstrip().splitlines()[-1]
# The literal last line of frontmatter content

Edit(
    file_path  = target_file,
    old_string = f"{last_field_line}\n---",
    new_string = f"{last_field_line}\n{field_name}: {default_value}\n---"
)
```

**Edge case — old_string not unique:** if the last frontmatter line text happens to appear elsewhere in the file (rare, but possible for comment-style lines), `Edit` will refuse. Fallback:

```
# Use a more specific old_string by including 2 lines of context
prev_line = second-to-last frontmatter line
old_string = f"{prev_line}\n{last_field_line}\n---"
new_string = f"{prev_line}\n{last_field_line}\n{field_name}: {default_value}\n---"
```

**Verification:**

```
grep -c "^{field_name}:" {target_file}  == 1
```

---

## P4 — fix_template_missing_frontmatter_field_ambiguous

**Trigger:** `template/missing_frontmatter_field` finding where `_field_derivability == "ambiguous"`

**Classification:** interactive

**Currently applies to:** `type` field only (per Rule 4 in template-version-validation.md). Future ambiguous fields will hook here.

**Execution:**

```
field_name = finding._field_name   # "type" for now

# Hint extraction from story body to inform user choice
Read(file_path = target_file) → content
story_lower = content.lower()

hints = []
IF re.search(r"\bbug(?:fix)?\b|\bdefect\b|\bregression\b|\bissue\s+\d+\b", content, re.IGNORECASE):
    hints.append("bugfix")
IF re.search(r"\brefactor(?:ing)?\b|\brestructure\b|\bcleanup\b|\bextract(?:ed|ing)?\b", content, re.IGNORECASE):
    hints.append("refactor")
IF re.search(r"\bdocumentation\b|\bREADME\b|\.md\s|\bdocs?\s+(?:update|change|add)", content, re.IGNORECASE):
    hints.append("documentation")
hint_str = f" (story body suggests: {', '.join(hints)})" if hints else ""

AskUserQuestion:
    Question: f"Set frontmatter '{field_name}' to which value?{hint_str}"
    Header: "Story Type"
    Options:
        - label: "feature (Recommended for most stories)"
          description: "Standard new feature work; runs all /dev phases"
        - label: "bugfix"
          description: "Bug remediation; some /dev phases may be skipped"
        - label: "documentation"
          description: "Docs-only story; /dev skips TDD phases"
        - label: "refactor"
          description: "Code restructure; activates content-preservation checks"

# Parse user choice. The 'Other' fallback (free text) and any literal "defer" / "skip" → defer path.

IF user_choice in {"feature", "bugfix", "documentation", "refactor"}:
    chosen = user_choice    # strip "(Recommended...)" suffix when parsing label
    new_value = chosen
    # Apply P3 with default_value = chosen
    Invoke P3 logic with field_name=field_name, default_value=new_value
    Mark finding status = "applied"
    change_summary = f"Set '{field_name}: {chosen}'"

ELSE:  # user deferred via Other → "skip" or unrecognized response
    marker = DEFERRED_MARKER(f"template/section_content_pending — '{field_name}' requires user disambiguation")
    new_value = f"null   {marker}"
    Invoke P3 logic with field_name=field_name, default_value=new_value
    Mark finding status = "deferred"
    change_summary = f"Inserted '{field_name}: null' with deferral marker"
```

**Verification:**

```
grep -c "^{field_name}:" {target_file}  == 1
```

Identical to P3. The deferral marker (if present) is on the SAME line as the field, so the field-presence grep still matches.

---

## P5 — fix_template_legacy_workflow_status

**Trigger:** `template/legacy_workflow_status` finding

**Classification:** automated

**Inputs:**

- `target_file` — story file path

**Execution:**

```
Read(file_path = target_file) → content

# Locate '## Workflow Status' section (header line through end of section)
ws_re = re.compile(r"^## Workflow Status\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
ws_match = ws_re.search(content)

IF not ws_match:
    Mark finding "failed" — section disappeared between Phase 2 and Phase 3
    RETURN

existing_body = ws_match.group(1).rstrip()
full_old_section = ws_match.group(0).rstrip("\n")
# full_old_section is the literal text "## Workflow Status\n{body}" without trailing newline

# Best-effort parse of legacy checkpoint lines
# Pattern: "- YYYY-MM-DD: description text"
legacy_lines = re.findall(
    r"^\s*-\s*(\d{4}-\d{2}-\d{2})\s*:\s*(.+?)$",
    existing_body,
    re.MULTILINE
)
# Each tuple: (date, change_description)

# Build new section
header_snippet = read_snippet("change_log_table_header")
table_rows = []
FOR (date, change) in legacy_lines:
    table_rows.append(f"| {date} | (legacy migration) | (migrated by /fix-story --upgrade) | {change.strip()} | (unknown) |")

new_section_body = header_snippet
IF table_rows:
    new_section_body += "\n" + "\n".join(table_rows)

new_section = f"## Change Log\n\n{new_section_body}"

Edit(
    file_path  = target_file,
    old_string = full_old_section,
    new_string = new_section
)
```

**Failure modes:**

- `## Workflow Status` no longer present → mark `failed` (concurrent edit)
- No legacy lines parseable → still proceed; table will have header only (no rows)
- `Edit` fails (whitespace mismatch on `old_string`) → fall back: use a smaller `old_string` of just the header line + one body line to anchor

**Verification:**

```
grep -c "^## Change Log$" {target_file}        == 1
grep -c "^## Workflow Status$" {target_file}   == 0
```

Both must hold.

---

## P6 — fix_template_legacy_format_ac (per-AC interactive)

**Trigger:** `template/legacy_format` finding (one per markdown AC block; Phase 03 dispatches once per finding)

**Classification:** interactive

**Pre-fix capture (one-time per story, done by Phase 03 Step 1 before invoking ANY P6 fix for this story):**

```
# Capture pre-fix AC-header count for Phase 04 preservation heuristic
Read(file_path = target_file) → content
ac_section_match = re.search(r"^## Acceptance Criteria\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
IF ac_section_match:
    ac_body = ac_section_match.group(1)
    pre_count = len(re.findall(r"^### AC#?\d+:", ac_body, re.MULTILINE)) + \
                len(re.findall(r"^### \d+\.\s+\[", ac_body, re.MULTILINE))
ELSE:
    pre_count = 0

Update checkpoint:
    template_legacy_format_pre_ac_count:
        {story_id}: pre_count
```

Phase 04 reads `pre_count` from checkpoint and asserts `post_count_xml + post_count_deferred == pre_count` for the story.

**Per-finding execution (one invocation per AC finding):**

```
ac_header = finding._ac_header           # e.g., "### AC1: Hook Integration"
ac_id_match = re.search(r"AC#?(\d+)", ac_header)
ac_id = f"AC{ac_id_match.group(1)}" if ac_id_match else "AC1"

# Locate the legacy block in target_file
Read(file_path = target_file) → content
ac_section_match = re.search(r"^## Acceptance Criteria\n(.*?)(?=^## |\Z)",
                              content, re.MULTILINE | re.DOTALL)
ac_section_body = ac_section_match.group(1)

# Match this specific AC block — from its header to the next ### or end of section
header_escaped = re.escape(ac_header)
block_re = re.compile(rf"{header_escaped}\n(.*?)(?=\n### |\Z)", re.DOTALL)
block_match = block_re.search(ac_section_body)
IF not block_match:
    Mark finding "failed" — AC block disappeared
    RETURN

inner_body = block_match.group(1)
legacy_block = ac_header + "\n" + inner_body   # the literal text to replace

# Extract Given / When / Then from the inner body (best-effort regex)
given_match = re.search(r"\*{0,2}Given\*{0,2}\s*:?\s*(.+?)(?=\n\s*\*{0,2}(?:When|Then|And)\*{0,2}\s*:|\Z)",
                         inner_body, re.DOTALL | re.IGNORECASE)
when_match  = re.search(r"\*{0,2}When\*{0,2}\s*:?\s*(.+?)(?=\n\s*\*{0,2}(?:Then|And)\*{0,2}\s*:|\Z)",
                         inner_body, re.DOTALL | re.IGNORECASE)
then_match  = re.search(r"\*{0,2}Then\*{0,2}\s*:?\s*(.+?)\Z",
                         inner_body, re.DOTALL | re.IGNORECASE)

given_text = given_match.group(1).strip() if given_match else "(missing — populate manually)"
when_text  = when_match.group(1).strip()  if when_match  else "(missing — populate manually)"
then_text  = then_match.group(1).strip()  if then_match  else "(missing — populate manually)"

Display:
    f"Converting {ac_header} to XML:"
    f"  Given: {given_text}"
    f"  When:  {when_text}"
    f"  Then:  {then_text}"

AskUserQuestion:
    Question: f"Supply <verification> for {ac_id}? (Required for ac-compliance-verifier to run on this AC during /dev Phase 4.5/5.5)"
    Header: f"{ac_id} Verification"
    Options:
        - label: "Supply source files now (Recommended)"
          description: "Enter file paths and test file inline — produces fully verifiable XML AC"
        - label: "Convert structure only, leave verification empty + AUDIT-DEFERRED"
          description: "XML structure created but ac-compliance-verifier still cannot run on this AC"
        - label: "Skip this AC entirely"
          description: "Keep markdown form; AUDIT-DEFERRED marker added to the markdown block"

# Branch on user choice

CHOICE 1: "Supply source files now"

    AskUserQuestion (free-text via 'Other'):
        Question: f"List source file paths for {ac_id} (comma-separated, relative to project root):"
    user_input = parse user response
    source_files = [path.strip() for path in user_input.split(",") if path.strip()]

    AskUserQuestion (free-text via 'Other'):
        Question: f"Test file path for {ac_id} (relative to project root):"
    test_file = user response (single string)

    sf_xml = "\n".join(f"      <file>{p}</file>" for p in source_files)
    new_xml_block = (
        "```xml\n"
        f"<acceptance_criteria id=\"{ac_id}\">\n"
        f"  <given>{given_text}</given>\n"
        f"  <when>{when_text}</when>\n"
        f"  <then>{then_text}</then>\n"
        "  <verification>\n"
        "    <source_files>\n"
        f"{sf_xml}\n"
        "    </source_files>\n"
        f"    <test_file>{test_file}</test_file>\n"
        "  </verification>\n"
        "</acceptance_criteria>\n"
        "```"
    )
    new_block = f"{ac_header}\n\n{new_xml_block}\n"
    Edit(file_path=target_file, old_string=legacy_block, new_string=new_block)
    Mark finding status = "applied"
    change_summary = f"{ac_id}: markdown → XML with verification supplied"

CHOICE 2: "Convert structure only, leave verification empty + AUDIT-DEFERRED"

    marker = DEFERRED_MARKER("template/section_content_pending — verification block requires source_files. Populate before running /dev.")
    new_xml_block = (
        f"{marker}\n"
        "```xml\n"
        f"<acceptance_criteria id=\"{ac_id}\">\n"
        f"  <given>{given_text}</given>\n"
        f"  <when>{when_text}</when>\n"
        f"  <then>{then_text}</then>\n"
        "</acceptance_criteria>\n"
        "```"
    )
    new_block = f"{ac_header}\n\n{new_xml_block}\n"
    Edit(file_path=target_file, old_string=legacy_block, new_string=new_block)
    Mark finding status = "applied" (structurally converted; user accepted deferred verification)
    change_summary = f"{ac_id}: markdown → XML structure only (verification deferred)"

CHOICE 3: "Skip this AC entirely"

    marker = DEFERRED_MARKER(f"template/legacy_format — markdown AC retained per user choice on {TODAY}")
    # Insert marker on the line immediately after the AC header
    Edit(
        file_path  = target_file,
        old_string = ac_header,
        new_string = f"{ac_header}\n{marker}"
    )
    Mark finding status = "deferred"
    change_summary = f"{ac_id}: deferred (markdown retained)"
```

**Verification (Phase 04 AC-count preservation heuristic — see `phase-04-verification.md`):**

After ALL P6 fixes for the story complete:

```
pre_count          = checkpoint.template_legacy_format_pre_ac_count[story_id]
post_count_xml     = `grep -c '<acceptance_criteria id="AC[0-9]\+"' target_file`
post_count_deferred = `grep -c 'AUDIT-DEFERRED: template/legacy_format' target_file`
total_post = post_count_xml + post_count_deferred

ASSERT total_post == pre_count

IF mismatch:
    FOR each template/legacy_format finding for this story_id:
        Mark status = "failed"
    Display: f"AC count mismatch for {story_id}: pre={pre_count}, post={total_post}. Manual review required."
```

This guards against silent AC loss during markdown→XML conversion.

---

## P7 — fix_template_informal_dependency

**Trigger:** `template/informal_dependency_detected` finding

**Classification:** interactive

**Inputs:**

- `target_file` — story file path
- `dep_id` — `finding._dependency_id` (e.g., `STORY-044`)
- `matched_phrase` — `finding._matched_phrase` (full text of the original prose match)

**Execution:**

```
Read(file_path = target_file) → content

# Locate the line containing the matched prose
matched_line_match = re.search(rf"^(.*?{re.escape(matched_phrase)}.*?)$", content, re.MULTILINE)
IF not matched_line_match:
    Mark finding "failed" — prose disappeared
    RETURN
matched_line = matched_line_match.group(1)

# Build context for display (3 lines surrounding match)
lines = content.splitlines()
match_idx = next(i for i, line in enumerate(lines) if matched_phrase in line)
context_start = max(0, match_idx - 3)
context_end   = min(len(lines), match_idx + 4)
context_block = "\n".join(lines[context_start:context_end])

Display:
    f"Story body mentions informal dependency: '{matched_phrase}'"
    f"Context:\n{context_block}"
    f"Frontmatter depends_on currently does NOT include {dep_id}."

AskUserQuestion:
    Question: f"Promote informal '{dep_id}' to formal depends_on array?"
    Header: "Dependency"
    Options:
        - label: "Yes, add to depends_on (Recommended if dep is real)"
          description: f"Insert '{dep_id}' into frontmatter depends_on array"
        - label: "No, mark prose as informal reference"
          description: "Add AUDIT-DEFERRED marker noting the reference is non-blocking"
        - label: "Defer"
          description: "Leave as-is; revisit later"

CHOICE 1: "Yes, add to depends_on"

    # Parse current depends_on array from frontmatter
    fm_match = re.search(r"^depends_on:\s*(\[.*?\])", content, re.MULTILINE)
    IF fm_match:
        current_array_literal = fm_match.group(1)   # e.g., "[]" or '["STORY-044"]'
        # Strip brackets, split, normalize
        inner = current_array_literal.strip("[]").strip()
        current_items = [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]
    ELSE:
        # No depends_on key in frontmatter — handle via P3 logic
        # (this should be rare; Rule 3 would have emitted TPL-FM for missing depends_on)
        current_items = []
        current_array_literal = "[]"

    IF dep_id in current_items:
        # Already present (race) — no-op
        Mark finding status = "applied" (no-op resolved)
        RETURN

    new_items = current_items + [dep_id]
    new_array_literal = "[" + ", ".join(f'"{item}"' for item in new_items) + "]"

    IF fm_match:
        Edit(
            file_path  = target_file,
            old_string = f"depends_on: {current_array_literal}",
            new_string = f"depends_on: {new_array_literal}"
        )
    ELSE:
        # Insert depends_on key via P3 logic with default_value = new_array_literal
        Invoke P3 with field_name="depends_on", default_value=new_array_literal

    Mark finding status = "applied"
    change_summary = f"Promoted {dep_id} from prose to formal depends_on"

CHOICE 2: "No, mark prose as informal reference"

    marker = DEFERRED_MARKER(f"template/informal_dependency_detected — '{dep_id}' is an informal reference, not a blocking dependency")
    Edit(
        file_path  = target_file,
        old_string = matched_line,
        new_string = f"{matched_line}\n{marker}"
    )
    Mark finding status = "applied" (marked as informal — resolved)
    change_summary = f"Marked '{dep_id}' as informal reference"

CHOICE 3: "Defer"

    Mark finding status = "deferred"
    change_summary = f"Deferred {dep_id} dependency promotion"
    # No file edit
```

**Verification:**

For `CHOICE 1` (applied):

```
grep -c "^depends_on:.*{dep_id}" {target_file}  >= 1
```

For `CHOICE 2` (applied with marker):

```
grep -c "AUDIT-DEFERRED.*{dep_id}" {target_file}  >= 1
```

For `CHOICE 3` (deferred): no file-state verification; checkpoint records deferral.

---

## P8 — fix_template_version_bump (GATED — runs LAST)

**Trigger:** `template/version_drift` finding (umbrella; emitted last by detection)

**Classification:** automated (with gating)

**Critical:** This procedure MUST run after every other `template/*` finding on the same story has been processed. The detection reference (template-version-validation.md) emits this finding with `finding_id: TPL-ZZZ-version-bump` to ensure alphabetical sort places it last in the audit-table; Phase 03 Step 1 processes findings in audit order; therefore P8 runs last.

**Inputs:**

- `target_file` — story file path
- `gated_by` — `finding._gated_by`, list of sibling finding IDs from Rules 1-6 for this story
- `target_version` — parsed from `finding.summary` (pattern: `"canonical template is X.Y"`)

**Execution:**

```
# Gate check: read checkpoint state for sibling findings
Read(file_path = f"tmp/.remediation-checkpoint-${SESSION_ID}.yaml") → checkpoint

failed_siblings = []
FOR fid in gated_by:
    sibling = find_finding_by_id(checkpoint, fid)
    IF sibling and sibling.status == "failed":
        failed_siblings.append(fid)

# Read story to find current_version
Read(file_path = target_file) → content
fm_match = re.search(r'^format_version:\s*"([\d.]+)"', content, re.MULTILINE)
IF not fm_match:
    Mark finding "failed" — format_version key missing from frontmatter (this is the umbrella; without a current version we cannot bump)
    RETURN
current_version = fm_match.group(1)

# Parse target_version from finding.summary
summary = finding.summary
target_match = re.search(r"canonical template is ([\d.]+)", summary)
IF not target_match:
    Mark finding "failed" — summary malformed
    RETURN
target_version = target_match.group(1)

# Gate decision
IF failed_siblings:
    Display: f"Version bump GATED — {len(failed_siblings)} sibling finding(s) failed: {failed_siblings}. Deferring."
    marker = DEFERRED_MARKER(f"template/version_drift — gated by failed siblings: {failed_siblings}. Re-run /fix-story after resolving.")
    Edit(
        file_path  = target_file,
        old_string = f'format_version: "{current_version}"',
        new_string = f'format_version: "{current_version}"\n{marker}'
    )
    Mark finding status = "deferred"
    change_summary = f"Deferred version bump; {len(failed_siblings)} sibling(s) failed"
    RETURN

# All clear — apply bump
Edit(
    file_path  = target_file,
    old_string = f'format_version: "{current_version}"',
    new_string = f'format_version: "{target_version}"'
)
Mark finding status = "applied"
change_summary = f"Bumped format_version: {current_version} → {target_version}"
```

**Note on `deferred-with-marker` siblings:** P8 considers `status: "deferred"` as resolved (not failed). A user choosing to defer a P6 AC conversion or a P4 type-field disambiguation does NOT block the version bump. Only `status: "failed"` (verification mismatch, edit failure, content drift between detection and execution) blocks it. This matches user intent: deferred items have AUDIT-DEFERRED markers and are tracked for future fix sessions.

**Verification:**

For `status == "applied"`:

```
grep -c '^format_version: "{target_version}"$' {target_file}   == 1
grep -c '^format_version: "{current_version}"$' {target_file}  == 0
```

For `status == "deferred"`:

```
grep -c 'AUDIT-DEFERRED: template/version_drift' {target_file}  >= 1
grep -c '^format_version: "{current_version}"$' {target_file}   == 1   # unchanged
```

---

## P9 — fix_quality_non_deterministic_AC (interactive — Rev 4 lesson, STORY-573 F-009 pattern)

**Finding type:** `quality/non_deterministic_AC`
**Emitted by:** Sub-Phase 3d (custody-chain-workflow.md) / Function #10 sub-step 1f (context-validation.md)
**Classification:** interactive | structural (fix-actions-catalog.md classification matrix)
**Severity:** HIGH — blocks ac-compliance-verifier in /dev Phase 4.5/5.5 because no DIRECT/INFERRED match can be made against an undefined contract.

### Inputs

```
finding = {
  affected:    [story_id],
  type:        "non_deterministic_AC",
  evidence:    "<multi-line>: AC#N <then>: {ac_then_text[:200]}\nOpen Question (story line {N}): {oq_text}\nShared concepts ({K}): [...]\nFormat-asking pattern: {bool}",
  remediation: "<canonical resolution prose>",
  phase:       "3d"
}
```

The procedure parses `evidence` to extract: `ac_id`, `ac_then_text`, `oq_line_number`, `oq_text`.

### Procedure

1. **Read target files:**
   - `Read("devforgeai/specs/Stories/{story_id}-*.story.md")` — locate via Glob if exact filename unknown.
   - From the file, extract:
     - The full AC#`ac_id` XML block via `Grep(pattern='<acceptance_criteria id="AC{ac_id}"', -B=0, -A=15)` OR markdown block `Grep(pattern='### AC#{ac_id}:')`.
     - The full Open Questions item at line `oq_line_number` (Read with offset+limit to capture the exact `- [ ] ...` line).

2. **Display context to user:**
   ```
   Display: f"""
   STORY-{story_id} AC#{ac_id} depends on an unresolved Open Question.

   AC#{ac_id} <then> clause:
     {ac_then_text}

   Open Question (line {oq_line_number}):
     {oq_text}

   ac-compliance-verifier in /dev Phase 4.5/5.5 will not be able to make a
   DIRECT or INFERRED match against an undefined contract. The format/schema
   must be defined before /dev can complete cleanly.
   """
   ```

3. **AskUserQuestion (3-option choice):**
   ```
   Question: f"How should the format for AC#{ac_id} be resolved?"
   Header:   "Resolve AC format"
   Options:
     - label: "Embed format in AC inline (Recommended)"
       description: "I will prompt you for the format spec (regex, JSON schema,
         markdown layout, etc.). Procedure patches AC#{ac_id} <then> with the
         spec and removes the Open Question. Best for minimum diff and direct
         test-assertion mapping."
     - label: "Move format to Implementation Guide § Architecture Decisions"
       description: "I will prompt you for the format spec. Procedure adds a new
         '### ADR-style entry: {format topic}' subsection under
         '## Implementation Guide → Architecture Decisions' with the spec,
         updates AC#{ac_id} <then> to reference that section, and removes the
         Open Question. Best when AC clarity is preserved while keeping the
         format spec discoverable from the Implementation Guide."
     - label: "Defer with spike (NOT recommended)"
       description: "Procedure adds an inline <!-- AUDIT-DEFERRED:
         quality/non_deterministic_AC --> comment to AC#{ac_id} and recommends
         creating a separate research/spike story to investigate the format.
         The Open Question remains. /dev will still HALT at Phase 4.5/5.5
         unless the spike resolves the format first. Use only when EPIC-073's
         (or the relevant consumer's) parser spec genuinely does not yet exist."
     multiSelect: false
   ```

4. **Branch (a) — Embed inline:**
   - AskUserQuestion follow-up — free-text prompt:
     ```
     Question: f"Provide the format spec for {oq_topic}. Must be deterministic
       (regex, JSON schema, YAML structure, or markdown layout with explicit
       grammar). Will be inserted into AC#{ac_id} <then>."
     Header:   "Format spec"
     ```
     The user's answer is captured as `format_spec_text`.
   - Edit() the story file: replace the AC#`ac_id` `<then>` clause with the
     original Then plus the format spec. Suggested template:
     ```
     <then>
     {original_then_text}

     **Format specification:**
     {format_spec_text}
     </then>
     ```
   - Edit() the story file: remove the resolved item from the Open Questions
     section. Match by exact `oq_text` (most reliable) OR by Grep for the
     oq_line_number content.
   - Update any DoD items that reference the now-resolved format (Step 6 below).

5. **Branch (b) — Move to Implementation Guide:**
   - AskUserQuestion follow-up — same free-text prompt as branch (a) for
     `format_spec_text`.
   - AskUserQuestion follow-up — short label prompt for the subsection title:
     ```
     Question: "Short title for the new Architecture Decision subsection"
     Header:   "Section title"
     ```
     Captured as `format_topic_label`.
   - Edit() the story file under `## Implementation Guide` → `### Architecture
     Decisions`: insert a new sub-subsection
     ```
     #### {format_topic_label}

     {format_spec_text}
     ```
     If the `### Architecture Decisions` section is currently empty (e.g.,
     just the placeholder "(Populate with key architectural decisions affecting
     this story.)"), REPLACE that placeholder with the new sub-subsection.
     Otherwise APPEND.
   - Edit() the AC#`ac_id` `<then>` clause: insert a reference at the end:
     ```
     <then>
     {original_then_text}

     **Format specification:** See "## Implementation Guide → Architecture
     Decisions → {format_topic_label}".
     </then>
     ```
   - Edit() the story file: remove the resolved Open Question item.

6. **DoD propagation (a and b only):**
   - Grep DoD section for items whose text contains any content word from
     `oq_topic` (e.g., "milestone", "format", "parseable", "schema").
   - FOR each match: AskUserQuestion:
     ```
     Question: f"DoD item '{dod_item_text}' may reference the format you just
       resolved. Should it be updated? (Will be edited to mention the new
       inline format / Architecture Decision reference.)"
     Header:   "DoD update"
     Options:
       - "Update DoD item to reference resolved format"
       - "Leave DoD item unchanged"
     ```
   - Apply edits per user choice.

7. **Branch (c) — Defer with spike:**
   - Edit() the AC#`ac_id` block: insert an inline comment at the top of the
     `<acceptance_criteria>` element:
     ```
     <!-- AUDIT-DEFERRED: quality/non_deterministic_AC — format unresolved as
          of {date}. Spike story required before /dev can complete Phase 4.5.
          Original Open Question (story line {oq_line_number}): {oq_text} -->
     ```
   - DO NOT remove the Open Question item.
   - Display: f"""
     AC#{ac_id} marked AUDIT-DEFERRED. Open Question preserved.
     RECOMMENDED next steps:
     1. Run `/create-story` to create a spike story to investigate the format
        contract. Suggested title: 'Spike: define {oq_topic} format for
        {consumer_or_epic}'.
     2. Once the spike completes and provides a format spec, re-run
        `/fix-story {story_id}` and select Branch (a) or (b).
     3. Until then, `/dev {story_id}` will HALT at Phase 4.5 on AC#{ac_id}.
     """

### Verification

For branches (a) and (b):
```
grep -A 5 '<acceptance_criteria id="AC{ac_id}"' {story_file} | grep -E "Format specification" >= 1
grep -c "{oq_text_first_8_words}" {story_file}  == 0   # Open Question removed
```

For branch (c):
```
grep -c "AUDIT-DEFERRED: quality/non_deterministic_AC" {story_file}  >= 1
grep -c "{oq_text_first_8_words}" {story_file}  == 1   # Open Question preserved
```

### Rollback

- Branch (a): revert AC#`ac_id` `<then>` to pre-procedure text; re-add the
  Open Question item at the recorded line number.
- Branch (b): same AC#`ac_id` revert; delete the new Architecture Decision
  sub-subsection; re-add the Open Question item.
- Branch (c): delete the AUDIT-DEFERRED comment.
- All branches: revert any DoD propagation edits made in step 6.

### Citations

- Detection rule: `src/claude/skills/spec-driven-stories/references/context-validation.md` Function #10 sub-step 1f.
- Severity rationale: ac-compliance-verifier 100% HALT guarantee per `.claude/skills/spec-driven-dev/phases/phase-04.5-ac-verification.md` line 17.
- Open Question authoring convention: `src/claude/skills/spec-driven-stories/assets/templates/story-template.md` (Notes section, v3.1).

---

## P10 — fix_dependency_undeclared (interactive — STORY-573 F-006 pattern, Sub-Phase 3b Pass 2)

**Finding type:** `dependency/undeclared_dependency`
**Emitted by:** Sub-Phase 3b dependency graph in custody-chain-workflow.md (both Pass 1 in-scope-pairs and Pass 2 archived-deps coverage).
**Classification:** interactive | structural (fix-actions-catalog.md classification matrix).
**Severity:** HIGH — implementation correctness depends on the host artifact existing; the dependency graph used by sprint-planner and parallel-orchestration would not know to gate the story on the undeclared dep.

### Inputs

```
finding = {
  affected:    [story_a_id, story_b_id],   # story_a is the one to patch
  type:        "undeclared_dependency",
  evidence:    f"{story_a} content references '{story_b}' but depends_on={...}; {story_b} lives at {path} with status={...}",
  remediation: "Add {story_b} to {story_a} depends_on list. Use /fix-story (interactive)...",
  phase:       "3b"
}
```

The procedure parses `evidence` to extract: `story_a_path`, `story_b_path` (may be in `archive/long-term/`), `story_b_status`.

### Procedure

1. **Read target files:**
   - `Read("devforgeai/specs/Stories/{story_a_id}-*.story.md")` — the story to patch.
   - `Read(story_b_path)` — for status, title, and the Dependencies-section text content.
   - From `story_b`, extract: `title` (line 3 frontmatter), `status` (frontmatter), `points` (frontmatter).

2. **Display context to user:**
   ```
   Display: f"""
   STORY-{story_a_id} references STORY-{story_b_id} in ACs/spec but does NOT
   declare it in `depends_on`.

   STORY-{story_b_id} '{title}' (status: {status}, points: {points})
     Location: {story_b_path}

   Current STORY-{story_a_id} depends_on: {current_depends_on_array}

   The dependency graph used by /create-sprint and parallel-orchestration
   subagents reads `depends_on`. An undeclared dependency silently breaks
   that graph — sprint planning may schedule the dependent story before its
   prereq.
   """
   ```

3. **AskUserQuestion (3-option choice):**
   ```
   Question: f"How should the STORY-{story_a_id} -> STORY-{story_b_id} dependency be recorded?"
   Header:   "Resolve dependency"
   Options:
     - label: f"Add STORY-{story_b_id} to depends_on (Recommended)"
       description: "Procedure inserts STORY-{story_b_id} into the depends_on
         array (alphabetically) and adds a corresponding entry to the
         Dependencies section with status={status} and a generic 'Why' line.
         Best when STORY-{story_b_id} genuinely produces an artifact that
         STORY-{story_a_id} consumes."
     - label: "Document as informal reference, do not add to depends_on"
       description: "Procedure adds a comment in the Dependencies section
         documenting the reference as informational ('see also' rather than
         'depends on'). I will prompt you for a one-line reason. Use when
         the reference is a 'see also' / 'related work' citation, not a
         hard prerequisite."
     - label: "Remove the inline reference from STORY-{story_a_id}"
       description: "Procedure helps locate the reference(s) in
         STORY-{story_a_id} and strikes them. Use sparingly — only when the
         reference is genuinely incorrect (e.g., copy-paste error from a
         template). I will show each match and ask for confirmation."
     multiSelect: false
   ```

4. **Branch (a) — Add to depends_on (recommended):**
   - Edit() the frontmatter line `depends_on:` to insert `story_b_id` alphabetically:
     ```
     depends_on: ["STORY-535", "STORY-536", "STORY-537", "STORY-538"]
     ```
   - Edit() the Dependencies section. Locate the section via Grep for
     `## Dependencies` OR `### Prerequisite Stories`. Insert a new entry:
     ```
     - [{checkbox}] **STORY-{story_b_id}:** {title}
       - **Status:** {status}
       - **Why:** Referenced in ACs/spec. {generic_or_extracted_reason}
     ```
     `{checkbox}` is `x` if `status` is `QA Approved` or `Released`, else `[ ]`.
     `{generic_or_extracted_reason}` defaults to "Implementation depends on this
     story's deliverable being available." If the evidence field includes a
     specific phrase (e.g., "produces src/claude/skills/researching-market/SKILL.md"),
     extract and use that.

5. **Branch (b) — Document as informal:**
   - AskUserQuestion follow-up:
     ```
     Question: f"One-line reason for treating STORY-{story_b_id} as informal
       (not a hard dependency):"
     Header:   "Informal reason"
     ```
     Captured as `informal_reason`.
   - Edit() the Dependencies section to add (NOT as a checkbox item — as a comment):
     ```
     <!-- Informal reference to STORY-{story_b_id}: {informal_reason}.
          Not a hard dependency (does NOT appear in depends_on frontmatter). -->
     ```
   - DO NOT modify the depends_on frontmatter array.

6. **Branch (c) — Remove inline reference:**
   - Grep the story file for every line containing `STORY-{story_b_id}`.
   - FOR each match: Display the line with 2 lines of context. AskUserQuestion:
     ```
     Question: f"Remove this reference?\n  Line: {line}"
     Header:   "Remove reference"
     Options:
       - "Remove this line"
       - "Keep this line (skip)"
     ```
   - Apply edits per user choice for each match.

### Verification

For branch (a):
```
grep -E '^depends_on: \[.*"STORY-{story_b_id}".*\]$' {story_a_file}  == 1
grep -c "STORY-{story_b_id}" {story_a_file}  >= 2   # depends_on + Dependencies section
```

For branch (b):
```
grep -c "Informal reference to STORY-{story_b_id}" {story_a_file}  >= 1
grep -E '^depends_on: \[.*"STORY-{story_b_id}".*\]$' {story_a_file}  == 0   # NOT in depends_on
```

For branch (c):
```
grep -c "STORY-{story_b_id}" {story_a_file}  decreases from initial value
```

### Rollback

- Branch (a): remove `story_b_id` from depends_on array; remove the Dependencies section entry.
- Branch (b): remove the `<!-- Informal reference... -->` comment.
- Branch (c): restore removed lines via `git diff` review (procedure should commit a checkpoint before edits to enable this).

### Citations

- Detection rule (Pass 1 + Pass 2): `src/claude/skills/spec-driven-stories/references/custody-chain-workflow.md` Sub-Phase 3b dependency graph block.
- Severity rationale: dependency-graph-analyzer at `.claude/agents/dependency-graph-analyzer.md` blocks on invalid statuses but not on undeclared deps; this procedure prevents the silent-miss from propagating.
- Related procedure (similar mechanical action, different finding type): P7 `fix_template_informal_dependency` above.

---

## Cross-Story Drift Handling

The `template/cross_story_drift` finding type (emitted by Sub-phase 3f in chain mode) is classified as **advisory** — no fix procedure exists. Resolution path:

1. The finding is reported in the audit file Section 4 with `advisory` classification.
2. Users run `/fix-story --upgrade` on each affected story individually.
3. After upgrading all stories in the epic, re-running `/validate-stories EPIC-NNN --chain` produces no `template/cross_story_drift` findings (idempotency filter satisfies version equality).

No automation; coordination is intentional.

---

## Procedure Index Quick Reference

| Finding type | Procedure | Classification |
|---|---|---|
| `template/missing_section` (Required) | P1 | automated |
| `template/missing_section` (Conditional) | P2 | automated |
| `template/missing_frontmatter_field` (derivable) | P3 | automated |
| `template/missing_frontmatter_field` (ambiguous) | P4 | interactive |
| `template/legacy_workflow_status` | P5 | automated |
| `template/legacy_format` | P6 | interactive |
| `template/informal_dependency_detected` | P7 | interactive |
| `template/version_drift` | P8 | automated (gated) |
| `template/cross_story_drift` | none | advisory |

---

## Citations

- **Custody Chain Finding schema:** `src/claude/skills/spec-driven-stories/references/context-validation.md` lines 728-740
- **Detection rules:** `src/claude/skills/spec-driven-stories/references/template-version-validation.md` (sibling reference)
- **Phase 03 dispatch convention:** `src/claude/skills/spec-driven-remediation/phases/phase-03-execution.md`
- **Phase 04 verification convention:** `src/claude/skills/spec-driven-remediation/phases/phase-04-verification.md` (plus AC-count preservation extension)
- **AUDIT-DEFERRED marker convention:** `src/claude/skills/spec-driven-remediation/phases/phase-03-execution.md` line 136
- **Canonical template SECTION_MANIFEST:** `src/claude/skills/spec-driven-stories/assets/templates/story-template.md` lines 9-172
- **Snippet library:** `src/claude/skills/spec-driven-remediation/assets/templates/template-upgrade-snippets.md`
