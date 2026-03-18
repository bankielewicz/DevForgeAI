# Phase G07: Post-Generation Integration

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G06 --to=G07 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G06 incomplete
```

## Contract

PURPOSE: Update root README.md with module blurb, update CHANGELOG.md with documentation entry, update story file Change Log. Only executes for greenfield mode with story ID.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: README.md module blurb, CHANGELOG.md entry, story Change Log row
STEP COUNT: 3 mandatory steps

**SKIP CONDITION:** This phase ONLY executes when `$MODE == "greenfield" AND $STORY_ID provided`. If condition not met, record phase as skipped and proceed to G08.

```
IF NOT ($MODE == "greenfield" AND $STORY_ID is not empty):
    Display: "Phase G07 skipped: Not a story-based greenfield workflow"
    devforgeai-validate phase-record ${SESSION_ID} --phase=G07 --step=SKIPPED --workflow=doc-gen
    devforgeai-validate phase-complete ${SESSION_ID} --phase=G07 --checkpoint-passed --workflow=doc-gen
    GOTO Phase G08
```

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/post-generation-workflow.md")
```

IF Read fails: HALT -- "Phase G07 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step G07.1: Update Root README.md Module Blurb

EXECUTE: Add or update module documentation blurb in README.md.
```
# Reference: post-generation-workflow.md Section 4 (Action 2)

readme_path = "README.md"
readme = Read(file_path=readme_path)

MODULE_START = "<!-- MODULE-DOC: {module_name} START -->"
MODULE_END = "<!-- MODULE-DOC: {module_name} END -->"

blurb = """
{MODULE_START}
### {Module Display Name}
{one-line description}. See [API Reference](docs/api/API.md#{module_name}), [Architecture](docs/architecture/ARCHITECTURE.md#{module_name}).
{MODULE_END}
"""

IF MODULE_START in readme:
    # Update existing blurb (idempotent)
    old_blurb = extract_between(readme, MODULE_START, MODULE_END, inclusive=true)
    Edit(file_path=readme_path, old_string=old_blurb, new_string=blurb)
    Display: "  README.md: Module blurb updated"
ELSE:
    # Find documentation section in README or append
    # Look for "## Documentation" or "## Modules" section
    Grep(pattern="## Documentation|## Modules", path=readme_path)
    IF found:
        # Insert after section heading
        Edit(file_path=readme_path, old_string=section_heading, new_string=section_heading + "\n" + blurb)
    ELSE:
        # Append before last section or at end
        Edit(file_path=readme_path, old_string=last_section, new_string=blurb + "\n" + last_section)
    Display: "  README.md: Module blurb added"
```
VERIFY: README.md contains MODULE_START marker for this module.
```
content = Read(file_path="README.md")
IF MODULE_START not in content:
    HALT: "Module blurb not found in README.md after update"
```
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G07 --step=G07.1 --workflow=doc-gen`

---

### Step G07.2: Update CHANGELOG.md

EXECUTE: Add documentation entry to CHANGELOG.md under [Unreleased] > Added.
```
# Reference: post-generation-workflow.md Section 5 (Action 3)

changelog_path = "CHANGELOG.md"
changelog = Read(file_path=changelog_path)

# Per-story idempotency: check if entry already exists
entry_marker = "Documentation for {module_name} ({$STORY_ID})"

IF entry_marker in changelog:
    Display: "  CHANGELOG.md: Entry already exists (idempotent skip)"
ELSE:
    # Find [Unreleased] > ### Added section
    Grep(pattern="### Added", path=changelog_path)

    IF found:
        entry = "- {entry_marker}"
        Edit(file_path=changelog_path,
             old_string="### Added",
             new_string="### Added\n{entry}")
        Display: "  CHANGELOG.md: Entry added under [Unreleased] > Added"
    ELSE:
        Display: "  CHANGELOG.md: No ### Added section found. Skipping."
```
VERIFY: If entry added, CHANGELOG.md contains entry_marker. If skipped (idempotent or no section), step acknowledged.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G07 --step=G07.2 --workflow=doc-gen`

---

### Step G07.3: Update Story File Change Log

EXECUTE: Add documentation row to the story file's Change Log table.
```
# Reference: post-generation-workflow.md Section 6 (Action 4)

story_file = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
Read(file_path=story_file)

# Find Change Log table in story
Grep(pattern="## Change Log|## Changelog", path=story_file)

IF Change Log section found:
    # Check for existing documentation row (idempotency)
    IF "Documentation generated" not in story_content:
        row = "| {current_date} | Documentation generated | {TYPES joined by ', '} | spec-driven-documentation |"
        # Append row to Change Log table
        Edit(file_path=story_file,
             old_string=last_table_row,
             new_string=last_table_row + "\n" + row)
        Display: "  {$STORY_ID}: Change Log row added"
    ELSE:
        Display: "  {$STORY_ID}: Documentation row already exists (idempotent skip)"
ELSE:
    Display: "  {$STORY_ID}: No Change Log section found. Skipping."
```
VERIFY: If row added, story file contains "Documentation generated". If skipped, step acknowledged.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G07 --step=G07.3 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G07 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G07 complete: Post-Generation Integration"
Display: "  README.md, CHANGELOG.md, story file updated"
Display: "  Proceeding to Phase G08: Validation & Quality Check"
```
