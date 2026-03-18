# Post-Generation Documentation Workflow

After the documentation-writer subagent produces section content (Phase 2) and sections are inserted into framework files (Phase 4), this workflow updates project-level files (README.md, CHANGELOG.md) and records the documentation event in the story's Change Log.

**Trigger:** Executes when `mode=greenfield AND story_id IS SET`.

**Skip:** If any trigger condition is not met, this workflow does not execute.

---

## Section 1: Module Name Derivation

Derive the module name used for section headings and HTML comment markers.

### Step 0: Check for Existing Module Sections

```
# Scan framework docs for existing sections from the same epic
story_epic = story.frontmatter.epic   # e.g., "EPIC-072"

FOR each framework_file in [docs/api/API.md, docs/architecture/ARCHITECTURE.md, ...]:
    Grep(pattern="<!-- SECTION:.*START -->", path=framework_file)

    FOR each marker found:
        module_name = extract from marker
        Grep(pattern=story_epic, path=framework_file, context around marker)

        IF epic found near existing section:
            RESULT: module_name = module_name, mode = "update"
            RETURN

# If no existing section matches this epic, fall through to Step 1
mode = "create"
```

### Step 1: Extract Skill Name from Story Technical Spec

```
Read story file
Search for technical_specification.components[].file_path entries

FOR each component in technical_specification.components:
    IF component.file_path contains "skills/":
        skill_name = extract directory name after "skills/"
        # e.g., "src/claude/skills/assessing-entrepreneur/SKILL.md" → "assessing-entrepreneur"
        module_name = skill_name
        RETURN

    IF component.file_path contains "agents/":
        agent_name = extract filename without ".md"
        candidate = agent_name
```

### Step 2: Derive from Story Title (Fallback)

```
IF module_name not set:
    title = story.frontmatter.title
    title = remove_suffixes(title, ["Skill", "Feature", "Module", "System", "Service"])
    module_name = kebab_case(title)
```

### Step 3: AskUserQuestion (Final Fallback)

```
IF module_name not set OR module_name is ambiguous:
    AskUserQuestion(
        question="What module name should be used for documentation section headings?",
        header="Module Name",
        options=[
            "{candidate} (derived from story)",
            "{story_epic} module"
        ]
    )
    module_name = user_response
```

### Output

- `module_name`: Kebab-case string (e.g., `assessing-entrepreneur`)
- `module_display`: Title-case string (e.g., `Assessing Entrepreneur`)
- `mode`: `"create"` or `"update"`

---

## Section 2: Section Insertion Map

Lookup table mapping documentation type to target framework file and section structure.

| Doc Type | Target File | Section Heading |
|----------|-------------|-----------------|
| api | `docs/api/API.md` | `## {Module Display Name}` |
| architecture | `docs/architecture/ARCHITECTURE.md` | `## {Module Display Name}` |
| developer-guide | `docs/guides/DEVELOPER-GUIDE.md` | `## {Module Display Name}` |
| troubleshooting | `docs/guides/TROUBLESHOOTING.md` | `## {Symptom}` (problem-first) |
| roadmap | `docs/guides/ROADMAP.md` | Entry under priority tier |

**Section markers:** Every module section is wrapped in HTML comment markers:
```
<!-- SECTION: {module_name} START -->
## {Module Display Name}
(content)
<!-- SECTION: {module_name} END -->
```

**Troubleshooting exception:** Troubleshooting sections use symptom-based headings, not module names. The marker still uses `{module_name}` for idempotency, but the visible heading is the symptom.

```
<!-- SECTION: assessing-entrepreneur START -->
## Profile not found after running /assess-me

Cause: ...
Fix: ...

## Recalibration produces unchanged scores

Cause: ...
Fix: ...
<!-- SECTION: assessing-entrepreneur END -->
```

**Framework-level file protection:** The section insertion map targets only existing framework files. If a target file does not exist, HALT and prompt the user rather than creating it (framework files should be created during `/create-context` or project setup).

---

## Section 3: Action 1 — Insert or Update Sections

### Create Mode (New Module)

```
FOR each doc_type in generated_sections:
    IF generated_sections[doc_type] == "SKIP":
        CONTINUE   # documentation-writer found nothing to say

    target = section_insertion_map[doc_type]
    content = Read(target)

    # Append section before final separator or at end of file
    # Find last "---" line, insert before it; if none, append to end
    Edit(file_path=target, ...)

    updated_files[doc_type] = target
```

### Update Mode (Existing Module Section)

