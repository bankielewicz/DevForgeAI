# Phase 05: Story File Creation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=04 --to=05 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 04 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Assemble complete story document from phases 01-04 outputs, write to disk, verify all required sections present
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Complete .story.md file written to `devforgeai/specs/Stories/`
- **STEP COUNT:** 5
- **REFERENCE FILES:**
  - `references/story-file-creation.md`
  - `references/story-structure-guide.md`
  - `assets/templates/story-template.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-stories/references/story-file-creation.md")
Read(file_path=".claude/skills/spec-driven-stories/references/story-structure-guide.md")
Read(file_path=".claude/skills/spec-driven-stories/assets/templates/story-template.md")
```

IF any Read fails: HALT -- "Phase 05 reference files not loaded."

---

## Mandatory Steps (5)

### Scope Discipline (applies to all 5 steps)

This phase writes one new story file from Phase 01-04 outputs; it does NOT inspect existing stories. The template + SECTION_MANIFEST is the sole structural authority. FORBIDDEN: `Read` on any sibling `.story.md`; `Glob(pattern="STORY-*")` (except as prescribed by a step); `Bash(grep|cat|head|tail|sed|awk)` on story files (per Critical Rule 2). Step 5.5 prescribes `Grep` only on `$STORY_FILE_PATH` (the newly-written file).

---

### Step 5.1: Derive Story File Path

The canonical structural authority is the SECTION_MANIFEST in `assets/templates/story-template.md` (parsed in Step 5.2). Do NOT Glob, Read, or cross-reference sibling stories — see Scope Discipline above.

**EXECUTE:**
```
# The output directory devforgeai/specs/Stories/ is canonically declared in
# source-tree/ and is always present in a valid DevForgeAI project. Do not
# verify its existence via Glob — Write() in Step 5.4 will fail cleanly with
# a clear error if the directory is missing.

output_dir = "devforgeai/specs/Stories/"
story_slug = slugify($FEATURE_DESCRIPTION)  # lowercase, hyphens

# FROM_RECOMMENDATIONS mode applies a filename prefix so follow-up stories
# surface visually in Glob listings (e.g. "STORY-700-advisory-hardening-of-*.story.md").
# The prefix is set by the skill reference story-discovery-from-recommendations.md
# Step R.6 ("advisory-" when all selected recs are MEDIUM/LOW, else "").
IF conversation contains "**From Recommendations:** true" AND "**Story Filename Prefix:**":
    prefix = extract value of "**Story Filename Prefix:**" marker   # "advisory-" or ""
    $STORY_FILE_PATH = "${output_dir}${STORY_ID}-${prefix}${story_slug}.story.md"
ELSE:
    $STORY_FILE_PATH = "${output_dir}${STORY_ID}-${story_slug}.story.md"

Display: "Output path: ${STORY_FILE_PATH}"
```

**VERIFY:** `$STORY_FILE_PATH` is set to a non-empty string matching `devforgeai/specs/Stories/STORY-*.story.md`.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.1 --project-root=.
```
Update checkpoint: `output.story_file_path = $STORY_FILE_PATH`
Update checkpoint: `phases["05"].steps_completed.append("5.1")`

---

### Step 5.2: Load Story Template and Parse SECTION_MANIFEST

**EXECUTE:**
```
# Template already loaded in Reference Loading above
# Step 5.2a: Extract template_version from YAML frontmatter
$TEMPLATE_VERSION = extract_frontmatter_field(story_template_content, "template_version")
IF $TEMPLATE_VERSION is empty or not found:
    HALT: "Template frontmatter missing template_version field — cannot stamp stories without version"

# Step 5.2b: Parse SECTION_MANIFEST from HTML comment block
#
# Sprint 3.2 — Read cache first, re-parse only on cache miss.
# Contract: src/claude/skills/spec-driven-stories/contracts/phase-output-schema.json (phase03Output).
# Cache hit requires ALL of: file exists, schema_version == "1.0", phase_id == "03",
# parsed_manifest is non-null. Any miss triggers fresh parse (no HALT).
$PARSED_MANIFEST = null
cache_path = "tmp/${SESSION_ID}/phase-outputs/phase-03.json"
IF file_exists(cache_path):
    cached = Read(file_path=cache_path)
    cached_obj = json_parse(cached)
    IF cached_obj.schema_version == "1.0" AND cached_obj.phase_id == "03" AND cached_obj.parsed_manifest != null:
        $PARSED_MANIFEST = cached_obj.parsed_manifest
        Display: "SECTION_MANIFEST loaded from phase-03.json cache (Sprint 3.2)"

