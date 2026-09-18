# Template Version Validation Reference

**Purpose:** Detect story-file template-version drift. Read by `/validate-stories` Phase 2 (Context Validation), specifically by Function #18 `validate_story_template_version()` in `context-validation.md`.

**Outputs:** Custody Chain Finding objects conforming to the schema in `context-validation.md` lines 728-740 (the `finding_id / severity / type / affected / summary / evidence / remediation / verification / phase` schema). Findings flow into the audit file at `devforgeai/qa/audit/custody-chain-audit-{scope}.md` Section 4.

**Determinism:** Rule-based. Every detection rule below is mechanical — Claude follows the rule literally and emits findings (or doesn't) based on observable structural facts. Ambiguity → INCONCLUSIVE (no finding emitted), per `.claude/rules/core/epistemic-integrity.md`.

**Consumers:** `/fix-story` Phase 03 reads the emitted findings and applies the appropriate procedure from `template-upgrade-procedures.md` (procedures P1-P8).

---

## Scope and Activation

Activated for **every story in scope** during `/validate-stories` Phase 2. Applies to:
- Single-story mode: `/validate-stories STORY-NNN`
- Multi-story chain mode: `/validate-stories EPIC-NNN --chain` or range syntax
- All-stories mode: `/validate-stories all`

**NOT activated for:** ad-hoc story content checks outside Phase 2.

---

## Inputs

Read **ONCE per Phase 2 invocation** (cache the rules across all stories in scope to avoid redundant token use):

### Input 1 — Canonical story template

```
File: src/claude/skills/spec-driven-stories/assets/templates/story-template.md
```

Extract two pieces of data:

1. **`template_version`** — the value at frontmatter line 3 (currently `"3.1"` as of 2026-05-10).
2. **`SECTION_MANIFEST`** — the YAML between the literal markers `<!-- SECTION_MANIFEST` and `END_SECTION_MANIFEST -->` (currently lines 9-172). Parse the YAML; the `sections:` list is the authoritative registry. Each entry has fields: `name`, `header_level`, `status` (one of `Required` / `Conditional` / `Optional`), and optionally `line_range` and `validation` sub-blocks.

### Input 2 — This reference file

```
File: src/claude/skills/spec-driven-stories/references/template-version-validation.md
```

You are reading it now. The rules below are executed against each story file.

### Input 3 — Per-story input

```
File: <story_file_path>   # supplied by Phase 2 for each story in scope
```

For each story in scope, read the file once.

---

## Pre-flight Filters (apply in order)

Before applying any detection rule, run these two filters per story. If either fires, emit ZERO findings for that story.

### Filter A — Grandfather completed stories

```
IF story.frontmatter.status ∈ {"QA Approved", "Released"}
   AND user did NOT pass `--include-completed`:
    Emit NO template/* findings for this story.
    Optionally record `skip_reason: "grandfathered"` in the audit narrative.
    SKIP remaining rules for this story.
```

Rationale: completed-state stories are immutable historical artifacts. Upgrading them would diff-pollute released work and break provenance.

The `--include-completed` flag is a command-layer argument captured at `/validate-stories` invocation time. Phase 2 receives it as context.

### Filter B — Idempotency

```
story_version    = parse_version(story.frontmatter.format_version)
canonical_version = parse_version(canonical.template_version)
# parse_version splits on '.' and casts to (major, minor) integer tuple; malformed → (0, 0)

IF story_version >= canonical_version:
    Emit NO template/* findings for this story.
    The story is at or beyond the canonical version. No drift.
    SKIP remaining rules for this story.
```

This makes the validation idempotent: re-running `/validate-stories` after a successful `/fix-story --upgrade` produces zero new findings.

---

## Detection Rules

Execute Rules 1–6 in order against each story that passed both pre-flight filters. Each rule may emit zero or more findings. After Rules 1–6, emit the Rule-Z version-drift umbrella finding.

### Rule 1 — Missing Section (Required and Conditional)

**Scope:** H2 sections only (`header_level: 2` entries in SECTION_MANIFEST). H3 subsections are out of scope for v1 of this validation.

```
FOR each entry in SECTION_MANIFEST.sections:
  IF entry.header_level != 2:
    SKIP
  IF entry.status == "Optional":
    SKIP  # Optional sections do not produce findings when absent

  # Anchored exact-text H2 header match
  pattern = f"^## {entry.name}$"   # multiline, anchored to line boundaries
  IF re.search(pattern, story_content, re.MULTILINE) matches:
    SKIP  # Section is present

  # Section is missing — emit finding
  Emit:
    finding_id:  TPL-MS-{seq}      # seq increments 001, 002, ... per story
    severity:    "MEDIUM" IF entry.status == "Required" ELSE "LOW"
    type:        "template/missing_section"
    affected:    [story.id]
    summary:     f"Section '## {entry.name}' missing ({entry.status} per SECTION_MANIFEST)"
    evidence:    f"No '^## {entry.name}$' header in story body"
    remediation: f"Insert '## {entry.name}' section + scaffold from template-upgrade-snippets.md (snippet key: '{snippet_key_for(entry.name)}')"
    verification: f"grep -c '^## {entry.name}$' {story_file} == 1"
    phase:       "2"
    _section_status: entry.status     # internal, drives /fix-story procedure selection
    _section_name:   entry.name
```

**Snippet-key mapping** (used in the `remediation` field, consumed by `/fix-story` procedures P1/P2):

| Section name | Snippet key |
|---|---|
| `Provenance` | `provenance_scaffold` |
| `Implementation Guide` | `implementation_guide_scaffold` |
| `Technical Limitations` | `technical_limitations_scaffold` |
| `Change Log` | `change_log_table_header` |
| `Acceptance Criteria Verification Checklist` | `ac_verification_checklist_scaffold` |
| `Edge Cases` | `edge_cases_scaffold` |
| `Notes` | `notes_scaffold` |
| *(any other section)* | `generic_section_scaffold` |

**Variant headers note:** This rule uses exact-text H2 match. A story with `## Provenance Notes` (not the canonical `## Provenance`) emits a `missing_section` finding for `Provenance`. Reconciling variant headers is out of scope for v1 and becomes a separate manual concern. The conservative behavior (flag missing canonical) is preferred over fuzzy matching that could miss real drift.

### Rule 2 — Legacy Markdown AC Format

**Scope:** stories that have a `## Acceptance Criteria` section (this rule skips if Rule 1 already flagged the section as missing).

```
ac_section_match = re.search(r"^## Acceptance Criteria\n(.*?)(?=^## |\Z)",
                              story_content,
                              re.MULTILINE | re.DOTALL)
IF not ac_section_match:
  SKIP  # Rule 1 already flagged this

ac_section_body = ac_section_match.group(1)

# Identify AC blocks. An AC block starts at any of these headers
# (case-sensitive) and ends at the next ### header or end of section.
ac_header_patterns = [
    r"^### AC#\d+:",     # template v2.6+ canonical
    r"^### AC\d+:",      # template v2.0-v2.5
    r"^### \d+\.\s+\[",  # very-early checkbox format
]

# Concatenated multiline regex for boundary detection
combined_re = re.compile("|".join(ac_header_patterns), re.MULTILINE)
header_matches = list(combined_re.finditer(ac_section_body))
IF not header_matches:
  SKIP  # No AC headers — Rule 1 region concern

# For each AC block, check whether an XML <acceptance_criteria> fence appears
boundaries = [m.start() for m in header_matches] + [len(ac_section_body)]
FOR i in range(len(header_matches)):
  block = ac_section_body[boundaries[i]:boundaries[i + 1]]
  header_text = header_matches[i].group(0).strip()

  # Case-insensitive substring check is sufficient — the canonical XML opens
  # with literal `<acceptance_criteria` and would never appear in markdown prose.
  IF "<acceptance_criteria" in block.lower():
    SKIP  # Already XML

  # Emit one finding per legacy AC block
  Emit:
    finding_id:  TPL-AC-{seq}
    severity:    "HIGH"                # blocks ac-compliance-verifier in /dev Phase 4.5/5.5
    type:        "template/legacy_format"
    affected:    [story.id]
    summary:     f"AC block '{header_text}' uses markdown Given/When/Then instead of XML <acceptance_criteria>"
    evidence:    f"Header '{header_text}' has no <acceptance_criteria> fence in its block"
    remediation: "Convert to XML <acceptance_criteria> block. Interactive — user must supply <verification><source_files> per AC."
    verification: f"grep -c '<acceptance_criteria id=\"AC[0-9]\\+\"' {story_file} accounts for {header_text} OR AUDIT-DEFERRED marker present"
    phase:       "2"
    _ac_header:  header_text
    _ac_block_pre_count: len(header_matches)   # total AC headers in section, used by Phase 04 AC-count preservation
```

### Rule 3 — Missing Frontmatter Field (derivable defaults)

```
DERIVABLE_FRONTMATTER = {
  "advisory":              "false",
  "source_gap":            "null",
  "source_story":          "null",
  "from_recommendations":  "false",
  "source_recommendations": "null",
  "cycle_recorded":        "null",
  "depends_on":            "[]",
}

FOR each (field, default) in DERIVABLE_FRONTMATTER.items():
  IF field in story.frontmatter:
    SKIP  # Field present, no drift

  Emit:
    finding_id:  TPL-FM-{seq}
    severity:    "LOW"
    type:        "template/missing_frontmatter_field"
    affected:    [story.id]
    summary:     f"Frontmatter field '{field}' missing (v3.1 schema)"
    evidence:    f"Story frontmatter does not contain key '{field}'"
    remediation: f"Insert '{field}: {default}' in frontmatter (derivable default)"
    verification: f"grep -c '^{field}:' {story_file} == 1"
    phase:       "2"
    _field_name:        field
    _field_default:     default
    _field_derivability: "derivable"
```

### Rule 4 — Missing Frontmatter Field (ambiguous — requires user judgment)

```
AMBIGUOUS_FRONTMATTER = ["type"]   # type field can be feature|bugfix|documentation|refactor

FOR each field in AMBIGUOUS_FRONTMATTER:
  IF field in story.frontmatter:
    SKIP

  Emit:
    finding_id:  TPL-FM-{seq}
    severity:    "MEDIUM"
    type:        "template/missing_frontmatter_field"
    affected:    [story.id]
    summary:     f"Frontmatter field '{field}' missing (v3.1 schema, ambiguous default)"
    evidence:    f"Story frontmatter does not contain key '{field}'; story body does not deterministically disambiguate"
    remediation: f"Interactive: user chooses value via AskUserQuestion, or marks as null + AUDIT-DEFERRED"
    verification: f"grep -c '^{field}:' {story_file} == 1"
    phase:       "2"
    _field_name:        field
    _field_derivability: "ambiguous"
```

### Rule 5 — Legacy Workflow Status

```
has_workflow_status = bool(re.search(r"^## Workflow Status$", story_content, re.MULTILINE))
has_change_log      = bool(re.search(r"^## Change Log$",      story_content, re.MULTILINE))

IF has_workflow_status AND NOT has_change_log:
  Emit:
    finding_id:  TPL-WS-001
    severity:    "MEDIUM"
    type:        "template/legacy_workflow_status"
    affected:    [story.id]
    summary:     "Legacy '## Workflow Status' section present; should be unified '## Change Log' table"
    evidence:    "Story body contains '^## Workflow Status$' but not '^## Change Log$'"
    remediation: "Rename section to '## Change Log' and convert checkpoint list to table per template-upgrade-snippets.md (snippet key: 'change_log_table_header')"
    verification: "grep -c '^## Change Log$' {story_file} == 1 AND grep -c '^## Workflow Status$' {story_file} == 0"
    phase:       "2"
```

Note: if BOTH headers are present (rare), no finding — the story is mid-migration and likely needs manual review.

### Rule 6 — Informal Dependency Detected

Scan story body (everything **outside** the YAML frontmatter, including all H2/H3 sections) for any of these phrasings, case-insensitive, matched against `STORY-\d+` capture:

| Phrasing pattern | `_dependency_direction` |
|---|---|
| `Depends?\s+on\s+(STORY-\d+)` | forward |
| `Builds?\s+on\s+(STORY-\d+)` | forward |
| `Requires?\s+(STORY-\d+)` | forward |
| `After\s+(STORY-\d+)\s+(?:ships?|completes?|lands?|is\s+done)` | forward |
| `Once\s+(STORY-\d+)\s+(?:ships?|completes?|lands?|is\s+done)` | forward |
| `Blocked\s+by\s+(STORY-\d+)` | forward |
| `Blocks?\s+(STORY-\d+)` | reverse |

```
declared = set(story.frontmatter.depends_on or [])
seen     = set()

FOR each matched phrase in story body:
  story_ref = extract STORY-NNN from match (uppercase normalize)
  direction = pattern's _dependency_direction column

  IF direction == "reverse":
    SKIP  # story_id is the blocker, not the blocked party

  IF story_ref in declared:
    SKIP  # Formal dependency satisfied

  IF story_ref in seen:
    SKIP  # Already emitted for this story_ref in this story

  seen.add(story_ref)

  Emit:
    finding_id:  TPL-ID-{seq}
    severity:    "MEDIUM"
    type:        "template/informal_dependency_detected"
    affected:    [story.id]
    summary:     f"Story body mentions informal dependency on '{story_ref}' but it is not in frontmatter depends_on"
    evidence:    f"Match: '{full_match_text}' at line {line_no}; depends_on currently: {sorted(declared)}"
    remediation: f"Interactive: promote '{story_ref}' to formal depends_on array, OR mark prose as informal reference with AUDIT-DEFERRED, OR defer"
    verification: f"grep -c '^depends_on:.*{story_ref}' {story_file} >= 1 OR AUDIT-DEFERRED marker present near matched line"
    phase:       "2"
    _dependency_id:   story_ref
    _matched_phrase:  full_match_text
```

### Rule 7 — Custody-Chain Marker Recognition (NEGATIVE — sets a flag, emits no finding)

This rule runs once per story and sets a flag for downstream consumption by `custody-chain-workflow.md` Sub-phase 3a.

```
provenance_section = extract H2 section body with header '^## Provenance$'

IF provenance_section is not None:
  IF re.search(r"<!--\s*AUDIT-DEFERRED:\s*template/section_content_pending", provenance_section):
    Set story.flags.provenance_intentionally_deferred = true
ELSE:
  story.flags.provenance_intentionally_deferred = false  # default
```

This flag is consumed by Sub-phase 3a's broken-brainstorm-ref detection. When `true`, 3a SKIPS emission of `provenance/broken_brainstorm_ref` for this story, treating the empty/scaffolded Provenance as intentional deferral. This prevents `/fix-story --upgrade`-inserted Provenance scaffolds from being re-flagged on subsequent `/validate-stories` runs.

### Rule Z — Version-Drift Umbrella (emitted LAST)

After Rules 1–6 have produced all their findings for the story, emit ONE final umbrella finding. This finding's `finding_id` uses the sentinel prefix `TPL-ZZZ-` to ensure alphabetical sort places it last in the audit table — which makes `/fix-story` Phase 03 Step 1 apply the version-bump fix LAST.

```
sibling_ids = [f.finding_id for f in findings_emitted_so_far]   # all TPL-* IDs from Rules 1-6

Emit:
  finding_id:  "TPL-ZZZ-version-bump"
  severity:    "MEDIUM"
  type:        "template/version_drift"
  affected:    [story.id]
  summary:     f"Story format_version is {story_version}; canonical template is {target_version}"
  evidence:    f"Frontmatter 'format_version: {story_version}' < canonical 'template_version: {target_version}'"
  remediation: f"After all sibling findings resolve to applied or deferred, bump 'format_version' to '{target_version}'. Gated by: {sibling_ids}"
  verification: f"grep -c '^format_version: \"{target_version}\"$' {story_file} == 1 AND all _gated_by findings have status in ('applied','deferred')"
  phase:       "2"
  _gated_by:   sibling_ids
```

If `sibling_ids` is empty (story passed all Rules 1-6 with zero findings) but `story_version < target_version`, this can only happen if the story already has all v3.1 sections and frontmatter but the version field literally lags. Still emit the umbrella; P8 will simply do the version bump with no gating concern.

---

## Output: Custody Chain Finding Schema

Every finding emitted by Rules 1-6 and Rule-Z conforms to the canonical schema from `context-validation.md` lines 728-740:

```
finding_id:   "TPL-CAT-NNN"          # TPL-MS, TPL-AC, TPL-FM, TPL-WS, TPL-ID, TPL-ZZZ, TPL-XS (Sub-phase 3f)
severity:     "HIGH | MEDIUM | LOW"
type:         "template/{specific}"
affected:     [<story_id>, ...]
summary:      "One-line description"
evidence:     "Quoted observation from source file"
remediation:  "Numbered or imperative fix instruction; references /fix-story procedure"
verification: "Grep command pattern that confirms fix"
phase:        "2"  (or "3f" for cross-story drift)
```

Plus internal `_*` keys consumed by `/fix-story` procedures (preserved through audit-file synthesis). Internal keys do NOT appear in the human-readable audit-file Findings table but ARE preserved in any structured JSON sidecar.

### Severity assignment summary

| Finding type | Severity | Rationale |
|---|---|---|
| `template/legacy_format` (markdown AC) | HIGH | Blocks ac-compliance-verifier subagent in `/dev` Phase 4.5/5.5 → cannot run TDD |
| `template/missing_section` (Required) | MEDIUM | Workflow degradation (custody chain incomplete, pre-commit DoD hook breaks, etc.) |
| `template/missing_section` (Conditional) | LOW | Documentation gap; no runtime risk |
| `template/missing_frontmatter_field` (derivable) | LOW | Default value mechanically derivable; auto-fix is safe |
| `template/missing_frontmatter_field` (ambiguous) | MEDIUM | Requires user judgment; wrong default changes `/dev` phase routing |
| `template/legacy_workflow_status` | MEDIUM | Feedback tools and Phase 07/09 history parsing degraded |
| `template/informal_dependency_detected` | MEDIUM | Dependency-graph blind spot during parallel execution |
| `template/version_drift` (umbrella) | MEDIUM | Drives the version bump; gated by sibling resolution |
| `template/cross_story_drift` (Sub-phase 3f only) | LOW | Advisory |

---

## Worked Examples

These examples anchor expected behavior. Each example shows the input story characteristics and the expected emitted findings. They serve the same anchoring role as the multishot examples in `fix-actions-catalog.md` lines 509-606.

The corresponding example story files live under `src/claude/skills/spec-driven-stories/references/examples/` and may be Read for ground-truth verification.

### Worked Example 1 — pre-Provenance v2.0 story

**Input:** `src/claude/skills/spec-driven-stories/references/examples/old-story-v2.0.story.md`

- `frontmatter.format_version`: `"2.0"`
- `frontmatter.status`: `Backlog` (not grandfathered)
- `frontmatter` missing: `type`, `depends_on`, `advisory`, `source_gap`, `source_story`, `from_recommendations`, `source_recommendations`, `cycle_recorded`
- Body has: `## Description`, `## Acceptance Criteria` (3 markdown ACs), `## Workflow Status`, `## Notes`
- `## Notes` body contains: `"Depends on STORY-044 informally mentioned here."`
- Missing H2 sections: `Provenance`, `Technical Specification`, `Implementation Guide`, `Technical Limitations`, `Non-Functional Requirements (NFRs)`, `Dependencies`, `Test Strategy`, `Acceptance Criteria Verification Checklist`, `Edge Cases`, `Definition of Done`, `Change Log`

**Expected findings (~25):**

| Finding ID | Severity | Type | Notes |
|---|---|---|---|
| TPL-MS-001 | MEDIUM | template/missing_section | `Provenance` (Required) |
| TPL-MS-002 | MEDIUM | template/missing_section | `Technical Specification` (Required) |
| TPL-MS-003 | LOW | template/missing_section | `Implementation Guide` (Conditional) |
| TPL-MS-004 | MEDIUM | template/missing_section | `Technical Limitations` (Required) |
| TPL-MS-005 | MEDIUM | template/missing_section | `Non-Functional Requirements (NFRs)` (Required) |
| TPL-MS-006 | MEDIUM | template/missing_section | `Dependencies` (Required) |
| TPL-MS-007 | MEDIUM | template/missing_section | `Test Strategy` (Required) |
| TPL-MS-008 | MEDIUM | template/missing_section | `Acceptance Criteria Verification Checklist` (Required) |
| TPL-MS-009 | MEDIUM | template/missing_section | `Edge Cases` (Required) |
| TPL-MS-010 | MEDIUM | template/missing_section | `Definition of Done` (Required) |
| TPL-MS-011 | MEDIUM | template/missing_section | `Change Log` (Required) |
| TPL-AC-001 | HIGH | template/legacy_format | AC1 markdown |
| TPL-AC-002 | HIGH | template/legacy_format | AC2 markdown |
| TPL-AC-003 | HIGH | template/legacy_format | AC3 markdown |
| TPL-FM-001 | LOW | template/missing_frontmatter_field | `advisory` |
| TPL-FM-002 | LOW | template/missing_frontmatter_field | `source_gap` |
| TPL-FM-003 | LOW | template/missing_frontmatter_field | `source_story` |
| TPL-FM-004 | LOW | template/missing_frontmatter_field | `from_recommendations` |
| TPL-FM-005 | LOW | template/missing_frontmatter_field | `source_recommendations` |
| TPL-FM-006 | LOW | template/missing_frontmatter_field | `cycle_recorded` |
| TPL-FM-007 | LOW | template/missing_frontmatter_field | `depends_on` |
| TPL-FM-008 | MEDIUM | template/missing_frontmatter_field | `type` (ambiguous) |
| TPL-WS-001 | MEDIUM | template/legacy_workflow_status | — |
| TPL-ID-001 | MEDIUM | template/informal_dependency_detected | STORY-044 |
| TPL-ZZZ-version-bump | MEDIUM | template/version_drift | umbrella; gated_by all preceding |

`story.flags.provenance_intentionally_deferred = false` (no Provenance section at all; Rule 7 default).

### Worked Example 2 — mid-evolution v2.7 story

**Input:** `src/claude/skills/spec-driven-stories/references/examples/old-story-v2.7.story.md`

- `frontmatter.format_version`: `"2.7"`
- `frontmatter` has `depends_on: []`, missing: `type`, `advisory`, `source_gap`, `source_story`, `from_recommendations`, `source_recommendations`, `cycle_recorded`
- Body has: `## Description`, `## Provenance` (populated), `## Acceptance Criteria` (2 markdown ACs), `## Definition of Done`, `## Notes`
- Missing H2 sections: `Technical Specification`, `Implementation Guide`, `Technical Limitations`, `NFRs`, `Dependencies`, `Test Strategy`, `AC Verification Checklist`, `Edge Cases`, `Change Log`

**Expected findings (~16):**

| Finding ID | Severity | Type | Notes |
|---|---|---|---|
| TPL-MS-001 | MEDIUM | template/missing_section | `Technical Specification` |
| TPL-MS-002 | LOW | template/missing_section | `Implementation Guide` (Conditional) |
| TPL-MS-003 | MEDIUM | template/missing_section | `Technical Limitations` |
| TPL-MS-004 | MEDIUM | template/missing_section | `Non-Functional Requirements (NFRs)` |
| TPL-MS-005 | MEDIUM | template/missing_section | `Dependencies` |
| TPL-MS-006 | MEDIUM | template/missing_section | `Test Strategy` |
| TPL-MS-007 | MEDIUM | template/missing_section | `Acceptance Criteria Verification Checklist` |
| TPL-MS-008 | MEDIUM | template/missing_section | `Edge Cases` |
| TPL-MS-009 | MEDIUM | template/missing_section | `Change Log` |
| TPL-AC-001 | HIGH | template/legacy_format | AC1 markdown |
| TPL-AC-002 | HIGH | template/legacy_format | AC2 markdown |
| TPL-FM-001 | LOW | template/missing_frontmatter_field | `advisory` |
| TPL-FM-002 | LOW | template/missing_frontmatter_field | `source_gap` |
| TPL-FM-003 | LOW | template/missing_frontmatter_field | `source_story` |
| TPL-FM-004 | LOW | template/missing_frontmatter_field | `from_recommendations` |
| TPL-FM-005 | LOW | template/missing_frontmatter_field | `source_recommendations` |
| TPL-FM-006 | LOW | template/missing_frontmatter_field | `cycle_recorded` |
| TPL-FM-007 | MEDIUM | template/missing_frontmatter_field | `type` (ambiguous) |
| TPL-ZZZ-version-bump | MEDIUM | template/version_drift | umbrella |

No `TPL-WS-*` (the v2.7 fixture has no Workflow Status section). No `TPL-ID-*` (no informal-dep prose). `story.flags.provenance_intentionally_deferred = false` (Provenance is populated).

### Worked Example 3 — compliant v3.1 story (idempotency)

**Input:** `src/claude/skills/spec-driven-stories/references/examples/current-story-v3.1.story.md`

- `frontmatter.format_version`: `"3.1"`
- `frontmatter` has all 9 v3.1 fields
- Body has all Required H2 sections plus Conditional `Implementation Guide`
- AC section uses XML `<acceptance_criteria>` blocks

**Expected findings:** **ZERO**

Idempotency filter (Filter B) fires: `story_version (3, 1) >= canonical_version (3, 1)`. Scan terminates before Rules 1–6 are applied.

### Worked Example 4 — grandfathered QA Approved story

**Input:** copy of Example 1 but with `frontmatter.status: QA Approved`

**Expected behavior:**

- With `--include-completed=false` (default): Filter A fires. ZERO findings emitted. Audit narrative records `skip_reason: "grandfathered"`.
- With `--include-completed=true`: Filter A is bypassed. Findings identical to Example 1 (~25 findings).

### Worked Example 5 — story with AUDIT-DEFERRED Provenance marker (allowlist check)

**Input:** synthetic — a v2.0 story upgraded by `/fix-story --upgrade` where Provenance was scaffolded with the marker but content not yet populated.

- `frontmatter.format_version`: `"3.1"` (already bumped by P8)
- `## Provenance` section contains literal text: `<!-- AUDIT-DEFERRED: template/section_content_pending — added by /fix-story --upgrade on 2026-05-10. Populate when context available. -->` followed by the empty `<provenance>...</provenance>` scaffold

**Expected behavior:**

- Idempotency filter (Filter B) fires (version is current). ZERO `template/*` findings emitted.
- Rule 7 sets `story.flags.provenance_intentionally_deferred = true`.
- Downstream Sub-phase 3a reads this flag and SKIPS emission of `provenance/broken_brainstorm_ref`. (This is the critical allowlist coupling that prevents `/fix-story --upgrade`-inserted scaffolds from being re-flagged.)

---

## Provenance and Citations

Every concrete claim in this reference is GROUNDED in source files read during reference authoring:

- **Canonical template structure and SECTION_MANIFEST at lines 9-172** — `src/claude/skills/spec-driven-stories/assets/templates/story-template.md`
- **v3.1 frontmatter fields** — same file, lines 385-408
- **`<provenance>` XML schema** — same file, lines 422-467
- **XML AC schema** — same file, lines 470-545
- **Custody Chain Finding schema** — `src/claude/skills/spec-driven-stories/references/context-validation.md` lines 728-740
- **Severity decision rules** — same file, lines 744-751
- **Fix Classification Matrix** — `src/claude/skills/spec-driven-remediation/references/fix-actions-catalog.md` lines 18-41
- **AUDIT-DEFERRED marker convention** — `src/claude/skills/spec-driven-remediation/phases/phase-03-execution.md` line 136
- **Epistemic Integrity (INCONCLUSIVE handling)** — `.claude/rules/core/epistemic-integrity.md`

---

## Behavior on Errors

If any input file cannot be read or parsed, HALT and record the error in the Phase 2 narrative rather than emitting partial findings:

- Canonical template unreadable → HALT (the entire validation depends on this)
- Story file unreadable → emit a single `quality/story_unreadable` finding (not a template/* finding) and SKIP all rules for this story
- Frontmatter YAML malformed → emit a single `quality/frontmatter_parse_failed` finding and SKIP all rules for this story
- SECTION_MANIFEST YAML malformed → HALT (the manifest is the authoritative registry; partial scans would emit false negatives)

These error findings live outside the `template/*` namespace and are handled by other context-validation functions; this reference is concerned only with `template/*` types.