```
FOR each doc_type in generated_sections:
    IF generated_sections[doc_type] == "SKIP":
        CONTINUE

    target = section_insertion_map[doc_type]
    content = Read(target)

    MARKER_START = "<!-- SECTION: {module_name} START -->"
    MARKER_END = "<!-- SECTION: {module_name} END -->"

    IF MARKER_START found in content:
        # Replace between markers (idempotent update)
        old_block = extract from MARKER_START to MARKER_END (inclusive)
        Edit(file_path=target, old_string=old_block, new_string=generated_sections[doc_type])
        Display: "Updated {module_name} section in {target}"
    ELSE:
        # Markers not found despite mode=update; fall back to append
        Append generated_sections[doc_type] to end of file
        Display: "Added {module_name} section to {target}"

    updated_files[doc_type] = target
```

---

## Section 4: Action 2 — Root README.md Integration

Add or update a module blurb in the project's root README.md.

### Idempotency Mechanism

```
MARKER_START = "<!-- MODULE-DOC: {module_name} START -->"
MARKER_END = "<!-- MODULE-DOC: {module_name} END -->"
```

### Build the Module Block

```
module_display = title_case(module_name.replace("-", " "))

description = extract one-line description from story user story or generated README section

block = """
{MARKER_START}
### {module_display}

{description}

| Document | Description |
|----------|-------------|
"""

# Link to anchors within framework docs, not to per-module files
FOR each doc_type in updated_files:
    anchor = slugify(module_display)   # e.g., "assessing-entrepreneur"
    link = "{updated_files[doc_type]}#{anchor}"
    label = display_name(doc_type)
    desc = brief_description(doc_type)
    block += "| [{label}]({link}) | {desc} |\n"

block += "{MARKER_END}"
```

### Insert or Replace

```
content = Read("README.md")

IF MARKER_START found in content:
    Extract old_block from MARKER_START to MARKER_END (inclusive)
    Edit(file_path="README.md", old_string=old_block, new_string=block)
ELSE:
    IF "## Module Documentation" not in content:
        IF "## Contributing" in content:
            Edit: insert "## Module Documentation\n\n{block}\n---\n\n## Contributing" replacing "## Contributing"
        ELSE:
            Append to end
    ELSE:
        Insert block after last entry in "## Module Documentation" section
```

---

## Section 5: Action 3 — CHANGELOG.md Entry

### Idempotency Check

```
content = Read("CHANGELOG.md")

IF content is null OR file does not exist:
    Display: "Warning: CHANGELOG.md not found. Skipping."
    RETURN

search = "Documentation: {module_display} ({story_id})"

IF search found in content:
    Display: "CHANGELOG already contains entry for {story_id}. Skipping."
    RETURN
```

### Build Entry

```
entry = """- **Documentation: {module_display} ({story_id})**"""

FOR each doc_type in updated_files:
    entry += "\n  - Updated {doc_type} section in {updated_files[doc_type]}"
```

### Insert Under [Unreleased]

```
IF "## [Unreleased]" in content:
    IF "### Added" exists under "## [Unreleased]":
        Edit: insert entry after "### Added" line
    ELSE:
        Edit: insert "### Added\n\n{entry}" after "## [Unreleased]"
ELSE:
    Edit: insert "## [Unreleased]\n\n### Added\n\n{entry}" after changelog header
```

---

## Section 6: Action 4 — Story File Changelog Row

### Idempotency Check

```
content = Read(story_file_path)

IF "Documentation" found in Change Log section AND "/document" in same row:
    Display: "Story changelog already has documentation entry. Skipping."
    RETURN
```

### Build Row

```
date = current_date()
count = length(updated_files)
files = comma_separated(updated_files.values())

action = "Updated {count} sections in framework docs via /document"
row = "| {date} | DevForgeAI AI Agent | Documentation | {action} | {files} |"
```

### Insert Row

```
Locate last_table_row in Change Log section
Edit(file_path=story_file_path,
     old_string=last_table_row,
     new_string=last_table_row + "\n" + row)
```

---

## Section 7: Error Handling

| Condition | Action |
|-----------|--------|
| CHANGELOG.md does not exist | Skip Action 3 with warning. Do NOT create CHANGELOG.md. |
| README.md does not exist | HALT. README.md should always exist at project root. |
| Target framework file does not exist | HALT. Framework files must exist before module sections can be inserted. |
| Module name derivation returns empty | HALT. Use AskUserQuestion (Step 3 fallback). |
| Section markers malformed or overlapping | HALT with error. Do not attempt partial replacement. |
| Write fails (permissions, disk) | HALT with error. Do not proceed to subsequent actions. |

---

## Idempotency Guards Summary

| Target | Guard | Detection |
|--------|-------|-----------|
| Framework doc sections | HTML comment markers | `<!-- SECTION: {module} START/END -->` — replace between markers |
| README.md module blurb | HTML comment markers | `<!-- MODULE-DOC: {module} START/END -->` |
| CHANGELOG.md | String search (per-story) | `"Documentation: {Display Name} (STORY-XXX)"` |
| Story Change Log | Row content search | `"Documentation"` + `/document` in same row |