IF $PARSED_MANIFEST == null:
    # Sprint 4.2 — Cache miss: PRIMARY path delegates to CLI validator.
    # Contract: src/claude/scripts/devforgeai_cli/validators/manifest.py (Sprint 4.1).
    # Exit codes: 0 = parsed OK, 1 = parse/validation failure (HALT), 2 = IO error, 127 = CLI not installed.
    cli_result = Bash("devforgeai-validate parse-manifest --template-file=.claude/skills/spec-driven-stories/assets/templates/story-template.md --format=json")

    IF cli_result.exit_code == 0:
        cli_parsed = json_parse(cli_result.stdout)
        $PARSED_MANIFEST = cli_parsed.parsed_manifest
        Display: f"SECTION_MANIFEST parsed via CLI ({cli_parsed.section_count} sections, Sprint 4.2)"
    ELSE IF cli_result.exit_code == 1:
        HALT: f"parse-manifest CLI reported validation errors: {cli_result.stdout}"
    ELSE IF cli_result.exit_code == 127:
        # CLI not installed — fall back to inline parsing (deprecated, removed post-Sprint-5).
        # Search for start marker: "<!-- SECTION_MANIFEST" and end marker: "END_SECTION_MANIFEST -->"
        manifest_start = find("<!-- SECTION_MANIFEST", story_template_content)
        manifest_end = find("END_SECTION_MANIFEST -->", story_template_content)

        IF manifest_start is not found OR manifest_end is not found:
            HALT: "SECTION_MANIFEST markers not found in template — template may be pre-v3.0"

        # Extract content between markers, strip HTML comment syntax
        manifest_raw = story_template_content[manifest_start..manifest_end]
        manifest_yaml = strip_comment_markers(manifest_raw)

        # Parse YAML content
        $PARSED_MANIFEST = parse_yaml(manifest_yaml)
        Display: "SECTION_MANIFEST parsed via inline fallback (CLI exit 127; deprecated path)"
    ELSE:
        # Exit 2 or other unexpected — treat as HALT.
        HALT: f"parse-manifest CLI unexpected exit code {cli_result.exit_code}: {cli_result.stdout}"

IF $PARSED_MANIFEST does not contain "sections" key:
    HALT: "SECTION_MANIFEST YAML missing 'sections' key"

# Step 5.2c: Validate manifest entries have required fields
FOR each entry in $PARSED_MANIFEST.sections:
    IF entry missing name, header_level, or status:
        HALT: "SECTION_MANIFEST entry missing required field (name, header_level, status)"

# Step 5.2d: Derive categorized section lists from manifest
$required_h2_sections = filter($PARSED_MANIFEST.sections, header_level=2, status="Required")
$conditional_h2_sections = filter($PARSED_MANIFEST.sections, header_level=2, status="Conditional")
$optional_h2_sections = filter($PARSED_MANIFEST.sections, header_level=2, status="Optional")
$required_h3_sections = filter($PARSED_MANIFEST.sections, header_level=3, status="Required")
$conditional_h3_sections = filter($PARSED_MANIFEST.sections, header_level=3, status="Conditional")

IF len($required_h2_sections) == 0:
    HALT: "SECTION_MANIFEST produced zero required h2 sections — manifest may be malformed"

section_count = len($PARSED_MANIFEST.sections)
Display: "Template loaded: v${TEMPLATE_VERSION} ({section_count} sections from SECTION_MANIFEST)"
```

**VERIFY:** Template content is non-empty, YAML frontmatter contains template_version, SECTION_MANIFEST parsed successfully with sections key, all entries have name/header_level/status.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.2 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.2")`

---

### Step 5.3: Construct Frontmatter & Build Sections

