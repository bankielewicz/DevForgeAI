# Phase G09: Export & Finalization

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G08 --to=G09 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G08 incomplete
```

## Contract

PURPOSE: Convert documentation to HTML/PDF if requested, apply styling, update story file with documentation references.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Exported files (if requested), story file updated with doc references
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step G09.1: Export to Requested Format

EXECUTE: If export format requested (html or pdf), convert documentation files.
```
IF $EXPORT_FORMAT == "html":
    FOR each doc_type, path in updated_files:
        html_path = path.replace(".md", ".html")

        # Try pandoc first
        result = Bash(command="pandoc {path} -o {html_path} --standalone --toc 2>&1")

        IF result.exit_code != 0:
            # Fallback: check for Python markdown
            Display: "pandoc not available. Attempting Python markdown fallback."
            Display: "Install: sudo apt install pandoc"
            Display: "Falling back to Markdown only for {doc_type}"
        ELSE:
            Display: "  Exported: {html_path}"

ELIF $EXPORT_FORMAT == "pdf":
    FOR each doc_type, path in updated_files:
        pdf_path = path.replace(".md", ".pdf")

        # Try pandoc with xelatex
        result = Bash(command="pandoc {path} -o {pdf_path} --pdf-engine=xelatex --toc 2>&1")

        IF result.exit_code != 0:
            # Try wkhtmltopdf via HTML intermediate
            html_temp = path.replace(".md", ".tmp.html")
            result1 = Bash(command="pandoc {path} -o {html_temp} --standalone 2>&1")
            result2 = Bash(command="wkhtmltopdf {html_temp} {pdf_path} 2>&1")

            IF result2.exit_code != 0:
                Display: "PDF export failed for {doc_type}."
                Display: "Install: sudo apt install pandoc texlive-xelatex OR wkhtmltopdf"
                Display: "Falling back to Markdown only"
            ELSE:
                Display: "  Exported: {pdf_path} (via wkhtmltopdf)"
        ELSE:
            Display: "  Exported: {pdf_path}"

ELIF $EXPORT_FORMAT == "markdown":
    Display: "Export format: Markdown (no conversion needed)"
```
VERIFY: If export requested, at least attempted conversion. Failures logged with install instructions.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G09 --step=G09.1 --workflow=doc-gen`

---

### Step G09.2: Update Story File with Documentation References

EXECUTE: Add generated documentation references section to story file (if story-based).
```
IF $STORY_ID provided:
    story_file = Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
    story_content = Read(file_path=story_file)

    # Check if Generated Documentation section already exists
    IF "## Generated Documentation" in story_content:
        # Update existing section
        old_section = extract_section(story_content, "## Generated Documentation")
        new_section = generate_doc_references_section()
        Edit(file_path=story_file, old_string=old_section, new_string=new_section)
        Display: "  Story file: Documentation references updated"
    ELSE:
        # Append new section before Implementation Notes or at end
        doc_section = """
## Generated Documentation

| Type | Path | Words |
|------|------|-------|
"""
        FOR each doc_type, path in updated_files:
            doc_section += "| {doc_type} | {path} | {word_counts[doc_type]} |\n"

        doc_section += """
- **Last Generated:** {current_timestamp}
- **Coverage:** {coverage}%
- **Session:** {SESSION_ID}
"""
        # Find insertion point
        IF "## Implementation Notes" in story_content:
            Edit(file_path=story_file,
                 old_string="## Implementation Notes",
                 new_string=doc_section + "\n## Implementation Notes")
        ELSE:
            Write(file_path=story_file, content=story_content + "\n" + doc_section)

        Display: "  Story file: Documentation references added"

ELSE:
    Display: "  No story ID -- skipping story file update"
```
VERIFY: If story-based, story file contains "## Generated Documentation" section.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G09 --step=G09.2 --workflow=doc-gen`

---

### Step G09.3: Update Session Checkpoint

EXECUTE: Update the session checkpoint with finalization status.
```
checkpoint = Read(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json")
# Parse JSON, update fields:
checkpoint.current_phase = "G09"
checkpoint.coverage = coverage
checkpoint.files_updated = list(updated_files.values())
checkpoint.export_format = $EXPORT_FORMAT
checkpoint.phases_completed.append("G09")

Write(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json", content=JSON(checkpoint))

Display: "Session checkpoint updated"
```
VERIFY: Checkpoint file updated with G09 in phases_completed.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G09 --step=G09.3 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G09 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G09 complete: Export & Finalization"
Display: "  Proceeding to Phase G10: Completion Summary"
```
