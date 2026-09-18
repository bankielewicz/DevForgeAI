# QA Recommendations Parsing Workflow (Phases 1-5)

Detailed pseudocode for parsing QA recommendation files and extracting validated recommendation entries.

This workflow is **inline to `/create-incident-from-recommendations`** (NOT delegated to a separate skill). The QA recs file format is structured YAML, not RCA markdown — the sibling pathway `/create-incident-from-rca` delegates RCA-markdown parsing because that format is established framework-wide; this pathway parses YAML directly because the format is dedicated to QA recs and the parser is small.

The output of this phase feeds:
- **Phase 6-9 (Selection)** — for filter logic (`--severity`, `--include-blocking`, `--rec-ids`) and the multi-select prompt
- **Phase 10 (Issue creation skill)** — passed forward as `selected_recommendations` after the user filters in Phase 6-9

**Authoritative schema:** `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`

---

## Phase 1: Locate QA Recs File (Prerequisite)

```
QA_RECS_FILE = "devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md"

Glob(pattern="${QA_RECS_FILE}")

IF no files found:
    Display: "❌ QA recommendations file not found: ${QA_RECS_FILE}"
    Display: ""
    Display: "Run /qa ${STORY_ID} first to generate QA recommendations."
    Display: ""
    Display: "Available QA recs files:"
    Glob(pattern="devforgeai/qa/recommendations/STORY-*-qa-recommendations.md")
    HALT

Display: "Parsing: ${QA_RECS_FILE}"
```

---

## Phase 2: Parse Frontmatter and Schema Manifest

```
Read(file_path="${QA_RECS_FILE}")

# Extract YAML frontmatter between --- markers
FRONTMATTER_PATTERN = content between first "---" and second "---"

qa_recs_document = {
    schema_version: extract_field("schema_version"),       # e.g., "1.0"
    story_id: extract_field("story_id"),                   # e.g., "STORY-661"
    qa_cycle: extract_field("qa_cycle"),                   # e.g., 2
    generated_at: extract_field("generated_at"),           # ISO timestamp
    last_posted_at: extract_field("last_posted_at"),       # optional, populated by skill BR-014
    recommendations: []
}

# Validate schema_version is recognized
KNOWN_SCHEMA_VERSIONS = {"1.0"}
IF qa_recs_document.schema_version NOT IN KNOWN_SCHEMA_VERSIONS:
    Display: "⚠ Unknown schema_version: ${schema_version}. Parser may miss new fields."
    # Do NOT HALT — degrade gracefully, surface warning, continue

# Sanity-check the SECTION_MANIFEST comment (not a HALT, just a parser self-check)
IF NOT Grep(pattern="<!-- SECTION_MANIFEST", path=QA_RECS_FILE):
    Display: "⚠ SECTION_MANIFEST comment missing — file may not match expected schema"
```

---

## Phase 3: Parse YAML Blocks Under Three Section Headers