**EXECUTE:**
```
# Build YAML frontmatter
frontmatter = {
  id: $STORY_ID,
  title: derive from $FEATURE_DESCRIPTION,
  status: "Backlog",
  priority: $PRIORITY,
  points: $POINTS,
  type: $TYPE,
  epic: $EPIC_ID or null,
  sprint: $SPRINT_ID or "Backlog",
  depends_on: $DEPENDS_ON or [],
  created: current date (YYYY-MM-DD),
  template_version: $TEMPLATE_VERSION
}

# FROM_RECOMMENDATIONS mode — populate v3.1 provenance fields emitted by
# story-discovery-from-recommendations.md Step R.8. These make the new
# story machine-queryable by REC-ID and source QA recommendations path for
# downstream tooling (e.g. QA back-linking, feedback analysis, /dev preflight).
IF conversation contains "**From Recommendations:** true":
    frontmatter["from_recommendations"] = true
    frontmatter["source_recommendations"] = parse_csv_list(
        extract value of "**Source Recommendation IDs:**" marker
    )   # -> ["REC-STORY-648-M-001", "REC-STORY-648-L-001", ...]
    frontmatter["cycle_recorded"] = int(
        extract value of "**Cycle Recorded:**" marker
    )
    source_story = extract value of "**Source Story:**" marker
    frontmatter["source_story"] = source_story
    frontmatter["source_devarch"] = f"devforgeai/qa/recommendations/{source_story}-qa-recommendations.md"
    frontmatter["advisory"] = (
        extract value of "**Is Advisory:**" marker == "true"
    )
    frontmatter["source_gap"] = null    # explicit; keep gap-source distinct from rec-source
ELSE:
    # Legacy gap-to-story path and interactive path leave advisory/source_*
    # fields at their template defaults (false / null) unless set by the
    # appropriate originating workflow (e.g. /review-qa-reports for gaps).
    pass

# DEVARCH pipeline — populate provenance fields when this story was seeded from a
# Development Architecture Document (Phase 01 Sub-step 1.2.0 set $SOURCE_DEVARCH and
# $FEATURE_REF). These link the story to the reviewed per-feature design; the
# backend-architect Development-Architecture Intake phase reads source_devarch.
# On the batch/interactive paths $SOURCE_DEVARCH is empty and the fields keep
# their template defaults ("").
IF $SOURCE_DEVARCH is set and non-empty:
    frontmatter["feature_ref"] = $FEATURE_REF
    frontmatter["source_devarch"] = $SOURCE_DEVARCH

# RCA pipeline (ADR-074) — populate RCA-traceability fields when this story was
# seeded from a /create-stories-from-rca batch invocation. The 6 markers
# $SOURCE_RCA, $SOURCE_RECOMMENDATION, $ADDRESSES_WHY, $EVIDENCE_FILES,
# $TEST_SPECIFICATION, $CONDITIONAL are set by batch-creation-workflow.md
# (consumer side of the ADR-074 tiered contract). On interactive / DEVARCH /
# legacy paths these markers are empty and the block is skipped.
IF $SOURCE_RCA is set and non-empty:
    frontmatter["source_rca"] = $SOURCE_RCA
    frontmatter["source_recommendation"] = $SOURCE_RECOMMENDATION
    frontmatter["rca_addresses_why"] = $ADDRESSES_WHY           # Required tier
    frontmatter["rca_evidence_files"] = $EVIDENCE_FILES         # Required tier

    # If the recommendation is Conditional, append a depends_on entry so
    # downstream sprint planning surfaces the trigger.
    IF $CONDITIONAL.type == "Conditional" AND $CONDITIONAL.condition is non-empty:
        frontmatter["depends_on"].append("rca-conditional:${CONDITIONAL.condition}")

    # The Provenance section augmentation (an <rca_origin> XML element
    # carrying addresses_why + evidence_files + test_specification verbatim)
    # is emitted in the Provenance-section assembly step below (Sprint 2.7
    # block). See "RCA traceability — Provenance section augmentation" there.

# VCS / PR lifecycle fields (ISSUE-724) — always emitted with null/false defaults.
# Written at runtime by /dev preflight (branch, pr_base, worktree_path) and
# /dev Phase 08 (pr_number, pr_url) and /qa Phase 06 (pr_merged, merged_sha, merged_at).
# Emit the following keys verbatim into story frontmatter:
branch: null
pr_base: null
worktree_path: null
pr_number: null
pr_url: null
pr_merged: false
merged_sha: null
merged_at: null

# Build document sections from phase outputs using SECTION_MANIFEST:
# Required sections (from manifest, status=Required, header_level=2) are always assembled.
# Conditional sections (from manifest, status=Conditional, header_level=2) are assembled
# only when their corresponding phase output is non-null.
# Optional sections (from manifest, status=Optional, header_level=2) are assembled
# when available.

# Assemble required sections (derived from $required_h2_sections):
FOR each section in $required_h2_sections:
    content = get_phase_output_for_section(section.name)

    # === Sprint 2.1 (USER MANDATE — full-fidelity story files) ============
    # When assembling "## Acceptance Criteria":
    # - Preserve the entire <acceptance_criteria> XML block from Phase 02's
    #   $REQUIREMENTS_OUTPUT, INCLUDING its <implementation> child element.
    # - Do NOT strip <implementation> blocks.
    # - Do NOT summarize <pseudocode>, <approach>, or <task_hint> as prose.
    # - Do NOT replace XML with narrative prose.
    # - Preserve CDATA sections and original whitespace.
    #
    # Rationale: a fresh /dev session reading this file must be able to feed
    # the <approach> / <pseudocode> / <task_hint> directly to test-automator
    # and backend-architect with no session handoff or sibling-file lookup.
    # Failure to embed produces the "new session without context" defect that
    # this sprint exists to eliminate.
    IF section.name == "Acceptance Criteria":
        FOR each <acceptance_criteria id="ACN"> in $REQUIREMENTS_OUTPUT:
            emit exact XML block (preserve CDATA, preserve whitespace,
            preserve <implementation>...<approach>...<pseudocode>...<task_hint>)
        # The result is appended as `content` for this section.
    # =====================================================================

    IF content is not null:
        assembled_sections.append(section.name, content)
    ELSE:
        assembled_sections.append(section.name, placeholder_for(section.name))

# Assemble conditional sections (derived from $conditional_h2_sections):
# This generalizes the STORY-580 Implementation Guide conditional logic.
FOR each section in $conditional_h2_sections:
    content = get_phase_output_for_section(section.name)
    IF content is not null:
        assembled_sections.append(section.name, content)
    ELSE:
        # Omit conditional section entirely — do NOT insert empty placeholder
        pass

# Assemble optional sections (derived from $optional_h2_sections):
FOR each section in $optional_h2_sections:
    content = get_phase_output_for_section(section.name)
    IF content is not null:
        assembled_sections.append(section.name, content)

# Populate provenance section if brainstorm/epic chain available
# === Sprint 2.7 (USER MANDATE — full-fidelity story files) ================
# A dangling <origin> link to an epic file fails the fresh-session test:
# /dev cannot read the epic to recover rationale. We MUST embed the literal
# epic feature text inline in the story's ## Provenance section.
IF $EPIC_ID is not null:
    # Sprint 3.3 — Prefer in-context $EPIC_CONTENT (written by phase-01.3).
    # Fallback to phase-01.json disk cache; ultimate fallback is a fresh Read.
    IF $EPIC_CONTENT is not null:
        epic_path = $EPIC_FILE_PATH
        epic_content = $EPIC_CONTENT
        Display: "Epic content reused from phase-01 in-context cache (Sprint 3.3)"
    ELSE:
        phase01_cache = "tmp/${SESSION_ID}/phase-outputs/phase-01.json"
        IF file_exists(phase01_cache):
            cached = json_parse(Read(file_path=phase01_cache))
            IF cached.schema_version == "1.0" AND cached.phase_id == "01" AND cached.epic_content != null:
                epic_path = cached.epic_file_path
                epic_content = cached.epic_content
                Display: "Epic content loaded from phase-01.json fallback (Sprint 3.3)"
        IF epic_content is null:
            epic_path = derive_epic_path($EPIC_ID)     # e.g., devforgeai/specs/Epics/EPIC-094.md
            epic_content = Read(file_path=epic_path)
            Display: "Epic content re-read from disk (no cache hit; Sprint 3.3 fallback)"

    # Locate the feature block whose body references $STORY_ID.
    # Master plan §2.7: extract "### Feature N.N" block in epic that
    # references $STORY_ID. Match by literal $STORY_ID occurrence inside
    # the feature body (between this ### Feature header and the next).
    epic_feature_text = extract_feature_block_for_story(epic_content, $STORY_ID)

    IF epic_feature_text is null:
        Display: "WARNING: $STORY_ID not referenced in any ### Feature block of {epic_path}. " \
                 "Provenance section will record the chain only; epic feature text cannot be embedded."

    Add ## Provenance section with:
      - <origin> chain (brainstorm -> epic -> story) preserving prior behavior
      - "### Epic Feature (verbatim from {epic_path})" subsection containing
        the full epic_feature_text as a quoted block (`>` prefix per line),
        OR a one-line note if epic_feature_text was null
      - source citation: "(Source: {epic_path})"
# ==========================================================================

# === RCA traceability — Provenance section augmentation (ADR-074) =========
# When this story originated from /create-stories-from-rca, embed an
# <rca_origin> XML element inside the Provenance section. This preserves
# 5-Whys traceability and the verbatim test specification from the RCA
# recommendation. The element is machine-queryable for back-linking
# (e.g., QA can find every story derived from a given RCA recommendation).
IF $SOURCE_RCA is set and non-empty:
    rca_origin_xml = """
    <rca_origin
        rca_id=\"${SOURCE_RCA}\"
        recommendation_id=\"${SOURCE_RECOMMENDATION}\"
        conditional=\"${CONDITIONAL.type}\">
      <!-- ADR-074 Required tier: 5-Whys traceability -->
      <addresses_why>${ADDRESSES_WHY}</addresses_why>
      <!-- ADR-074 Required tier: evidence file list (parsed CSV) -->
      <evidence_files>
${render each path in $EVIDENCE_FILES as: <file>${path.trim()}</file>}
      </evidence_files>
      <!-- ADR-074 Rendered tier: test specification table verbatim -->
      <test_specification><![CDATA[
${TEST_SPECIFICATION}
      ]]></test_specification>
${if $CONDITIONAL.type == "Conditional": "      <condition>${CONDITIONAL.condition}</condition>"}
    </rca_origin>
    """

    Insert rca_origin_xml inside the existing <provenance>...</provenance>
    block (immediately before the closing </provenance> tag). If no
    Provenance section exists yet (no $EPIC_ID + no brainstorm context),
    create one containing only the <rca_origin> element.

    Display: "RCA traceability embedded in Provenance: ${SOURCE_RCA} / ${SOURCE_RECOMMENDATION}"
# ==========================================================================

$STORY_CONTENT = assemble full document from frontmatter + assembled_sections (in manifest order)
```

**VERIFY:** `$STORY_CONTENT` contains YAML frontmatter and all section headers from SECTION_MANIFEST.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.3 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.3")`

---

### Step 5.4: Write to Disk

**EXECUTE:**
```
Write(file_path=$STORY_FILE_PATH, content=$STORY_CONTENT)
```

**VERIFY:** `Write()` errors on failure. Trust the return value — no re-Read or Glob needed.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.4 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.4")`

---

### Step 5.5: Verify Required Sections (absorbs Phase 5-6 Gate)

**EXECUTE:**
```
# Sprint A (STORY-646): CLI validation of story file sections via validate-story-sections
# --template-file validates section manifest structure; validates $STORY_FILE_PATH section presence.
cli_vss_result = Bash(f"devforgeai-validate validate-story-sections --template-file={$TEMPLATE_FILE_PATH} --format=json")
IF cli_vss_result.exit_code == 0:
  vss_parsed = json_parse(cli_vss_result.stdout)
  Display: f"Section manifest validated: {vss_parsed.section_count} sections OK (validate-story-sections, STORY-646)"
ELSE IF cli_vss_result.exit_code == 1:
  vss_parsed = json_parse(cli_vss_result.stdout)
  FOR each err in vss_parsed.errors:
    Display: f"  HALT: Section manifest error: {err.type} — {err.message}"
  HALT: "Story sections invalid per validate-story-sections CLI. Errors: " + str(vss_parsed.errors)
ELSE IF cli_vss_result.exit_code == 127:
  Display: "WARNING: validate-story-sections CLI not installed — using inline section Grep (exit 127 fallback)"

# Read the written file fresh
story_content = Read(file_path=$STORY_FILE_PATH)

# Derive validation arrays from SECTION_MANIFEST (parsed in Step 5.2)
# All arrays below are manifest-derived — no hardcoded section names.
# MUST-match ## headers: from manifest entries where header_level=2 AND status=Required
required_h2_headers = new empty list
FOR each section in $required_h2_sections:
    pattern = "^## " + regex_escape(section.name)
    required_h2_headers.append(pattern)

# MUST-match ### subsections: from manifest entries where header_level=3 AND status=Required
required_h3_subsections = new empty list
FOR each section in $required_h3_sections:
    pattern = "^### " + regex_escape(section.name)
    required_h3_subsections.append(pattern)

# Conditional ## headers: from manifest conditional_sections (header_level=2 AND status=Conditional)
conditional_h2_headers = new empty list
FOR each section in $conditional_h2_sections:
    pattern = "^## " + regex_escape(section.name)
    conditional_h2_headers.append(pattern)

IF len(required_h2_headers) == 0:
    HALT: "SECTION_MANIFEST produced zero required h2 headers — cannot validate story structure"

# NOTE: regex_escape handles metacharacters like parentheses in
# "Non-Functional Requirements (NFRs)" — escape ( and ) for grep patterns
# NOTE: The manifest uses "Files Created/Modified" as the canonical section name.
# Do NOT use the drifted name "Files Created" — always derive from SECTION_MANIFEST.

missing_sections = []

# Validate conditional sections: only check if their phase output was non-null
FOR each pattern in conditional_h2_headers:
    section_name = extract_name_from_pattern(pattern)
    phase_output = get_phase_output_for_section(section_name)
    IF phase_output is not null:
        # Section was assembled — verify it appears in the story
        IF NOT Grep(pattern=pattern, path=$STORY_FILE_PATH):
            missing_sections.append(pattern)
        # Also validate expected subsections from $conditional_h3_sections
        conditional_subsections = filter($conditional_h3_sections, parent=section_name)
        found_subsections = count matches in story file
        IF found_subsections < 2:
            Display: "WARNING: {section_name} has fewer than 2 subsections ({found_subsections} found)"

FOR each pattern in required_h2_headers:
    IF NOT Grep(pattern=pattern, path=$STORY_FILE_PATH):
        missing_sections.append(pattern)

FOR each pattern in required_h3_subsections:
    IF NOT Grep(pattern=pattern, path=$STORY_FILE_PATH):
        missing_sections.append(pattern)

IF missing_sections is NOT empty:
    HALT: "Phase 5-6 Gate FAILED: Missing {len(missing_sections)} required sections"
    Display missing sections list
    DO NOT proceed

h2_count = len(required_h2_headers) + len(conditional_h2_headers)
h3_count = len(required_h3_subsections) + len(conditional_h3_sections)
Display: f"Phase 5-6 Gate PASSED: All sections confirmed present ({h2_count} ## + {h3_count} ### from SECTION_MANIFEST)"
```