```
# QA recs files have three top-level sections, in this order:
SECTIONS = [
    ("Blocking",  "## Blocking Recommendations"),
    ("Advisory",  "## Advisory Recommendations"),
    ("Deferred",  "## Deferred Recommendations"),
]

FOR (section_name, section_header) in SECTIONS:
    # Find the section's YAML block range:
    # - Starts after `${section_header}\n`
    # - Ends at the next `## ` header OR end-of-file
    section_yaml = extract_section_body(QA_RECS_FILE, section_header)

    IF section_yaml is empty OR section_yaml == "_None._":
        # Section exists but no recs — fine, skip
        continue

    # Each rec is a YAML list item starting with "- id: \"REC-..."
    yaml_blocks = parse_yaml_list(section_yaml)

    FOR rec_yaml in yaml_blocks:
        rec = {
            section: section_name,
            # Required fields per schema:
            id: rec_yaml["id"],                                # e.g., "REC-STORY-661-M-001"
            severity: rec_yaml["severity"],                    # CRITICAL|HIGH|MEDIUM|LOW
            provenance: rec_yaml["provenance"],                # GROUNDED|DERIVED|INCONCLUSIVE
            title: rec_yaml["title"],
            file: rec_yaml.get("file"),
            line: rec_yaml.get("line"),                        # int OR null
            line_range: rec_yaml.get("line_range"),            # [start, end] OR null
            category: rec_yaml["category"],                    # correctness|security|performance|anti_pattern|test_quality|documentation
            blocking_release: rec_yaml.get("blocking_release", False),
            estimated_effort_minutes: rec_yaml["estimated_effort_minutes"],
            verification: rec_yaml.get("verification", {}),    # {command, expected}

            # Optional / category-conditional fields:
            before_code: rec_yaml.get("before_code"),
            after_code: rec_yaml.get("after_code"),
            remediation_steps: rec_yaml.get("remediation_steps"),  # alternative to before/after
            classification: rec_yaml.get("classification"),    # REGRESSION|PRE_EXISTING (anti_pattern only per schema; broadened to any cat per skill BR-010)
            cycle_first_seen: rec_yaml.get("cycle_first_seen"),
            dependencies: rec_yaml.get("dependencies", []),
            references: rec_yaml.get("references", []),

            # Linkage marker (set if previous /create-incident-from-recommendations posted this rec):
            posted_as_marker: extract_posted_as_marker(rec_yaml),  # e.g., "Issue-42" if `**Posted as:** Issue-42 — ...` line present
        }

        validate_rec_against_schema(rec)  # see Phase 4
        qa_recs_document.recommendations.append(rec)

Display: "Parsed ${len(qa_recs_document.recommendations)} recommendations from ${QA_RECS_FILE}"
```

---

## Phase 4: Validate Each Entry Against Schema

The authoritative schema is `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`. The parser validates each entry against these requirements:

| Field | Required for | Validation |
|-------|--------------|------------|
| `id` | All | Pattern: `^REC-STORY-\d+-[CHML]-\d{3}$` |
| `severity` | All | Enum: `CRITICAL|HIGH|MEDIUM|LOW` |
| `provenance` | All | Enum: `GROUNDED|DERIVED|INCONCLUSIVE` |
| `title` | All | Non-empty string, ≤200 chars |
| `category` | All | Enum: `correctness|security|performance|anti_pattern|test_quality|documentation` |
| `file` | All except `category=documentation` | Path string |
| `line` OR `line_range` | `correctness|security|performance|anti_pattern|test_quality` | Int OR `[start, end]`. Both missing → HALT |
| `verification.command` | All | Non-empty string |
| `verification.expected` | All | Non-empty string |
| `estimated_effort_minutes` | All | Positive integer |
| `classification` | `anti_pattern` (per schema; broadened to any category per BR-010) | Enum: `REGRESSION|PRE_EXISTING` |
| `before_code` + `after_code` | If `remediation_steps` absent | Non-empty strings |
| `remediation_steps` | If `before_code`/`after_code` absent | Array of strings, ≥1 entry |

```
validate_rec_against_schema(rec):
    errors = []

    IF NOT regex_match(r"^REC-STORY-\d+-[CHML]-\d{3}$", rec.id):
        errors.append(f"id format invalid: {rec.id}")

    IF rec.severity NOT IN {"CRITICAL", "HIGH", "MEDIUM", "LOW"}:
        errors.append(f"severity invalid: {rec.severity}")

    IF rec.category IN {"correctness", "security", "performance", "anti_pattern", "test_quality"}:
        IF rec.line is None AND rec.line_range is None:
            errors.append("line or line_range required for code-change category")

    IF rec.category != "documentation" AND not rec.file:
        errors.append("file required for non-documentation category")

    IF NOT rec.before_code AND NOT rec.remediation_steps:
        errors.append("before_code/after_code OR remediation_steps required")

    IF NOT rec.verification or NOT rec.verification.get("command"):
        errors.append("verification.command required")

    IF errors:
        Display: f"❌ Schema violations in {rec.id}:"
        FOR e in errors:
            Display: f"   • {e}"
        Display: f"   File: {QA_RECS_FILE}"
        HALT