**VERIFY:** Zero missing sections. All required sections present. Section names derived from SECTION_MANIFEST — "Files Created/Modified" is the correct manifest name (not drifted "Files Created"). Validation counts reflect manifest-derived totals.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=05 --step=5.5 --project-root=.
```
Update checkpoint: `phases["05"].steps_completed.append("5.5")`

---

## Exit Gate

```bash
devforgeai-validate verify-story-creation ${STORY_FILE_PATH} --project-root=. --format=json
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=05 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Story file exists on disk at `$STORY_FILE_PATH`
- [ ] File is non-empty
- [ ] All required ## headers present (manifest-derived required h2 + conditional h2 where assembled)
- [ ] All required ### subsections present (manifest-derived required h3 + conditional h3 where assembled)
- [ ] YAML frontmatter is valid
- [ ] Story ID in frontmatter matches `$STORY_ID`
- [ ] If `from_recommendations: true`, `source_devarch` equals `devforgeai/qa/recommendations/${source_story}-qa-recommendations.md` and that file exists
- [ ] Section names match SECTION_MANIFEST (no drifted names)

IF any unchecked: HALT -- "Phase 05 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 05 complete. Story file written: ${STORY_FILE_PATH}"
Display: f"All required sections verified ({h2_count} ## + {h3_count} ### from SECTION_MANIFEST)."
Display: "Proceeding to Phase 06: Epic/Sprint Linking..."
```