```

---

## Phase 5: Return Parsed Document

```
# qa_recs_document is now fully parsed and validated. The next phase (selection)
# applies user-supplied filters (--severity, --include-blocking, --rec-ids)
# before invoking the skill.

Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  QA Recommendations: ${qa_recs_document.story_id} (cycle ${qa_recs_document.qa_cycle})"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Counts by section
blocking  = [r for r in recs if r.section == "Blocking"]
advisory  = [r for r in recs if r.section == "Advisory"]
deferred  = [r for r in recs if r.section == "Deferred"]

Display: "  Blocking:  ${len(blocking)}"
Display: "  Advisory:  ${len(advisory)}"
Display: "  Deferred:  ${len(deferred)}"

# Already-linked count
# Primary source: posting-manifest.json (post-fix; per linking-workflow.md)
# Legacy fallback: inline **Posted as:** marker in QA recs file
manifest_path = f"tmp/{STORY_ID}/posting-manifest.json"
manifest_linked_ids = set()
IF file_exists(manifest_path):
    manifest = json.parse(Read(file_path=manifest_path))
    manifest_linked_ids = { l["rec_id"] for l in manifest.get("links", []) }

linked = [r for r in recs if r.posted_as_marker or r.id in manifest_linked_ids]
IF linked:
    Display: "  Already linked: ${len(linked)} (will be detected for idempotency by skill Phase 1.5; sources: posting-manifest.json + legacy inline markers)"
```

---

## Edge Cases Handled

| Edge case | Behavior |
|-----------|----------|
| Missing file | HALT with hint to run `/qa STORY-NNN` first |
| Unknown schema_version | Warn, continue parsing — degrade gracefully |
| Missing SECTION_MANIFEST comment | Warn, continue |
| Empty section (`_None._`) | Skip silently |
| YAML parse error in a single rec | HALT with file:line context |
| Schema violation (any required field) | HALT with file:line + violations list |
| `category=documentation` lacks `file`/`line` | Allowed (documentation is whole-file scope) |
| `category=anti_pattern` lacks `classification` | HALT (REGRESSION/PRE_EXISTING is required by schema for this category) |
| Both `line` and `line_range` present | Use `line` if scalar; ignore `line_range` |
| `**Posted as:** Issue-N` marker present | Capture into `posted_as_marker` (legacy fallback). Post-fix, the primary idempotency source is `tmp/${STORY_ID}/posting-manifest.json` — skill Phase 1.5 reads both |

---

## Why this is NOT delegated to a separate parsing skill

Three reasons:

1. **Format scope** — RCA markdown is a constitutional document format consumed by multiple framework workflows (`/create-stories-from-rca`, `/create-incident-from-rca`, future analytics). Centralizing the parser there made sense. QA recs are a single-format / single-source-pathway artifact (`/qa` produces, `/create-incident-from-recommendations` consumes); there's no second consumer to share with.

2. **Parser size** — RCA parsing involves regex-matching `### REC-N:` markdown headers, parsing ad-hoc effort estimates ("4 hours" / "2 story points"), extracting variable-format checklists. QA recs parsing is ~50 lines of YAML loading + schema validation against a JSON Schema document. Inline is appropriate.

3. **Schema enforcement** — The QA recs format has a formal JSON Schema at `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`. Validation is mechanical: load YAML, walk the schema. RCA parsing is heuristic (the RCA template evolves; parsing tolerates legacy formats). Different rigor levels are appropriate to different formats.

If a third QA-recs consumer ever emerges (unlikely — this format is purpose-built), this parsing logic is straightforward to extract into a skill at that time.
